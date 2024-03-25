$(".bingo-card").each(function() {
    for(let i = 0; i < 27; i++){
        $(this).append('<div class="bingo-spot"></div>');
    }
});

$(".bingo-card .bingo-spot").on("click", function() {
    $.ajax({
        context: this,
        type: 'post',
        url: '/assets/php/bingo_validate_spot.php',
        data: {card: $(this).parents(".bingo-card_wrapper").index(), idx: $(this).index()},
        dataType: 'json',
        success: function (resp) {
            if (resp.resp){
                $(this).css("background-color", "red");
            }
        }
    });
});