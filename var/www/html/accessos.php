<?php
	$db = new SQLite3('basededatos.sql');
	$tablesquery = $db->query('select * from autenticacio order by tiempo desc limit 10;');
	while($row = $tablesquery->fetchArray()){
		echo $row[0] . '    ' . $row[1] . '    ' . $row[2] . '    '  . '<br/>';
	}
?>
