from model import Logistic
import torch
import tenseal as ts
from transmission.utils import flatten_tensors, unflatten_tensors
import collections
import numpy as np
import copy

# torch.manual_seed(1234)
# x = torch.tensor([[2., 1.], [1., 1.], [1., 1.]])
# y = torch.tensor([1, 0, 1]).to(torch.float)
# model = LRModel(n_f=2)
# optimizer = torch.optim.Adam(model.parameters())

# print(model.state_dict())
# print(x)
# print(model.linear.weight.shape)
# print(x.shape)
# print(x @ model.linear.weight.T + model.linear.bias)
# print(model(x))
# loss_f = torch.nn.BCELoss()
# y_pred = model(x)
# loss = loss_f(y_pred, y.unsqueeze(dim=1))
# loss.backward()
# optimizer.step()
# print(optimizer.state, '\n')
# param_list = []
# for group in optimizer.param_groups:
#     for p in group['params']:
#         with torch.no_grad():
#             p.mul_(0.5)
#             param_list.append(p)
#
# flat_tensor = flatten_tensors(param_list)
# received_list = (flat_tensor * 4).tolist()
# print(received_list, '\n')
# received_tensor = torch.tensor(received_list)
# for f, t in zip(unflatten_tensors(received_tensor, param_list), param_list):
#     with torch.no_grad():
#         t.set_(f)
#
# # print(model.state_dict())
# print(optimizer.state, '\n')
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
# index = np.random.choice(5,4, p=[0.1,0.1,0.3,0.2,0.3])
# index = sorted(index.tolist())
# print(index)
# select_clients = []
# select_index = []
# repeated_times = []
# clients=['a','b','c','d','e']
#
# for i in index:
#     if i not in select_index:
#         select_clients.append(clients[i])
#         select_index.append(i)
#         repeated_times.append(1)
#     else:
#         repeated_times[-1] += 1
# print(select_clients)
# print(repeated_times)
#
# print(torch.randint(low=1,high=100,size=(10,2)))
# print(torch.randint(low=0,high=2,size=(10,)))

y_pred = torch.tensor([[4.3913, -1.4485],
                       [3.2421, -1.6527],
                       [-11.3252, -0.7763],
                       [5.3851, -3.3057],
                       [-6.7641, -1.0049],
                       [4.1136, -3.7467],
                       [-7.7996, -0.6339],
                       [6.0476, -3.2254]])
print(torch.softmax(y_pred, dim=1).argmax(dim=1))
y = torch.tensor([0, 0, 1, 0, 1, 0, 1, 0])
print(y_pred.argmax(dim=1).eq(y))
