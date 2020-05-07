#! /bin/env python3.6
import jax
import jax.numpy as np
from jax import grad, jit, vmap
from jax import random

print("-----GPU devices information-----")
print(jax.devices())
print("GPU host id: {0}".format(jax.host_id(backend="gpu")))
print("---------------------------------")

key = random.PRNGKey(0)
size = 3000
print("Generate a random matrix")
x = random.normal(key, (size, size), dtype=np.float32)
print(x)
print("Multiply by its transpose:")
print("result of matrix multiplication")
print("=================================")
# Run on the GPU
res = np.dot(x, x.T).block_until_ready()
print(res)
