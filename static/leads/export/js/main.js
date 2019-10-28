setTimeout(function() {
    $('#message').fadeOut('slow');
}, 5000 );


$(document).ready(function(){

    $('.collapseAll').click(function(){
        $('.collapse')
         .collapse('hide');
     });
     $('.expandAll').click(function(){
     $('.collapse')
         .collapse('show');
     });
  
 
 });

$(document).ready(function(){
    $('div.comment_approval_toggle').on('click', jQFav);
        function jQFav(e) {
            $(this).find('.btn').toggleClass('btn-primary btn-dark');
            $(this).find('.fa').toggleClass('fa-comment-slash fa-comment');
        }
});