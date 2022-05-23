var se = window.localStorage.getItem("s");
function refreshtblData() {
    $.ajax({
        url: BASE_URL + 'crud/get_subjects_details?s=' + se,
        method: 'GET',
        success: function (output, status, xhr) {

            const return_obj = JSON.parse(output);
            if (return_obj.status == 1) {
                var t = $('#datatable-buttons').DataTable();
                t.clear();
                return_obj['data'].forEach(function (item, index, arr) {
                    // subject_name, b.sect_name, acad_year
                    t.row.add([
                        `<a href="javascript:;" onclick="get_edit_subject('` + item[0] + `')" data-target="#modalEdit" data-toggle="modal"  title="Edit" class="mr-3"><i class="fas fa-edit"></i></a>
                        `,
                        // <a href="#" onclick="goto('`+item[0]+`',0)" title="View Attendance" class="mr-3"><i class="fas fa-book"></i></a>
                        item[1],
                        item[2],
                        item[3],
                        item[4],
                        item[5]
                    ]).draw();
                });
                // $('#edit-name').val(return_obj.data);
            }
            else
                fAlert(return_obj.message);
        }

    });
}

function refreshArchivedtblData() {
    $.ajax({
        url: BASE_URL + 'crud/get_archived_subjects_details?s=' + se,
        method: 'GET',
        success: function (output, status, xhr) {

            const return_obj = JSON.parse(output);
            if (return_obj.status == 1) {
                var t = $('#archived-datatable-buttons').DataTable();
                t.clear();
                return_obj['data'].forEach(function (item, index, arr) {
                    // subject_name, b.sect_name, acad_year
                    t.row.add([
                        `<a href="javascript:;" onclick="get_edit_subject('` + item[0] + `')" data-target="#modalEdit" data-toggle="modal"  title="Edit" class="mr-3"><i class="fas fa-edit"></i></a>
                        `,
                        // <a href="#" onclick="goto('`+item[0]+`',0)" title="View Attendance" class="mr-3"><i class="fas fa-book"></i></a>
                        item[1],
                        item[2],
                        item[3],
                        item[4],
                        item[5]
                    ]).draw();
                });
                // $('#edit-name').val(return_obj.data);
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

    PopulateSelect("sectionA", "crud/get_section?s=" + se, "Select Section", null, true);


    setTimeout(function () {
        PopulateSelect("teacherA", "crud/get_teachers?s=" + se, "Select Teacher", null, true);
    }, 250);

    setTimeout(function () {
        PopulateSelect("deptA", "crud/get_departments?s=" + se, "Select Department", null, true);
    }, 500);

    setTimeout(function () {
        PopulateSelect("aayear", "crud/get_years?s=" + se, "Select Year", null, true);
    }, 750);

    initDBTable();
    refresh();
    function initDBTable() {
        $('#datatable').DataTable({
            "order": []
        });

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
        add_class(1);
    });

    $('#AddSaveNew').click(function () {
        add_class(2);
    });

    function add_class(type) {
        if (checkFormC("formAddNew"))
            $.ajax({
                url: BASE_URL + 'crud/add_subject?s=' + se,
                method: 'post',
                data: $("#formAddNew").serialize(),
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

    $('#EditSave').click(function () {
        if (checkFormC("formEdit"))
            $.ajax({
                url: BASE_URL + 'crud/edit_subject?s=' + se,
                method: 'POST',
                data: $("#formEdit").serialize(),
                success: function (output, status, xhr) {
                    const return_obj = JSON.parse(output);
                    if (return_obj.status == 1) {
                        $('#modalEdit').modal('hide');
                        refresh();
                        sAlert(return_obj.message, '');
                    }
                    else
                        fAlert(return_obj.message);
                }
            });
    });


});

function goto(s, type) {
    var arr = [["set_attendance", "attendance"], ["set_management", "students"]]
    $.ajax({
        url: BASE_URL + 'crud/' + arr[type][0] + '?s=' + se,
        method: 'POST',
        data: { 's': s },
        success: function (output, status, xhr) {
            const return_obj = JSON.parse(output);
            if (return_obj.status == 1) {
                window.location.href = "./" + arr[type][1];
            }
            else
                fAlert(return_obj.message);
        }
    });
};

function get_edit_subject(s) {
    $.ajax({
        url: BASE_URL + 'crud/get_edit_subject?s=' + se,
        method: 'POST',
        data: { 's': s },
        success: function (output, status, xhr) {
            const return_obj = JSON.parse(output);
            if (return_obj.status == 1) {
                $('#edit-name').val(return_obj.data[1]);
                // PopulateSelect("sectionE", "crud/get_section?s="+se, "Select Section", null, true);
                PopulateSelect("sectionE", "crud/get_section?s=" + se, "Select Section", return_obj.data[2], true);
                // $('#edit-ayear').val(return_obj.data[3]);
                setTimeout(function () {
                    PopulateSelect("teacherE", "crud/get_teachers?s=" + se, "Select Teacher", return_obj.data[4], true);
                }, 250);
                setTimeout(function () {
                    PopulateSelect("deptE", "crud/get_departments?s=" + se, "Select Department", return_obj.data[5], true);
                }, 500);
                setTimeout(function () {
                    PopulateSelect("ayear", "crud/get_years?s=" + se, "Select Year", return_obj.data[3], true);
                }, 750);
                $("#eIsActive").prop("checked", (return_obj.data[6] == "1" ? true : false));
            }
            else
                fAlert(return_obj.message);
        }
    });
};




