# coding=utf-8
import os
import random


# dataset_config为数据集的配置dict，if_override为当该数据集文件已存在时是否重新生成
def create_train_test(name, dataset_config, train_file, test_file, ratio_train=0.8, if_override=False):
    if not os.path.exists(train_file) or not os.path.exists(test_file) or if_override:
        # 判断是否需要生成训练集
        print('Creating dataset: ' + name)
        create_set(dataset_config, train_file, test_file, ratio_train)
        print('Created dataset: ' + name)
    else:
        print('Dataset already exist: ' + name)


def create_set(dataset_config, train_file, test_file, ratio_train):
    filelist = []
    for sub_dataset_name in dataset_config:
        sub_dataset = dataset_config[sub_dataset_name]
        filelist_src = sub_dataset['filelist']
        count = sub_dataset['count']
        prefix = sub_dataset['prefix']
        white_black = sub_dataset['white_black']

        fi = open(filelist_src, 'r')
        lines = fi.readlines()
        random.shuffle(lines)
        for i in range(count):
            filelist.append(prefix + lines[i].strip('\n') + ' ' + white_black + '\n')
        fi.close()
    random.shuffle(filelist)
    len_train = int(len(filelist) * ratio_train)
    fo = open(train_file, 'w+')
    for i in range(len_train):
        fo.write(filelist[i])
    fo.close()
    fo = open(test_file, 'w+')
    for i in range(len_train, len(filelist)):
        fo.write(filelist[i])
    fo.close()

    pass