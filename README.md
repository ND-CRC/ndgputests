# CAML-ND GPU Tests


In order to use CAML resources, we require defining singularity images on PATHs. E.g.: Via cvmfs.

The following Notre Dame image (available via CVMFS) supports TensorFlow, Keras and PyTorch:

```
/cvmfs/singularity.opensciencegrid.org/notredamedulac/el7-tensorflow-pytorch:latest
```
is built from: https://github.com/NDCMS/el7-tensorflow-gpu

## Setting up this tutorial examples

Once you log in into camlnd.crc.nd.edu, type: 

```
cd /scratch365/$USER
git clone https://github.com/khurtado/ndgputests
cd ndgputests
```
Then, follow one or both of the examples below.

### Tensorflow example

```
$ condor_submit submit_tensorflow.jdl
```
Output example:
```
  - Executing python TensorFlow matrix multiplication example
  2020-03-25 13:18:29.845113: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compil    ed to use: AVX2 AVX512F FMA
  2020-03-25 13:18:30.004982: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1432] Found device 0 with properties:
  name: Quadro RTX 6000 major: 7 minor: 5 memoryClockRate(GHz): 1.62
  pciBusID: 0000:2f:00.0
  totalMemory: 22.17GiB freeMemory: 22.00GiB
  2020-03-25 13:18:30.005161: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1511] Adding visible gpu devices: 0
  2020-03-25 13:18:30.570670: I tensorflow/core/common_runtime/gpu/gpu_device.cc:982] Device interconnect StreamExecutor with strength 1 edge matrix:
  2020-03-25 13:18:30.570757: I tensorflow/core/common_runtime/gpu/gpu_device.cc:988]      0
  2020-03-25 13:18:30.570794: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1001] 0:   N
  2020-03-25 13:18:30.570954: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1115] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU    :0 with 21320 MB memory) -> physical GPU (device: 0, name: Quadro RTX 6000, pci bus id: 0000:2f:00.0, compute capability: 7.5)
  result of matrix multiplication
  ===============================
  [[ 1.0000000e+00  0.0000000e+00]
   [-4.7683716e-07  1.0000002e+00]]
  ===============================
 ```

### Pytorch example

```
$ condor_submit submit_pytorch.jdl
```
Output example:
```
  - Executing python torch matrix multiplication example
  --- Debug information ---
  - torch version: 1.4.0
  - GPU information:
  -- CUDA Available: True
  -- Number of devices: 1
  -- CUDA Device Name: Quadro RTX 6000
  -- Current CUDA device: 0
  ------
  result of matrix multiplication
  ===============================
  tensor([[ 1.0000e+00,  0.0000e+00],
          [-4.7684e-07,  1.0000e+00]], device='cuda:0')
 ```

## Amber example:

```
$ condor_submit submit_amber.jdl
```
Output example:
```

```
