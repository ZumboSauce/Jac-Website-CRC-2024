<?php
    error_reporting(E_ALL);
    ini_set('display_errors', '1');

    header('Content-Type: text/event-stream');
    header('Cache-Control: no-cache');
    $sock = stream_socket_client("unix:///assets/php/bingo.sock", $errno, $errst);
    if(!$sock) {
        echo("data: $errno - $errstr\n\n");
        ob_flush();
        flush();
    } else {
        while (TRUE) {
            $msg = fread($sock, 1024);
            echo("data: {$msg}\n\n");
            ob_flush();
            flush();
        }
    }