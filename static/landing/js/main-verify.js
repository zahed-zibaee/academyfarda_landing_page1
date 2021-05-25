//global var
//variable def
var discount_status = 404;
var timeRemaining = -5;
var currentTime = 0;
var expiredDate = 0;
var sent = false;
var connect = true;
//function check connection
function checkconnection() {
  $.ajax({
    url: "/heartbeat/",
    method: "GET",
    crossDomain: true,
    timeout: 5000,
    success: function (res) {
        if (connect == false) {
          setTimeout(function () {
            $("#serverconnectionerror").removeClass("show").addClass("hide");
          }, 1);
          setTimeout(function () {
            $("#serverconnectionreconnect")
              .removeClass("hide")
              .addClass("show");
          }, 1);
          setTimeout(function () {
            $("#serverconnectionreconnect")
              .removeClass("show")
              .addClass("hide");
          }, 5000);
          connect = true;
        }
    },
    error: function (error) {
      console.log(error);
      setTimeout(function () {
        $("#serverconnectionerror").removeClass("hide").addClass("show");
      }, 1);
      connect = false;
    },
  });
}
//check for connection with server
checkconnection();
setInterval(function () {
  checkconnection();
}, 10000);
// loading add and remove 
function loadingadd() {
  setTimeout(function () {
    $("body").addClass("body-on-loading");
    $("#loading2").removeClass("force-hide");
  }, 100);
}
function loadingremove() {
  setTimeout(function () {
    $("body").removeClass("body-on-loading");
    $("#loading2").addClass("force-hide");
  }, 100);
}
//get cookie
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');
// make toast function
function make_toast(header, body, color="red") {
  var toastHeader = $("#toast").find("#toast-header");
  var toastBody = $("#toast").find("#toast-body");
  toastHeader.html(header);
  toastBody.html(body);
  if (color == "G"){
    toastHeader.addClass("green");
    toastHeader.removeClass("red");
    toastHeader.removeClass("orange");
  } else if(color == "R") {
    toastHeader.addClass("red");
    toastHeader.removeClass("green");
    toastHeader.removeClass("orange");
  } else if(color == "O") {
    toastHeader.addClass("orange");
    toastHeader.removeClass("green");
    toastHeader.removeClass("red");
  } else {
    toastHeader.addClass("green");
    toastHeader.removeClass("red");
    toastHeader.removeClass("orange");
  }
  $("#toast").toast("show");
}
/* 
    <-- DISCOUNT -->
*/ 
function discount_state_check(){
  if(discount_state == "N"){
  }else if(discount_state == "A"){
    $('#input-discount-code').tokenfield('createToken', code);
    $("#discount-success").removeClass("hide");
    $("#discount-unsuccess").addClass("hide");
    $("#discount-delete-success").addClass("hide");
    var message = "کد تخفیف " + code + " به مبلغ " + amount + " تومان اعمال گردید. "
    make_toast("اعمال کد تخفیف", message, "G");
  }else if(discount_state == "R"){
    $("#discount-success").addClass("hide");
    $("#discount-unsuccess").addClass("hide");
    $("#discount-delete-success").removeClass("hide");
    make_toast("حذف کد تخفیف","کد تخفیف از پرداخت حذف شد.", "O");
  }
}
// check code
function CheckDiscount(discount_code) {
  loadingadd();
  data = {
    discount_code: discount_code,
  }
  return $.ajax({
    type: "PATCH",
    data: JSON.stringify(data),
    dataType: "text",
    contentType: 'application/json; charset=utf-8',
    headers: { "X-CSRFToken": csrftoken },
    async: false,
    success: function (res, textStatus, xhr) {
      console.log(res);
      var regex = /\/?\??state=[R,A]/i;
      url = window.location.href.replace(regex, '');
      if(xhr.status == 200){
        window.location.href = url + "?state=R"
      } else if(xhr.status == 201){
        window.location.href = url + "?state=A"
      }
    },
    error: function (error) {
      console.log(error);
      $("#discount-success").addClass("hide");
      $("#discount-unsuccess").removeClass("hide");
      $("#discount-delete-success").addClass("hide");
      if(error.status == 404){
        make_toast("اعمال کد تخفیف","کد تخفیف وارد شده اشتباه است.", "R");
        loadingremove();
      } else {
        make_toast("اعمال کد تخفیف","ارتباط با سرور با مشکل مواجه است.", "R");
        loadingremove();
      }
    },
  });
}
// button change function
$("#check_discount").click(function() {
  $('#input-discount-code').tokenfield('createToken', $('#input-discount-code-tokenfield')[0].value);
  $('#input-discount-code-tokenfield')[0].value = "";
});
// tokenize input
$('#input-discount-code')
.on('tokenfield:createtoken', function (e) {
  // make input valid
  if(discount_state != "A"){
    discount_status = CheckDiscount(e.attrs.value).status;
    if(discount_status != 201 || discount_status != 200){
      discount_state = "F";
      discount_state_check();
      return false;
    }
  }
})
.on('tokenfield:removetoken', function (e) {
  // remove discount code
  CheckDiscount('');
}).tokenfield({
    tokens: [code,],
    limit: 1,
});
$("#form-discount").submit(function (e) {
  e.preventDefault();
});	
discount_state_check();
/* 
    <-- SMS -->
*/ 
//verify botton behavior
$("#send_sms_validator").click(function (e) {
  e.preventDefault();
  if (sent == false) {
    loadingadd();
    sendsms();
  } else {
  $("#exampleModal001").modal("show");
  setTimeout(() => {
    $("#token")[0].focus();
    $("#token").select();
  }, 500);
  }
});
//function sms send
function sendsms() {
  $.ajax({
    type: "PUT",
    headers: { "X-CSRFToken": csrftoken },
    success: function (res, textStatus, xhr) {
        console.log(xhr.status);
        $("#exampleModal001").modal("show");
        setTimeout(() => {
          $("#token")[0].focus();
          $("#token").select();
        }, 500);
        sent = true;
        countDownSetup();
        make_toast("ارسال کد احراز هویت","کد احراز هویت شما با موفقیت به شماره تلفن شما sms شد.", "G");
        loadingremove();
    },
    error: function (error) {
      if(error.status == 403) {
        make_toast("ارسال کد احراز هویت","نمیتوان در هر دقیقه بیش از یک پیام ارسال کرد. لطفا صبر کنید و دوباره تلاش کنید.", "R");
        console.log(error);
      }else{
        make_toast("ارسال کد احراز هویت","اشکال در ارسال اس ام اس.", "R");
        console.log(error);
      }
      loadingremove();
    },
  });
}
//count down
function countDownSetup() {
  currentTime = Math.floor(new Date().getTime() / 1000);
  expiredDate = Math.floor(new Date().getTime() / 1000) + 31
  timeRemaining = expiredDate - currentTime;
  $("#timer").removeClass("hide");
  $("#resend-btn").addClass("hide");
}
setInterval(function () {
  if(timeRemaining > 0){
    currentTime = Math.floor(new Date().getTime() / 1000);
    timeRemaining = expiredDate - currentTime;
    $("#timeleft").html(timeRemaining);
  } else if(timeRemaining == 0 || timeRemaining == -1){
    $("#timer").addClass("hide");
    $("#resend-btn").removeClass("hide");
    timeRemaining = -5
  }
}, 1000);
//resend sms after 60 sec
$("#resend-btn").click(function (e) {
  e.preventDefault();
  loadingadd();
  sendsms();
});
//sms code input and loading functions
function badsmsinputremover() {
  $("#token").removeClass("bad");
  $("#token")[0].focus();
  $("#token").select();
  $("#wrong-code").addClass("hide");
}
function badsmsinput() {
  $("#token").addClass("bad");
  $("#wrong-code").removeClass("hide");
}
function clearsmsinput() {
  $("#token").val("");
  $("#token")[0].focus();
  $("#token").select();
}
//on click on submit_code button check for validations
$("#submit_code").click(function (e) { 
  e.preventDefault();
  if($("#token").val().length != 6){
    badsmsinput();
    clearsmsinput();
    make_toast("احراز هویت","کد وارد شده اشتباه است.", "R");
  }else{
    loadingadd();
    submit();
  }
});
function submit(){
  var data = $("#form").serialize();
  $.ajax({
    type: "POST",
    data: data,
    headers: { "X-CSRFToken": csrftoken },
    success: function (res, textStatus, xhr) {
      console.log(xhr.status);
      window.location.href = res;
      loadingremove();
    },
    error: function (error) {
      console.log(error);
      badsmsinput();
      clearsmsinput();
      if(error.status == 403){
        make_toast("احراز هویت","کد وارد شده اشتباه است.", "R");
      } else {
        make_toast("احراز هویت","مشکل ارتباط با درگاه پرداخت.", "R");
      }
      loadingremove();
    },
  });
}