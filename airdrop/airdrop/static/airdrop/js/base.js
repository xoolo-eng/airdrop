$(window).ready(function(){
    var hh = $('#header').height();
    var fh = $('#footer').height();
    var wh = $(window).height();
    var сh = wh - hh - fh -13;
    $('#content .container').css('min-height', сh);
});

$(window).resize(function(){
    var hh = $('#header').height();
    var fh = $('#footer').height();
    var wh = $(window).height();
    var сh = wh - hh - fh -13;
    $('#content .container').css('min-height', сh);
});