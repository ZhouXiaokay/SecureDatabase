from torch.multiprocessing import Process
from conf import args_parser
from data_modeling.trainer import LogisticTrainer
import torch
from data_modeling.data_loader import MysqlDataSet


def run(arg):
    cols_list = ['fixed acidity', 'volatile acidity', 'citric acid',
                 'residual sugar', 'chlorides', 'free sulfur dioxide',
                 'total sulfur dioxide', 'density', 'pH', 'sulphates', 'alcohol',
                 'color']
    mysql_dataset_2 = MysqlDataSet("database_2", "wine_quality", cols_list)
    lr_trainer = LogisticTrainer(arg, mysql_dataset_2)
    for rnd in range(args.rounds):
        print("round: ", rnd)
        update_flag = lr_trainer.is_update()
        print(update_flag)
        if update_flag:
            lr_trainer.one_local_round()
        else:
            print("not participate in this round")
        # print(rnd, logistic_trainer.model.linear.bias, '\n')


if __name__ == '__main__':
    args = args_parser()
    args.rank = 1
    processes = []
    # for rank in range(2):
    #     p = Process(target=run, args=args)
    #     processes.append(p)
    #     p.start()
    # for p in processes:
    #     p.join()
    run(args)
