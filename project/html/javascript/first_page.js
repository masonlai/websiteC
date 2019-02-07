$(window).scroll(function(){
var scroll_postion = $(window).scrollTop()/2;
$('section').css({
'background-position-x': - scroll_postion + 'px',
})
})

