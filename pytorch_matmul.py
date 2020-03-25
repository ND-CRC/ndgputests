#! /bin/env python
# simple example to show the matrix multiplication using torch

import torch

print("--- Debug information ---")
print("- torch version: {version}".format(version=torch.__version__))
print("- GPU information:")
if torch.cuda.is_available():
    print("-- CUDA Available: True")
    print("-- Number of devices: {0}".format(torch.cuda.device_count()))
    print("-- CUDA Device Name: {0}".format(torch.cuda.get_device_name(0)))
    print("-- Current CUDA device: {0}".format(torch.cuda.current_device()))
else:
    print("- No CUDA devices available. Torch will use CPU instead")
print("------")

device = torch.device('cuda:{0}'.format(torch.cuda.current_device()) if torch.cuda.is_available() else 'cpu')

matrix1 = torch.tensor([[1.0,2.0],[3.0,4.0]]).to(device)
matrix2 = matrix1.inverse()
product = torch.matmul(matrix1, matrix2)
print("result of matrix multiplication")
print("===============================")
print(product)
print("===============================")
