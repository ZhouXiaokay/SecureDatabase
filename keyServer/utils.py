import numpy as np


def generate_noise_list(db_num, noise_type):
    sensitivity = 1
    epsilon = 1e-7
    noise_type = noise_type.upper()
    # generate laplace noise list
    noise_list = np.random.laplace(loc=0, scale=sensitivity / epsilon, size=db_num - 1)

    if noise_type == "INT":
        noise_list = noise_list.astype(int)

    noise_list = noise_list.tolist()
    last_noise = 0 - sum(noise_list)
    noise_list.append(last_noise)

    return noise_list


def get_noise(cid, qid, db_name, total_noise_list):
    result = []
    for noise_dict in total_noise_list:
        if noise_dict['cid'] == cid and noise_dict['qid'] == qid:
            noise_list = noise_dict['noise_list']
            result.append(noise_list[db_name - 1])
            return result

def remove_noise_list(cid,qid,total_noise_list):
    for noise_dict in total_noise_list:
        if noise_dict['cid'] == cid and noise_dict['qid'] == qid:
            total_noise_list.remove(noise_dict)


