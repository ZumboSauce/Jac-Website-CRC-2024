$(document).ready(function() {
    $("#id01 .tab_container button").on("click", function(){
        $("#id01 .popup-mc").children("." + $(this).attr('class')).css("display", "grid").siblings().css("display", "none");
    });

    $("#id01 tab_container button[name='bingo-login']").click();
});