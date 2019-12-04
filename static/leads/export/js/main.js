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
        var editing = $(this).data("id");
        $("table").children(".editing"+editing).hide(100);
        var static = $(this).data("id");
        $("table .static"+static).show(300);
        var child = $(this).data("id");
        $("table .collapseTableHeaders"+child).hide();
        });

}); 
