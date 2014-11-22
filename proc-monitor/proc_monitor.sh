# !/bin/sh

function run()
{
	cfgfile="proc.config";
	cat $cfgfile | while read line
	do
		if [ ${#line} -ge 1 -a "${line:0:1}x" != "#x" ]; then # 去掉空行和注释行
			#echo "LINE: $line";	
			i=0;
			proc="";
			cmd="";
			for item in $line; # 提取进程名和启动进程的命令
			do
				if [ $i -eq 0 ]; then
					proc=$item;
				else
					cmd="$cmd$item ";
				fi
				((i=$i+1));
				#echo $item;
				#echo $i;
			done
			#echo "name: $proc, cmd: $cmd";
			#$cmd; 
			#proc_test_cmd="ps auxf";
			proc_test=`ps auxf | grep $proc | grep -v grep`;
			if [ ${#proc_test} -le 2 ]; then
				echo $proc_test;
				$cmd; 
			fi
		fi
	done
}

run;
