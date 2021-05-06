$(function () {

    var $countsChart = $("#counts-chart");

    $.ajax({
        url: $countsChart.data("url"),
        success: function (data) {
            
        var ctx = $countsChart[0].getContext("2d");

        new Chart(ctx, {
            type: 'bar',
            data: {
            labels: data.labels,
            datasets: [{
                label: 'Count',
                backgroundColor: 'grey',
                data: data.data
            }]          
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false,
                    },
                    title: {
                        display: true,
                        text: 'Top 20 clones (by appearances in papers)'
                    }
                }
            }
        });

        }
    });
});