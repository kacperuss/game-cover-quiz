<?php

header("Access-Control-Allow-Origin: *");

function return_json($data) {
    header("Content-Type: application/json");
    echo json_encode($data);
    exit();
}

function grab_POST_json() {
    return (array) json_decode(file_get_contents('php://input'));
}

function save_report($report, $game, $img) {
    $data = [];
    if( file_exists('reports.json') ) 
        $data = json_decode(file_get_contents('reports.json'));
    array_push($data, ['game' => $game, 'img' => $img, 'report' => $report]);
    file_put_contents('reports.json', json_encode($data));
}

function check_token($id, $token) {
    $used_ids = [];
    if( file_exists('used_ids.json') ) 
        $used_ids = json_decode(file_get_contents('used_ids.json'));
    if(array_search($id, $used_ids) !== false)
        return false;

    $secret = md5(strval($id));
    $secret = md5(substr($secret, 16) . substr($secret, 0, 16)) . md5(md5($secret));
    if($secret !== $token)
        return false;

    array_push($used_ids, $id);
    file_put_contents('used_ids.json', json_encode($used_ids));

    return true;
}

$data = grab_POST_json();

if(!check_token($data['id'], $data['token'])) {
    return_json(['200 OK']);
}
save_report($data['report'], $data['game'], $data['image']);
return_json(['200 OK']);

?>