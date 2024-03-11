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
    console.dir(data);
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
    $('#id02 .bingo-card_container').append('<div class="bingo-card_wrapper"><div class="bingo-card"></div></div>');
}

$(".bingo-card").each(function() {
    for(let i = 0; i < 27; i++){
        $(this).append('<div class="bingo-spot"></div>');
    }
});

$("#id01 tab_container button[name='bingo-login']").click();