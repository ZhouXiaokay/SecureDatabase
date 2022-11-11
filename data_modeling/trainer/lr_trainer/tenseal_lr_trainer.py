from transmission.utils import flatten_tensors, unflatten_tensors
from conf import args_parser
import torch.nn
from data_modeling.model import LRModel
import sys
import torch.optim as optim

sys.path.append("../../../")
from data_modeling.client import Client


class LRTrainer(object):

    def __init__(self, args):
        self.args = args

        # initialize logistic model, optimizer:Adam
        self.sample_num = args.sample_num
        self.n_f = self.args.n_features
        self.model = LRModel(n_f=self.n_f)
        self.optimizer = optim.Adam(self.model.parameters())
        self.criterion = torch.nn.BCELoss()

        # initialize the communication params with server
        self.max_msg_size = 900000000
        self.options = [('grpc.max_send_message_length', self.max_msg_size),
                        ('grpc.max_receive_message_length', self.max_msg_size)]

        self.server_address = args.server_address
        self.client = Client(self.server_address, args.rank, self.sample_num, args.ctx_file)

    # send model params to server, and get the sum params
    def transmit(self, params_list):
        flat_tensor = flatten_tensors(params_list).detach()
        # get the average params from server
        received_list = self.client.transmit(flat_tensor)
        received_tensors = torch.tensor(received_list, dtype=flat_tensor.dtype, device=flat_tensor.device)

        return received_tensors

    def is_update(self):
        flag, init_params_list = self.client.transmit([], operator="update_flag")
        if flag:
            params_list = self.get_params_list()
            init_params_tensor = torch.tensor(init_params_list)
            for f, t in zip(unflatten_tensors(init_params_tensor, params_list), params_list):
                with torch.no_grad():
                    t.set_(f)
        return flag

    # from optimizer get the model params,return a list
    def get_params_list(self):
        param_list = []
        for group in self.optimizer.param_groups:
            for p in group['params']:
                with torch.no_grad():
                    p.mul_(self.sample_num)
                    param_list.append(p)

        return param_list

    # update the model params with average params
    def average_params(self):
        params_list = self.get_params_list()
        average_params = self.transmit(params_list)
        # set average params as the new params
        for f, t in zip(unflatten_tensors(average_params, params_list), params_list):
            with torch.no_grad():
                t.set_(f)

    # one communication round
    # def one_round(self, n_epoch, data_loader):
    #     for epoch in range(n_epoch):
    #         for batch in data_loader:
    #             train_x, train_y = batch
    #             y_pred = self.model(train_x)
    #             self.optimizer.zero_grad()
    #             loss = self.criterion(y_pred, train_y)
    #             loss.backward()
    #             self.optimizer.step()
    #     self.average_params()

    def one_round(self,x,y):
        print("init", self.model.linear.bias)
        for i in range(10):
            y_pred = self.model(x)
            loss_f = torch.nn.BCELoss()
            loss = loss_f(y_pred, y.unsqueeze(dim=1))
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
        print("before", self.model.linear.bias)
        self.average_params()
        print("after", self.model.linear.bias, '\n')


if __name__ == '__main__':
    args = args_parser()
    lr_trainer = LRTrainer(args)
    # lr_trainer.one_round()
