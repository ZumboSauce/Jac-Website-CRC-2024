<?php
    error_reporting(E_ALL);
    ini_set('display_errors', '1');

    header('Content-Type: text/event-stream');
    header('Cache-Control: no-cache');
    $sock = stream_socket_client("unix://{$_SERVER['DOCUMENT_ROOT']}assets/php/bingo.sock", $errno, $errst);
    if (!$sock) {
        echo("data: cum\n\n");
        ob_flush();
        flush();
    } else {
        echo("data: connected\n\n");
        while (TRUE) {
            $msg = fread($sock, 1024);
            echo("event: call\n");
            echo("data: {{$msg}}\n\n");
            ob_flush();
            flush();
            if (connection_aborted()) break;
        }
    }