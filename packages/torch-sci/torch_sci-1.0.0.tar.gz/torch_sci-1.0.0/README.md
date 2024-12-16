# torch-sci

![Test](https://github.com/github/docs/actions/workflows/test.yml/badge.svg)

Differentiable PyTorch functions to calculate scientific notation.

## Installation

Bring your own PyTorch, then install this package:

```bash
pip install torch-sci
```

## Usage

```python
import torch

import torch_sci


x = torch.tensor(1234.0, requires_grad=True)
sig, exp = torch_sci.to_sci(x)
sig, exp
# => tensors: 1.234, 3.0

# some made up loss function, to test differentiability
loss = sig * exp
loss.backward()
assert x.grad != 0.0

torch_sci.from_sci(sig, exp)
# => tensor: 1234

# more test cases
torch_sci.to_sci(torch.tensor(-1234.0, requires_grad=True))
# => -1.234, 3
torch_sci.to_sci(torch.tensor(-0.1234, requires_grad=True))
# => -1.234, -1
torch_sci.to_sci(torch.tensor(0.0, requires_grad=True))
# => 0, -8 (common trick of + 1e-8 to avoid log 0)
torch_sci.to_sci(torch.tensor(0.1234, requires_grad=True))
# => 1.234, -1
torch_sci.to_sci(torch.tensor(1234.0, requires_grad=True))
# => 1.234, 3
```

## Development

### Setup

[Install uv](https://docs.astral.sh/uv/getting-started/installation/) for dependency management if you haven't already. Then run:

```bash
# setup virtualenv
venv sync
```

### Unit Tests

```bash
uv run pytest
```
