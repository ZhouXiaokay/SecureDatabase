from conf import args_parser
import torch.nn
from data_modeling.model import Logistic
import sys
import torch.optim as optim
from data_modeling.trainer.base_trainer import BaseTrainer
from torch.utils.data import DataLoader

sys.path.append("../../../")


class LogisticTrainer(BaseTrainer):
    def __init__(self, args, dataset):
        super().__init__(args, dataset)
        self.model = Logistic(n_f=self.n_f)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.args.lr)
        self.criterion = torch.nn.BCELoss()

    def one_local_round(self):
        data_loader = DataLoader(self.dataset, batch_size=self.batch_size, sampler=self.train_sampler)
        for e in range(self.epoch):
            accum_loss = 0
            accum_correct = 0
            set_size = 0

            for batch in data_loader:
                train_x, train_y = batch
                train_y = train_y.unsqueeze(dim=1)

                y_pred = self.model(train_x)
                loss = self.criterion(y_pred, train_y)
                accum_loss += loss.item()

                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
                set_size += train_x.size(0)
                accum_correct += y_pred.ge(0.5).squeeze().eq(train_y.squeeze()).sum().item()
            if e % 2 == 0:
                print("loss: ", accum_loss)
                print("train accuracy: ", accum_correct / set_size)
        self.average_params()

    def test(self):
        data_loader = DataLoader(self.dataset, batch_size=self.batch_size, sampler=self.test_sampler)
        accum_correct = 0
        set_size = 0
        for batch in data_loader:
            test_x, test_y = batch
            test_y = test_y.unsqueeze(dim=1)
            y_pred = self.model(test_x)
            set_size += test_x.size(0)
            accum_correct += y_pred.ge(0.5).squeeze().eq(test_y.squeeze()).sum().item()
        print("test accuracy: ", accum_correct / set_size)


if __name__ == '__main__':
    args = args_parser()
    # lr_trainer = LogisticTrainer(args)
    # logistic_trainer.one_round()
