import torch


def floor_ste(x):
    '''Use straight-through estimator for differentiable approximation of floor function'''
    return x.floor() - (x - x.detach())


def exponent(x):
    '''Calculate the exponent in scientific notation; differentiable. E.g. exponent(1234) = 3.0'''
    log10_abs_x = (x + 1e-8).abs().log10()
    return floor_ste(log10_abs_x)


def significand(x, exponent):
    '''Calculate the significand in scientific notation. Differentiable'''
    return x / torch.pow(10.0, exponent)


def to_sci(x):
    '''Turn a number into scientific notation - exponent and significand. Differentiable'''
    exp = exponent(x)
    sig = significand(x, exp)
    return sig, exp


def from_sci(significand, exponent):
    '''Calculate the number from scientific notation exponent and significant. Differentiable.'''
    return significand * (10 ** exponent)
