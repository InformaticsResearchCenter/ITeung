html_presensi = '''
<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <meta name="google-signin-client_id" content="403092275269-8ubnhiaih6ngk6t3vf3bidlak6f92ten.apps.googleusercontent.com">
    <script src="https://apis.google.com/js/client:platform.js?onload=renderButton" async defer></script>
    <script src="https://rawgit.com/schmich/instascan-builds/master/instascan.min.js"></script>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"></script>
    <title>Absensi with ITeung</title>
  </head>
  <body>
    <center>
      <div id="gSignIn"></div>
      <div class="userContent" style="display: none;"></div>
      <video id="preview" style="display: none;"></video>
      <embed src="beep.wav" autostart="false" width="0" height="0" id="sound" enablejavascript="true">
      <div id='groupname' style="display: none;">#GROUP#</div>
      <div class="btn-group btn-group-toggle mb-5" data-toggle="buttons">
          <label class="btn btn-primary active">
            <input type="radio" name="options" value="1" autocomplete="off" checked> Front Camera
          </label>
          <label class="btn btn-secondary">
            <input type="radio" name="options" value="2" autocomplete="off"> Back Camera
          </label>
        </div>
    </center>
    <script>
      function renderButton() {
          gapi.signin2.render('gSignIn', {
              'scope': 'profile email',
              'width': 240,
              'height': 50,
              'longtitle': true,
              'theme': 'dark',
              'onsuccess': onSuccess
          });
      }

      function send_data(data) {
        var jsondata = {
            phonenumber: data,
            groupname: document.getElementById('groupname').value
        };
        fetch(`${window.origin}/data/proses/phonenumber/to/database`, {
            method: "POST",
            credentials: "include",
            body: JSON.stringify(jsondata),
            cache: "no-cache",
            headers: new Headers({
                "content-type": "application/json"
            })
        })
      }

      function scannerQR() {
        let scanner = new Instascan.Scanner(
          {
            video: document.getElementById('preview')
          });
        scanner.addListener('scan', function(content){
          console.log(content);
<!--          PlaySound();-->
          send_data(content);
        });
        Instascan.Camera.getCameras().then(function(cameras){
          if (cameras.length > 0) {
            scanner.start(cameras[0])
            $('[name="options"]').on('change',function(){
                if($(this).val()==1){
                    if(cameras[0]!=""){
                        scanner.start(cameras[0]);
                    }else{
                        alert('No Front camera found!');
                    }
                }else if($(this).val()==2){
                    if(cameras[1]!=""){
                        scanner.start(cameras[1]);
                    }else{
                        alert('No Back camera found!');
                    }
                }
            });
          } else {
            console.log('No camera Found!');
          }
        }).catch(function(e){
          console.error(e);
        });
      }

      function onSuccess(googleUser) {
          gapi.client.load('oauth2', 'v2', function () {
              var request = gapi.client.oauth2.userinfo.get({
                  'userId': 'me'
              });
              request.execute(function (resp) {
                  var profileHTML = '<h3>Welcome '+resp.given_name+'! <a href="javascript:void(0);" onclick="signOut();">Sign out</a></h3>';
                  profileHTML += '<img src="'+resp.picture+'"/><p><b>Google ID: </b>'+resp.id+'</p><p><b>Name: </b>'+resp.name+'</p><p><b>Email: </b>'+resp.email+'</p><p><b>Gender: </b>'+resp.gender+'</p><p><b>Locale: </b>'+resp.locale+'</p><p><b>Google Profile:</b> <a target="_blank" href="'+resp.link+'">click to view profile</a></p>';
                  document.getElementsByClassName("userContent")[0].innerHTML = profileHTML;
                  document.getElementById("gSignIn").style.display = "none";
                  document.getElementsByClassName("userContent")[0].style.display = "block";
                  document.getElementById("preview").style.display = "block";
                  scannerQR();
              });
          });
      }

      function signOut() {
        var auth2 = gapi.auth2.getAuthInstance();
        auth2.signOut().then(function () {
            document.getElementsByClassName("userContent")[0].innerHTML = '';
            document.getElementsByClassName("userContent")[0].style.display = "none";
            document.getElementById("gSignIn").style.display = "block";
        });

        auth2.disconnect();
      }

<!--      function PlaySound() {-->
<!--        var sound = new Audio('beep.wav');-->
<!--        sound.play()-->
<!--      }-->
    </script>
  </body>
</html>

'''