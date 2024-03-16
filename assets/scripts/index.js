function Appear()
{
    document.getElementById("chest").style.display="none";
    document.getElementById("cheststuff").style.animation="picswitch 2s linear";
    document.getElementById("cheststuff").style.display="flex";
    
    if (document.getElementById("cheststuff").style.display=="flex"){
        document.getElementById("on").style.display="flex";
    }
    
    // console.log("nope")

    // if (document.getElementById("on").style.display == "none")
    // {
    //     document.getElementById("on").style.display ="flex";
    //     console.log("Hi!")
        
    // }
    // else
    // {
        
    //     document.getElementById("on").style.display = "none";
    //     console.log("hii!!!")
    // }
}

function rotate(name){
    var angle = 0;
    document.getElementById(name).style.transform= "rotate3d(0, 1, 0, angle)";
    angle++;
    console.log("test",angle);
}
    