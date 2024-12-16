import pytest
import torch

import torch_sci


def test_floor_ste():
    x = torch.tensor(1.234, requires_grad=True)
    result = torch_sci.floor_ste(x)
    result.backward()

    # Check that gradient is not zero
    assert x.grad != 0.0
    # Check that floor_ste approximates the floor function
    assert torch.isclose(result, torch.tensor(1.0))


@pytest.mark.parametrize('x,res_sig,res_exp', [
    (-1234.0, -1.234, 3.0),
    (-0.1234, -1.234, -1.0),
    (0.0, 0.0, -8.0),
    (0.1234, 1.234, -1.0),
    (1234.0, 1.234, 3.0),
])
def test_exponent(x, res_sig, res_exp):
    x = torch.tensor(x, requires_grad=True)
    exp = torch_sci.exponent(x)
    exp.backward()

    # Check that gradient is not zero
    assert x.grad != 0.0
    # Check the correctness of the exponent
    assert torch.isclose(exp, torch.tensor(res_exp))


@pytest.mark.parametrize('x,res_sig,res_exp', [
    (-1234.0, -1.234, 3.0),
    (-0.1234, -1.234, -1.0),
    (0.0, 0.0, -8.0),
    (0.1234, 1.234, -1.0),
    (1234.0, 1.234, 3.0),
])
def test_significand(x, res_sig, res_exp):
    x = torch.tensor(x, requires_grad=True)
    exp = torch_sci.exponent(x)
    sig = torch_sci.significand(x, exp)
    sig.backward()

    # Check that gradient is not zero
    assert x.grad != 0.0
    # Check the correctness of the significand
    assert torch.isclose(sig, torch.tensor(res_sig))


@pytest.mark.parametrize('x,res_sig,res_exp', [
    (-1234.0, -1.234, 3.0),
    (-0.1234, -1.234, -1.0),
    (0.0, 0.0, -8.0),
    (0.1234, 1.234, -1.0),
    (1234.0, 1.234, 3.0),
])
def test_to_sci_and_from_sci(x, res_sig, res_exp):
    x = torch.tensor(x, requires_grad=True)
    sig, exp = torch_sci.to_sci(x)
    re_x = torch_sci.from_sci(sig, exp)
    re_x.backward()

    # Check differentiability
    assert x.grad != 0.0
    # Check inverse correctness
    assert torch.isclose(x, re_x)
    # Check the correctness of the significand
    assert torch.isclose(sig, torch.tensor(res_sig))
    # Check the correctness of the exponent
    assert torch.isclose(exp, torch.tensor(res_exp))
