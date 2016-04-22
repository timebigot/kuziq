(function( $ ){
    $.fn.playmusic = function() {
        
        $('.selected').removeClass('selected')
        $(this).addClass('selected');

        var artist = $(this).attr("artist");
        var title = $(this).attr("title");

        $.get('/stream', {artist: artist, title: title}, function(data){
            $('#player').attr('src', data);
            var player = $('audio');

            player[0].pause();
            player[0].load();

            player[0].play();
        });
    }; 
})( jQuery );

$('body').on('click','#get_stream',function() {  
    $(this).playmusic();
});

$('audio').on('ended', function() {
    currentSong = $('.selected')
    nextSong = $('.selected').closest('li').next().find('#get_stream');
    nextSong.playmusic();
    $('audio').on('play', function() {
        currentSong.removeClass('selected');
    });
});
