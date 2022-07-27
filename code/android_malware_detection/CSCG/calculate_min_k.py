# coding=utf-8
import zipfile
import json

def calculate_min_k(dataset, java_path, train_file, ts_max, min_k_tmp_file):
    # 先判断是否已经计算过min_k,若是则直接load
    fi = open(min_k_tmp_file, 'r')
    line = fi.read()
    fi.close()
    texts = json.loads(line.strip())
    if dataset in texts:
        return texts[dataset]

    # 否则重新计算，并更新min_k_tmp_file
    total_java = []
    apk_files = []
    fi = open(train_file, 'r')
    while True:
        lines = fi.readlines(10000)
        if not lines:
            break
        for line in lines:
            apk_files.append(line.split(' ')[0])
    fi.close()

    for apk_file in apk_files:
        count_java = 0
        JavaZipFilePath = java_path + apk_file + '.zip'
        JavaZipFile = zipfile.ZipFile(JavaZipFilePath, 'r')
        java_file_list = JavaZipFile.namelist()
        for _file in java_file_list:
            if _file.endswith('.java'):
                count_java += 1
        JavaZipFile.close()
        total_java.append(count_java)

    # 取中位数
    total_java.sort()
    median = total_java[int(len(total_java)/2)]

    # 计算min_k
    min_k = max(round(median / ts_max), 1)

    texts[dataset] = min_k
    fo = open(min_k_tmp_file, 'w+')
    new_line = json.dumps(texts)
    fo.write(new_line)
    fo.close()
    return min_k