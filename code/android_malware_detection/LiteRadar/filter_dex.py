# coding=utf-8
from ._settings import *
import json
from .literadar import LibRadarLite
import datetime
from multiprocessing import Pool


# 在要打印的内容前添加时间后打印
def time_print(string):
    time = datetime.datetime.now()
    print(time.strftime("%Y-%m-%d %H:%M:%S") + ' : ' + str(string))


def literadar(apk_file, _3rd_file_path, log_info):
    time_print(log_info + ' ' + apk_file)
    try:
        iron_apk_path = apk_file
        lrd = LibRadarLite(iron_apk_path)
        res = lrd.compare()
        fo = open(_3rd_file_path, 'w+')
        result = json.dumps(res, indent=4, sort_keys=True)
        fo.write(result)
        fo.close()
    except Exception as e:
        time_print (apk_file + ' ' + str(e))


def filter_dex(apk_path, result_path, total_process):
    apk_files = os.listdir(apk_path)
    
    size_dict = {}
    for apk_file in apk_files:
        size = os.path.getsize(apk_path + apk_file)
        size_dict[apk_file] = size
    # 按大小顺序排序，保证大文件先处理，尽量减少最后处理大文件导致时间开销大
    apk_files = [i[0] for i in sorted(size_dict.items(), key=lambda L: L[1], reverse=True)]

    pool = Pool(processes = total_process)
    for i in range(len(apk_files)):
        # TODO remove
        # if i > 5:
        #     break
        filename = apk_files[i]
        apk_file = apk_path + apk_files[i]

        if filename.endswith('.apk'):
            _3rd_filename = filename[:-4]
        else:
            _3rd_filename = filename
        if os.path.exists(result_path+_3rd_filename+'.3rd'):
            continue
        log_info = apk_path + ' already filter: ' + str(i + 1) + ', total : ' + str(len(apk_files))
        # literadar(apk_file, result_path + _3rd_filename + '.3rd', log_info)
        pool.apply_async(literadar, (apk_file, result_path + _3rd_filename + '.3rd', log_info, ))
        # if (i + 1) % 100 == 0:
        #     time_print()
        # literadar(apk_file,result_path + _3rd_filename + '.3rd', log_info)
    pool.close()
    pool.join()


# if __name__ == '__main__':
#     apk_path = '/data2/android_malware_detection/dataset/Androzoo/white/'
#     result_path = '/data2/android_malware_detection/3rd/Androzoo/white/'
#     filter_dex(apk_path, result_path)


