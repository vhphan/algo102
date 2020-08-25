const chartDiv = 'main-chart';
const barChartDiv = 'bar-chart';
const pieChartDiv = 'pie-chart';
const gaugeChartDiv = 'gauge-chart';

const chartContainer = document.getElementById(chartDiv);
const tableContainer = document.getElementById('profile-container');
const selectTopPick = document.getElementById('select-top-picks');
const selectChartType = document.getElementById('select-chart-type');
const selectMinMarkerCap = document.getElementById('select-market-cap-min');
const spinner = document.getElementById('spinner');
const currentUrl = document.location.href

let mainChart = echarts.init(document.getElementById(chartDiv));
const aggChart = echarts.init(document.getElementById(pieChartDiv), 'dark');
const gaugeChart = echarts.init(document.getElementById(gaugeChartDiv), 'dark');

const base_url = getBaseURL(currentUrl);

new ResizeObserver(entries => {
    if (entries.length === 0 || entries[0].target !== chartContainer) {
        return;
    }
    const newRect = entries[0].contentRect;
    mainChart.resize();
    aggChart.resize();

}).observe(chartContainer);

let breakoutList;
const breakingOut = True;
let breakoutWindowPercentage, breakoutWindowLength, breakoutMinMarketCap
breakoutWindowPercentage = 2;
breakoutWindowLength = 15;
breakoutMinMarketCap = 100;
let breakoutMin, breakoutMax;

function loadBreakouts() {
    fetch(base_url + '/fh/breakouts')
        .then((r) => r.json())
        .then((response) => {
                breakoutList = response;
                add_symbol_to_list(response);
                reloadCharts(response[0].symbol)
                breakoutMin =  response[0].min;
                breakoutMax =  response[0].max;

            }
        ).catch(error => {
        console.log(error);

    });

}


document.addEventListener("DOMContentLoaded", function () {
    loadBreakouts();
//    change ticker event
//     selectTopPick.onchange(function (e) {
//         console.log(e);
//         console.log(this.value);
//     });
    selectTopPick.addEventListener('change', function () {
        console.log('You selected: ', this.value);
        reloadCharts(this.value);
    });

    selectChartType.addEventListener('change', function () {
        let symbol = selectTopPick.value;
        mainChart.dispose();
        mainChart = echarts.init(document.getElementById(chartDiv), 'light')

        drawCandlestickChart(data, dates, symbol, volumes);
    });


    selectMinMarkerCap.addEventListener('change', function () {
        let symbol = selectTopPick.value;
        let filtered = symbols_details.filter(item => item['marketCapitalization'] >= this.value);
        console.log(filtered);
        selectTopPick.innerText = null;
        filtered.forEach(function (item, index) {
            let option = document.createElement("option");
            option.text = item.symbol;
            option.value = item.symbol;
            option.selected = index === 0;
            selectTopPick.add(option);
        });

        if (filtered[0].symbol !== symbol) {
            reloadCharts(filtered[0].symbol);
        }
        showSuccess('List filtered.')
    })
    // eventFire(document.getElementById('sidebarCollapse'), 'click');

    // let mainDiv = document.getElementById('main')
    // let indicatorsDiv = document.getElementById('indicators')
    // let aboutDiv = document.getElementById('about-content')
    //
    // document.getElementById('section1').addEventListener('click', (e) => {
    //     e.preventDefault();
    //     mainDiv.scrollIntoView();
    // });
    // document.getElementById('section2').addEventListener('click', (e) => {
    //     e.preventDefault();
    //     indicatorsDiv.scrollIntoView();
    // });
    // document.getElementById('section3').addEventListener('click', (e) => {
    //     e.preventDefault();
    //     aboutDiv.scrollIntoView();
    // });


});
