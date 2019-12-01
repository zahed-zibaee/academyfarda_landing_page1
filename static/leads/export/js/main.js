setTimeout(function() {
    $('#message').fadeOut('slow');
}, 5000 );


$(document).ready(function(){
    $("table").children("tbody").hide();
    $("table .editing").hide();

    $("table thead tr").children(".collapseTableHeadersbutton").click(function(){
        var editing = $(this).data("id")
        $("table").children(".editing"+editing).hide();
        var child = $(this).data("id");
        $("table .collapseTableHeaders"+child).toggle();
        $("table thead th .edit").show();
        $("table thead th .editing").hide();
        });

    $('.collapseAll').click(function(){
        $(".collapseTableHeaders").hide('300');
        });
    $('.expandAll').click(function(){
        $(".collapseTableHeaders").show('300');
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


$(document).ready(function(){

    $('.table-success-hover111').click(function(){
        $(this).toggleClass( "table-success-hover2" );    
    });
    $('.table-danger-hover111').click(function(){
        $(this).toggleClass( "table-danger-hover2" );    
    });
    $('.thead-light-hover111').click(function(){
        $(this).toggleClass( "thead-light-hover2" );    
    });
});
