$(".bingo-machine").on('bingo-machine:call', function () {
    $(this).prepend('<div class="bingo-roll">5</div>');
    $(this).children().last().animate({'flex-grow': 0}, {duration: 3000, easing: "swing",
        start: function(){
            $(this).siblings().first().animate({'flex-grow': 1}, 3000, "swing");
        },
        complete: function(){
            $(this).remove();
        }
    });
});