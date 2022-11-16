from conf import args_parser
import torch.nn
from data_modeling.model import Linear
import sys
import torch.optim as optim
from data_modeling.trainer.base_trainer import BaseTrainer
from torch.utils.data import DataLoader
import numpy as np

sys.path.append("../../../")


class LinearTrainer(BaseTrainer):
    def __init__(self, args, dataset):
        super().__init__(args, dataset)
        self.model = Linear(n_f=self.n_f)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.args.lr)
        self.criterion = torch.nn.MSELoss()

    def one_local_round(self):
        data_loader = DataLoader(self.dataset, batch_size=self.batch_size, sampler=self.train_sampler)
        mse_f = torch.nn.MSELoss(reduction='sum')
        for e in range(self.epoch):
            accum_loss = 0
            size_set = 0
            mse_loss = 0
            for batch in data_loader:
                train_x, train_y = batch
                train_y = train_y.unsqueeze(dim=1)

                y_pred = self.model(train_x)
                loss = self.criterion(y_pred, train_y)
                accum_loss += loss.item()
                size_set += train_x.size(0)

                mse_loss += mse_f(y_pred, train_y).item()

                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

            if e == 4:
                print("loss: ", accum_loss)
                print("RMSE: ", np.sqrt(mse_loss / size_set))
                print(size_set)
        self.average_params()

    def test(self):
        data_loader = DataLoader(self.dataset, batch_size=self.batch_size, sampler=self.test_sampler)
        accum_mse = 0
        size_set = 0
        mse_f = torch.nn.MSELoss(reduction='sum')
        for batch in data_loader:
            test_x, test_y = batch
            test_y = test_y.unsqueeze(dim=1)
            y_pred = self.model(test_x)
            accum_mse += mse_f(y_pred, test_y).item()
            size_set += test_x.size(0)
        print("test-set RMSE: ", np.sqrt(accum_mse / size_set))


if __name__ == '__main__':
    arg = args_parser()
    # lr_trainer = LogisticTrainer(args)
    # logistic_trainer.one_round()
