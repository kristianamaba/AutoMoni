var se = window.localStorage.getItem("s");
$(document).ready(function () {
    getData();

    $('#submit').click(function () {
        if (checkFormC("formAdvSet"))
            $.ajax({
                url: BASE_URL + 'crud/edit_adv_set?s=' + se,
                method: 'post',
                data: $("#formAdvSet").serialize(),
                success: function (output, status, xhr) {
                    const return_obj = JSON.parse(output);
                    if (return_obj.status == 1) {
                        sAlert(return_obj.message, '');
                        getData();
                    }
                    else
                        fAlert(return_obj.message);
                }
            });
    });

    function getData() {

        $.ajax({
            url: BASE_URL + 'crud/get_adv_set?s=' + se,
            method: 'GET',
            success: function (output, status, xhr) {
                const return_obj = JSON.parse(output);
                if (return_obj.status == 1) {
                    $('#absent_num').val(return_obj['data'][0][1]);
                    $('#late_num').val(return_obj['data'][1][1]);
                    setTimeout(function () {
                        PopulateSelect("ayear", "crud/get_years?s=" + se, "Select Year", return_obj['data'][2][1], true);
                    }, 500);
                }
                else
                    fAlert(return_obj.message);
            }
        });
    }




});
