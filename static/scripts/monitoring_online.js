var se = window.localStorage.getItem("s");
$(document).ready(function () {
  let namespace = "live";
  // let video = document.querySelector("#videoElement");
  // let canvas = document.querySelector("#canvasElement");
  // let ctx = canvas.getContext('2d');
  let names = [];
  // photo = document.getElementById('photo');
  var last = 0;
  // let enable = "1";
  // var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
  var socket = io.connect(BASE_URL + namespace, { query: "s=" + se });
  var att_stat = ['Absent', 'Present', 'Late', 'Excused'];
  function sendSnapshot(udata) {

    // canvas.height = video.videoHeight;
    // canvas.width = video.videoWidth;
    // ctx.drawImage(video, 0, 0);
    // let dataURL = canvas.toDataURL('image/jpeg');



    // socket.emit('input image', dataURL);

    socket.emit('live-list-check', [udata[2], udata[3], last], 1, udata[5])
    socket.on('live-list-out', function (data) {
      $.each(data, function (key, value) {
        if (names.indexOf(value[1]) == -1) {
          if (udata[5] == 1)
            $("#live_list").prepend('<div class="alert alert-success" role="alert"> <h4 class="alert-heading">' + value[1] + '</h4> <p>Marked as ' + att_stat[Number(value[3])] + ' on ' + value[2] + '</p></div>');
          else if (udata[5] == 2)
            $("#live_list").prepend('<div class="alert alert-success" role="alert"> <h4 class="alert-heading">' + value[1] + '</h4> <p>Attendance Validated on ' + value[2] + '</p></div>');
          names.push(value[1]);
          last = value[0];
          // console.log(last);
        }

      });
    });

    // if(enable == "1"){
    //   var img = new Image();
    //   socket.on('out-image-event',function(data){
    //   if(data.enable == "1"){
    //     img.src = dataURL//data.image_data
    //     photo.setAttribute('src', data.image_data);
    //   }
    //   else
    //     $( "#title_live_feed" ).html("<span class='rqd'>Live Feed Disabled</span> ");

    //   enable = data.enable;

    //   });
    // }




  }

  socket.on('connect', function () {
    console.log('Connected!');
  });

  // var constraints = {
  //   video: {
  //     width: { min: video.videoWidth },
  //     height: { min: video.videoHeight }
  //     // ,
  //     // facingMode: {
  //     //   exact: 'environment'
  //     // }
  //   }
  // };

  // navigator.clipboard.writeText(copyText.value);
  $('#copy_link').click(function () {
    navigator.clipboard.writeText($("#link").html());
    showToast("Copied to Clipboard", "success");
  });

  $.ajax({
    url: BASE_URL + 'crud/getUserData?s=' + se,
    method: 'get',
    success: function (output, status, xhr) {
      const return_obj = JSON.parse(output);
      if (return_obj.status == 1) {
        $("#link").html(return_obj.enc);
        setInterval(function () {
          sendSnapshot(return_obj.data);
        }, 1000);
      }
      else
        fAlert(return_obj.message);
    }
  });

  // setInterval(function () {
  //   sendSnapshot();
  // }, 600);

  // navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
  //   video.srcObject = stream;
  //   localMediaStream = stream;

  //   setInterval(function () {
  //     sendSnapshot();
  //   }, 600);
  // }).catch(function(error) {
  //   console.log(error);
  // });

  $('#stop_monitoring').click(function () {
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
  });


});

