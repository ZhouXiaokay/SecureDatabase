import torch
from torch import nn


class Linear(nn.Module):
    def __init__(self, n_f):
        super().__init__()
        self.linear = nn.Linear(n_f, 1)

    def forward(self, x):
        x = self.linear(x)

        return x
