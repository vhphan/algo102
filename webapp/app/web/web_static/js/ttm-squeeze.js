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
const base_url = getBaseURL(currentUrl);


new ResizeObserver(entries => {
    if (entries.length === 0 || entries[0].target !== chartContainer) {
        return;
    }
    const newRect = entries[0].contentRect;
    mainChart.resize();
    aggChart.resize();

}).observe(chartContainer);

function ttmloadChartData(symbol) {

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
                symbols_details = response;
                add_symbol_to_list(response);

                // ttmReloadCharts(response[0].symbol);
            }
        ).catch(error => {
        console.log(error);

    });
}

document.addEventListener("DOMContentLoaded", function () {
    ttmLoadTopPicks();

    selectTopPick.addEventListener('change', function () {
        console.log('You selected: ', this.value);
        reloadCharts(this.value);
    });

    selectChartType.addEventListener('change', function () {
        let symbol = selectTopPick.value;
        mainChart.dispose();
        mainChart = echarts.init(document.getElementById(chartDiv), 'light')

        // drawCandlestickChart(data, dates, symbol, volumes);
    });




});

