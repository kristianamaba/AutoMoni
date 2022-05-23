var return_obj;
const att_stat = ['Absent', 'Present', 'Late', 'Excused'];
let studID = "";
function mailIndex(index) {

  let email = return_obj.data[index].data[4];
  let subject = "Attendance Appeal - " + return_obj.data[index].data[1];
  let body = "Good day, Mr./Mrs. " + return_obj.data[index].data[3] + ",%0D%0A %0D%0AStudent Name:" + return_obj.data[index].data[6] + "%0D%0AStudent ID:" + studID + "%0D%0A %0D%0AConcern:";
  window.open("mailto:" + email + "?subject=" + subject + "&body=" + body, "_blank")
}

function exportExcel(name, index) {
  filename = name + '.xlsx';
  data = []
  tempData = {}
  return_obj.data[index].header.forEach(function (item, index2) {
    tempData[item[1] + " (" + (index2 + 1) + ")"] = att_stat[return_obj.data[index].attendance[0][Number(index2) + 1]];
  });
  data.push(tempData);
  var ws = XLSX.utils.json_to_sheet(data, { skipHeader: true });
  var ws = XLSX.utils.json_to_sheet(data);
  var wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, "Day per Day Attendance");
  XLSX.writeFile(wb, filename);
}

$('#searchStudent').click(function () {
  studID = $("#studId").val();
  if (checkFormC("searchStudentfrm")) {
    $.ajax({
      url: BASE_URL + 'crud/get_stud_att_details',
      method: 'post',
      data: $("#searchStudentfrm").serialize(),
      success: function (output, status, xhr) {
        return_obj = JSON.parse(output);
        $("#studSubDetails").html("");
        if (return_obj.status == 1) {
          sAlert(return_obj.message, '');
          return_obj.data.forEach(function (item, index) {
            let counts = {};
            // console.log(item);
            for (let num of item.attendance[0]) {
              counts[num] = Number(counts[num]) ? Number(counts[num]) + 1 : 1;
            }
            let sum_a = (counts[0] != null ? counts[0] : 0) + " : " + Math.round(((counts[0] != null ? counts[0] : 0) / (item.attendance[0].length - 1)) * 100) + "% ";
            let sum_p = (counts[1] != null ? counts[1] : 0) + " : " + Math.round(((counts[1] != null ? counts[1] : 0) / (item.attendance[0].length - 1)) * 100) + "% ";
            let sum_l = (counts[2] != null ? counts[2] : 0) + " : " + Math.round(((counts[2] != null ? counts[2] : 0) / (item.attendance[0].length - 1)) * 100) + "% ";
            let sum_e = (counts[3] != null ? counts[3] : 0) + " : " + Math.round(((counts[3] != null ? counts[3] : 0) / (item.attendance[0].length - 1)) * 100) + "% ";
            $("#studSubDetails").append(`
        <div class="col-sm-12 mt-2">
                            <div class="card">
                                <div class="card-body mb-3">
                                    <h3 class="page-title text-truncate text-dark font-weight-medium m-4">`+ item.data[1] + `
                                        <button type="button" onclick="mailIndex('` + index + `')" class="float-right btn btn-primary rounded-0">Submit
                                            an Appeal</button>
                                        <button type="button" class="float-right btn btn-primary mr-4 rounded-0" onclick="exportExcel('`+ (item.data[1] + item.data[3]).replace(/[\W_]+/g, "") + `', '` + index + `')">Detailed
                                            Attendance</button>

                                    </h3>
                                    <h4>Attendance Summary</h4>
                                    <div class="row align-items-center mt-2">
                                        <div class="col">
                                            <b>Absent:</b>
                                            `+ sum_a.replace('NaN%', 'N/A') + `
                                        </div>

                                        <div class="col">
                                            <b>Present:</b>
                                            `+ sum_p.replace('NaN%', 'N/A') + `
                                        </div>

                                        <div class="col">
                                            <b>Late:</b>
                                            `+ sum_l.replace('NaN%', 'N/A') + `
                                        </div>

                                        <div class="col">
                                            <b>Excused:</b>
                                            `+ sum_e.replace('NaN%', 'N/A') + `
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>`);
          });

        }
        else
          fAlert(return_obj.message);
      }
    });
  }
});


$(document).ready(function () {

});

