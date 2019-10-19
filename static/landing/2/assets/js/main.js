function dwtoast( txt ) {
    var $toast = jQuery('#dwtoast');

    $toast.html(txt);
    $toast.addClass('show');

    // After 3 seconds, remove the show class from DIV
    setTimeout(function(){ $toast.removeClass('show') }, 12000 );
}

(function($){
    /**
     * "Scroll to" links
    */
    $("a.scroll_link").click(function(e) {
        e.preventDefault();
        var target = $(this).data("target") || $(this).attr("href");

        $("html, body").animate({
            scrollTop: $(target).offset().top + "px"
        }, {
            duration: 500,
            easing: "swing"
        });

        return false;
    });

  $('#register_form').submit(function(e) {
    e.preventDefault();

    var $form = $(this);
    var data  = $form.serializeArray();

    data.push({
      name: 'token',
      value: '123'
    });

    $.ajax({
      url: 'http://127.0.0.1:8000/submit/leads',
      method: 'POST',
      data: data,
      crossDomain: true,
      success: function(res) {
        console.log(res);

        if (res.status == 'submited') {
          dwtoast($form.find('.success-message').html())

          setTimeout(function() {
            window.location.href = '/thanks'
          }, 2000)

        } else if (res.status == 'registeration_error') {
          dwtoast($form.find('.error-registeration').html())

        } else if (res.status == 'phone_number_needed') {
            dwtoast($form.find('.error-phone-number-needed').html())

        } else if (res.status == 'repetitive_ phone_number') {
            dwtoast($form.find('.error-repeated-phone').html())

        } else if (res.status == 'name_needed') {
            dwtoast($form.find('.error-name_needed').html())

        } else if (res.status == 'unknown_error') {
            dwtoast($form.find('.error-server').html())

        } else {
          dwtoast($form.find('.error-message').html())

        }

      },
      error: function(e, v) {
        dwtoast($form.find('.error-message').html())
      }
    });
  });

    /**
     * modal definations
    */
   window.globalmodal = new tingle.modal({
    footer: false,
    stickyFooter: false,
    closeMethods: ['overlay', 'button', 'escape'],
    closeLabel: "Close",
    beforeOpen: function() {

    }
});

$(document).on('click', '[data-modal]', function(e) {
    e.preventDefault();

    var $target = $( $(this).data('modal') );

    if ($target.length) {
        window.globalmodal.setContent($target.html());
        $(document).trigger('modal_content_loaded');
        window.globalmodal.open();
    }
});

    var swiper = new Swiper('#license_slide', {
        grabCursor: true,
        centeredSlides: false,
        slidesPerView: 'auto',
        direction: 'vertical',
        effect: 'coverflow',
        coverflowEffect: {
          rotate: 0,
          stretch: 250,
          depth: 150,
          modifier: 2,
          slideShadows : true,
        },
        pagination: {
          el: '.license-slide-pagination',
          clickable: true
        },
        breakpoints:{
            991:{
                coverflowEffect: {
                    rotate: 0,
                    stretch: 189,
                    depth: 150,
                    modifier: 2,
                    slideShadows : true,
                }
            },
            380:{
                coverflowEffect: {
                    rotate: 0,
                    stretch: 186,
                },
            },
            372:{
                coverflowEffect: {
                    rotate: 0,
                    stretch: 182,
                },
            },

            365:{
                coverflowEffect: {
                    stretch: 180,
                    depth: 150,
                },
            },
            350:{
                coverflowEffect: {
                    stretch: 175,
                    depth: 150,
                },
            },
            348:{
                coverflowEffect: {
                    stretch: 170,
                }
            },
            333:{
                coverflowEffect: {
                    stretch: 175,
                }
            },

            320:{
                coverflowEffect: {
                    stretch: 158,
                }
            },

      }});


      var swiper2 = new Swiper('#picture_slide', {
        slidesPerView: 4,
        initialSlide: 3,
        spaceBetween: 0,
        centeredSlides:false,
        freeMode: false,
        // autoplay:{
        //   delay:4000,
        //   disableOnIntraction: false,

        // } ,

        navigation: {
          nextEl: '.swiper-buttons-next',
          prevEl: '.swiper-buttons-prev',
        },
        pagination: {
          el: '.pic-slide-pagination',
          clickable: true
        },
        on: {
            init: function () {
                var $wrapper = this.$wrapperEl;

                var transform = $wrapper[0].style.transform.replace('translate3d', '').replace('(',  '').replace(')', '').replace(/px/g, '').split(', ')

                transform[0] -= $(this.$wrapperEl).find('.swiper-slide').width() * 0.4

                transform[0]+= 'px';
                transform[1]+= 'px';
                transform[2]+= 'px';

                transform = 'translate3d(' + transform.join(', ') + ')';

                setTimeout(function() {
                    $wrapper[0].style.transform = transform;

                }, 50)
            },
        },
        breakpoints:{
            991:{
                slidesPerView: 3,
                initialSlide: 2,
            },
            767:{
                slidesPerView: 2,
                initialSlide: 1,
            },
            520:{
                slidesPerView: 1,
                freeMode: false,
                initialSlide: 1,
            },

        },
    });

})(jQuery)

