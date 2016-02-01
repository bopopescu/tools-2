<?php 

define('NUM_ROOT_PATH', './');
require_once("db.php");

enter();
function enter()
{
	$param = $_POST['no'];
	//echo $param."\n";

	$db_host     = "";
    $db_user     = "";
    $db_password = "";
    $db_name     = "";

    $handle = new MysqlDB();
    $handle->open($db_host, $db_user, $db_password, $db_name);

	$items = explode(';', $param);
	$total = 0;
	$success = 0;
	foreach( $items as $i ){
		$tmp = explode(':', $i);
		if(count($tmp) != 2) continue;
		$total++;
		$qq['qun'] = $tmp[0];
		$qq['no'] = $tmp[1];
		if(check_number_valid($qq['qun']) == true and check_number_valid($qq['no']) == true){
			if($handle->add_qq_num($qq) != false){
				$success++;
			}
		}
	}
	echo "{total:$total;success:$success;}";
}

//init();
function init()
{
	$db_host     = "127.0.0.1";
    $db_user     = "root";
    $db_password = "123456";
    $db_name     = "qqnum";

    $handle = new MysqlDB();
    $handle->open($db_host, $db_user, $db_password, $db_name);
	$handle->exec_sql_file("qqnum.sql");
}

function check_number_valid($no)
{
	$len = strlen($no);
	//echo "length of '$no': $len\n";
	if($len < 5 or $len > 12) return false;
	for($i = 0; $i < $len; $i++)
	{
		if($no[$i] < '0' or $no[$i] > '9'){
			return false;
		}
	}
	return true;
}
?>
