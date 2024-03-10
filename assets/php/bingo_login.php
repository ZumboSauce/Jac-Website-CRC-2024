<?php

error_reporting(E_ALL);
ini_set('display_errors', '1');

include $_SERVER['DOCUMENT_ROOT'] . '.config/config.php';

$conn = new mysqli(SERVERNAME, USERNAME, PASSWORD, DB);

if($conn->connect_error) {
    echo "fail";
    die("Connection failed: " . $conn->connect_error);
}

