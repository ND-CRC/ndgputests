#! /bin/bash

### Debugging
date
hostname
printf "User:" ; whoami
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

# Executing Amber
echo "- Executing pmemd.cuda"
pmemd.cuda -O -i inputs_amber/mdin.GPU -o mdout -p inputs_amber/prmtop -c inputs_amber/inpcrd
exitcode=$?

if [ "x$exitcode" != "x0" ]; then
    echo "- Error executing amber job."
else
    echo "- Amber job is completed."
fi
echo "- Exit code: $exitcode"

exit $exitcode
