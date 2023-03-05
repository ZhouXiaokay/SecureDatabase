from torch.multiprocessing import Process
from conf import args_parser
from data_modeling.trainer.logistic_trainer import LogisticTrainer
import torch
from data_modeling.data_loader import MysqlDataSet


def run(arg):
    cols_list = ['fixed acidity', 'volatile acidity', 'citric acid',
                 'residual sugar', 'chlorides', 'free sulfur dioxide',
                 'total sulfur dioxide', 'density', 'pH', 'sulphates', 'alcohol',
                 'color']
    mysql_dataset_1 = MysqlDataSet("database_1", "wine_quality", cols_list)
    lr_trainer = LogisticTrainer(arg, mysql_dataset_1)

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
    processes = []
    # for rank in range(2):
    #     p = Process(target=run, args=args)
    #     processes.append(p)
    #     p.start()
    # for p in processes:
    #     p.join()
    run(args)

# def run(arg, rank):
#     arg.rank = rank
#     cols_list = ['fixed acidity', 'volatile acidity', 'citric acid',
#                  'residual sugar', 'chlorides', 'free sulfur dioxide',
#                  'total sulfur dioxide', 'density', 'pH', 'sulphates', 'alcohol',
#                  'color']
#     mysql_dataset = MysqlDataSet("database_{0}".format(rank+1), "wine_quality", cols_list)
#     lr_trainer = LogisticTrainer(arg, mysql_dataset)
#     lr_trainer.launch()
#
#
# if __name__ == '__main__':
#     args = args_parser()
#     processes = []
#     for i in range(3):
#         p = Process(target=run, args=(args, i))
#         processes.append(p)
#         p.start()
#     for p in processes:
#         p.join()
