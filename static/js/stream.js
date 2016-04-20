$('body').on('click','#get_stream',function() {  
    
    var artist = $(this).attr("artist");
    var title = $(this).attr("title");

    $.get('/stream', {artist: artist, title: title}, function(data){
        $('#player').attr('src', data);
        var player = $('audio');

        player[0].pause();
        player[0].load();

        player[0].oncanplaythrough = player[0].play();
    });
});
