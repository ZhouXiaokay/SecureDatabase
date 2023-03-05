import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


# 加载数据返回dataframe
def load_data():
    data = pd.read_csv('data/agaricus-lepiota.data', index_col=False, header=None,
                       names=['target', 'x1', 'x2', 'x3', 'x4', 'x5',
                              'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12',
                              'x13', 'x14', 'x15', 'x16', 'x17', 'x18', 'x19',
                              'x20', 'x21', 'x22'])
    return data


# 特征工程：补齐缺失值对离散特征进行独热码以及对target进行label encode
def deal_feature(data):
    # 首先使用knn对特征进行补齐
    # 在此之前先将数据集进行独热码处理，否则无法使用knn
    # 需要补齐得数据
    l_data = data.loc[data['x11'].isin(['?'])]
    # 训练数据
    t_data = data.loc[data['x11'] != '?']
    # 训练数据得x
    t_x = t_data.loc[:, ['target', 'x1', 'x2', 'x3', 'x4', 'x5',
                         'x6', 'x7', 'x8', 'x9', 'x10', 'x12',
                         'x13', 'x14', 'x15', 'x16', 'x17', 'x18', 'x19',
                         'x20', 'x21', 'x22']]
    # 独热码,实际是增加了维度
    t_x = pd.get_dummies(t_x)
    # 训练得y
    t_y = t_data.loc[:, ['x11']]
    # 对目标labelencoder处理
    x11_l = LabelEncoder()
    # 处理训练集得y
    t_y = x11_l.fit_transform(t_y)
    # 需要补齐得数据，测试集
    l_x = l_data.loc[:, ['target', 'x1', 'x2', 'x3', 'x4', 'x5',
                         'x6', 'x7', 'x8', 'x9', 'x10', 'x12',
                         'x13', 'x14', 'x15', 'x16', 'x17', 'x18', 'x19',
                         'x20', 'x21', 'x22']]
    l_data = l_x
    l_x = pd.get_dummies(l_x)
    # 由于数据不随机性导致。特征值缺失，所以只能将训练集和测试集得共同特征提取出来
    f = []
    # 之对共同特征进行处理
    f = l_x.columns.intersection(t_x.columns)
    t_x = t_x.loc[:, f]
    # 首先将特征转化为独热码以及x11转化为lable
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(t_x, t_y)
    l_x = l_x.loc[:, f]
    x11 = knn.predict(l_x)
    x11 = x11_l.inverse_transform(x11)
    # 将x11放到data中
    # 形成新得dataframe
    # t_data和l_data,x11,
    l_data.insert(11, 'x11', x11)
    # data为填充好得数据
    data = pd.concat([t_data, l_data])
    # 首先对target进行类别编码
    target_le = LabelEncoder()
    y = target_le.fit_transform(data['target'].values)
    a = ['x1', 'x2', 'x3', 'x4', 'x5',
         'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12',
         'x13', 'x14', 'x15', 'x16', 'x17', 'x18', 'x19',
         'x20', 'x21', 'x22']
    # 对离散化特征独热码处理
    x = pd.get_dummies(data[a])
    return x, y


def deal_pca(data):
    pca = PCA(n_components=70)
    t_data = pca.fit_transform(data)
    return t_data


def test_L(x, y):
    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.7, random_state=2)
    # 逻辑回归。写出损失函数
    LR = LogisticRegression(C=1.0, penalty='l2', tol=0.01)
    LR.fit(x_train, y_train)
    LR.predict(x_test)
    print(LR.score(x_test, y_test))


if __name__ == '__main__':
    # 处理特征
    x, y = deal_feature(load_data())
    test_L(x, y)
    # pca降维处理
    x = deal_pca(x)
    test_L(x, y)
    # 画图

    # 划分训练集,测试集
    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.7, random_state=1)
