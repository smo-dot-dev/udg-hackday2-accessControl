<?php
	$jsonData = json_decode(trim(file_get_contents('php://input')), true);
	$usuari = $jsonData['user'];
	$contra = $jsonData['passwd'];
	echo $usuari. "   " . $contra;
	$db = new SQLite3('basededatos.sql');
	$tablesquery = $db->query('insert into usuaris values('. $usuari .','. $contra . ');');
?>
