<?php
    include './bingo_socket.php';
    session_start();
    header('Content-Type: text/event-stream');
    header('Cache-Control: no-cache');
    $sock = stream_socket_client("unix://{$_SERVER['DOCUMENT_ROOT']}assets/php/bingo.sock", $errno, $errst, $flags = STREAM_CLIENT_CONNECT | STREAM_CLIENT_ASYNC_CONNECT);
    $_SESSION['user_id'] = 1;
    session_write_close();
    if($sock){
        fwrite($sock, "{\"bingo_subscribe\": {\"reconnect\": \"true\", \"id\": {$_SESSION['user_id']}}}");
        $msg = fread($sock, 1024);
        client_write("event: call\ndata: {$msg}\n\n");
        while (TRUE) {
            $msg = fread($sock, 1024);
            client_write("event: call\ndata: {$msg}\n\n");
            if (connection_aborted() ) {
                socket_close($sock);
                break;
            }
        }
    }