var se = window.localStorage.getItem("s");
function refreshtblData() {
    $.ajax({
        url: BASE_URL + 'crud/get_accounts_details?s=' + se,
        method: 'GET',
        success: function (output, status, xhr) {
            const return_obj = JSON.parse(output);
            if (return_obj.status == 1) {
                var t = $('#datatable-buttons').DataTable();
                t.clear();


                return_obj['data'].forEach(function (item, index, arr) {
                    if (item[2] === null)
                        item[2] = "None";
                    t.row.add([
                        `<a href="javascript:;" onclick="get_edit_account('` + item[0] + `')" data-target="#modalEdit" data-toggle="modal"  title="Edit" class="mr-3"><i class="fas fa-edit"></i></a>`,
                        item[1],
                        item[2],
                        item[3]
                    ]).draw();
                });
                // $('#edit-name').val(return_obj.data);
            }
            else
                fAlert(return_obj.message);
        }
    });

}

function refreshArchivetblData() {
    $.ajax({
        url: BASE_URL + 'crud/get_archived_accounts_details?s=' + se,
        method: 'GET',
        success: function (output, status, xhr) {
            const return_obj = JSON.parse(output);
            if (return_obj.status == 1) {
                var t = $('#archived-datatable-buttons').DataTable();
                t.clear();


                return_obj['data'].forEach(function (item, index, arr) {
                    if (item[2] === null)
                        item[2] = "None";
                    t.row.add([
                        `<a href="javascript:;" onclick="get_edit_account('` + item[0] + `')" data-target="#modalEdit" data-toggle="modal"  title="Edit" class="mr-3"><i class="fas fa-edit"></i></a>`,
                        item[1],
                        item[2],
                        item[3]
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
        refreshArchivetblData();
    }, 1000);
}
$(document).ready(function () {

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
    setTimeout(function () {
        PopulateSelect("roles", "crud/get_roles?s=" + se, "Select Role", null, true);
    }, 250);

    setTimeout(function () {
        PopulateSelect("deptA", "crud/get_departments?s=" + se, "Select Department", null, true);
    }, 500);


    $('#AddSave').click(function () {
        add_section(1);
    });

    $('#AddSaveNew').click(function () {
        add_section(2);
    });

    function add_section(type) {
        if (checkFormC("formAddNew"))
            $.ajax({
                url: BASE_URL + 'crud/add_account?s=' + se,
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
                url: BASE_URL + 'crud/edit_account?s=' + se,
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

function get_edit_account(section) {
    $.ajax({
        url: BASE_URL + 'crud/get_edit_account?s=' + se,
        method: 'POST',
        data: { 's': section },
        success: function (output, status, xhr) {
            const return_obj = JSON.parse(output);
            if (return_obj.status == 1) {
                $('#nameE').val(return_obj.data[0]);
                $('#emailE').val(return_obj.data[1]);
                PopulateSelect("rolesE", "crud/get_roles?s=" + se, "Select Role", return_obj.data[2], true);
                if (return_obj.data[3] === undefined || return_obj.data[3] === null || isNaN(return_obj.data[3])) {
                    $('#deptERow').html("");

                }
                else {
                    resetDept();
                    setTimeout(function () {
                        PopulateSelect("deptE", "crud/get_departments?s=" + se, "Select Department", return_obj.data[3], true);
                    }, 500);
                }
                $("#eIsActive").prop("checked", (return_obj.data[4] == "1" ? true : false));

            }
            else
                fAlert(return_obj.message);
        }
    });
};

function resetDept() {
    $('#deptERow').html(`<div class="col-md-4"> <h5 class="mb-0 text-center">Department</h5> </div> <div class="col-md-8"> <div id="deptE-spinner" class="spinner-border spinner-border-sm"> <span class="sr-only">Loading...</span> </div> <select name="deptE" style="width: 100%; display: none;" required></select> </div>`);
}


