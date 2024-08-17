# Automation Toolbox
### Python · Bash · PowerShell

Placeholder for Python, Bash and PowerShell material, and other CLI snippets that I want to keep track of, for future reference and educational purposes.

 * Some of the scripts were used for Qwiklabs, Colab, and Jupyter assessments.

## Pythonic modules cheat sheet:
Multiprocessing (CPU-bound tasks):

```
from multiprocessing import Pool
```

Thread and process pool executors:

```
from concurrent import futures
```

Asynchronous I/O:

```
import asyncio

async def main():
    print('Hello ...')
    await asyncio.sleep(1)
    print('... World!')

asyncio.run(main())
```

Guppy:

```
from guppy import hpy
h = hpy()
print h.heap()
```

Beautiful Soup:

```
from bs4 import BeautifulSoup
```

MSTICPy (>v3.8, if working on local, create a virtual environment first):

```
import msticpy as mp
```

NumPy ("pip3 install matplotlib" on virtual environment):

```
import numpy as np
```

PyTorch (>v3.8, if CUDA support is needed with NVIDIA GPUs, check the Tensors documentation):

```
import torch
torch.cuda.is_available()
```

Pandas (>v3.9, use Anaconda to install the PyData stack. This includes Matplotlib, NumPy, SciPy, etc):
 * https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf

Others:

```
from memory_profiler import profile # Memory profiler
@profile # Don't forget the decorator

from tqdm import tqdm # "Te quiero demasiado" progression bars

import zimply # RIM reader, for Wikipedia
import zimply.zimply

```
