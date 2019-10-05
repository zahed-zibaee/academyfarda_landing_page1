$('#opencommends').click(function(){
  if($(this).find($("#opencommends")).hasClass('fa-chevron-down'))
  {
    $(this).find($("#opencommends")).removeClass('fa-chevron-down').addClass('fa-chevron-up');
  }
 else if($(this).find($("#opencommends")).hasClass('fa-chevron-up'))
  {                     
    $(this).find($("#opencommends")).removeClass('fa-chevron-up').addClass('fa-chevron-down');    
  }  
});

setTimeout(function() {
    $('#message').fadeOut('slow');
}, 5000 );



function opencommends(id) {
    var x = document.getElementById("opencommends" + id);
    if (x.className === "fas fa-chevron-left") {
      x.className = "fas fa-chevron-down";
    } else {
      x.className = "fas fa-chevron-left";
    }
  };
