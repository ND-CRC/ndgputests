#! /bin/bash

date
hostname
printf "User:" ; whoami
printf "Initial path: "; pwd

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
if command -v nvidia-smi; then
    echo "- Nvidia info:"
    nvidia-smi
fi

echo 
echo "- Executing python JAX matrix multiplication example"
# Note we need to invoke python 3.6, since 3.5 is not supported.
python3.6 jax_matmul.py 2>&1

exitcode=$?
exit $exitcode

#echo
#echo ------ ENVIRONMENT ----
#env
