<?php
    session_start();
    error_reporting(E_ALL);
    ini_set('display_errors', '1');
    include './bingo_socket.php';
    session_write_close();
    $sock = stream_socket_client("unix://{$_SERVER['DOCUMENT_ROOT']}assets/php/bingo.sock", $errno, $errst, $flags = STREAM_CLIENT_CONNECT | STREAM_CLIENT_ASYNC_CONNECT);
    if ($sock) {
        fwrite($sock, "{\"validate_spot\": {\"user_id\": {$_SESSION["user_id"]}, \"card_id\": {$_POST["card"]}, \"space_id\": {$_POST["idx"]}}}");
        client_write(fread($sock, 1024));
    }