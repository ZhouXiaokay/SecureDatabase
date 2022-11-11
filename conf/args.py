#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python version: 3.6

import argparse


def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rank',
                        default=0,
                        type=int,
                        help='the client rank')
    parser.add_argument('--rounds',
                        default=10,
                        type=int,
                        help='total communication rounds')
    parser.add_argument('--epoch',
                        default=5,
                        type=int,
                        help='number of local epochs')
    parser.add_argument('--batch_size',
                        default=4,
                        type=int,
                        help='local batch size')
    parser.add_argument('--seed',
                        default=1,
                        type=int,
                        help='random seed')
    parser.add_argument('--trainer_address',
                        default='127.0.0.1:60000',
                        type=str,
                        help='init method')
    parser.add_argument('--server_address',
                        default='127.0.0.1:50090',
                        type=str,
                        help='init method')
    parser.add_argument('--sample_num',
                        default=3,
                        type=float,
                        help='local_count/sum_count')
    parser.add_argument('--n_features',
                        default=10,
                        type=int,
                        help='the number of features')
    parser.add_argument('--ctx_file',
                        default='../../transmission/ts_ckks.config',
                        type=str,
                        help='the number of features')
    args = parser.parse_args()
    return args
