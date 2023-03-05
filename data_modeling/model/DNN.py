import torch
from torch import nn


class DNN(nn.Module):
    def __init__(self, n_f):
        super().__init__()
        self.dense_1 = nn.Linear(n_f, n_f)
        nn.init.xavier_normal_(self.dense_1.weight)
        self.dense_2 = nn.Linear(n_f, 2)
        nn.init.xavier_normal_(self.dense_2.weight)

    def forward(self, x):
        x = self.dense_1(x)
        x = torch.relu(x)
        x = self.dense_2(x)
        return x
