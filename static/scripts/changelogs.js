var se = window.localStorage.getItem("s");



$(document).ready(function () {

    initDBTable();
    refreshtblData();

    function refreshtblData() {
        $.ajax({
            url: BASE_URL + 'crud/get_changelogs?s=' + se,
            method: 'GET',
            success: function (output, status, xhr) {
                const return_obj = JSON.parse(output);
                if (return_obj.status == 1) {
                    var t = $('#datatable-buttons').DataTable();
                    t.clear();
                    return_obj['data'].forEach(function (item, index, arr) {
                        t.row.add([
                            item[0],
                            item[1],
                            item[2]
                        ]).draw();
                    });
                    // $('#edit-name').val(return_obj.data);
                }
                else
                    fAlert(return_obj.message);
            }
        });
    }


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
    }






    // $('#AddSave').click(function(){
    //     add_section(1);
    // });

    // $('#AddSaveNew').click(function(){
    //     add_section(2);
    // });

    // function add_section(type){
    //     $.ajax({
    //         url:BASE_URL+'crud/add_section?s='+se,
    //         method: 'post',
    //         data: $("#formAddNew").serialize(),
    //         success: function(output, status, xhr){
    //             const return_obj = JSON.parse(output);
    //             if(return_obj.status == 1){
    //                 $('#modalAddNew').modal('hide');
    //                 refreshtblData();
    //                 if(type==2){
    //                     $("#formAddNew")[0].reset();
    //                     sAlert(return_obj.message, ''); 
    //                 }
    //                 else
    //                     sAlert(return_obj.message, ''); 
    //             }
    //             else
    //                 fAlert(return_obj.message);  
    //         }
    //     });
    // };

    // $('#EditSave').click(function(){
    //     $.ajax({
    //         url:BASE_URL+'crud/edit_section?s='+se,
    //         method: 'POST',
    //         data: $("#formEdit").serialize(),
    //         success: function(output, status, xhr){
    //             const return_obj = JSON.parse(output);
    //             if(return_obj.status == 1){
    //                 $('#modalEdit').modal('hide');
    //                 refreshtblData();
    //                 sAlert(return_obj.message, ''); 
    //             }
    //             else
    //                 fAlert(return_obj.message);  
    //         }
    //     });
    // });


});




