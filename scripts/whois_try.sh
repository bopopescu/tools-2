#!/bin/sh

#
# $1: domain
#
function whois_try()
{
	domain=$1
	cmd="/usr/bin/whois $domain -h whois.nic.xyz"
	$cmd
	ret=`$cmd | grep -i 'Domain Name:'`
	echo $ret
	if [ "SS$ret" == "SS" ]; then
		return 0
	else
		return 1
	fi

	sleep 2
}

function char2()
{
	for x in {a..z}
	do
		domain="$x.xyz"
		whois_try $domain
		ret=$?
		echo "$ret $domain"

		for y in {a..z}
		do
			domain="$x$y.xyz"
			whois_try $domain
			ret=$?
			echo "$ret $domain"
		done
		#return 0
	done
}

function int2()
{
	for x in {0..9}
	do
		domain="$x.xyz"
		whois_try $domain
		ret=$?
		echo "$ret $domain"

		for y in {0..9}
		do
			domain="$x$y.xyz"
			whois_try $domain
			ret=$?
			echo "$ret $domain"
		done
		#return 0
	done
}

function main()
{
	echo "in main"
	whois_try "85.xyz"
	ret=$?
	echo $ret
	return 1

	int2
	char2
	return 1

	echo "in main"
	whois_try "abc.xyz"
	ret=$?
	echo $ret
}

main

