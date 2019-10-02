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
  }