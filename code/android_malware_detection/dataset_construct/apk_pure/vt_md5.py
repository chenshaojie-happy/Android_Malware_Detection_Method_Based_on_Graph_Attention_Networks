import os
import json
import csv
import subprocess
from multiprocessing import Pool
import time

def virustotal_process(md5, apikey,outfile):
    print(md5, apikey)
    cmd = "curl --request GET --url 'https://www.virustotal.com/vtapi/v2/file/report?apikey=" + apikey + "&resource=" + md5 + "'"
    cmd += ' > ' + outfile
    result = subprocess.getoutput(cmd)
    # time.sleep(15)
    # print(cmd)
    # print(result)

    return result


def load_api_key(apifile):
    fi = open(apifile, 'r')
    keys = []
    for line in fi.readlines():
        keys.append(line.strip())
    return keys

# 将文件移动到旧路径
def get_md5(csv_file):
    fi = open(csv_file, encoding='utf-8')
    md5s = []
    f_csv = csv.reader(fi)
    number = 0
    for row in f_csv:
        # 去掉csv的表头
        number += 1
        if number == 1:
            continue
        md5s.append(row[2])
    fi.close()
    return md5s


if __name__ == '__main__':
    outroot = '/data2/android_malware_detection/dataset/apkpure/vt/'
    csv_file = '/data2/android_malware_detection/dataset/apkpure/apk_details.csv'
    outfile = outroot + 'f28ba3a29a9ec5430cb298405ebfec53.json'
    # pool = Pool(processes=13)
    api_keys = load_api_key('keys.txt')
    md5s = get_md5(csv_file)
    # print(md5s)
    # print(api_keys)
    finish = os.listdir(outroot)
    count = 0
    for md5 in md5s:
        if (md5 + '.json' in finish) and (os.path.getsize(outroot + md5 + '.json') != 0):
            print(md5 + ' already finished!')
            continue
        count += 1
        # print(md5, api_keys[count % 35])
    #     pool.apply_async(virustotal_process, [md5, api_keys[count % 35], outroot + md5 + '.json',])
    # pool.close()
    # pool.join()
    #     virustotal_process(md5, '5c5fcfe07c13c1377ab6ae24f7b527438d5db81aa8f56b0376566fb969feb4c6', outroot + md5 + '.json')
        virustotal_process(md5, api_keys[count % 35], outroot + md5 + '.json')

        if os.path.getsize(outroot + md5 + '.json') == 0:
            print(md5, api_keys[count % 35], 'fail!')
        else:
            fi = open(outroot + md5 + '.json')
            if fi.readline().endswith("ng scans\"}"):
                count += 1
                fo = open(outroot + md5 + '.ok', 'w')
                fo.close()
            fi.close()
                # print(md5, filename[md5])
                # filename_ = fileroot + filename[md5]
                #
                # result = virustotal_process(filename_, api_keys[count % 35], outroot + md5 + '.json')
                # fo = open(outroot + md5 + '.ok', 'w')
                # fo.write(result)
                # fo.close()
    #     time.sleep(15)
    # for api_key in api_keys:
    #     print(api_key)
    #     virustotal_process('f28ba3a29a9ec5430cb298405ebfec53', api_key, 'result/' + api_key)
