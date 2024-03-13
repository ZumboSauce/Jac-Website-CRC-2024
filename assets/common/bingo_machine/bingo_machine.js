$(".bingo-machine").on('click', function () {
    $(this).prepend('<div class="bingo-roll">5</div>');
    $(this).children().last().animate({'flex-grow': 0}, {duration: 2000, easing: "swing",
        start: function(){
            $(this).siblings().first().animate({'flex-grow': 1}, 2000, "swing");
        },
        complete: function(){
            $(this).remove();
        }
    });
});