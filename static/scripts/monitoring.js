var se = window.localStorage.getItem("s");

$(document).ready(function () {
    $.ajax({
        url: BASE_URL + 'crud/get_pending_attendance?s=' + se,
        method: 'GET',
        success: function (output, status, xhr) {
            const return_obj = JSON.parse(output);
            if (return_obj.status == 1) {
                return_obj.data.forEach(function (item) {
                    $("#pending_list").prepend(`<a href="#" onclick="openPending('` + item[0] + `')"><div class="alert alert-warning" role="alert"> 
                        <h4 class="alert-heading"> 
                            `+ item[1] + ` :  ` + item[2] + `
                        </h4> 
                        <p>Schedule On:  `+ item[3] + `</p> 
                    </div></a>`);
                });

            }
            else
                fAlert(return_obj.message);
        }
    });
    setTimeout(function () {
        PopulateSelect("section", "crud/get_subject?s=" + se, "Select Subject", null, true);
    }, 250);

    setTimeout(function () {
        PopulateSelect("sectionM", "crud/get_subject?s=" + se, "Select Subject", null, true);
    }, 250);


    setTimeout(function () {
        getData();
    }, 500);
    function getData() {
        $.ajax({
            url: BASE_URL + 'crud/get_adv_set?s=' + se,
            method: 'GET',
            success: function (output, status, xhr) {
                const return_obj = JSON.parse(output);
                if (return_obj.status == 1) {
                    $('#latetime').val(return_obj['data'][1][1]);
                }
                else
                    fAlert(return_obj.message);
            }
        });
    }



    $('#submitA').click(function () {
        if (checkFormC("setmonitoringfrm")) {
            var type = $('#atype').val();
            //$("#loader").show(); // shows the loading screen
            window.swal({
                title: "Loading...",
                text: "Please wait",
                icon: "https://c.tenor.com/I6kN-6X7nhAAAAAj/loading-buffering.gif",
                showConfirmButton: false,
                allowOutsideClick: false
            });
            $.ajax({
                url: BASE_URL + 'crud/setmonitoring?s=' + se,
                method: 'post',
                data: $("#setmonitoringfrm").serialize(),
                success: function (output, status, xhr) {
                    const return_obj = JSON.parse(output);
                    if (return_obj.status == 1) {
                        if (Number(type) == 1)
                            sAlert(return_obj.message, './monitoring_cam');
                        else
                            sAlert(return_obj.message, './monitoring_online');
                    }
                    else if (return_obj.status == 2) {
                        swal({
                            title: "Warning",
                            text: return_obj.message,
                            type: "warning",
                            buttons: {
                                o1: 'Continue Monitoring',
                                o2: 'Stop Monitoring',
                                o3: 'Close',
                            },
                        }).then((value) => {
                            switch (value) {
                                case 'o1':
                                    sAlert("Redirecting you to Monitoring Page", './monitoring_cam');
                                    break;
                                case 'o2':
                                    stopMonitoring();
                                    break;

                                case 'o3':
                                    swal.close();
                                    break;
                            }
                        });
                    }
                    else {
                        fAlert(return_obj.message);
                        swal.close();
                    }

                }
            });
        }
    });

    $('#sectionM').on('change', function () {
        $("#manual_sched").html(
            `<div id="scheduleM-spinner" class="spinner-border spinner-border-sm">
            <span class="sr-only">Loading...</span>
        </div>
        <select name="scheduleM" style="width: 100%; display: none;" required></select>`
        );
        PopulateSelect("scheduleM", "crud/get_schedules?sid=" + this.value + '&s=' + se, "Select Schedule", null, true);
    });

    $('#submitM').click(function () {
        if (checkFormC("setmanualmonitoringfrm"))
            $.ajax({
                url: BASE_URL + 'crud/manual_att?s=' + se,
                method: 'post',
                data: $("#setmanualmonitoringfrm").serialize(),
                success: function (output, status, xhr) {
                    const return_obj = JSON.parse(output);
                    if (return_obj.status == 1)
                        sAlert(return_obj.message, './manual');
                    else
                        fAlert(return_obj.message);
                }
            });
    });

});
// var optionButtons = $('<div>')
//     .append(createButton('Continue Monitoring', function () {

//     })).append(createButton('Stop Monitoring', function () {

//     })).append(createButton('Cancel Action', function () {

//     }));
// function createButton(text, cb) {
//     return $(`<button type="button" class="btn btn-info">` + text + `</button>`).on('click', cb);
// }

function stopMonitoring() {
    $.ajax({
        url: BASE_URL + 'crud/stop_monitoring?s=' + se,
        method: 'GET',
        success: function (output, status, xhr) {
            const return_obj = JSON.parse(output);
            if (return_obj.status == 1) {
                window.location.href = "./manual";
            }
            else
                fAlert(return_obj.message);
        }
    });
}

function openPending(id) {
    window.swal({
        title: "Loading...",
        text: "Please wait",
        icon: "https://c.tenor.com/I6kN-6X7nhAAAAAj/loading-buffering.gif",
        showConfirmButton: false,
        allowOutsideClick: false
    });
    $.ajax({
        url: BASE_URL + 'crud/continue_pending_monitoring?s=' + se,
        method: 'POST',
        data: { 'id': id },
        success: function (output, status, xhr) {
            const return_obj = JSON.parse(output);
            if (return_obj.status == 1) {
                sAlert(return_obj.message, './monitoring_cam');
            }
            else if (return_obj.status == 2) {
                swal({
                    title: "Warning",
                    text: return_obj.message,
                    type: "warning",
                    buttons: {
                        o1: 'Continue Monitoring',
                        o2: 'Stop Monitoring',
                        o3: 'Close',
                    },
                }).then((value) => {
                    switch (value) {
                        case 'o1':
                            sAlert("Redirecting you to Monitoring Page", './monitoring_cam');
                            break;
                        case 'o2':
                            stopMonitoring();
                            break;

                        case 'o3':
                            swal.close();
                            break;
                    }
                });
            }
            else {
                fAlert(return_obj.message);
                swal.close();
            }
        }
    });
};


