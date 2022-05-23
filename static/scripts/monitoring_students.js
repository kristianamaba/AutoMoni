// var se = window.localStorage.getItem("s");
$(document).ready(function () {
  let namespace = "live";
  let video = document.querySelector("#videoElement");
  let canvas = document.querySelector("#canvasElement");
  let ctx = canvas.getContext('2d');
  let names = [];
  photo = document.getElementById('photo');
  var localMediaStream = null;
  let enable = "1";
  // var last = 0;
  // var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
  var socket = io.connect(BASE_URL + namespace, { query: "s=" + tse });
  var att_stat = ['Absent', 'Present', 'Late', 'Excused'];
  function sendSnapshot(udata) {
    if (!localMediaStream) {
      return;
    }
    // ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight, 0, 0, 300, 150);
    // let dataURL = canvas.toDataURL('image/jpeg');

    canvas.height = video.videoHeight;
    canvas.width = video.videoWidth;
    ctx.drawImage(video, 0, 0);
    let dataURL = canvas.toDataURL('image/jpeg');



    socket.emit('input image', dataURL, udata, 2, udata[5]);

    // socket.emit('output image')
    // live-list-check live-list-out

    socket.emit('live-list-check', [], 2, udata[5])
    socket.on('live-list-out', function (data) {
      $.each(data, function (key, value) {
        if (names.indexOf(value[0]) == -1) {
          if (udata[5] == 1)
            $("#live_list").prepend('<div class="alert alert-success" role="alert"> <h4 class="alert-heading">' + value[0] + '</h4> <p>Marked as ' + att_stat[Number(value[2])] + ' on ' + value[1] + '</p></div>');
          else if (udata[5] == 2)
            $("#live_list").prepend('<div class="alert alert-success" role="alert"> <h4 class="alert-heading">' + value[0] + '</h4> <p>Attendance Validated on ' + value[1] + '</p></div>');

          names.push(value[0]);
          // last = value[0];
          // console.log(last);
        }

      });
    });

    if (enable == "1") {
      var img = new Image();
      socket.on('out-image-event', function (data) {
        if (data.enable == "1") {
          img.src = dataURL//data.image_data
          photo.setAttribute('src', data.image_data);
        }
        else
          $("#title_live_feed").html("<span class='rqd'>Live Feed Disabled</span> ");

        enable = data.enable;

      });
    }




  }

  socket.on('connect', function () {
    console.log('Connected!');
  });

  var constraints = {
    video: {
      width: { min: video.videoWidth },
      height: { min: video.videoHeight }
      // ,
      // facingMode: {
      //   exact: 'environment'
      // }
    }
  };

  navigator.mediaDevices.getUserMedia(constraints).then(function (stream) {
    video.srcObject = stream;
    localMediaStream = stream;
    $.ajax({
      url: BASE_URL + 'crud/getUserData?s=' + tse,
      method: 'get',
      success: function (output, status, xhr) {
        const return_obj = JSON.parse(output);
        if (return_obj.status == 1) {
          setInterval(function () {
            sendSnapshot(return_obj.data);
          }, 1000);
        }
        else
          window.location.href = "/login";
      },
      error: function (output) {
        window.location.href = "/login";
      }
    });


  }).catch(function (error) {
    console.log(error);
  });


});

