from model import LRModel
import torch
import tenseal as ts
from transmission.utils import flatten_tensors, unflatten_tensors
import collections
import numpy as np
sk_ctx_bytes = open('../transmission/ts_ckks.config', 'rb').read()
ctx = ts.context_from(sk_ctx_bytes)
torch.manual_seed(1234)
x = torch.tensor([[2., 1.], [1., 1.], [1., 1.]])
y = torch.tensor([1, 0, 1]).to(torch.float)
model = LRModel(n_f=2)
optimizer = torch.optim.Adam(model.parameters())
# print(model.state_dict())
# print(x)
# print(model.linear.weight.shape)
# print(x.shape)
# print(x @ model.linear.weight.T + model.linear.bias)
# print(model(x))
loss_f = torch.nn.BCELoss()
y_pred = model(x)
loss = loss_f(y_pred, y.unsqueeze(dim=1))
loss.backward()
optimizer.step()
print(optimizer.state, '\n')
param_list = []
for group in optimizer.param_groups:
    for p in group['params']:
        with torch.no_grad():
            p.mul_(0.5)
            param_list.append(p)

flat_tensor = flatten_tensors(param_list)
received_list = (flat_tensor * 4).tolist()
print(received_list, '\n')
received_tensor = torch.tensor(received_list)
for f, t in zip(unflatten_tensors(received_tensor, param_list), param_list):
    with torch.no_grad():
        t.set_(f)

# print(model.state_dict())
print(optimizer.state, '\n')
# uf_t = torch.cat([t.unsqueeze(dim=0) for t in uf], dim=0)
# for t in uf:
#     print(t.unsqueeze(dim=0))
# print(uf_t)
# for group in optimizer.param_groups:
#     for p in group['params']:
#         param_state = optimizer.state[p]
#         param_state['old_init'] = torch.clone(p.data).detach()
#
# print(optimizer.state)

print(np.random.random([100,10]))