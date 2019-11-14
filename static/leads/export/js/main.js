setTimeout(function() {
    $('#message').fadeOut('slow');
}, 5000 );


$(document).ready(function(){

    $('.collapseAll').click(function(){
     $('.collapseExample')
         .collapse('hide');
     });
     $('.expandAll').click(function(){
     $('.collapseExample')
         .collapse('show');
     });
 });

 
$(document).ready(function(){

    $('.collapsebuttomALL').click(function(){
        $('.collapsebuttom')
         .collapse('hide');
        $('.expandbuttomE')
         .collapse('show');
     });

 
 });
$(document).ready(function(){

    $('.expandlabelALL').click(function(){
        $('.expandlabelE')
        .collapse('show');
    });

});
$(document).ready(function(){

    $('.table-success-hover').click(function(){
        $(this).toggleClass( "table-success-hover2" );    
    });
    $('.table-danger-hover').click(function(){
        $(this).toggleClass( "table-danger-hover2" );    
    });
    $('.thead-light-hover').click(function(){
        $(this).toggleClass( "thead-light-hover2" );    
    });
});

$(document).ready(function(){
    $('.comment_approval_toggle').on('click', jQFav);
        function jQFav(e) {
            $(this).toggleClass('btn-primary btn-dark');
            $(this).find('.fa').toggleClass('fa-comment-slash fa-comment');
        }
});