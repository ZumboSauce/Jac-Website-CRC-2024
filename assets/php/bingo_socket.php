<?php
    function client_write($msg){
        echo($msg);
        ob_flush();
        flush();
    }