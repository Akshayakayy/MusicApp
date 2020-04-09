$(document).ready(function(){
  $('.Playlist').on('click',function(){
    var songname=$(this).parent().attr('class');
    var access=$(this).attr('id');
    var element=$(this);
    $.ajax({
      type:'POST',
      url:'/discover/pop',
      data:
      {
        type:access,
        name:songname,
      },
      success:function(){
       alert('Song Added');
     },
      error:function(){
        alert('Song was not added to playlist');
      }
    });
  });

  $('.play').on('click',function(){
    var url=$(this).attr('id');
    str = "/webApp/static/"
    var song_name=$(this).next().attr('class');
    filename="../static/"+url.slice(str.length,url.length)+"/"+song_name+".mp3";

    var audio=$('#play-song').attr("src",filename)[0];
    audio.play();
    console.log($('.mp3').attr('src'));
  })
})
