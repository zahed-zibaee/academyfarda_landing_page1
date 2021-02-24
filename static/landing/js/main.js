//variable def
var connect = true;
//soft scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  if (anchor.hash != "#nothing") {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      document.querySelector(this.getAttribute('href')).scrollIntoView({
          behavior: 'smooth'
      });
  });
  }
});
//end soft scroll
//check for connection with server function
function checkconnection() {
  $.ajax({
    url: "/hi",
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
//end check for server connection
function make_toast(header, body, color="red") {
  var toastHeader = $("#toast").find("#toast-header");
  var toastBody = $("#toast").find("#toast-body");
  toastHeader.html(header);
  toastBody.html(body);
  if (color == "G"){
    toastHeader.addClass("green");
    toastHeader.removeClass("red");
  } else {
    toastHeader.addClass("red");
    toastHeader.removeClass("green");
  }
  $("#toast").toast("show");
}
//this is for send lead
function send_leads(element){
  var $form = element;
  var data = $form.serializeArray();
  data.push({
    name: "token",
    value: "OcfLGIGkoex3SDI1o2AeHTBdpwWA1usEuxf04JbiNy9uZHlbzLd6sFaI1U6Qemiy",
  });
  $.ajax({
    url: "/leads/api/submitnew/",
    method: "POST",
    data: data,
    async: false,
    success: function (res) {
      console.log(res);
      make_toast("ثبت گردید","فرم مشاوره با موفقیت ارسال شد<br> در اولین فرصت همکاران ما با شما تماس خواهند گرفت.", "G");
    },
    error: function (e, v) {
      console.log(e);
      if(e.status == 405){
        make_toast("خطا","فرم مشاوره با این شماره قبلا ارسال شده است.");
      } else if(e.status == 403){
        make_toast("خطا","خطای احراز هویت.");
      } else if(e.status == 400){
        make_toast("خطا","اطلاعات ارسالی را چک کنید.");
      } else {
        make_toast("خطا","خطای نا‌مشخص .");
      }
    },
  });
};
$(function () {
  $("#consult-form")
    .parsley()
    .on("form:submit", function () {
      send_leads($("#consult-form"));
    });
});
$("#consult-form").submit(function (e) {
  e.preventDefault();
});
// click on register course
$(".register-me").click(function() {
  $(class_select).val($(this).attr("data-id")).change();
});
//prevent form default submit register forms
$("#register_form").submit(function(e){
  e.preventDefault();
});
// validation check
$(function () {
  $("#register_form")
    .parsley()
    .on("form:submit", function () {
      $("#register_form")[0].submit();
    });
});
//swipers
$(window)
  .on("ready resize", function () {
    var swiper = new Swiper("#license_slide", {
      grabCursor: true,
      centeredSlides: false,
      slidesPerView: "auto",
      direction: "vertical",
      effect: "coverflow",
      coverflowEffect: {
        rotate: 0,
        stretch: 250,
        depth: 150,
        modifier: 2,
        slideShadows: true,
      },
      pagination: {
        el: ".license-slide-pagination",
        clickable: true,
      },
      breakpoints: {
        1199: {
          coverflowEffect: {
            rotate: 0,
            stretch: 189,
            depth: 150,
            modifier: 2,
            slideShadows: true,
          },
        },
        991: {
          direction: "horizontal",
          coverflowEffect: {
            rotate: 0,
            stretch: 150,
            depth: 10,
            modifier: 2,
            slideShadows: false,
            grabCursor: false,
          },
        },
      },
    });
    if ($(window).width() < 560) {
      swiper.destroy();
      var swiper = new Swiper("#license_slide", {
        slidesPerView: 1,
        initialSlide: 3,
        spaceBetween: 0,
        centeredSlides: false,
        freeMode: false,
        pagination: {
          el: ".license-slide-pagination",
          clickable: true,
        },
        breakpoints: {
          380: {
            direction: "horizontal",
            coverflowEffect: {
              rotate: 0,
              stretch: 186,
            },
          },
          372: {
            direction: "horizontal",
            coverflowEffect: {
              rotate: 0,
              stretch: 182,
            },
          },

          365: {
            direction: "horizontal",
            coverflowEffect: {
              stretch: 180,
              depth: 150,
            },
          },
          350: {
            direction: "horizontal",
            coverflowEffect: {
              stretch: 175,
              depth: 150,
            },
          },
          348: {
            direction: "horizontal",
            coverflowEffect: {
              stretch: 170,
            },
          },
          333: {
            direction: "horizontal",
            coverflowEffect: {
              stretch: 175,
            },
          },

          320: {
            direction: "horizontal",
            spaceBetween: 0,
            centeredSlides: true,
            freeMode: true,

            coverflowEffect: {},
          },
          200: {
            direction: "horizontal",
            spaceBetween: 0,
            centeredSlides: true,
            freeMode: true,

            coverflowEffect: {},
          },
        },
      });
    }
  })
  .resize();
var swiper2 = new Swiper("#picture_slide", {
  slidesPerView: 3,
  initialSlide: 3,
  spaceBetween: 0,
  centeredSlides: false,
  freeMode: false,
  loop: true,
  autoplay: {
    delay: 4000,
    disableOnIntraction: false,
  },

  navigation: {
    nextEl: "#swiper-buttons-next",
    prevEl: "#swiper-buttons-prev",
  },
  pagination: {
    el: ".pic-slide-pagination",
    clickable: true,
  },
  on: {
    init: function () {
      var $wrapper = this.$wrapperEl;

      var transform = $wrapper[0].style.transform
        .replace("translate3d", "")
        .replace("(", "")
        .replace(")", "")
        .replace(/px/g, "")
        .split(", ");

      transform[0] -= $(this.$wrapperEl).find(".swiper-slide").width() * 0.4;

      transform[0] += "px";
      transform[1] += "px";
      transform[2] += "px";

      transform = "translate3d(" + transform.join(", ") + ")";

      setTimeout(function () {
        $wrapper[0].style.transform = transform;
      }, 50);
    },
  },
  breakpoints: {
    1199: {
      slidesPerView: 3,
      initialSlide: 2,
    },
    991: {
      slidesPerView: 2,
      initialSlide: 1,
    },
    767: {
      slidesPerView: 2,
      initialSlide: 1,
    },
    520: {
      slidesPerView: 2,
      freeMode: false,
      initialSlide: 1,
    },
    200: {
      slidesPerView: 1,
      freeMode: false,
      initialSlide: 1,
    },
  },
});
var swiper3 = new Swiper("#picture_slide2", {
  slidesPerView: 3,
  initialSlide: 3,
  spaceBetween: 0,
  centeredSlides: false,
  freeMode: false,
  loop: true,
  autoplay: {
    delay: 4000,
    disableOnIntraction: false,
  },

  navigation: {
    nextEl: "#swiper-buttons-next2",
    prevEl: "#swiper-buttons-prev2",
  },
  pagination: {
    el: ".pic-slide-pagination2",
    clickable: true,
  },
  on: {
    init: function () {
      var $wrapper = this.$wrapperEl;

      var transform = $wrapper[0].style.transform
        .replace("translate3d", "")
        .replace("(", "")
        .replace(")", "")
        .replace(/px/g, "")
        .split(", ");

      transform[0] -= $(this.$wrapperEl).find(".swiper-slide").width() * 0.4;

      transform[0] += "px";
      transform[1] += "px";
      transform[2] += "px";

      transform = "translate3d(" + transform.join(", ") + ")";

      setTimeout(function () {
        $wrapper[0].style.transform = transform;
      }, 50);
    },
  },
  breakpoints: {
    1199: {
      slidesPerView: 3,
      initialSlide: 2,
    },
    991: {
      slidesPerView: 2,
      initialSlide: 1,
    },
    767: {
      slidesPerView: 2,
      initialSlide: 1,
    },
    520: {
      slidesPerView: 2,
      freeMode: false,
      initialSlide: 1,
    },
    200: {
      slidesPerView: 1,
      freeMode: false,
      initialSlide: 1,
    },
  },
});
// Main list tracker and activator
window.addEventListener("DOMContentLoaded", () => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      const id = entry.target.getAttribute("id");
      if (entry.intersectionRatio > 0) {
        document
          .querySelector("li a[href='#" + id + "']")
          .parentElement.classList.add("active");
      } else {
        document
          .querySelector("li a[href='#" + id + "']")
          .parentElement.classList.remove("active");
      }
    });
  });
  // Track all sections that have an `id` applied
  document.querySelectorAll("section[id]").forEach((section) => {
    observer.observe(section);
  });
});
//modal close by click on link
$(document).on("click", ".close-modal", function (e) {
  $("#exampleModal001").modal("hide");
});
//free session 
$(document).on("click", ".go-to-consult-form-1fs", function (e) {
  $("#question2").val(
    "می‌خواهم یک جلسه رایگان به عنوان مهمان در کلاس شرکت کنم."
  );
  $("#question2").removeClass("highlight001");
  setTimeout(function () {
    $("#question2").addClass("highlight001");
  }, 100);
});
$(document).on("click", ".go-to-consult-form", function (e) {
  $("#question2").removeClass("highlight001");
});
