<?php

if(!defined('NUM_ROOT_PATH'))
{
    header("HTTP/1.1 403 Forbidden");
    exit();
}


class MysqlDB
{
    public $mysqli;

    function __construct()
    {
    }

    function open($host, $usr, $passwd, $db)
    {
        $this->mysqli = new mysqli($host, $usr, $passwd, $db);
    }

    function close()
    {
        $this->mysqli->close();
    }

    function exec_sql_file($sql_file)
    {
        $commands = file_get_contents($sql_file);
        return $this->mysqli->multi_query($commands);
    }

	/*
	 *	$qq['qun']
	 *	$qq['no']
	 */
    function add_qq_num($qq)
	{
		if($qq['no'] == '') return;
		// find if already has it.
		$sql = "select count(id) as n from qq_no where qq_qun = '".$qq['qun']."' and qq_no = '".$qq['no']."';";
		if($result = $this->mysqli->query($sql))
        {
            $row = $result->fetch_array(MYSQLI_ASSOC);
            //var_dump($row);
			if($row['n'] > 0) return false;
		}
		//echo $sql."\n";
		//return;

		// insert
		$sql =  "INSERT INTO qq_no (qq_qun, qq_no) ".
				"VALUES ('".$qq['qun']."', '".$qq['no']."');";
		//echo "$sql\n";
		//return;
		if($this->mysqli->query($sql) == false)
        {
            return false;
        }
        return $this->mysqli->insert_id;
	}
}
