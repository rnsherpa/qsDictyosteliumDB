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
                label: 'Clone',
                backgroundColor: 'grey',
                data: data.data
            }]          
            },
            options: {
            responsive: true,
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Top 20 clones (by apprearances in papers)'
            }
            }
        });

        }
    });
});