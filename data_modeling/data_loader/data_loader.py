from torch.utils.data import Dataset, DataLoader


class MysqlDataSet(Dataset):
    def __init__(self,db_conn):
        self.conn = db_conn

