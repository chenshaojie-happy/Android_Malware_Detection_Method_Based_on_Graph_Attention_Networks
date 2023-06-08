# coding=utf-8
import os
import shutil
import subprocess
import datetime
from multiprocessing import Pool

# 在要打印的内容前添加时间后打印
def time_print(string):
    time = datetime.datetime.now()
    print(time.strftime("%Y-%m-%d %H:%M:%S") + ' : ' + str(string))


def apktool_single(out_path, filename, apk_file, dex_path):
    jar_command = 'apktool d --force-manifest --no-res --no-src -o ' + out_path + '/' + filename + '/ ' + apk_file

    # jar_command = 'apktool d --force-manifest --no-res --no-src ' + apk_file
    child = subprocess.Popen(jar_command, shell=True)
    child.wait()

    result_path = out_path + filename
    # 若路径不存在，跳过
    if not os.path.exists(result_path):
        return

    # 将Manifest.xml和class.dex分别移动到对应的文件夹下，并删掉其他文件
    for this_file in os.listdir(result_path):
        if os.path.isfile(result_path + '/' + this_file):
            if "AndroidManifest.xml" == this_file:
                continue
            elif this_file.endswith(".dex"):
                if not os.path.exists(dex_path + filename):
                    os.mkdir(dex_path + filename)
                shutil.move(result_path + '/' + this_file, dex_path + filename + '/' + this_file)
            else:
                os.remove(result_path + '/' + this_file)
        else:
            try:
                shutil.rmtree(result_path + '/' + this_file)
            except Exception as e:
                print(e)
                print("shutil retree error: " + result_path)


# 使用apktool工具进行反编译
def apktool(apk_path, out_path, dex_path, total_process):
    # os.chdir(out_path)
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
        if (i + 1) % 100 == 0:
            time_print(apk_path + ' already decompile: ' + str(i+1) + ', total : ' + str(len(apk_files)))
        filename = apk_files[i]
        apk_file = apk_path + apk_files[i]
        if not filename.endswith('.apk'):
            os.rename(apk_file, apk_file + '.apk')
            apk_file = apk_file + '.apk'
            filename = filename + '.apk'
            print("rename: " + apk_file)
        if os.path.exists(out_path + '/' + filename):
            time_print("File already unpacked: " + out_path + '/' + filename)
            continue
        pool.apply_async(apktool_single,(out_path, filename, apk_file, dex_path,))
        # apktool_single(out_path, filename, apk_file, dex_path)
    pool.close()
    pool.join()

