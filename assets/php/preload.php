<?php
$QUERIES = [
    "check_spot" => function ($args) { return array("user_id" => $_SESSION['user_id'], "card_id" => $args['card_id'], "space_id" => $args['space_id'], "space_number" => $args['space_num']); },
    "request_cards" => function ($args) { return array("user_id" => $_SESSION['user_id']); },
    "sse_subscribe" => function ($args) { return array("user_id" => $_SESSION['user_id'], "reconnect" => 1); }
];
    