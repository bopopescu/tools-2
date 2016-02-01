#!/bin/sh

curl -L -x "192.168.0.96:8087" --cacert "/home/hua/bin/goagent-3.2.3/local/CA.crt" "https://www.google.com/"

