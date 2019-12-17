import torch
import functools
import sys


def patch(model, name=None):
    if name is None:
        name = type(model).__name__
    else:
        name = name + ': ' + type(model).__name__
    old_forward = type(model).forward

    def wrap_with_name(_name=name, _model=model):

        @functools.wraps(old_forward)
        def wrapped_forward(*args, **kwargs):
            torch.cuda.nvtx.range_push(_name)
            result = old_forward(_model, *args, **kwargs)
            torch.cuda.nvtx.range_pop()
            return result

        return wrapped_forward

    model.forward = wrap_with_name()

    for name, child in model.named_children():
        patch(child, name)

    return model


sys.modules[__name__] = patch
