setTimeout(function() {
    $('#message').fadeOut('slow');
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
        $(".card form").find("input").val("");
        $(".card form").find("select").prop('selectedIndex',0);
        });

    $(".togglecard").click(function(){
        $(this).siblings().slideToggle(500);
        $(this).find("i").toggleClass("fa-caret-square-up fa-caret-square-down");
        });


    var to, from;
    to = $(".range-to-example").persianDatepicker({
        inline: true,
        format: "L",
        altField: '.range-to-example-alt',
        altFormat: 'X',
        initialValue: false,
        responsive: true,
        onSelect: function (unix) {
            to.touched = true;
            if (from && from.options && from.options.maxDate != unix) {
                var cachedValue = from.getState().selected.unixDate;
                from.options = {maxDate: unix};
                if (from.touched) {
                    from.setDate(cachedValue);
                }
            }
        }
    });
    from = $(".range-from-example").persianDatepicker({
        inline: true,
        format: "L",
        altField: '.range-from-example-alt',
        altFormat: 'X',
        initialValue: false,
        responsive: true,
        onSelect: function (unix) {
            from.touched = true;
            if (to && to.options && to.options.minDate != unix) {
                var cachedValue = to.getState().selected.unixDate;
                to.options = {minDate: unix};
                if (to.touched) {
                    to.setDate(cachedValue);
                }
            }
        }
    });
});
