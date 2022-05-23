var se = window.localStorage.getItem("s");
var stud_photos = 0;
function refreshtblData() {
    $.ajax({
        url: BASE_URL + 'crud/get_all_management_det?s=' + se,
        method: 'GET',
        success: function (output, status, xhr) {
            const return_obj = JSON.parse(output);
            if (return_obj.status == 1) {
                var t = $('#datatable-buttons').DataTable();
                t.clear();
                return_obj['data'].forEach(function (item, index, arr) {
                    t.row.add([
                        `<a href="javascript:;" onclick="get_edit_student('` + item[0] + `')" data-target="#modalEdit" data-toggle="modal"  title="Edit" class="mr-3"><i class="fas fa-edit"></i></a>`,
                        item[4],
                        item[1],
                        item[2],
                        item[3]
                    ]).draw();
                });
                // $('#section_t').html(return_obj.section);
                // $('#section_st').html(return_obj.section + " Master File");
            }
            else
                fAlert(return_obj.message);
        }
    });
}

function refreshArchivedtblData() {
    $.ajax({
        url: BASE_URL + 'crud/get_archived_all_management_det?s=' + se,
        method: 'GET',
        success: function (output, status, xhr) {
            const return_obj = JSON.parse(output);
            if (return_obj.status == 1) {
                var t = $('#archived-datatable-buttons').DataTable();
                t.clear();
                return_obj['data'].forEach(function (item, index, arr) {
                    t.row.add([
                        `<a href="javascript:;" onclick="get_edit_student('` + item[0] + `')" data-target="#modalEdit" data-toggle="modal"  title="Edit" class="mr-3"><i class="fas fa-edit"></i></a>`,
                        item[4],
                        item[1],
                        item[2],
                        item[3]
                    ]).draw();
                });
                // $('#section_t').html(return_obj.section);
                // $('#section_st').html(return_obj.section + " Master File");
            }
            else
                fAlert(return_obj.message);
        }
    });
}

function refresh() {
    refreshtblData();
    setTimeout(function () {
        refreshArchivedtblData();
    }, 1000);
}
$(document).ready(function () {

    initDBTable();
    refresh();
    PopulateSelectMultiple("eSubjectList", "crud/get_subject_management?s=" + se, 'Select Subjects', true, 300);
    PopulateSelectMultiple("aSubjectList", "crud/get_subject_management?s=" + se, 'Select Subjects', true, 600);

    function initDBTable() {
        $('#datatable').DataTable({
            "order": []
        });

        //Buttons examples
        var table = $('#datatable-buttons').DataTable({
            lengthChange: false,
            buttons: [{ name: 'copy', extend: 'copy', exportOptions: { columns: ':gt(0)', orthogonal: 'export' } },
            { name: 'excel', extend: 'excel', exportOptions: { columns: ':gt(0)', orthogonal: 'export' } },
            { name: 'pdf', extend: 'pdf', exportOptions: { columns: ':gt(0)', orthogonal: 'export' } }, 'colvis',
            ]

        });

        table.buttons().container()
            .appendTo('#datatable-buttons_wrapper .col-md-6:eq(0)');

        var table2 = $('#archived-datatable-buttons').DataTable({
            lengthChange: false,
            buttons: [{ name: 'copy', extend: 'copy', exportOptions: { columns: ':gt(0)', orthogonal: 'export' } },
            { name: 'excel', extend: 'excel', exportOptions: { columns: ':gt(0)', orthogonal: 'export' } },
            { name: 'pdf', extend: 'pdf', exportOptions: { columns: ':gt(0)', orthogonal: 'export' } }, 'colvis',
            ]

        });

        table2.buttons().container()
            .appendTo('#archived-datatable-buttons_wrapper .col-md-6:eq(0)');

    }




    $('#AddSave').click(function () {
        add_student(1);
    });

    $('#AddSaveNew').click(function () {
        add_student(2);
    });

    function add_student(type) {
        if (checkFormC("formAddNew"))
            $.ajax({
                url: BASE_URL + 'crud/add_student_management?s=' + se,
                method: 'post',
                data: {
                    'studId': $('#add-studId').val(),
                    'name': $('#add-name').val(),
                    'email': $('#add-email').val(),
                    'subjects': JSON.stringify($('#aSubjectList').val())
                },
                success: function (output, status, xhr) {
                    const return_obj = JSON.parse(output);
                    if (return_obj.status == 1) {
                        $('#modalAddNew').modal('hide');
                        refresh();
                        if (type == 2) {
                            $("#formAddNew")[0].reset();
                            sAlert(return_obj.message, '');
                        }
                        else
                            sAlert(return_obj.message, '');
                    }
                    else
                        fAlert(return_obj.message);
                }
            });
    };



    let video = document.querySelector("#videoElement");
    let canvas = document.querySelector("#canvasElement");
    let ctx = canvas.getContext('2d');
    let photo_names = [];

    $('#DeleteSnap').click(function () {
        $.ajax({
            url: BASE_URL + 'crud/delete_student_photos?s=' + se,
            method: 'post',
            success: function (output, status, xhr) {
                sAlert("Sucessfully Deleted Photos", "");
                photo_names = [];
                stud_photos = 0;
            }
        });
    });

    $('#EditSnap').click(function () {
        if (stud_photos < 3) {
            canvas.height = video.videoHeight;
            canvas.width = video.videoWidth;
            ctx.drawImage(video, 0, 0);
            let dataURL = canvas.toDataURL('image/jpeg');
            // var img = new Image();
            $.ajax({
                type: "POST",
                url: BASE_URL + "crud/insert_image?s=" + se,
                data: { 'imgBase64': dataURL },
                success: function (output, status, xhr) {
                    const return_obj = JSON.parse(output);
                    if (return_obj.status == 1) {
                        sAlert(return_obj.message, '');
                        photo_names.push(return_obj.data[0]);
                        stud_photos++;
                    }
                    else
                        fAlert(return_obj.message);
                }
            });
        }
        else {
            fAlert("Error: Delete Photos First (Max: 3 per student)");
        }

    });


    var constraints = {
        video: {
            width: { min: video.videoWidth },
            height: { min: video.videoHeight }
        }
    };

    navigator.mediaDevices.getUserMedia(constraints).then(function (stream) {
        video.srcObject = stream;

        // setInterval(function () {
        //   sendSnapshot();
        // }, 1000);
    }).catch(function (error) {
        console.log(error);
    });



    $('#EditSave').click(function () {
        if (checkFormC("formEdit"))
            $.ajax({
                url: BASE_URL + 'crud/edit_student_management?s=' + se,
                method: 'POST',
                data: {
                    'name': $('#edit-name').val(),
                    'email': $('#edit-email').val(),
                    'photo_names': JSON.stringify(photo_names),
                    'subjects': JSON.stringify($('#eSubjectList').val()),
                    'isValid': ($('#eIsActive').is(':checked') ? 1 : 0)
                },
                success: function (output, status, xhr) {
                    const return_obj = JSON.parse(output);
                    refresh();
                    if (return_obj.status == 1) {
                        $('#modalEdit').modal('hide');
                        sAlert(return_obj.message, '');
                    }
                    else
                        fAlert(return_obj.message);
                }
            });
    });

});

function get_edit_student(student) {
    $.ajax({
        url: BASE_URL + 'crud/get_edit_student_rev?s=' + se,
        method: 'POST',
        data: { 's': student },
        success: function (output, status, xhr) {
            const return_obj = JSON.parse(output);
            if (return_obj.status == 1) {
                $('#edit-name').val(return_obj.data[0]);
                stud_photos = Number(return_obj.data[1]);
                $('#edit-email').val(return_obj.data[2]);
                if (return_obj.data[3] !== null) {
                    const subjectList = return_obj.data[3].split(",");
                    AddSelectMultiple("eSubjectList", subjectList);
                }
                $("#eIsActive").prop("checked", (return_obj.data[4] == "1" ? true : false));
            }
            else
                fAlert(return_obj.message);
        }
    });
};