async function textures_load(){
    const resp = await fetch('/assets/ressources/texture.json');
    const textures = await resp.json();
    return textures;
}


textures_load().then(textures => {    
    $(".bingo-machine").on('bingo-machine:call', function () {
        $(this).prepend(`<div class="bingo-roll" style="--idx: 1"><div style="background-image: url(${textures[arg1].texture})"></div>`);
        $(this).children().last().animate({'flex-grow': 0}, {duration: 3000, easing: "swing",
            start: function(){
                $(this).siblings().first().animate({'flex-grow': 1}, 3000, "swing");
            },
            complete: function(){
                $(this).remove();
            }
        });
    });
});
