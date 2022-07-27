# coding=utf-8


import os


def combine_lsi_permission(dataset_name, LSI_corpus_path, permission_dir_path, combined_feature_file):
    if os.path.exists(combined_feature_file):
        print('Combined feature file exist: ' + dataset_name)
        return
    # 读取保存的LSI特征
    fi = open(LSI_corpus_path, 'r')
    filelist = []
    atype = []
    lsi_feature = []
    while True:
        lines = fi.readlines(1000)
        if not lines:
            break
        for line in lines:
            parts = line.strip().split(',')
            if len(parts) < 3:
                print('error in line: "' + line + '"')
            filelist.append(parts[0])
            atype.append(parts[1])
            lsi_feature.append(parts[2].split(' '))
    fi.close()

    # 读取permission特征
    for i in range(len(filelist)):
        filename = filelist[i]
        fi = open(permission_dir_path + filename + '.permission', 'r')
        permission_feature = fi.readline().strip().split(' ')
        if len(permission_feature) != 59:
            print(len(permission_feature))
            print('error in file: ' + filename)
        lsi_feature[i] += permission_feature
        fi.close()
        if (i+1) % 100 == 0 or i == len(filelist) - 1:
            print('Already combine feature file count: '+ str(i+1) + ', total: ' + str(len(filelist)) + ', dataset: ' + dataset_name)

    # 写入拼接后特征文件
    fo = open(combined_feature_file, 'w+')
    for i in range(len(filelist)):
        new_line = filelist[i] + ',' + atype[i] + ','
        for j in lsi_feature[i]:
            new_line += str(j) + ' '
        new_line.strip(' ')
        fo.write(new_line + '\n')
    fo.close()
    print('Save combined features finish: ' + dataset_name)


