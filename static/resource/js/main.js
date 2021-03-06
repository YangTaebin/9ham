function resi() {
  var limit = 990;
  console.log(window.innerWidth);
  if (window.innerWidth < limit) {
    document.getElementById("main_top").setAttribute("style", "display: block;");
    document.getElementById("main_3").setAttribute("style", "margin-top: 0px;");
  } else {
    document.getElementById("main_top").setAttribute("style", "display: flex;");
    document.getElementById("main_3").setAttribute("style", "margin-top: -260px;");
  }
}

function setCookie(name, value, exp) {
  var date = new Date();
  date.setTime(date.getTime() + exp*60*60*1000);
  document.cookie = name + '=' + value + ';expires=' + date.toUTCString() + ';path=/';
}
function getCookie(name) {
  var value = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
  return value? value[2] : null;
}

const delCookie = function delCookie_by_name(name){
    let date = new Date();
    date.setDate(date.getDate() - 100);
    let Cookie = `${name}=;Expires=${date.toUTCString()}`
    document.cookie = Cookie;
}

function Redirect_login(cookie, username) {
  var base = username
  setCookie("username", base, 2);
  setCookie("auth", cookie, 2);
  document.location.href="/";
}

function logout() {
  delCookie("auth");
  delCookie("username");
  document.location.href="/";
}

function move_to_regist() {
  document.location.href="/registration";
}

function test_submit() {
  if (already_username != true) {
    submit_button = document.getElementById("regist_button");
    submit_button.setAttribute("type", "button");
    submit_button.setAttribute("onclick", "already_error();");
  }
  else if (match_password != true) {
    submit_button = document.getElementById("regist_button");
    submit_button.setAttribute("type", "button");
    submit_button.setAttribute("onclick", "miss_match_password();");
  }
  else if (email_check_finished != true) {
    submit_button = document.getElementById("regist_button");
    submit_button.setAttribute("type", "button");
    submit_button.setAttribute("onclick", "email_miss_checked();");
  }
  else {
    submit_button = document.getElementById("regist_button");
    submit_button.setAttribute("type", "button");
    submit_button.setAttribute("onclick", "regist_error();");
  }
  if (exist_username && exist_password && match_password && exist_profile_picture && email_check_finished && already_username) {
    submit_button = document.getElementById("regist_button");
    submit_button.setAttribute("type", "submit");
    submit_button.setAttribute("onclick", "");
  }
}

function readFile() {
  if (this.files && this.files[0]) {
    var FR= new FileReader();
    FR.addEventListener("load", function(e) {
      document.getElementById("login_container").setAttribute("style", "height: 1070px;")
      document.getElementById("regist_profile_img").src = e.target.result;
      document.getElementById("regist_profile_img").height = "100";
      var filename = document.getElementById("inp").files[0].name;
      var bas = (e.target.result).toString();
      if (filename.split(".")[1] == "jpg"){
        var only_bas = bas.split('data:image/jpeg;base64,')[1];
      } else if (filename.split(".")[1] == "png"){
        var only_bas = bas.split('data:image/png;base64,')[1];
      } else {
        alert("????????? jpg, png ??? ??????????????????.");
        return
      }
      var input_base64 = document.createElement('input');
      input_base64.setAttribute("name", "profile_img");
      input_base64.setAttribute("type", "hidden");
      input_base64.setAttribute("value", only_bas);
      var input_base64_name = document.createElement('input');
      input_base64_name.setAttribute("name", "profile_img_filename");
      input_base64_name.setAttribute("type", "hidden");
      input_base64_name.setAttribute("value", filename);
      document.getElementById("regist_profile").appendChild(input_base64);
      document.getElementById("regist_profile").appendChild(input_base64_name);
      exist_profile_picture = true;
      test_submit();
    });
    FR.readAsDataURL( this.files[0] );
  }
}

function regist_error() {
  alert("?????? ???????????? ?????? ????????? ????????????.")
}

function already_error() {
  alert("????????? ?????? ????????? ????????????.")
}

function miss_match_password() {
  alert("??????????????? ???????????? ????????????.")
}

function email_miss_checked() {
  alert("????????? ????????? ????????????.")
}

function username_update(e) {
  var check_button = document.getElementById("username_check_button");
  check_button.style.visibility = "visible";
  already_username = false;
  if(e.target.value != "") {
    exist_username = true;
  }
  else {
    exist_username = false;
  }
  test_submit();
}

function username_check() {
  var username = document.getElementById("regist_username").value;
  $.ajax({
    type: "POST",
    url: "/already_username",
    data: JSON.stringify({"username": username}),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function(data){
      if (data["exist"] == 0){
        alert("?????? ????????? ??????????????????.");
        var check_button = document.getElementById("username_check_button");
        check_button.style.visibility = "hidden";
        already_username = true;
        test_submit();
      }
      else if (data["exist"] == 1) {
        alert("???????????? ??????????????????.");
      }
      else if (data["exist"] == 2) {
        alert("????????? ??? ?????? ??????????????? ????????????????????????.\n\\ / : * ? \" < > |");
      }
    },
    error: function(errMsg) {
        alert(errMsg);
    }
  });
}

function pw_update(e) {
  if(e.target.value != "") {
    var checked = document.getElementById("password_check").value;
    if(checked == e.target.value) {
      exist_password = true;
      match_password = true;
    } else {
      exist_password = true;
      match_password = false;
    }
  }
  else {
    exist_password = false;
    match_password = false;
  }
  test_submit();
}

function pw_check(e) {
  var password = document.getElementById("regist_password").value;
  if(password != "") {
    if(e.target.value == password) {
      exist_password = true;
      match_password = true;
    } else {
      exist_password = true;
      match_password = false;
    }
  }
  else {
    exist_password = false;
    match_password = false;
  }
  test_submit();
}

function email_check() {
  email = document.getElementById("regist_email").value;
  var send_button = document.getElementById("send_email");
  var type_checker = document.getElementById("type_checker");
  var send_checker = document.getElementById("send_checker");
  send_button.style.visibility = "hidden";
  send_button.style.width = "0";
  send_button.style.height = "0";
  send_checker.style.visibility = "visible";
  type_checker.setAttribute("type", "number");
  $.ajax({
    type: "POST",
    url: "/email_check",
    data: JSON.stringify({"Email": email}),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function(data){
      if(data["error"] == 1) {
        alert("????????? ????????? ??????????????????.");
        var send_button = document.getElementById("send_email");
        var type_checker = document.getElementById("type_checker");
        var send_checker = document.getElementById("send_checker");
        send_button.style.visibility = "visible";
        send_button.setAttribute("style", "padding-left: 10px;padding-right: 10px;padding-up: 10px;padding-buttom: 10px;")
        send_checker.style.visibility = "hidden";
        type_checker.setAttribute("type", "hidden");
      }
      if(data["error"] == 2) {
        alert("?????? ????????? ??????????????????.");
        var send_button = document.getElementById("send_email");
        var type_checker = document.getElementById("type_checker");
        var send_checker = document.getElementById("send_checker");
        send_button.style.visibility = "visible";
        send_button.setAttribute("style", "padding-left: 10px;padding-right: 10px;padding-up: 10px;padding-buttom: 10px;")
        send_checker.style.visibility = "hidden";
        type_checker.setAttribute("type", "hidden");
      }
      if(data["error"] == 0) {
        var send_button = document.getElementById("send_email");
        var type_checker = document.getElementById("type_checker");
        var send_checker = document.getElementById("send_checker");
        send_button.style.visibility = "hidden";
        send_button.style.width = "0";
        send_button.style.height = "0";
        send_checker.style.visibility = "visible";
        type_checker.setAttribute("type", "number");
        alert("?????? ???????????? ??????????????? ??????????????????.");
      }
    },
    error: function(errMsg) {
        alert(errMsg);
    }
  });
}

function sendchecker() {
  email = document.getElementById("regist_email").value;
  checker = document.getElementById("type_checker").value;
  $.ajax({
    type: "POST",
    url: "/checker_check",
    data: JSON.stringify({"email": email, "checker": checker}),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function(data){
      if(data["error"] == 1) {
        alert("???????????? ?????? ??????????????????.");
      }
      if(data["error"] == 2) {
        alert("??????????????? ?????? ????????????.");
      }
      if(data["error"] == 3) {
        alert("??????????????? ??????????????????.");
      }
      if(data["error"] == 0) {
        var email = document.getElementById("regist_email");
        var type_checker = document.getElementById("type_checker");
        var send_checker = document.getElementById("send_checker");
        email.readOnly = true;
        send_checker.style.width = "0";
        send_checker.style.height = "0";
        send_checker.style.visibility = "hidden";
        type_checker.setAttribute("type", "hidden");
        type_checker.setAttribute("width", "0");
        type_checker.setAttribute("height", "0");
        email_check_finished = true;
        alert("????????? ??????????????????.");
        test_submit();
      }
    },
    error: function(errMsg) {
        alert(errMsg);
    }
  });
}

function email_change() {
  var send_button = document.getElementById("send_email");
  var type_checker = document.getElementById("type_checker");
  var send_checker = document.getElementById("send_checker");
  send_button.style.visibility = "visible";
  send_button.setAttribute("style", "padding-left: 10px;padding-right: 10px;padding-up: 10px;padding-buttom: 10px;")
  send_checker.style.visibility = "hidden";
  type_checker.setAttribute("type", "hidden");
}

function matching_redirect() {
  document.location.href = "/matching";
}


function qna_redirect() {
  document.location.href = "/qna";
}

var Request = function() {
  this.getParameter = function(name) {
    var rtnval = '';
    var nowAddress = unescape(location.href);
    var parameters = (nowAddress.slice(nowAddress.indexOf('?') + 1,nowAddress.length)).split('&');
    for (var i = 0; i < parameters.length; i++) {
      var varName = parameters[i].split('=')[0];
      if (varName.toUpperCase() == name.toUpperCase()) {
        rtnval = parameters[i].split('=')[1];
        break;
      }
    }
    return rtnval;
  }
}

function change_profile() {
  document.location.href = "/change_profile";
}

function tag_change() {
  document.location.href = "/tag_change";
}

function add_tag() {
  place = document.getElementById("tags");
  var space = document.createElement("br");
  var new_select = document.createElement("select");
  var num = document.getElementsByClassName("selects").length;
  new_select.add(new Option("3D ?????????","3d modeling"));
  new_select.add(new Option("???????????????","motiongraphic"));
  new_select.add(new Option("???????????????","photographic"));
  new_select.add(new Option("????????????","design"));
  new_select.add(new Option("??????","planning"));
  new_select.add(new Option("?????????","marketing"));
  new_select.add(new Option("?????? ??????","video editing"));
  space.setAttribute("id","select_"+num);
  new_select.setAttribute("id","select_"+num+"_tags");
  new_select.setAttribute("name","select_"+num+"_tags");
  new_select.setAttribute("class","selects");
  new_select.setAttribute("style","margin-top: 5px;");
  place.appendChild(space);
  place.appendChild(new_select);
}

function remove_tag() {
  var num = document.getElementsByClassName("selects").length;
  document.getElementById("select_"+(num-1)).remove();
  document.getElementById("select_"+(num-1)+"_tags").remove();
}
