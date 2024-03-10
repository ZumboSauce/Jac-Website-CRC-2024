<?php
    
error_reporting(E_ALL);
ini_set('display_errors', '1');

foreach ($_POST as $key => $value)
    echo $key.'='.$value.'<br />';

include $_SERVER['DOCUMENT_ROOT'].'.config/config.php';

$conn = new mysqli(SERVERNAME, USERNAME, PASSWORD, DB);

if($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

