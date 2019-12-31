import torch
import sys


def patch(model, name=None):
    if name is None:
        name = type(model).__name__
    else:
        name = name + ': ' + type(model).__name__

    def push(*args, _name=name, **kwargs):
        torch.cuda.nvtx.range_push(_name)

    def pop(*args, **kwargs):
        torch.cuda.nvtx.range_pop()

    model.register_forward_pre_hook(push)
    model.register_forward_hook(pop)

    for name, child in model.named_children():
        patch(child, name)

    return model


sys.modules[__name__] = patch
