#!/bin/sh


function send_mail()
{
	mail=""

    subject=$1
    message=$2
    cc_to=""
	
	user=""
	passwd=""

    /usr/local/bin/sendEmail -s $mail -xu "$user" -xp "$passwd" \
        -f $user \
        -t "$cc_to" \
        -cc "$cc_to" \
        -u "$subject" \
        -m "$message"
}

function suicide()
{
	echo "$0 suicide."
	#rm -rf $0
	exit 0
}

function get_gfs_storage()
{
	#gfs_result=`gfs -dus /gdrive/resource`
	gfs_result=`gfs -ls /`
	echo $gfs_result
}

function do_task()
{
	result="task done."
	echo $result
}

function run()
{
	res=$(do_task)
	send_mail "GFS storage on `hostname`" "$res"
	suicide
}

run
