import torch
from torch.utils.data import DataLoader, IterableDataset
from data_modeling.data_loader import engine
import pandas as pd
import numpy as np
import time
import math


#
class MysqlDataSet(IterableDataset):
    def __init__(self, db_name, tb_name, cols):
        super(MysqlDataSet).__init__()
        self.db_name = db_name
        self.tb_name = tb_name
        self.cols = cols


    def __iter__(self):
        conn = engine(self.db_name)
        self.data_iter = pd.read_sql(self.tb_name, con=conn, chunksize=1, index_col=None, columns=self.cols)
        for data in self.data_iter:
            tensor = torch.from_numpy(np.array(data, dtype=np.float32).flatten())
            x, y = tensor[:-1], tensor[-1]
            yield x, y


# class MysqlDataSet(IterableDataset):
#
#     def __init__(self, file_path: str):
#         super(MysqlDataSet).__init__()
#         self.file_path = file_path
#         self.info = self._get_file_info(file_path)
#         self.start = self.info['start']
#         self.end = self.info['end']
#
#     def __iter__(self):
#         worker_info = torch.utils.data.get_worker_info()
#         if worker_info is None:  # single worker
#             iter_start = self.start
#             iter_end = self.end
#         else:  # multiple workers
#             per_worker = int(math.ceil((self.end - self.start) / float(worker_info.num_workers)))
#             worker_id = worker_info.id
#             iter_start = self.start + worker_id * per_worker
#             iter_end = min(iter_start + per_worker, self.end)
#         sample_iterator = self._sample_generator(iter_start, iter_end)
#         return sample_iterator
#
#     def __len__(self):
#         return self.end - self.start
#
#     def _get_file_info(self, file_path):
#         info = {
#             "start": 1,
#             "end": 0,
#             "id_colum": 0,
#             "article_colum": 1,
#             "summary_colum": 2
#         }
#         with open(file_path, 'r') as fin:
#             for _ in enumerate(fin):
#                 info['end'] += 1
#         return info
#
#     def _sample_generator(self, start, end):
#         id_c, art_c, sum_c = self.info['id_colum'], self.info['article_colum'], self.info['summary_colum']
#         with open(self.file_path, 'r') as fin:
#             for i, line in enumerate(fin):
#                 if i < start: continue
#                 if i >= end: return StopIteration()
#                 items = line.strip().split('\t')
#                 sample = {"id": items[id_c], "article": items[art_c], "summary": items[sum_c]}
#                 yield sample
#
#
# train_dataset = SummaryDataset(args.train_dataset)
# train_dataloader = DataLoader(train_dataset, shuffle=False, batch_size=args.batch_size, num_workers=args.num_workers)

if __name__ == "__main__":
    cols_list = ['index', 'fixed acidity', 'volatile acidity', 'citric acid',
                 'residual sugar', 'chlorides', 'free sulfur dioxide',
                 'total sulfur dioxide', 'density', 'pH', 'sulphates', 'alcohol',
                 'quality', 'color']
    mysql_dataset = MysqlDataSet("database_1", "wine_quality", cols_list)
    dataloader = DataLoader(mysql_dataset, batch_size=4, num_workers=0)
    start_time = time.time()
    for batch in dataloader:
        x, y = batch
        print(y.unsqueeze(dim=-1))
        print(x)

    end_time = time.time()
    print(end_time - start_time)
    # conn = engine("database_test")
    # data_iter = pd.read_sql("wine_quality", con=conn, chunksize=2, index_col=None, columns=cols_list)
    # for data in data_iter:
    #     data = data.values
    #     print(torch.from_numpy(data))