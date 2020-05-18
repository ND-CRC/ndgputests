#! /bin/bash

date
hostname
printf "User:" ; whoami

echo
echo "- OS Release:"
if [ -f /etc/redhat-release ]; then
  cat /etc/redhat-release
elif [ -f /etc/issue ]; then
  cat /etc/issue
else
  echo "OS not known"
fi

current=$PWD
# Setup DeepSphere package in local mode
cd /scratch365/$(whoami)
if [ ! -d DeepSphere ]; then
       git clone https://github.com/NDCMS/DeepSphere/
fi

echo 
echo "- Executing DeepSphere example"
python3 deepSphere.py 2>&1

exitcode=$?
exit $exitcode

#echo
#echo ------ ENVIRONMENT ----
#env
