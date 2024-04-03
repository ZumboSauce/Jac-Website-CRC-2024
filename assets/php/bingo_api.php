<?php

require_once __DIR__ . "/defines.php";

session_start(array('read_and_close' => true));
error_reporting(E_ALL);
ini_set('display_errors', '1');
$sock = stream_socket_client("unix://{$_SERVER['DOCUMENT_ROOT']}assets/php/bingo.sock", $errno, $errst, $flags = STREAM_CLIENT_CONNECT | STREAM_CLIENT_ASYNC_CONNECT);
if(! $sock){
    echo json_encode(array('conn_failed' => 1));
} else {
    fwrite($sock, json_encode(array($_POST['QUERY'] => QUERIES[ $_POST['QUERY'] ]($_POST['ARGS']) )));
    $resp = fread($sock, 1024);
    echo $resp;
    ob_flush();
    flush();
}