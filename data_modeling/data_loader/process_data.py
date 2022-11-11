import pandas as pd
import numpy as np
from sklearn.utils import shuffle
from sqlalchemy import create_engine


def process_wine_data(rpath, wpath, spath):
    red_df = pd.read_csv(rpath, sep=';')
    white_df = pd.read_csv(wpath, sep=';')
    color_red = pd.Series(np.repeat(0, 1599))
    color_white = pd.Series(np.repeat(1, 4898))
    red_df['color'] = color_red
    white_df['color'] = color_white

    wine_df = pd.concat([white_df, red_df], ignore_index=True)
    wine_df = shuffle(wine_df)
    wine_df.to_csv(spath, index=False)


def engine(db_name):
    engine = create_engine('mysql+pymysql://root:9966@127.0.0.1:3336/{}'.format(db_name), encoding='utf-8')
    return engine


def readFile_to_sql(db_name, csv_path):
    try:
        filename = csv_path.split('/')[-1]
        df = pd.read_csv(csv_path, encoding="utf8", sep=',', dtype={'code': str})
        table_name = filename.split('.')[0]
        df.to_sql(table_name, con=engine(db_name), if_exists='append', index=True)

    except Exception as e:
        raise e


def split_iid_data(df, size):
    df = shuffle(df)
    df_list = np.array_split(df, size)
    for i in range(size):
        spath = 'data/table_{0}.csv'.format(i + 1)
        df_list[i].to_csv(spath, index=False)


if __name__ == '__main__':
    red_wine_path = 'data/winequality-red.csv'
    white_wine_path = 'data/winequality-white.csv'
    save_path = 'data/wine_quality.csv'
    # process_wine_data(red_wine_path, white_wine_path, save_path)
    # readFile_to_sql('database_1', save_path)
    # wine_df = pd.read_csv(save_path, encoding="utf8", sep=',', dtype={'code': str})
    # # split_iid_data(wine_df, 3)
    # for i in range(3):
    #     readFile_to_sql('database_{0}'.format(i+1), 'data/wine_quality_{0}.csv'.format(i+1))
    # value_1 = np.random.randint(1, 100, (600, 1))
    # value_2 = np.random.randint(100, 1000, (600, 1))
    # query_data = np.concatenate((value_1, value_2), axis=1)
    # name = ['value_1', 'value_2']
    # df = pd.DataFrame(query_data, columns=name)
    # df.to_csv('data/table.csv', index=False)
    # readFile_to_sql('database_test', 'data/table.csv')
    df = pd.read_csv('data/table.csv')
    split_iid_data(df, 3)
    for i in range(3):
        readFile_to_sql('database_{0}'.format(i+1), 'data/table_{0}.csv'.format(i+1))
