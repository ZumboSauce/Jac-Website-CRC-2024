<?php
    session_start();
    error_reporting(E_ALL);
    ini_set('display_errors', '1');
    include './bingo_socket.php';

    $sock = bingo_connect("conn error");
    if (!$sock) {
        fwrite($sock, "{\"request_card\": {\"id\": {$_SESSION["user_id"]}");
        client_write(fread($sock, 1024));
    }