var se = window.localStorage.getItem("s");
$(document).ready(function () {

    $('#RepeatPWSave').click(function () {
        $.ajax({
            url: BASE_URL + 'crud/change_pass?s=' + se,
            method: 'post',
            data: $("#formChangePW").serialize(),
            success: function (output, status, xhr) {
                const return_obj = JSON.parse(output);
                if (return_obj.status == 1)
                    sAlert(return_obj.message, '');
                else
                    fAlert(return_obj.message);
            }
        });
    });




});

// $(function () {
//     "use strict";

//     getLoginDetail();

//     let changeAcadInfo = false;
//     $("#AcademicInfoBtn").on('click', function () {
//         if (changeAcadInfo && confirm("Are you sure you want to update your academic information?")) {
//             changeAcadInfo = false;

//             $.ajax({
//                 url: BASE_URL + 'settings/updateAcadInfo',
//                 type: 'POST',
//                 data: {data: SerializeForm($("#formChangeAcad"))},
//                 success: function (resp) {
//                     let data = JSON.parse(resp);

//                     if (data.success) {
//                         showToast('Successfully Changed Academic Information.', 'success');
//                     } else {
//                         showToast(data.data, 'error');
//                     }

//                 }
//             });

//             $(this).html("Change");
//             $("#AcademicInfoCancelBtn").css("display", "none");
//             $("[name=degree]").prop("readonly", true);
//             $("[name=institution]").prop("readonly", true);
//         } else {
//             changeAcadInfo = true;
//             $(this).html("Save");
//             $("#AcademicInfoCancelBtn").css("display", "inline-block");
//             $("[name=degree]").prop("readonly", false);
//             $("[name=institution]").prop("readonly", false);
//         }
//     });

//     $("#AcademicInfoCancelBtn").on('click', function () {
//         changeAcadInfo = false;
//         $("#AcademicInfoCancelBtn").css("display", "none");
//         $("#AcademicInfoBtn").html("Change");
//         $("[name=degree]").prop("readonly", true);
//         $("[name=institution]").prop("readonly", true);
//     });

//     $("#formChangePW").on('submit', function () {
//         let restore = $("#RepeatPWSave");
//         $("#RepeatPWSave").html(processingSpinner).attr('disabled', true);

//         $.ajax({
//             url: BASE_URL + 'settings/changePW',
//             data: { data: SerializeForm($("#formChangePW")) },
//             type: 'POST',
//             success: function (resp) {
//                 let data = JSON.parse(resp);

//                 if (data.success) {
//                     $("#formChangePW").trigger('reset').trigger('change');
//                     $("#modalAddFunc").modal("hide");
//                     $('#tblDBTable').DataTable().ajax.reload();
//                     showToast('Successfully Changed Password.', 'success');
//                 } else {
//                     showToast(data.data, 'error');
//                 }

//                 $("#RepeatPWSave").html(restore).attr('disabled', false);
//             }
//         });

//         return false;
//     });

//     function getLoginDetail() {
//         $.ajax({
//             url: BASE_URL + 'settings/getLoginDetail',
//             type: 'POST',
//             success: function (resp) {
//                 let data = JSON.parse(resp);

//                 $("#logdetailTBL tbody").html();
//                 for (let i = 0; i < data.length; i++) {

//                     let detail = data[i].Description.split(",");

//                     $("#logdetailTBL tbody").append(
//                         `<tr>
//                             <td>`+ detail[0].replace("Date:", "") + `</td>
//                             <td>`+ detail[1].replace("IP:", "") + `</td>
//                             <td>`+ detail[2].replace("Platform:", "") + `</td>
//                             <td>`+ detail[3].replace("Version:", "") + `</td>
//                             <td>`+ detail[4].replace("Browser:", "") + `</td>
//                         </tr>`
//                     );
//                 }

//             }
//         });

//         $.ajax({
//             url: BASE_URL + 'settings/getUserInfo',
//             type: 'POST',
//             success: function (resp) {
//                 let data = JSON.parse(resp)[0];
//                 $("[name=degree]").val(data.Degree);
//                 $("[name=institution]").val(data.Institution);

//             }
//         });

//     }

// });