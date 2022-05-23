$(document).ready(function () {
    // alert(window.localStorage.getItem("session"));
    var se = window.localStorage.getItem("s");
    $.ajax({
        url: BASE_URL + "crud/get_dashboard_details?s=" + se,
        type: 'GET',
        success: function (output) {

            const return_obj = JSON.parse(output);
            Highcharts.chart('bar_container', {
                chart: {
                    type: 'bar'
                },
                title: {
                    text: 'Total Status per Section'
                },
                subtitle: {
                    text: 'The following is the total number of Absent, Present, Late and Excused per Section'
                },
                xAxis: {
                    categories: return_obj[0][0],
                    title: {
                        text: null
                    }
                },
                // yAxis: {
                //     min: 0,
                //     title: {
                //         text: 'Population (millions)',
                //         align: 'high'
                //     },
                //     labels: {
                //         overflow: 'justify'
                //     }
                // },
                // tooltip: {
                //     valueSuffix: ' students'
                // },
                plotOptions: {
                    bar: {
                        dataLabels: {
                            enabled: true
                        }
                    }
                },
                legend: {
                    layout: 'vertical',
                    align: 'right',
                    verticalAlign: 'top',
                    x: -40,
                    y: 80,
                    floating: true,
                    borderWidth: 1,
                    backgroundColor:
                        Highcharts.defaultOptions.legend.backgroundColor || '#FFFFFF',
                    shadow: true
                },
                credits: {
                    enabled: false
                },
                series: [{
                    name: 'Present',
                    data: return_obj[0][2]
                }, {
                    name: 'Late',
                    data: return_obj[0][3]
                }, {
                    name: 'Excused',
                    data: return_obj[0][4]
                }, {
                    name: 'Absent',
                    data: return_obj[0][1]
                }]
            });


            Highcharts.chart('line_container', {

                title: {
                    text: 'Total Status per Month'
                },

                subtitle: {
                    text: 'The following is the total number of Absent, Present, Late and Excused per Month'
                },

                // yAxis: {
                //     title: {
                //         text: 'Number of Employees'
                //     }
                // },

                xAxis: {
                    accessibility: {
                        rangeDescription: 'Range: 2010 to 2017'
                    },
                    categories: return_obj[1][0]
                },
                legend: {
                    layout: 'vertical',
                    align: 'right',
                    verticalAlign: 'middle'
                },

                series: [{
                    name: 'Present',
                    data: return_obj[1][2]
                }, {
                    name: 'Late',
                    data: return_obj[1][3]
                }, {
                    name: 'Excused',
                    data: return_obj[1][4]
                }, {
                    name: 'Absent',
                    data: return_obj[1][1]
                }],

                responsive: {
                    rules: [{
                        condition: {
                            maxWidth: 500
                        },
                        chartOptions: {
                            legend: {
                                layout: 'horizontal',
                                align: 'center',
                                verticalAlign: 'bottom'
                            }
                        }
                    }]
                }

            });

            $("#a1").html(return_obj[2][2]);
            $("#a2").html(return_obj[2][1]);
            $("#a3").html(return_obj[2][0]);
            $("#a4").html(return_obj[2][3]);

        }
    });







});

