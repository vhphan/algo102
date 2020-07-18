const chartDiv = 'main-chart';
const chartContainer = document.getElementById(chartDiv);
const tableContainer = document.getElementById('profile-container');
const selectTopPick = document.getElementById('select-top-picks');
const spinner = document.getElementById('spinner');
const snackbar = document.getElementById('snackbar');
const currentUrl = document.location.href

function getBaseURL(url) {
    let pathArray = url.split('/');
    let protocol = pathArray[0];
    let host = pathArray[2];
    return protocol + '//' + host
}

const base_url = getBaseURL(currentUrl);

const convertLinks = (input) => {

    let text = input;
    const linksFound = text.match(/(?:www|https?)[^\s]+/g);
    const aLink = [];

    if (linksFound != null) {

        for (let i = 0; i < linksFound.length; i++) {
            let replace = linksFound[i];
            if (!(linksFound[i].match(/(http(s?)):\/\//))) {
                replace = 'http://' + linksFound[i]
            }
            let linkText = replace.split('/')[2];
            if (linkText.substring(0, 3) == 'www') {
                linkText = linkText.replace('www.', '')
            }
            if (linkText.match(/youtu/)) {

                let youtubeID = replace.split('/').slice(-1)[0];
                aLink.push('<div class="video-wrapper"><iframe src="https://www.youtube.com/embed/' + youtubeID + '" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>')
            } else if (linkText.match(/vimeo/)) {
                let vimeoID = replace.split('/').slice(-1)[0];
                aLink.push('<div class="video-wrapper"><iframe src="https://player.vimeo.com/video/' + vimeoID + '" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe></div>')
            } else {
                aLink.push('<a href="' + replace + '" target="_blank">' + linkText + '</a>');
            }
            text = text.split(linksFound[i]).map(item => {
                return aLink[i].includes('iframe') ? item.trim() : item
            }).join(aLink[i]);
        }
        return text;

    } else {
        return input;
    }
}


function eventFire(el, etype){
  if (el.fireEvent) {
    el.fireEvent('on' + etype);
  } else {
    var evObj = document.createEvent('Events');
    evObj.initEvent(etype, true, false);
    el.dispatchEvent(evObj);
  }
}

function hasClass(el, className) {
    if (el.classList)
        return el.classList.contains(className);
    return !!el.className.match(new RegExp('(\\s|^)' + className + '(\\s|$)'));
}

function addClass(el, className) {
    if (el.classList)
        el.classList.add(className)
    else if (!hasClass(el, className))
        el.className += " " + className;
}

function removeClass(el, className) {
    if (el.classList)
        el.classList.remove(className)
    else if (hasClass(el, className)) {
        var reg = new RegExp('(\\s|^)' + className + '(\\s|$)');
        el.className = el.className.replace(reg, ' ');
    }
}

function showSpinner() {
    addClass(spinner, 'spinner-border');
    addClass(spinner, 'text-primary');
}

function hideSpinner() {
    removeClass(spinner, 'spinner-border');
    removeClass(spinner, 'text-primary');
}


function linkify(inputText) {
    var replacedText, replacePattern1, replacePattern2, replacePattern3;

    //URLs starting with http://, https://, or ftp://
    replacePattern1 = /(\b(https?|ftp):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/gim;
    replacedText = inputText.replace(replacePattern1, '<a href="$1" target="_blank">$1</a>');

    //URLs starting with "www." (without // before it, or it'd re-link the ones done above).
    replacePattern2 = /(^|[^\/])(www\.[\S]+(\b|$))/gim;
    replacedText = replacedText.replace(replacePattern2, '$1<a href="http://$2" target="_blank">$2</a>');

    //Change email addresses to mailto:: links.
    replacePattern3 = /(([a-zA-Z0-9\-\_\.])+@[a-zA-Z\_]+?(\.[a-zA-Z]{2,6})+)/gim;
    replacedText = replacedText.replace(replacePattern3, '<a href="mailto:$1">$1</a>');

    return replacedText;
}

let chart = LightweightCharts.createChart(chartContainer, {
    width: 900,
    height: 600,
    layout: {
        backgroundColor: '#000000',
        textColor: 'rgba(255, 255, 255, 0.9)',
    },
    grid: {
        vertLines: {
            color: 'rgba(197, 203, 206, 0.5)',
        },
        horzLines: {
            color: 'rgba(197, 203, 206, 0.5)',
        },
    },
    crosshair: {
        mode: LightweightCharts.CrosshairMode.Normal,
    },
    priceScale: {
        borderColor: 'rgba(197, 203, 206, 0.8)',
    },
    timeScale: {
        borderColor: 'rgba(197, 203, 206, 0.8)',
    },
});

var candleSeries = chart.addCandlestickSeries({
    upColor: 'rgba(255, 144, 0, 1)',
    downColor: '#000',
    borderDownColor: 'rgba(255, 144, 0, 1)',
    borderUpColor: 'rgba(255, 144, 0, 1)',
    wickDownColor: 'rgba(255, 144, 0, 1)',
    wickUpColor: 'rgba(255, 144, 0, 1)',
});


function loadChartData(symbol = 'DOCU', from = null, to = null) {
    showSpinner();
    const url = base_url + '/fh/hist/' + symbol;
    fetch(url)
        .then((r) => r.json())
        .then((response) => {
                candleSeries.setData(response);
                chart.timeScale().fitContent();
                hideSpinner();
            }
        ).catch(err => {
        hideSpinner();
    });

}

function loadCompanyProfile(symbol) {
    const url = base_url + '/fh/company-profile/' + symbol;
    fetch(url)
        .then((r) => r.text())
        .then((response) => {
                tableContainer.innerHTML = linkify(response);
            }
        );
}

new ResizeObserver(entries => {
    if (entries.length === 0 || entries[0].target !== chartContainer) {
        return;
    }
    const newRect = entries[0].contentRect;
    chart.applyOptions({height: newRect.height, width: newRect.width});
    chart.timeScale().fitContent();


}).observe(chartContainer);

function loadTopPicks() {
    fetch(base_url + '/fh/top-picks')
        .then((r) => r.json())
        .then((response) => {
                console.log(response);
                response.forEach(function (item, index) {
                    let option = document.createElement("option");
                    option.text = item.symbol;
                    option.value = item.symbol;
                    option.selected = index === 0;
                    selectTopPick.add(option);
                });
                //    set data to first symbol
                loadChartData(response[0].symbol);
                loadCompanyProfile(response[0].symbol)
            }
        ).catch(error => {
        console.log(error);

    });


}


document.addEventListener("DOMContentLoaded", function () {
    loadTopPicks();
//    change ticker event
//     selectTopPick.onchange(function (e) {
//         console.log(e);
//         console.log(this.value);
//     });
    selectTopPick.addEventListener('change', function () {
        console.log('You selected: ', this.value);
        loadChartData(this.value);
        loadCompanyProfile(this.value);
    });
    // eventFire(document.getElementById('sidebarCollapse'), 'click');

});
