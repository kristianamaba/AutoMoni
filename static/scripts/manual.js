var se = window.localStorage.getItem("s");
let studentCount = 0;
$(document).ready(function () {

    $('#submit').click(function () {
        disableExcess();
        var data = new FormData($('#manualfrm')[0]);
        $.ajax({
            url: BASE_URL + 'crud/set_manual_att?s=' + se,
            method: 'post',
            data: data,
            mimeType: "multipart/form-data",
            contentType: false,
            processData: false,
            success: function (output, status, xhr) {
                const return_obj = JSON.parse(output);
                if (return_obj.status == 1)
                    sAlert(return_obj.message, './monitoring');
                else
                    fAlert(return_obj.message);
            }
        });
    });

    $.ajax({
        url: BASE_URL + 'crud/get_manual_att?s=' + se,
        method: 'GET',
        success: function (output, status, xhr) {
            const return_obj = JSON.parse(output);
            if (return_obj.status == 1) {
                return_obj['data'].forEach(function (item, index, arr) {
                    studentCount++;
                    $("#unlisted_manual_list").append(
                        `<div class="col-sm-3">
                        <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">`+ item[1] + `</h5>
                            <input type="hidden" id="validH`+ studentCount + `" value="0" name="isValid">
                            <input type="checkbox" id="valid`+ studentCount + `" value="1" name="isValid"> Validated
                            <select class="form-control" name="stat">
                                <option SELECTED value="0">Absent</option>
                                <option value="1">Present</option>
                                <option value="2">Late</option>
                                <option value="3">Excused</option>
                            </select>
                            <input type="hidden" name="id" value="`+ item[0] + `">
                        </div>
                        </div> 
                    </div> `
                    ).show('slow');
                });

                if (return_obj['data'].length === 0) {
                    $("#ulist_title").hide();
                    $("#list_title").hide();
                    // $("#unlisted_manual_list").html("<p class='ml-4'>Nothing to show</p>");
                }
                // $('#edit-name').val(return_obj.data);
            }
            else
                fAlert(return_obj.message);
        }
    });

    setTimeout(function () {
        $.ajax({
            url: BASE_URL + 'crud/get_manual_att_listed?s=' + se,
            method: 'GET',
            success: function (output, status, xhr) {
                const return_obj = JSON.parse(output);
                if (return_obj.status == 1) {
                    return_obj['data'].forEach(function (item, index, arr) {
                        studentCount++;
                        $("#listed_manual_list").append(
                            `<div class="col-sm-3">
                            <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">`+ item[1] + `</h5>
                                <input type="hidden" id="validH`+ studentCount + `" value="0" name="isValid">
                                <input type="checkbox" id="valid`+ studentCount + `"  value="1" name="isValid"> Validated
                                <select class="form-control" name="stat">
                                    <option `+ (item[2] == 0 ? "selected" : "") + ` value="0">Absent</option>
                                    <option `+ (item[2] == 1 ? "selected" : "") + ` value="1">Present</option>
                                    <option `+ (item[2] == 2 ? "selected" : "") + ` value="2">Late</option>
                                    <option `+ (item[2] == 3 ? "selected" : "") + ` value="3">Excused</option>
                                </select>
                                <input type="hidden" name="id" value="`+ item[0] + `">
                            </div>
                            </div> 
                        </div> `
                        ).show('slow');
                        if (item[3] == 1)
                            $("#valid" + studentCount).prop("checked", true);
                    });
                    // $('#edit-name').val(return_obj.data);
                    if (return_obj['data'].length === 0) {
                        $("#listed_manual_list").html("<p class='ml-4'>Nothing to show</p>");
                    }
                }
                else
                    fAlert(return_obj.message);
            }
        });
    }, 250);

});


function disableExcess() {
    for (let i = 1; i <= studentCount; i++) {
        if ($('#valid' + i).is(":checked")) {
            $('#validH' + i).prop("disabled", true);
        }
    }
}


