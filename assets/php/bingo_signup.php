<?php

require_once $_SERVER['DOCUMENT_ROOT'].'.config/config.php';

$conn = new mysqli($SERVERNAME, $USERNAME, $PASSWORD, $DB);

if($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

echo "Connected Succesfully";