from transmission.utils import flatten_tensors, unflatten_tensors
from conf import args_parser
import torch.nn
import sys

sys.path.append("../../../")
from data_modeling.client import Client

from data_modeling.data_loader import MysqlDataSet
import sklearn
import numpy as np
from torch.utils.data.sampler import SubsetRandomSampler


class BaseTrainer(object):

    def __init__(self, args, dataset):
        self.args = args

        # initialize settings
        self.sample_num = args.sample_num
        self.n_f = self.args.n_features
        self.epoch = self.args.epoch
        self.batch_size = self.args.batch_size
        self.dataset = dataset
        self.train_split = 0.7
        self.shuffle_dataset = True
        self.random_seed =  self.args.seed
        self.train_sampler, self.test_sampler = self.split_train_test()

        # initialize model and optimizer
        # self.model = Logistic(n_f=self.n_f)
        # self.optimizer = optim.Adam(self.model.parameters(), lr= self.args.lr)
        # self.criterion = torch.nn.BCELoss()
        self.model = None
        self.optimizer = None
        self.criterion = None

        # initialize the communication params with server
        self.max_msg_size = 900000000
        self.options = [('grpc.max_send_message_length', self.max_msg_size),
                        ('grpc.max_receive_message_length', self.max_msg_size)]

        self.server_address = args.server_address
        self.client = Client(self.server_address, args.rank, self.sample_num, args.ctx_file)

    def split_train_test(self):
        dataset_size = len(self.dataset)
        indices = list(range(dataset_size))
        split = int(np.floor(self.train_split * dataset_size))
        if self.shuffle_dataset:
            np.random.seed(self.random_seed)
            np.random.shuffle(indices)
        train_indices, test_indices = indices[:split], indices[split:]
        train_sampler = SubsetRandomSampler(train_indices)
        test_sampler = SubsetRandomSampler(test_indices)
        return train_sampler, test_sampler

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
    def one_local_round(self):
        raise NotImplementedError

    def test(self):
        raise NotImplementedError

    def launch(self):
        for rnd in range(self.args.rounds):
            print("round: ", rnd)
            update_flag = self.is_update()
            print(update_flag)
            if update_flag:
                self.one_local_round()
            else:
                print("not participate in this round")


if __name__ == '__main__':
    arg = args_parser()
    # trainer = BaseTrainer(arg)
    # logistic_trainer.one_round()
