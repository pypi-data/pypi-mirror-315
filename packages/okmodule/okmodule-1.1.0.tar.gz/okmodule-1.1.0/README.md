# okmodule: a very simple modular implementation

## Installation

```shell
pip install okmodule
```

## Usage

### Module

```python
from okmodule import Module


class MyModule(Module):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def main(self):
        self.log(f'Calculating, x = {self.x}, y = {self.y}')
        return self.x + self.y


result1 = MyModule(1, 2)()  # invoke directly
my_module = MyModule(3, 4)  # create Module object
result2 = my_module()  # invoke module
```

### Command

```python
from okmodule import Option, Flag, Command


class Blastn(Command):
    query = Option('-query')
    db = Option('-db')
    outfmt = Option('-outfmt')
    num_threads = Option('-num_threads')
    out = Option('-out')
    help = Flag('-help')

# show help message
Blastn(help=True)()

# invoke blastn
blastn = Blastn(query='test/query.fa', db='test/db/test', outfmt=6, num_threads=6, out='test/result.txt')
blastn()
```
