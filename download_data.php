<?php

require "user_info.php";

$dbh=mysql_connect ($dbhost, $db_user, $db_pw) or die ('I cannot connect to the database because: ' . mysql_error());
mysql_select_db ($database);

$sql = "SELECT ID,url,filetype FROM Files WHERE (filetype = 'TXT' OR filetype = 'XML') AND file IS NULL";


$sql = "SELECT Package.year,fi.* FROM (SELECT ID,ContentID,url,filetype FROM Files WHERE (filetype = 'TXT' OR filetype = 'XML') AND file IS NULL) as fi, ContentPages, Package WHERE fi.ContentID = ContentPages.ID AND ContentPages.PackageID = Package.ID AND Package.year = 2010 LIMIT 100;";

$sql = "SELECT Package.year,fi.* FROM (SELECT ID,ContentID,url,filetype FROM Files WHERE (filetype = 'TXT' OR filetype = 'XML')) as fi, ContentPages, Package WHERE fi.ContentID = ContentPages.ID AND ContentPages.PackageID = Package.ID AND Package.year = 2011;";
$res = mysql_query($sql);

while($f = mysql_fetch_assoc($res)) {
	echo $f['ID']." - ".$f['url']."\n";
	usleep(200000);
	$data = file_get_contents($f['url']);
	$sql2 = "UPDATE Files SET file = '".mysql_real_escape_string($data)."' WHERE  ID = ".$f['ID'].";";
	$res2 = mysql_query($sql2);

	$handle=fopen("data/".$f['ID'].".".strtolower($f['filetype']),'w');
	fwrite($handle,$data);
	fclose($handle);
}



?>
