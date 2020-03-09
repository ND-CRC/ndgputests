#! /bin/bash

date
hostname

echo
echo "- OS Release:"
if [ -f /etc/redhat-release ]; then
  cat /etc/redhat-release
elif [ -f /etc/issue ]; then
  cat /etc/issue
else
  echo "OS not known"
fi
echo
echo "- Do we have cvmfs mounted inside the container?"
echo "ls -ld /cvmfs/cms.cern.ch"
ls -ld /cvmfs/cms.cern.ch
echo
if command -v nvidia-smi; then
    echo "- Nvidia info:"
    nvidia-smi
fi

echo 
echo "- Executing python TensorFlow matrix multiplication example"
python tf_matmul.py 2>&1
