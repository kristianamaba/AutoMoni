var se = window.localStorage.getItem("s");
let sect_name = "";
$(document).ready(function () {

    // const columnNames = [{"title": 'Action'},{"title": 'Name'}];
    // columnNames.push({"title": obj[0][x-1]['c2']});
    const att_stat = ['A', 'P', 'L', 'E'];
    var max_absent = 0;
    getData();

    setTimeout(function () {
        initDBTable();
    }, 250);


    function getData() {
        $.ajax({
            url: BASE_URL + 'crud/get_adv_set?s=' + se,
            method: 'GET',
            success: function (output, status, xhr) {
                const return_obj = JSON.parse(output);
                if (return_obj.status == 1) {
                    max_absent = Number(return_obj['data'][0][1]);
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
        $.ajax({
            url: BASE_URL + 'crud/get_attendance_sum?s=' + se,
            method: 'GET',
            success: function (output, status, xhr) {
                const return_obj = JSON.parse(output);
                sect_name = return_obj['section'];
                if (return_obj.status == 1) {
                    // $('#edit-name').val(return_obj.data);
                    const columnNames = [{ "title": 'Action' }, { "title": 'Status' }, { "title": 'Name' }];
                    for (let i = 0; i < return_obj['header'].length; i++) {
                        columnNames.push({ "title": return_obj['header'][i][1] });
                    }
                    var table = $('#datatable-buttons').DataTable({
                        lengthChange: false,
                        buttons: [{ name: 'copy', extend: 'copy', exportOptions: { columns: ':gt(0)', orthogonal: 'export' } },
                        { name: 'excel', extend: 'excel', exportOptions: { columns: ':gt(0)', orthogonal: 'export' } },
                        { name: 'pdf', extend: 'pdf', exportOptions: { columns: ':gt(0)', orthogonal: 'export' } }, 'colvis'
                        ]
                        , columns: columnNames
                    });

                    table.buttons().container().appendTo('#datatable-buttons_wrapper .col-md-6:eq(0)');

                    for (let i = 0; i < return_obj['data'].length; i++) {
                        var rowData = []
                        rowData.push(`<a href="javascript:;" onclick="getSummary('` + return_obj['data'][i][0] + `')" data-target="#modalSum"  data-toggle="modal"  title="View Summary" class="mr-2 ml-3"><i class="fas fa-book"></i></a>`);
                        for (let i2 = 1; i2 < return_obj['data'][i].length; i2++) {



                            if (i2 == 1) {
                                var counts = [];
                                for (const num of return_obj['data'][i].slice(2)) {
                                    counts[num] = counts[num] ? counts[num] + 1 : 1;
                                }
                                var percent = counts[0] / max_absent;
                                percent = (percent > 1 ? 100 : Math.round(percent * 100));
                                var prog_stat = (percent == 100 ? "danger" : (percent >= 50 ? "warning" : "success"))

                                rowData.push(`<div class="progress"><div class="progress-bar bg-` + prog_stat + `" role="progressbar" style="width: ` + percent + `%" aria-valuenow="` + percent + `" aria-valuemin="0" aria-valuemax="100"></div></div>`);
                                // rowData.push(counts[0]);
                                rowData.push(return_obj['data'][i][i2]);
                            }
                            else {
                                // if (sect_name === "Elective 2" && Number(att_stat[return_obj['data'][i][i2]]) !== 0)
                                //     rowData.push(att_stat[Number(return_obj['data'][i][i2]) / 2]);
                                // else
                                rowData.push(att_stat[return_obj['data'][i][i2]]);
                            }


                        }
                        table.row.add(rowData).draw();
                    }
                    $('#section_t').html(return_obj['section']);
                    $('#section_st').html(return_obj['section'] + " Attendance Monitoring");
                }
                else
                    fAlert(return_obj.message);
            }
        });




    }
});

function getSummary(s) {
    $.ajax({
        url: BASE_URL + 'crud/get_stud_att_sum?s=' + se,
        method: 'POST',
        data: { 's': s },
        success: function (output, status, xhr) {
            const return_obj = JSON.parse(output);


            $("#stud_name").html(return_obj[0][0][0]);

            const counts = {};

            for (const num of return_obj[0][0]) {
                counts[num] = counts[num] ? counts[num] + 1 : 1;
            }

            $("#sum_a").html((counts[0] != null ? counts[0] : 0) + " : " + Math.round(((counts[0] != null ? counts[0] : 0) / (return_obj[0][0].length - 1)) * 100) + "% ");
            $("#sum_p").html((counts[1] != null ? counts[1] : 0) + " : " + Math.round(((counts[1] != null ? counts[1] : 0) / (return_obj[0][0].length - 1)) * 100) + "% ");
            $("#sum_l").html((counts[2] != null ? counts[2] : 0) + " : " + Math.round(((counts[2] != null ? counts[2] : 0) / (return_obj[0][0].length - 1)) * 100) + "% ");
            $("#sum_e").html((counts[3] != null ? counts[3] : 0) + " : " + Math.round(((counts[3] != null ? counts[3] : 0) / (return_obj[0][0].length - 1)) * 100) + "% ");
            // sum_a

            // console.log(counts[5], counts[2], counts[9], counts[4]);
            // if(return_obj.status == 1){
            //     $('#edit-name').val(return_obj.data);
            // }
            // else
            //     fAlert(return_obj.message);  
        }
    });
};

