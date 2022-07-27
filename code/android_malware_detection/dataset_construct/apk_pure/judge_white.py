import os
import csv
import json
import shutil

def read_csv(csv_in):
    details = []

    fi = open(csv_in, 'r')
    f_csv = csv.reader(fi)
    number = 0
    for row in f_csv:
        # 去掉csv的表头
        number += 1
        if number == 1:
            continue
        detail = {}
        detail['new_name'] = row[0]
        detail['type'] = row[1]
        detail['md5_file'] = row[2]
        detail['old_name'] = row[3]
        detail['md5_type'] = row[4]
        details.append(detail)
    fi.close()
    return details

# 将文件详细信息转换为csv格式
def transform_csv_vt(details, csv_file):
    headers = ['new_name', 'type', 'md5_file', 'old_name', 'md5_type', 'vt_black', 'vt_json']

    fo = open(csv_file, 'w',encoding='utf-8')
    fo.write(headers[0] + ',' + headers[1] + ',' + headers[2] + ',' + headers[3] + ',' + headers[4] + ',' + headers[5] + ',' + headers[6] + '\n')
    for detail in details:
        fo.write('"' + detail['new_name'] + '","' + detail['type'] + '","' + detail['md5_file'] + '","' + detail['old_name'] + '","' + detail['md5_type'] + '","' + str(detail['vt_black']) + '","' + detail['vt_json'] + '"\n')
    fo.close()


def load_vt_result(vt_root, vt_filename):
    fi = open(vt_root + vt_filename, 'r')
    line = fi.readline()
    texts = json.loads(line)
    vt_result = int(texts["positives"])
    fi.close()
    return vt_result, line.replace(',', '\,')


def move_file(old_file, new_file):
    shutil.move(old_file, new_file)
    pass

if __name__ == '__main__':
    vt_root = '/data2/android_malware_detection/dataset/apkpure/vt/'
    csv_file = '/data2/android_malware_detection/dataset/apkpure/apk_details.csv'
    csv_file_vt = '/data2/android_malware_detection/dataset/apkpure/apk_details_vt.csv'
    fileroot = '/data2/android_malware_detection/dataset/apkpure/white/'
    fileroot_vt_black = '/data2/android_malware_detection/dataset/apkpure/vt_black/'


    details = read_csv(csv_file)
    for i in range(len(details)):
        md5 = details[i]['md5_file']
        vt_file = md5 + '.json'
        filename = details[i]['new_name']
        vt_result, vt_json = load_vt_result(vt_root, vt_file)
        details[i]['vt_black'] = vt_result
        details[i]['vt_json'] = vt_json
        if vt_result > 0:
            move_file(fileroot + filename, fileroot_vt_black + filename)
        print(details[i])
    transform_csv_vt(details, csv_file_vt)
    print('save csv file done!')
