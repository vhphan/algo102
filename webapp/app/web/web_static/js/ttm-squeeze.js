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
// const aggChart = echarts.init(document.getElementById(pieChartDiv), 'dark');
// const gaugeChart = echarts.init(document.getElementById(gaugeChartDiv), 'dark');

let dates, data, volumes, symbols_details, last_update;
const base_url = getBaseURL(currentUrl);
let lowerBand
let upperBand
let lowerKeltner
let upperKeltner
let linearRegression
let seriesNames

new ResizeObserver(entries => {
    if (entries.length === 0 || entries[0].target !== chartContainer) {
        return;
    }
    const newRect = entries[0].contentRect;
    mainChart.resize();
    // aggChart.resize();

}).observe(chartContainer);

function ttmloadChartData(symbol) {
    showSpinner();
    const url = base_url + '/bb/hist/' + symbol;
    fetch(url + '?indicators=ttm-squeeze')
        .then((r) => r.json())
        .then((rawData) => {
                dates = rawData.map(function (item) {
                    return unixtimeToDateString(item['time']);
                });
                data = rawData.map(function (item) {
                    return [+item['open'], +item['close'], +item['low'], +item['high']]; // oclh
                });
                volumes = unpack('volume', rawData)
                // 'lower_band',
                // 'upper_band',
                // 'lower_keltner',
                // 'upper_keltner'
                lowerBand = unpack('lower_band', rawData)
                upperBand = unpack('upper_band', rawData)
                lowerKeltner = unpack('lower_keltner', rawData)
                upperKeltner = unpack('upper_keltner', rawData)
                linearRegression = unpack('linreg', rawData)
                seriesNames = ['bollinger_lower', 'bollinger_upper', 'lower_keltner', 'upper_keltner', 'momentum']
                drawCandlestickChart(data,
                    dates,
                    symbol,
                    volumes,
                    [{
                        name: 'ttm',
                        seriesNames,
                        data: [lowerBand, upperBand, lowerKeltner, upperKeltner, linearRegression],
                        colors: ['blue', 'blue', 'red', 'red', '']
                    }], false);
                console.log(data, dates, symbol, volumes)
                hideSpinner();
                clearError();
            }
        ).catch(err => {
        showError('getting data for ' + symbol);
        hideSpinner();
    });

}

function ttmReloadCharts(symbol) {
    ttmloadChartData(symbol);
    // ttmloadAggregateIndicators(symbol)
    // ttmloadSymbolProfile(symbol)
}


function ttmLoadTopPicks() {
    fetch(base_url + '/bb/squeeze-list')
        .then((r) => r.json())
        .then((response) => {
                console.log(response);
                symbols_details = response['data'];
                last_update = response['last_update'];
                document.getElementById('last_update').innerText = last_update;

                add_symbol_to_list(response['data']);

                ttmReloadCharts(symbols_details[0].symbol);
            }
        ).catch(error => {
        console.log(error);
    });
}

document.addEventListener("DOMContentLoaded", function () {
    ttmLoadTopPicks();

    selectTopPick.addEventListener('change', function () {
        console.log('You selected: ', this.value);
        ttmReloadCharts(this.value);
    });

    selectChartType.addEventListener('change', function () {
        let symbol = selectTopPick.value;
        mainChart.dispose();
        mainChart = echarts.init(document.getElementById(chartDiv), 'light')

        // drawCandlestickChart(data, dates, symbol, volumes);
        drawCandlestickChart(data,
            dates,
            symbol,
            volumes,
            [{
                name: 'ttm',
                seriesNames,
                data: [lowerBand, upperBand, lowerKeltner, upperKeltner, linearRegression],
                colors: ['blue', 'blue', 'red', 'red', '']
            }], false);
    });


});

