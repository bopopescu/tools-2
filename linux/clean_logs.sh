#!/bin/sh

function current_df()
{
	df -h
}

function clean_logs()
{

	# /var/log
	cd /var/log
	echo "cleaning /var/log"
	ls | grep "tsar.data." | xargs -i rm -rf {}
	ls | grep "cron-" | xargs -i rm -rf {}
	ls | grep "dracut.log-" | xargs -i rm -rf {}
	ls | grep "maillog-" | xargs -i rm -rf {}
	ls | grep "messages-" | xargs -i rm -rf {}
	ls | grep "secure-" | xargs -i rm -rf {}
	ls | grep "spooler-" | xargs -i rm -rf {}
	ls | grep "yum.log-" | xargs -i rm -rf {}
	ls | grep "goagent.log-" | xargs -i rm -rf {}
	cd -

	# /var/log/sa
	cd /var/log/sa
	echo "cleaning /var/log/sa"
	ls | grep 'sa[1-9]' | xargs -i rm -rf {}
	ls | grep 'sar[1-9]' | xargs -i rm -rf {}
	cd -

	# /var/log/httpd
	cd /var/log/httpd
	echo "cleaning /var/log/httpd"
	ls | grep 'dashang-access_log-' | xargs -i rm -rf {}
	ls | grep 'dashang-error_log-' | xargs -i rm -rf {}
	ls | grep 'access_log-' | xargs -i rm -rf {}
	ls | grep 'error_log-' | xargs -i rm -rf {}
	ls | grep 'ddns.log-' | xargs -i rm -rf {}
	ls | grep 'www-access_log-' | xargs -i rm -rf {}
	ls | grep 'www-error_log-' | xargs -i rm -rf {}
	cd -
	
	# /usr/local/sa/agent/log/
	cd /usr/local/sa/agent/log/
	echo "cleaning /usr/local/sa/agent/log"
	ls | grep ".log." | xargs -i rm -rf {}
	cd -

	cd /usr/local/sa/agent/plugins
	echo "cleaning /usr/local/sa/agent/plugins"
	ls | grep ".log." | xargs -i rm -rf {}
	cd -

	# /usr/local/agenttools/agent
	cd /usr/local/agenttools/agent
	echo "cleaning /usr/local/agenttools/agent"
	ls | grep '[0-9].log' | xargs -i rm -rf {}
	cd -

	# /usr/local/TsysAgent/bin/monlog.log
	echo "cleaning /usr/local/TsysAgent/bin/monlog.log"
	echo "" > /usr/local/TsysAgent/bin/monlog.log

	# /usr/local/ats/var/log/trafficserver 	
	cd /usr/local/ats/var/log/trafficserver
	echo "cleaning /usr/local/ats/var/log/trafficserver"
	ls | grep "access.log_" | xargs -i rm -rf {}
	ls | grep "error.log_" | xargs -i rm -rf {}
	ls | grep "squid.blog_" | xargs -i rm -rf {}
	cd -

	# /usr/local/qcloud/monitor/barad/log
	cd /usr/local/qcloud/monitor/barad/log
	echo "cleaning /usr/local/qcloud/monitor/barad/log"
	ls | grep "dispatcher.log." | xargs -i rm -rf {}
	ls | grep "executor.log." | xargs -i rm -rf {}
	cd -

	# /usr/local/nginx/logs (not use)
}

function main()
{
	current_df
	clean_logs
	current_df
}

main

