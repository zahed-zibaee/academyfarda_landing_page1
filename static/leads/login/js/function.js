$(document).ready(function(){

	$(".login-form-link").click(function(e){
	$("#forgot-form").slideUp(0);	
	$("#login-form").fadeIn(300);	
	});

	$(".forgot-form-link").click(function(e){
	$("#login-form").slideUp(0);
	$("#forgot-form").fadeIn(300);
	});
});

