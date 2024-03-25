<?php
    session_start();
    session_write_close();
    error_reporting(E_ALL);
    ini_set('display_errors', '1');
    include './bingo_socket.php';
    $sock = stream_socket_client("unix://{$_SERVER['DOCUMENT_ROOT']}/assets/php/bingo.sock", $errno, $errst, $flags = STREAM_CLIENT_CONNECT);
    if ($sock) {
        fwrite($sock, "{\"request_cards\": {\"user_id\": {$_SESSION["user_id"]}}}");
        client_write(fread($sock, 1024));
    }