from torch.multiprocessing import Process
from conf import args_parser
from data_modeling.trainer import LRTrainer
import torch

def run(arg):
    lr_trainer = LRTrainer(arg)
    x = torch.randint(low=1,high=100,size=(10,10)).float()
    y = torch.randint(low=0,high=2,size=(10,)).float()
    for rnd in range(args.rounds):
        print("round: ", rnd)
        update_flag= lr_trainer.is_update()
        print(update_flag)
        if update_flag:
            lr_trainer.one_round(x,y)
        else:
            print("not participate in this round")
        # print(rnd, lr_trainer.model.linear.bias, '\n')


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
