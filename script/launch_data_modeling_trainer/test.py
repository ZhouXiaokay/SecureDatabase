from torch.multiprocessing import Process
from conf import args_parser
from data_modeling.trainer import LRTrainer

def run(arg):
    lr_trainer = LRTrainer(arg)
    for rnd in range(args.rounds):
        lr_trainer.one_round()
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
