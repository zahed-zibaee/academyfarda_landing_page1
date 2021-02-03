//global var
//variable def
var discount_code = "NULL";
var timeLeft = 0;
var sent = false;
var token1 = "";
var token2 = "";
var connect = true;
//function check connection
function checkconnection() {
  $.ajax({
    url: "/hi",
    method: "POST",
    crossDomain: true,
    timeout: 5000,
    success: function (res) {
      if (res.ans == "hi") {
        setTimeout(function () {
          $("#serverconnectionerror").removeClass("show").addClass("hide");
        }, 1);
        if (connect == false) {
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
      } else {
        setTimeout(function () {
          $("#serverconnectionerror").removeClass("hide").addClass("show");
        }, 1);
        connect = false;
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
//check for token input validation
function check_token_validation(){
  gettokens();
  badsmsinputremover();
  $("#wrong-code").addClass("hide");
  var error = false;
  if ($('#num1').val() == ""){
    $("#num1").addClass("bad");
    error = true;
  }
  if ($('#num2').val() == ""){
    $("#num2").addClass("bad");
    error = true;
  }
  if ($('#num3').val() == ""){
    $("#num3").addClass("bad");
    error = true;
  }
  if ($('#num4').val() == ""){
    $("#num4").addClass("bad");
    error = true;
  }
  if ($('#num5').val() == ""){
    $("#num5").addClass("bad");
    error = true;
  }
  if ($('#num6').val() == ""){
    $("#num6").addClass("bad");
    error = true;
  }
  if (error == false){
    return true;
  }else {
    $("#wrong-code").removeClass("hide");
    return false;
  }
}
//on click on submit_code button check for validations
$("#submit_code").click(function (e) { 
  e.preventDefault();
  var valid = check_token_validation();
  if (valid == true){
    pre_submit()
  }
});
//check for validation code
function pre_submit(){
  badsmsinputremover();
  $("#wrong-code").addClass("hide");
  loadingadd();
  var res_check_connection = checkconnection2();
  var res_check_course_validation = check_course_validation();
  var res_check_data_validation = check_data_validation();
  if (
    res_check_connection == true &&
    res_check_course_validation == true &&
    res_check_data_validation == true
  ) {
    submit();
  } else if (
    res_check_connection == false) {
    loadingremove();
    alert(
      "ارتباط خود را با اینترنت چک کنید."
    );
  }else if (
    res_check_course_validation == false &&
    res_check_data_validation == true) {
    loadingremove();
    alert(
      "دوره انتخاب شده وجود ندارد و یا غیر فعال است."
    );
  }else if (
    res_check_course_validation == true &&
    res_check_data_validation == false) {
    loadingremove();
    alert(
      "اطلاعات وارد شده را بررسی کنید و یا با پشتیبانی تماس حاصل کنید."
    );
  }else{
    loadingremove();
    alert(
      "ارور سرور در صورتی که نمیدانید چه اتفاقی افتاده با ما تماس بگیرید."
    );
  }
}
//function sms send
function sendsms() {
  var phone = fixNumbers($urlParam("phone"));
  var data = "phone=" + phone;
  var url = "http://127.0.0.1:8000/SMS/lookup";
  $.ajax({
    url: url,
    type: "POST",
    data: data,
    crossDomain: true,
    success: function (res) {
      if (res.status == 200) {
        verify_id = res.id;
        console.log(res);
        $("#exampleModal001").modal("show");
        setTimeout(() => {
          $("#num1")[0].focus();
          $("#num1").select();
        }, 500);
        sent = true;
        loadingremove();
      } else {
        alert("پیام ارسال نشد. " + res.status_message);
        loadingremove();
      }
    },
    error: function (error) {
      if(error.status == 500) {
        alert("نمیتوان در هر دقیقه بیش از یک پیام ارسال کرد. لطفا صبر کنید و دوباره تلاش کنید.");
        console.log(error.responseText);
      }else if (error.status == 403){
        alert("نمیتوان در یک روز بیش از 10 پیام ارسال کرد.");
        console.log(error.responseText);
      }else{
        alert("اشکال در ارسال اس ام اس لطفا با ما تماس بگیرید.");
        console.log(error.responseText);
      }
      loadingremove();
    },
  });
}
//send validation sms
$("#send_sms_validator").click(function (e) {
  e.preventDefault();
  if (sent == false) {
    loadingadd();
    sendsms();
    timeLeft = 61;
  } else {
  $("#exampleModal001").modal("show");
  setTimeout(() => {
    $("#num1")[0].focus();
    $("#num1").select();
  }, 500);
  }
});
//verify data for validation functions
function check_course_validation() {
  var data = "course_id=" + course_id;
  var url = "http://127.0.0.1:8000/payments/checkcourse";
  var aj = $.ajax({
    url: url,
    type: "POST",
    data: data,
    async: false,
    crossDomain: true,
    success: function (res) {
      console.log(res);
      setTimeout(() => {
        $("#class_time").text(res.name);
      }, 100);
    },
    error: function (error) {
      console.log("دوره انتخاب شده فعال نیست و یا اصلا وجود ندارد.");
    },
  });
  if (aj.status == 200 && aj.responseJSON.active== "true") {
    return true;
  } else {
    return false;
  }
}
function get_total(discount) {
  var course_id = $urlParam("class_time");
  var data = "course_id=" + course_id;
  if(discount == true){
    var discount_c = $("#input-discount").val();
    data += "&" + "discount_code=" + discount_c 
  }
  var url = "http://127.0.0.1:8000/payments/getcoursetotal";
  $.ajax({
    url: url,
    type: "POST",
    data: data,
    crossDomain: true,
    success: function (res) {
      console.log(res);
      if(discount == true){
        discount_code = discount_c;
        setTimeout(() => {
          $("#discount_total").removeClass("hide");
          $("#course_total").addClass("linethrough");
          $("#discount-code").html(discount_code);
          $("#discount-ans-g").removeClass("hide");
          $("#discount-ans-b").addClass("hide");
          $("#discount-ans-r").addClass("hide");
          $("#remove_discount").removeClass("force-hide");
          $("#total2").html($.persianNumbers(res.total));
        }, 100);
        loadingremove();
      }else{
        setTimeout(() => {
          $("#total").html($.persianNumbers(res.total));
        }, 100);
      }
      return true;
    },
    error: function (error) {
      console.log(error);
      if(discount == true){
        discount_code = "NULL";
        setTimeout(() => {
          $("#discount_total").addClass("hide");
          $("#course_total").removeClass("linethrough");
          $("#discount-code").html(discount_code);
          $("#total2").html($.persianNumbers(""));
          $("#discount-ans-g").addClass("hide");
          $("#discount-ans-b").removeClass("hide");
          $("#discount-ans-r").addClass("hide");
        }, 100);
        loadingremove();
      }
      return false;
    },
  });
}
function check_data_validation() {
  var regex_failed = false;
  var regex_names = RegExp("^.{3,200}$");
  if (regex_names.test(decodeURIComponent($urlParam("name"))) == false) {
    console.log(
      "نام شما کمتر از سه حرف یا بیشتر از مقدار در نظر گرفته شده می‌باشد."
    );
    regex_failed = true;
  }
  if (regex_names.test(decodeURIComponent($urlParam("family"))) == false) {
    console.log(
      "نام خانوادگی شما کمتر از سه حرف یا بیشتر از مقدار در نظر گرفته شده می‌باشد."
    );
    regex_failed = true;
  }
  if (regex_names.test(decodeURIComponent($urlParam("father_name"))) == false) {
    console.log(
      "نام پدر شما کمتر از سه حرف یا بیشتر از مقدار در نظر گرفته شده می‌باشد."
    );
    regex_failed = true;
  }
  var regex_gender = RegExp("^[M,F]$");
  if (regex_gender.test(decodeURIComponent($urlParam("gender"))) == false) {
    console.log(
      "نام خانوادگی شما کمتر از سه حرف یا بیشتر از مقدار در نظر گرفته شده می‌باشد."
    );
    regex_failed = true;
  }
  var regex_meli = RegExp("^[0-9]{10}$");
  if (regex_meli.test(fixNumbers(decodeURIComponent($urlParam("code_meli")))) == false) {
    console.log("کد ملی باید شامل 10 رقم باشد.");
    regex_failed = true;
  }
  var regex_phone = RegExp("^09[0-9]{9}$");
  if (regex_phone.test(fixNumbers(decodeURIComponent($urlParam("phone")))) == false) {
    console.log("شماره موبایل باید با 09 شروع و 9 رقم ادامه داشته باشد.");
    regex_failed = true;
  }
  var regex_address = RegExp("^.{10,2000}$");
  if (regex_address.test(decodeURIComponent($urlParam("address"))) == false) {
    console.log("آدرس شما بسیار کوتاه و یا بسیار طولانی است.");
    regex_failed = true;
  }
  var regex_payment_type = RegExp("^option[1-2]$");
  if (
    regex_payment_type.test(decodeURIComponent($urlParam("payment_type"))) ==
    false
  ) {
    console.log("نوع پرداخت باید یکی از دو حالت قسطی و یا نقدی باشد.");
    regex_failed = true;
  }
  if (regex_failed == false) {
    return true;
  } else {
    return false;
  }
}
//checking discount on click
$("#check_discount").click(function (e) {
  e.preventDefault();
  loadingadd();
  get_total(true);
});
//sms code input and loading functions
function badsmsinputremover() {
  $("#num1").removeClass("bad");
  $("#num2").removeClass("bad");
  $("#num3").removeClass("bad");
  $("#num4").removeClass("bad");
  $("#num5").removeClass("bad");
  $("#num6").removeClass("bad");
  $("#num1")[0].focus();
  $("#num1").select();
  $("#wrong-code").addClass("hide");
}
function badsmsinput() {
  $("#num1").addClass("bad");
  $("#num2").addClass("bad");
  $("#num3").addClass("bad");
  $("#num4").addClass("bad");
  $("#num5").addClass("bad");
  $("#num6").addClass("bad");
  $("#wrong-code").removeClass("hide");
}
function clearsmsinput() {
  $("#num1").val("");
  $("#num2").val("");
  $("#num3").val("");
  $("#num4").val("");
  $("#num5").val("");
  $("#num6").val("");
  $("#num1")[0].focus();
  $("#num1").select();
}
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
//count down
function countDown() {
  timeLeft = timeLeft - 1;
  return timeLeft;
}
setInterval(function () {
  var time = countDown(timeLeft);
  if (time > 0) {
    $("#timeleft").html($.persianNumbers(time));
    $("#timer").removeClass("hide");
    $("#resend-btn").addClass("hide");
  } else {
    $("#timer").addClass("hide");
    $("#resend-btn").removeClass("hide");
  }
}, 1000);
//resend sms after 60 sec
$("#resend-btn").click(function (e) {
  e.preventDefault();
  sendsms();
  timeLeft = 61;
});
//get 2 tokens from inputs
function gettokens() {
  token1 =
    $("#num1").val().toString() +
    $("#num2").val().toString() +
    $("#num3").val().toString();
  token2 =
    $("#num4").val().toString() +
    $("#num5").val().toString() +
    $("#num6").val().toString();
}
//remove discount 
$("#remove_discount").click(function(e){
  e.preventDefault();
  discount_code = "NULL";
  $("#discount_total").addClass("hide");
  $("#course_total").removeClass("linethrough");
  $("#discount-code").html(discount_code);
  $("#total2").html($.persianNumbers(""));
  $("#discount-ans-g").addClass("hide");
  $("#discount-ans-b").addClass("hide");
  $("#discount-ans-r").removeClass("hide");
  $("#remove_discount").addClass("force-hide");
});