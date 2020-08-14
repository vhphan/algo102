const chartDiv = 'main-chart';
const barChartDiv = 'bar-chart';
const pieChartDiv = 'pie-chart';
const gaugeChartDiv = 'gauge-chart';


// var dates = rawData.map(function (item) {
//     return item[0];
// });
//
// var data = rawData.map(function (item) {
//     return [+item[1], +item[2], +item[5], +item[6]]; // oclh
// });
const chartContainer = document.getElementById(chartDiv);
const tableContainer = document.getElementById('profile-container');
const selectTopPick = document.getElementById('select-top-picks');
const selectChartType = document.getElementById('select-chart-type');
const selectMinMarkerCap = document.getElementById('select-market-cap-min');
const spinner = document.getElementById('spinner');
const snackbar = document.getElementById('snackbar');
const currentUrl = document.location.href

let mainChart = echarts.init(document.getElementById(chartDiv));
const aggChart = echarts.init(document.getElementById(pieChartDiv), 'dark');
const gaugeChart = echarts.init(document.getElementById(gaugeChartDiv), 'dark');

let dates, data, volumes, symbols_details;

// const myBarChart = echarts.init(document.getElementById(barChartDiv));
function getTheme(theme) {
    fetch(`/static/json/${theme}.json`)
        .then(response => JSON.parse(response))
        .then(themeObj => echarts.registerTheme(theme, themeObj))

    // Assume the theme name is "vintage".
    // var xhr = new XMLHttpRequest();
    // xhr.open('GET', `/static/json/${theme}.json`, true);
    // xhr.onload = function () {
    //     var themeJSON = this.response;
    //     echarts.registerTheme(theme, JSON.parse(themeJSON))
    // }
    // xhr.send();
}

function showError(addMsg = '') {
    const errorDiv = document.getElementById('ajax-fail');
    const htmlVal = "" +
        "<div class=\"alert alert-danger alert-dismissible fade show\" role=\"alert\">\n" +
        "  <strong>Holy guacamole!</strong> Error." + addMsg + "\n" +
        "  <button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\">\n" +
        "    <span aria-hidden=\"true\">&times;</span>\n" +
        "  </button>\n" +
        "</div>";
    errorDiv.innerHTML += htmlVal;
}


function removeFadeOut(el, speed) {
    var seconds = speed / 1000;
    el.style.transition = "opacity " + seconds + "s ease";

    el.style.opacity = 0;
    setTimeout(function () {
        el.parentNode.removeChild(el);
    }, speed);
}


function showSuccess(addMsg = '') {
    const errorDiv = document.getElementById('ajax-fail');
    const htmlVal = "" +
        "<div id='show-success' class=\"alert alert-success alert-dismissible fade show\" role=\"alert\">\n" +
        "  <strong>Success!</strong>" + addMsg + "\n" +
        "  <button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\">\n" +
        "    <span aria-hidden=\"true\">&times;</span>\n" +
        "  </button>\n" +
        "</div>";
    errorDiv.innerHTML += htmlVal;

    // removeFadeOut(document.getElementById('show-success'), 1500)
    setTimeout(function () {
        $("#show-success").alert('close');
    }, 1500);
    setTimeout(function () {
        errorDiv.innerHTML = '';
    }, 3500);
}

function clearError() {
    const errorDiv = document.getElementById('ajax-fail');
    const htmlVal = "";
    if (errorDiv.innerHTML.indexOf("Error") !== -1) {
        errorDiv.innerHTML = htmlVal;
    }
}

function unpack(key, obj) {
    return obj.map(function (item) {
        return item[key];
    });
}

function calculateMA(dayCount, data) {
    var result = [];
    for (var i = 0, len = data.length; i < len; i++) {
        if (i < dayCount) {
            result.push('-');
            continue;
        }
        var sum = 0;
        for (var j = 0; j < dayCount; j++) {
            sum += data[i - j][1];
        }
        result.push((sum / dayCount).toFixed(2));
    }
    return result;
}

function barChart(rawData0) {
    // rawData = rawData0.reverse().slice(0, 11);
    rawData = rawData0.reverse();
    let data = {};
    data['buy'] = unpack('buy', rawData);
    data['hold'] = unpack('hold', rawData);
    data['sell'] = unpack('sell', rawData);
    data['strong_buy'] = unpack('strong_buy', rawData)
    data['strong_sell'] = unpack('strong_sell', rawData);
    data['period'] = unpack('period', rawData);
    console.log(rawData);
    console.log(data);
    let option = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        legend: {
            data: ['strong_buy', 'buy', 'hold', 'sell', 'strong_sell']
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                textStyle: {
                    color: '#fff'
                }
            }
        },
        xAxis: {
            type: 'category',
            data: data['period'],
            axisLabel: {
                textStyle: {
                    color: '#fff'
                }
            }
        },
        series: [
            {
                name: 'strong buy',
                type: 'bar',
                stack: '总量',
                label: {
                    show: true,
                    position: 'insideRight'
                },
                data: data['strong_buy'],
                color: '#025817'
            },
            {
                name: 'buy',
                type: 'bar',
                stack: '总量',
                label: {
                    show: true,
                    position: 'insideRight'
                },
                data: data['buy'],
                color: '#34ee0c'
            },
            {
                name: 'hold',
                type: 'bar',
                stack: '总量',
                label: {
                    show: true,
                    position: 'insideRight'
                },
                data: data['hold'],
                color: '#2c15e7'
            },
            {
                name: 'sell',
                type: 'bar',
                stack: '总量',
                label: {
                    show: true,
                    position: 'insideRight'
                },
                data: data['sell'],
                color: '#de0b0b'
            },

            {
                name: 'strong sell',
                type: 'bar',
                stack: '总量',
                label: {
                    show: true,
                    position: 'insideRight'
                },
                data: data['strong_sell'],
                color: '#890202'
            }
        ]
    };
    myBarChart.setOption(option);

}


function drawCandlestickChart(data, dates, symbol, volumes) {
    const dataMA10 = calculateMA(10, data);
    const dataMA20 = calculateMA(20, data);
    const dataMA50 = calculateMA(50, data);
    const dataMA100 = calculateMA(100, data);
    const windows = [10, 20, 50, 100]
    let dataMA = [];
    let dataNameMA = []
    windows.forEach((window, index) => {
        dataMA.push(calculateMA(window, data));
        dataNameMA.push(`MA${window}`);
    });
    let option1 = {
        backgroundColor: '#000',
        legend: {
            data: [symbol].concat(dataNameMA),
            inactiveColor: '#777',
            textStyle: {
                color: '#fff'
            }
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                animation: false,
                type: 'cross',
                lineStyle: {
                    color: '#376df4',
                    width: 2,
                    opacity: 1
                }
            }
        },
        xAxis: {
            type: 'category',
            data: dates,
            axisLine: {lineStyle: {color: '#8392A5'}}
        },
        yAxis: {
            scale: true,
            axisLine: {lineStyle: {color: '#8392A5'}},
            splitLine: {show: false}
        },
        grid: {
            bottom: 80,
            left: '3%',
            right: '3%'
        },
        dataZoom: [{
            textStyle: {
                color: '#8392A5'
            },
            handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
            handleSize: '80%',
            dataBackground: {
                areaStyle: {
                    color: '#8392A5'
                },
                lineStyle: {
                    opacity: 0.8,
                    color: '#8392A5'
                }
            },
            handleStyle: {
                color: '#fff',
                shadowBlur: 3,
                shadowColor: 'rgba(0, 0, 0, 0.6)',
                shadowOffsetX: 2,
                shadowOffsetY: 2
            },
            start: 50,
            end: 100
        }, {
            type: 'inside',
            start: 50,
            end: 100
        }],
        animation: false,
        series: [

            {
                type: 'candlestick',
                name: symbol,
                data: data,
                itemStyle: {
                    color: '#0CF49B',
                    color0: '#FD1050',
                    borderColor: '#0CF49B',
                    borderColor0: '#FD1050'
                }
            },
            {
                name: dataNameMA[0],
                type: 'line',
                data: dataMA[0],
                smooth: true,
                showSymbol: false,
                lineStyle: {
                    width: 1
                }
            },
            {
                name: dataNameMA[1],
                type: 'line',
                data: dataMA[1],
                smooth: true,
                showSymbol: false,
                lineStyle: {
                    width: 1
                }
            },
            {
                name: dataNameMA[2],
                type: 'line',
                data: dataMA[2],
                smooth: true,
                showSymbol: false,
                lineStyle: {
                    width: 1
                }
            },
            {
                name: dataNameMA[3],
                type: 'line',
                data: dataMA[3],
                smooth: true,
                showSymbol: false,
                lineStyle: {
                    width: 1
                }
            }
        ]
    };

    const upColor = '#00da3c';
    const downColor = '#ec0000';
    let volumes2 = volumes.map((item, i) => {
        return [i, item, data[i][0] > data[i][1] ? 1 : -1];
    });

    let option2 = {
        backgroundColor: '#000',
        animation: false,
        legend: {
            bottom: 10,
            left: 'center',
            data: [symbol].concat(dataNameMA),
            textStyle: {color: '#fff'}
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross'
            },
            // backgroundColor: 'rgba(245, 245, 245, 0.8)',
            borderWidth: 1,
            // borderColor: '#ccc',
            padding: 10,
            textStyle: {
                // color: '#000'
            },
            position: function (pos, params, el, elRect, size) {
                var obj = {top: 10};
                obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 30;
                return obj;
            },
            extraCssText: 'width: 170px'
        },
        axisPointer: {
            link: {xAxisIndex: 'all'},
            label: {
                backgroundColor: '#777'
            }
        },
        toolbox: {
            feature: {
                dataZoom: {
                    yAxisIndex: false
                },
                brush: {
                    type: ['lineX', 'clear']
                }
            }
        },
        brush: {
            xAxisIndex: 'all',
            brushLink: 'all',
            outOfBrush: {
                colorAlpha: 0.1
            }
        },
        visualMap: {
            show: false,
            seriesIndex: 5,
            dimension: 2,
            pieces: [{
                value: 1,
                color: downColor
            }, {
                value: -1,
                color: upColor
            }]
        },
        grid: [
            {
                left: '3%',
                right: '3%',
                height: '50%',
            },
            {
                left: '3%',
                right: '3%',
                top: '63%',
                height: '16%',
            }
        ],
        xAxis: [
            {
                type: 'category',
                data: dates,
                scale: true,
                boundaryGap: false,
                axisLine: {onZero: false},
                splitLine: {show: false},
                splitNumber: 20,
                min: 'dataMin',
                max: 'dataMax',
                axisPointer: {
                    z: 100
                },
                axisLabel: {show: false},
            },
            {
                type: 'category',
                gridIndex: 1,
                data: dates,
                scale: true,
                boundaryGap: false,
                axisLine: {onZero: false},
                axisTick: {show: false},
                splitLine: {show: false},
                splitNumber: 20,
                min: 'dataMin',
                max: 'dataMax',
                axisPointer: {
                    label: {
                        formatter: function (params) {
                            var seriesValue = (params.seriesData[0] || {}).value;
                            return params.value
                                + (seriesValue != null
                                        ? '\n' + echarts.format.addCommas(seriesValue)
                                        : ''
                                );
                        }
                    }
                },
                axisLabel: {textStyle: {color: '#fff'}}

            }
        ],
        yAxis: [
            {
                scale: true,
                // splitArea: {
                //     show: true
                // }
                axisLabel: {textStyle: {color: '#fff'}},
                splitLine: {show: false},


            },
            {
                scale: true,
                gridIndex: 1,
                // splitNumber: 2,
                axisLabel: {show: false},
                axisLine: {show: false},
                axisTick: {show: false},
                splitLine: {show: false},
            }
        ],
        dataZoom: [
            {
                type: 'inside',
                xAxisIndex: [0, 1],
                start: 50,
                end: 100
            },
            {
                show: true,
                xAxisIndex: [0, 1],
                type: 'slider',
                top: '85%',
                start: 50,
                end: 100
            }
        ],
        color: ['#1E96FC', '#A2D6F9', '#FCF300', '#FFC600'],
        series: [
            {
                name: symbol,
                type: 'candlestick',
                data: data,
                itemStyle: {
                    normal: {
                        color: upColor,
                        color0: downColor,
                        borderColor: null,
                        borderColor0: null
                    }
                },
            },
            {
                name: dataNameMA[0],
                type: 'line',
                data: dataMA[0],
                showSymbol: false,
                smooth: true,
                lineStyle: {
                    width: 1
                }
            },
            {
                name: dataNameMA[1],
                type: 'line',
                data: dataMA[1],
                showSymbol: false,
                smooth: true,
                lineStyle: {
                    width: 1

                }
            },
            {
                name: dataNameMA[2],
                type: 'line',
                data: dataMA[2],
                showSymbol: false,
                smooth: true,
                lineStyle: {
                    width: 1


                }
            },
            {
                name: dataNameMA[3],
                type: 'line',
                data: dataMA[3],
                showSymbol: false,
                smooth: true,
                lineStyle: {
                    width: 1

                }
            },
            {
                name: 'Volume',
                type: 'bar',
                xAxisIndex: 1,
                yAxisIndex: 1,
                data: volumes2
            }
        ]
    };
    let chartOptions = [option1, option2]
    option = chartOptions[parseInt(selectChartType.value) - 1];
    mainChart.setOption(option);

}


function drawPieChart(chartData) {

    // rawData = [
    //     {value: 335, name: 'buy'},
    //     {value: 310, name: 'neutral'},
    //     {value: 274, name: 'sell'},
    // ]
    const sortedData = chartData.sort(function (a, b) {
        return a.value - b.value;
    });
    const color_map = {
        'buy': '#47ff00',
        'sell': '#fd0020',
        'neutral': '#0055ff',
    }
    let colors = [];
    sortedData.forEach(function (item, index) {
        colors.push(color_map[item['name']]);
    })

    // const option = {
    //     // backgroundColor: 'rgba(95,99,101,0.58)',
    //     backgroundColor: 'rgba(238,231,231,0.58)',
    //
    //     title: {
    //         text: 'Aggregate Indicators',
    //         left: 'center',
    //         top: 20,
    //         textStyle: {
    //             color: '#ccc'
    //         }
    //     },
    //
    //     tooltip: {
    //         trigger: 'item',
    //         formatter: '{a} <br/>{b} : {c} ({d}%)'
    //     },
    //
    //     visualMap: {
    //         show: false,
    //         min: 80,
    //         max: 600,
    //         inRange: {
    //             colorLightness: [0, 1]
    //         }
    //     },
    //     series: [
    //         {
    //             color: colors,
    //             name: 'Aggregate Indicators (Daily)',
    //             type: 'pie',
    //             radius: '55%',
    //             center: ['50%', '50%'],
    //             data: sortedData,
    //             roseType: 'radius',
    //             label: {
    //                 color: 'rgba(255, 255, 255, 0.3)'
    //             },
    //             labelLine: {
    //                 lineStyle: {
    //                     color: 'rgba(255, 255, 255, 0.3)'
    //                 },
    //                 smooth: 0.2,
    //                 length: 10,
    //                 length2: 20
    //             },
    //             // itemStyle: {
    //             //     shadowBlur: 200,
    //             //     shadowColor: 'rgba(0, 0, 0, 0.5)'
    //             // },
    //
    //             animationType: 'scale',
    //             animationEasing: 'elasticOut',
    //             animationDelay: function (idx) {
    //                 return Math.random() * 200;
    //             }
    //         }
    //     ]
    // };
    const option = {
        backgroundColor: '#000',
        radius: [0, '100%'],
        grid: {
            left: 0,
            top: 0,
            right: 0,
            bottom: 0
        },
        title: {
            bottom: 0,
            text: 'Aggregated Indicators',
            subtext: '# of indicators for each signal',
            left: 'center',
            textStyle: {color: '#fff'}

        },
        tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b} : {c} ({d}%)'
        },

        series: [
            {
                name: 'Aggregated Indicators',
                type: 'pie',
                radius: '55%',
                center: ['40%', '50%'],
                data: sortedData,
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                },
                color: colors

            }
        ]
    };
    aggChart.setOption(option);
}

function drawGaugeChart(chartData = [{value: 40, name: 'ADX'}], trending) {

    if (trending === undefined) {
        if (chartData[0]['value'] < 25) {
            trending = 'weak';
        } else if (chartData[0]['value'] < 50) {
            trending = 'strong';
        } else if (chartData[0]['value'] < 75) {
            trending = 'very strong';
        } else if (chartData[0]['value'] < 100) {
            trending = 'extremely strong';
        }
    }
    const option = {
        radius: '100%',
        // left: 0,
        // right: 0,
        // top: 0,
        // bottom: 0,
        // grid: {
        //     left: 0,
        //     top: 0,
        //     right: 0,
        //     bottom: 0
        // },
        title: {
            text: 'Average Directional Index',
            subtext: 'Trending=' + trending,
            left: 'center',
            textStyle: {color: '#fff'},
            bottom: 0,
        },
        backgroundColor: '#000',
        tooltip: {
            formatter: '{a} <br/>{c} {b}'
        },
        toolbox: {
            show: true,
            feature: {
                mark: {show: true},
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        series: [
            {
                name: 'Average Directional Index',
                type: 'gauge',
                min: 0,
                max: 100,
                splitNumber: 5,
                radius: '50%',
                axisLine: {            // 坐标轴线
                    lineStyle: {       // 属性lineStyle控制线条样式
                        color: [[0.25, 'lime'], [0.50, '#1e90ff'], [0.75, '#e57d1e'], [1, '#ff4500']],
                        width: 3,
                        shadowColor: '#fff', //默认透明
                        shadowBlur: 10
                    }
                },
                axisLabel: {            // 坐标轴小标记
                    fontWeight: 'bolder',
                    color: '#fff',
                    shadowColor: '#fff', //默认透明
                    shadowBlur: 10
                },
                axisTick: {            // 坐标轴小标记
                    length: 15,        // 属性length控制线长
                    lineStyle: {       // 属性lineStyle控制线条样式
                        color: 'auto',
                        shadowColor: '#fff', //默认透明
                        shadowBlur: 10
                    }
                },
                splitLine: {           // 分隔线
                    length: 25,         // 属性length控制线长
                    lineStyle: {       // 属性lineStyle（详见lineStyle）控制线条样式
                        width: 3,
                        color: '#fff',
                        shadowColor: '#fff', //默认透明
                        shadowBlur: 10
                    }
                },
                pointer: {           // 分隔线
                    shadowColor: '#fff', //默认透明
                    shadowBlur: 5
                },
                title: {
                    textStyle: {       // 其余属性默认使用全局文本样式，详见TEXTSTYLE
                        fontWeight: 'bolder',
                        fontSize: 20,
                        fontStyle: 'italic',
                        color: '#fff',
                        shadowColor: '#fff', //默认透明
                        shadowBlur: 10
                    }
                },
                detail: {
                    backgroundColor: 'rgba(30,67,255,0.8)',
                    borderWidth: 1,
                    borderColor: '#fff',
                    shadowColor: '#fff', //默认透明
                    shadowBlur: 5,
                    offsetCenter: [0, '50%'],       // x, y，单位px
                    textStyle: {       // 其余属性默认使用全局文本样式，详见TEXTSTYLE
                        fontWeight: 'bolder',
                        color: '#fff'
                    },
                    // formatter: '{value}%'

                },
                data: chartData
            },
        ]
    };
    gaugeChart.setOption(option);

}


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

function eventFire(el, etype) {
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

function formatDate(date) {
    let d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2)
        month = '0' + month;
    if (day.length < 2)
        day = '0' + day;

    return [year, month, day].join('-');
}

function unixtimeToDateString(unixTime) {
    const milliseconds = unixTime * 1000 // 1575909015000
    const dateObject = new Date(milliseconds)
    return formatDate(dateObject);
}

function loadAggregateIndicators(symbol = 'DOCU', from = null, to = null) {
    const url = base_url + '/fh/aggregate-indicators/' + symbol;
    fetch(url)
        .then((r) => r.json())
        .then((rawData) => {

                let countObj = rawData['technical_analysis']['count'];
                let data = [];
                Object.keys(countObj).forEach((key, index) => {
                    let item = {}
                    item['name'] = key;
                    item['value'] = countObj[key];
                    data.push(item);
                })
                drawPieChart(data);
                console.log(data);

                let trend = rawData['trend'];
                let trending = rawData['trending'];
                drawGaugeChart([{value: Math.round(trend['adx']), name: 'ADX'}], trending)

            }
        ).catch(err => {
    });
}


function loadChartData(symbol = 'DOCU', from = null, to = null) {
    showSpinner();
    const url = base_url + '/fh/hist/' + symbol;
    fetch(url)
        .then((r) => r.json())
        .then((rawData) => {
                dates = rawData.map(function (item) {
                    return unixtimeToDateString(item['time']);
                });
                data = rawData.map(function (item) {
                    return [+item['open'], +item['close'], +item['low'], +item['high']]; // oclh
                });
                volumes = unpack('volume', rawData)
                drawCandlestickChart(data, dates, symbol, volumes);
                hideSpinner();
                clearError();
            }
        ).catch(err => {
        showError('getting data for ' + symbol);
        hideSpinner();
    });

}

function loadBarChartData(symbol = 'DOCU', from = null, to = null) {
    showSpinner();
    const url = base_url + '/fh/recommendation-trends/' + symbol;
    fetch(url)
        .then((r) => r.json())
        .then((rawData) => {

                barChart(rawData);
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
    mainChart.resize();
    aggChart.resize();

}).observe(chartContainer);

function reloadCharts(symbol) {
    //    set data to first symbol
    loadChartData(symbol);
    loadAggregateIndicators(symbol)
    // loadBarChartData(response[0].symbol);
    loadCompanyProfile(symbol)
}

function loadTopPicks() {

    fetch(base_url + '/fh/top-picks')
        .then((r) => r.json())
        .then((response) => {
                console.log(response);
                symbols_details = response;
                response.forEach(function (item, index) {
                    let option = document.createElement("option");
                    option.text = item.symbol;
                    option.value = item.symbol;
                    option.selected = index === 0;
                    selectTopPick.add(option);
                });
                reloadCharts(response[0].symbol);
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

(function () {


})();