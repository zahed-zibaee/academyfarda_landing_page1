$(document).ready(function(){

	$(document).ready(function(){
	$("#register-form").hide();
	$("#forgot-form").hide();	
	$(".register-form-link").click(function(e){
	$("#login-form").slideUp(0);
	$("#forgot-form").slideUp(0)	
	$("#register-form").fadeIn(300);	
	});

	$(".login-form-link").click(function(e){
	$("#register-form").slideUp(0);
	$("#forgot-form").slideUp(0);	
	$("#login-form").fadeIn(300);	
	});

	$(".forgot-form-link").click(function(e){
	document.getElementById("forgot-form").style.opacity = "1";
	$("#login-form").slideUp(0);
	$("#forgot-form").fadeIn(300);
	});
	});

	});

const floatField = document.getElementById('floatField');
const floatContainer = document.getElementById('floatContainer');
floatField.addEventListener('focus', () => {
  floatContainer.classList.add('active');
});
floatField.addEventListener('blur', () => {
  floatContainer.classList.remove('active');
});