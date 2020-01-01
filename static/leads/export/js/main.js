setTimeout(function() {
    $('.message').fadeOut(1000);
}, 10000 );


$(document).ready(function(){

    $("table thead tr").children(".collapseTableHeadersbutton").click(function(){
        $(this).parent().parent(".table-success-hover").toggleClass("table-success-hover2");
        $(this).parent().parent(".table-danger-hover").toggleClass("table-danger-hover2");
        $(this).parent().parent(".thead-light-hover").toggleClass("thead-light-hover2");
        var editing = $(this).data("id");
        $("table").children(".editing"+editing).hide();
        var child = $(this).data("id");
        $("table .collapseTableHeaders"+child).toggle();
        $("table thead th .edit").show();
        $("table thead th .editing").hide();
        });

    $('.collapseAll').click(function(){
        $(".collapseTableHeaders").hide();
        $("table .table-success-hover2").removeClass("table-success-hover2");
        $("table .table-danger-hover2").removeClass("table-danger-hover2");
        $("table .thead-light-hover2").removeClass("thead-light-hover2");
        $("table .editing").hide();
        $("table .static").show();
        });
    $('.expandAll').click(function(){
        $(".collapseTableHeaders").show();
        $("table .table-success-hover2").removeClass("table-success-hover2");
        $("table .table-danger-hover2").removeClass("table-danger-hover2");
        $("table .thead-light-hover2").removeClass("thead-light-hover2");
        $("table .editing").hide();
        $("table .static").show();
        });

    $("table thead th .edit").click(function(){
        var editing = $(this).data("id");
        $("table").children(".editing"+editing).show(300);
        var static = $(this).data("id");
        $("table .static"+static).hide(100);
        var child = $(this).data("id");
        $("table .collapseTableHeaders"+child).hide();
        });
    $("table thead th .times").click(function(){
        $("table .table-success-hover2").removeClass("table-success-hover2");
        $("table .table-danger-hover2").removeClass("table-danger-hover2");
        $("table .thead-light-hover2").removeClass("thead-light-hover2");
        var editing = $(this).data("id");
        $("table").children(".editing"+editing).hide(100);
        var static = $(this).data("id");
        $("table .static"+static).show(300);
        var child = $(this).data("id");
        $("table .collapseTableHeaders"+child).hide();
        });
    
    $("#clear_value_search").click(function(){
        if($('#advanced_search').css('display') == 'none'){
            $(".card form").find("#search_phrase").val("");
        }
        else{
            $(".card form").find("input").val("");
            $(".card form").find("select").prop('selectedIndex',0);    
        }
    });

    $("#togglecard").click(function(){
        $(".card").find("#advanced_search").slideToggle(500);
        $(this).text($(this).text() == 'Advanced Search' ? 'Normal Search' : 'Advanced Search');
        });
    $("#togglecard2").click(function(){
        $("#options").slideToggle(500);
        });


    $("#range-to-example").persianDatepicker({
        "inline": false,
        "format": "L",
        "viewMode": "day",
        "initialValue": true,
        "autoClose": true,
        "position": "auto",
        "altFormat": "l",
        "altField": "#range-to-example-alt",
        "onlyTimePicker": false,
        "onlySelectOnDate": true,
        "calendarType": "persian",
        "inputDelay": 800,
        "observer": true,
        "persianDigit" :false,
        "calendar": {
            "persian": {
            "locale": "en",
            "showHint": false,
            "leapYearMode": "algorithmic"
            },
            "gregorian": {
            "locale": "en",
            "showHint": false
            }
        },
        "navigator": {
            "enabled": true,
            "scroll": {
            "enabled": false
            },
            "text": {
            "btnNextText": "<",
            "btnPrevText": ">"
            }
        },
        "toolbox": {
            "enabled": true,
            "calendarSwitch": {
            "enabled": false,
            "format": "MMMM"
            },
            "todayButton": {
            "enabled": true,
            "text": {
                "fa": "امروز",
                "en": "Today"
            }
            },
            "submitButton": {
            "enabled": false,
            "text": {
                "fa": "تایید",
                "en": "Submit"
            }
            },
            "text": {
            "btnToday": "امروز"
            }
        },
        "timePicker": {
            "enabled": false,
            "step": 1,
            "hour": {
            "enabled": true,
            "step": null
            },
            "minute": {
            "enabled": true,
            "step": null
            },
            "second": {
            "enabled": true,
            "step": null
            },
            "meridian": {
            "enabled": true
            }
        },
        "dayPicker": {
            "enabled": true,
            "titleFormat": "YYYY MMMM"
        },
        "monthPicker": {
            "enabled": true,
            "titleFormat": "YYYY"
        },
        "yearPicker": {
            "enabled": true,
            "titleFormat": "YYYY"
        },
        "responsive": true
    });
    $("#range-from-example").persianDatepicker({
        "inline": false,
        "format": "L",
        "viewMode": "day",
        "initialValue": true,
        "minDate": null,
        "maxDate": null,
        "autoClose": true,
        "position": "auto",
        "altFormat": "l",
        "altField": "#range-from-example-alt",
        "onlyTimePicker": false,
        "onlySelectOnDate": true,
        "calendarType": "persian",
        "inputDelay": 800,
        "observer": true,
        "persianDigit" :false,
        "calendar": {
            "persian": {
            "locale": "en",
            "showHint": false,
            "leapYearMode": "algorithmic"
            },
            "gregorian": {
            "locale": "en",
            "showHint": false
            }
        },
        "navigator": {
            "enabled": true,
            "scroll": {
            "enabled": false
            },
            "text": {
            "btnNextText": "<",
            "btnPrevText": ">"
            }
        },
        "toolbox": {
            "enabled": true,
            "calendarSwitch": {
            "enabled": false,
            "format": "MMMM"
            },
            "todayButton": {
            "enabled": true,
            "text": {
                "fa": "امروز",
                "en": "Today"
            }
            },
            "submitButton": {
            "enabled": false,
            "text": {
                "fa": "تایید",
                "en": "Submit"
            }
            },
            "text": {
            "btnToday": "امروز"
            }
        },
        "timePicker": {
            "enabled": false,
            "step": 1,
            "hour": {
            "enabled": true,
            "step": null
            },
            "minute": {
            "enabled": true,
            "step": null
            },
            "second": {
            "enabled": true,
            "step": null
            },
            "meridian": {
            "enabled": true
            }
        },
        "dayPicker": {
            "enabled": true,
            "titleFormat": "YYYY MMMM"
        },
        "monthPicker": {
            "enabled": true,
            "titleFormat": "YYYY"
        },
        "yearPicker": {
            "enabled": true,
            "titleFormat": "YYYY"
        },
        "responsive": true 
    });
});
