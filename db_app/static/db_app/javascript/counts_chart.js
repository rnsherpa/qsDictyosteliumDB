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
                maintainAspectRatio: false,
                scaleShowValues: true,
                scales: {
                    x: {
                    ticks: {
                        autoSkip: false
                    }
                    }
                },
                plugins: {
                    legend: {
                        display: false,
                    },
                    title: {
                        display: true,
                        text: 'Top 50 clones (by appearances in papers)'
                    }
                }
            }
        });

        }
    });
});