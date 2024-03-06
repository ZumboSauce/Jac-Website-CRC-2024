<?php
$servername = 'localhost';
$username = 'cheese';
$password = 'pass';
$dbname = 'bingo';

$conn = new mysqli($servername, $username, $password, $dbname);

if($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}



echo "Connected Succesfully";
?>