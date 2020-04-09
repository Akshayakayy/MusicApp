$(document).ready(function(){
  $('.list').hide();

  $('.display').on('click',function(){
    var access=$(this).attr('id');
    if (access=='private')
    {
      $('#privatelist').show();
      $('#publiclist').hide();
    }
    else {
      $('#publiclist').show();
      $('#privatelist').hide();
    }
  });

/*  var user=$('.form-control').val();
  $('#enter').on('click',function(){
  $.ajax({
    type:'POST',
    url:'/profile',
    data:
    {
      name:user
    },
    success:function(){
      console.log('Success');
    },
    error:function(){
      console.log('Error');
    }
  });
});*/

});
