#! /bin/bash

### Output for Debugging
date
hostname
printf "User:" ; whoami
echo "- Initial directory:"
pwd

echo
echo "- OS Release:"
if [ -f /etc/redhat-release ]; then
  cat /etc/redhat-release
elif [ -f /etc/issue ]; then
  cat /etc/issue
else
  echo "OS not known"
fi

if command -v nvidia-smi; then
    echo "- Nvidia info:"
    nvidia-smi
fi

### end of Debugging
echo "- Entering scratch365 submit directory"
cd $_CONDOR_JOB_IWD
echo "- Executing pmemd.cuda"
pmemd.cuda -O -i amber_inputs/mdin.GPU -o mdout -p amber_inputs/prmtop -c amber_inputs/inpcrd
exitcode=$?

if [ "x$exitcode" != "x0" ]; then
    echo "- Error executing amber job."
else
    echo "- Amber job is completed."
fi
echo "- Exit code: $exitcode"
exit $exitcode
