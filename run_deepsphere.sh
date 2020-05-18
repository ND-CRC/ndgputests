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

# Setup DeepSphere package in local mode
pushd /scratch365/$(whoami)
if [ ! -d DeepSphere ]; then
       git clone https://github.com/NDCMS/DeepSphere/
fi
popd

echo 
echo "- Executing DeepSphere example"
python3 deepsphere.py 2>&1

exitcode=$?
exit $exitcode

#echo
#echo ------ ENVIRONMENT ----
#env
