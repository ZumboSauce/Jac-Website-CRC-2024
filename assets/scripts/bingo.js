async function api_request(query, args){
    $.ajax({
        type: 'post',
        url: '/assets/php/bingo_api.php',
        data: { QUERY: query, ARGS: args},
        dataType: 'json',
        success: function (resp) {
            return JSON.parse(resp);
        }
    });
};

$("#id01 .tab_container :not(.close)").on("click", function(){
    $("#id01 .popup-mc > *").css("display", "none");
    switch($(this).attr('class')){
        case 'login':
            $("#login").css("display", "grid");
            break;
        case 'signup':
            $("#signup").css("display", "grid");
            break;
        default:
            break;
    }
});

function span_input_fetch(target_form){
    let data = {};
    console.log(target_form.children());
    target_form.find(".sign-mc-input span").each(function() {
        data[$(this).attr('name')] = $(this).text();
    });
    return data;
}

$('#login-form').on('submit', function (e) {
    e.preventDefault();
    $.ajax({
        type: 'post',
        url: '/assets/php/bingo_login.php',
        data: span_input_fetch($(this)),
        success: function () {
            alert('thang');
        }
    });
});

$('#signup-form').on('submit', function (e) {
    e.preventDefault();
    $.ajax({
        type: 'post',
        url: '/assets/php/bingo_signup.php',
        data: span_input_fetch($(this)),
        success: function () {
            alert('thang');
        }
    });
});

for(let i = 0; i < 6; i++){
    $('#id02 .bingo-card_container').append('<div class=bingo-card_wrapper><div class="bingo-card"></div></div>');
}

for(let i = 0; i < 7; i++) {
    $("#bingo-machine .bingo-machine").append(`<div class="bingo-roll" style="flex-grow: 1"><div></div></div>`);
}

$("#id01 tab_container button[name='bingo-login']").trigger("click");

async function textures_load(){
    const resp = await fetch('/assets/ressources/texture.json');
    const textures = await resp.json();
    return textures;
}

textures_load().then(textures => {
    api_request("request_cards", "{}");
    
    var timeout = 1000;
    var bingosrv;
    function bingosrv_reconnect(){ setTimeout(() => {
        timeout *= 2; 
        bingosrv_connect();
    }, timeout)};

    function bingosrv_connect(){
        bingosrv = new EventSource("http://localhost:5600/bingo_game/");
        bingosrv.addEventListener("call", function(event) {
            item = JSON.parse(event.data).call;
            $("#bingo-machine .bingo-machine").trigger("bingo-machine:call", textures[textures["idx"][item]].texture);
        });
        bingosrv.onerror = (err) => {
            bingosrv.close();
            console.log("sse");
            if(timeout > 64){
                console.log("kys");
            } else {
                bingosrv_reconnect();
            }
        };
    }
    bingosrv_connect();
});