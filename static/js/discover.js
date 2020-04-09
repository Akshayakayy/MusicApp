$(document).ready(function(){
  /*$(document).scroll(function(){
    var pos = $(this).scrollTop();
    var hgt = $(document).height()-100;
    if(pos > 1):
      $('.rock').fadeOut();
  });*/

 $('.veil').hide();
 $('#pop').hide();
 $('#jazz').hide();
 $('#downtempo').hide();
 $('#bollywood').hide();

 $('.genres').on('mouseenter',function(){
    $(this).children().slideDown(800);
  });

 $('.genres').on('mouseleave',function(){
     $(this).children().slideUp(800);
 });

 flag = 1;
 $('.arrowdown').on('click',function(){
  if(flag == 1){
   $('#rock').fadeOut();
   $('#jazz').fadeIn();
   flag = 2;}
  else if(flag == 2){
   $('#jazz').fadeOut();
   $('#pop').fadeIn();
   flag = 3;}
  else if(flag == 3){
   $('#pop').fadeOut();
   $('#downtempo').fadeIn();
   flag = 4;}
  else if(flag == 4){
   $('#downtempo').fadeOut();
   $('#bollywood').fadeIn();
   flag = 5;}
   else if(flag == 5){
     $('#rock').fadeIn();
     $('#bollywood').fadeOut();
     flag=1;
   }
 });

  $('.arrowup').on('click',function(){
    if(flag == 1){
      $('#rock').fadeOut();
      $('#bollywood').fadeIn();
      flag=5;
    }
    else if(flag == 2){
     $('#rock').fadeIn();
     $('#jazz').fadeOut();
     flag = 1;}
    else if(flag == 3){
     $('#jazz').fadeIn();
     $('#pop').fadeOut();
     flag = 2;}
    else if(flag == 4){
     $('#pop').fadeIn();
     $('#downtempo').fadeOut();
     flag = 3;}
    else if(flag == 5){
     $('#downtempo').fadeIn();
     $('#bollywood').fadeOut();
     flag = 4;}
  });
});
