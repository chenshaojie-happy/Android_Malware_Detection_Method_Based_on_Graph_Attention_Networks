# coding=utf-8
import os
# import shutil
import subprocess
import time
from multiprocessing import Pool
import signal
# jar_path = '/home/audr/syc_disk/syc/AndroZoo_white/Androzoo_white_4_dex/'
# java_path = '/home/audr/syc_disk/syc/AndroZoo_white/Androzoo_white_4_java/'


def jar2java(jar_path, java_path, java_src_tmp_path, program_root, total_process):
    # jar_path: class.dex存放文件夹，java_path: java压缩包存放位置，
    # java_src_tmp_path: 临时存放反编译后src/文件夹的位置（设置在固态硬盘上，提高IO速度）
    # program_root: 用于在该部分执行完成后将当前路径还原到程序根目录下
    # 每个文件先在java_src_tmp_path下解压得到src文件夹，删除src/resources后，打包成.zip放在java_path下，防止java_path下碎文件太多，影响IO速度
    if not os.path.exists(java_src_tmp_path):
        os.system("mkdir -p " + java_src_tmp_path)
    os.chdir(java_src_tmp_path)
    pool = Pool(processes=total_process)
    filenames = sorted(os.listdir(jar_path), reverse=True)

    size_dict = {}
    for apk_file in filenames:
        size = 0
        parent = jar_path + apk_file + '/'
        for file_ in os.listdir(parent):
            size += os.path.getsize(parent + file_)

        size_dict[apk_file] = size
    # 按大小顺序排序，保证大文件先处理，尽量减少最后处理大文件导致时间开销大
    filenames = [i[0] for i in sorted(size_dict.items(), key=lambda L: L[1], reverse=True)]

    # print(filenames)
    # raise Exception
    for filename in filenames:
        # jar2java_single(jar_path, java_path, java_src_tmp_path, filename)
        pool.apply_async(jar2java_single, (jar_path, java_path, java_src_tmp_path, filename))
    pool.close()
    pool.join()
    os.chdir(program_root)


def jar2java_single(jar_path, java_path, java_src_tmp_path, filename):

    if os.path.exists(java_path + filename + '.zip'):
        print('File already exist: ' + java_path + filename + '.zip')
        return
    if not os.path.exists(jar_path + filename + '/classes.dex'):
        print("step over :" + filename)
        return
    # 在java_src_tmp_path下新建文件夹filename，用于临时存filename反编译出来的java代码
    new_java_src_tmp_path = java_src_tmp_path + '/' + filename

    if not os.path.exists(new_java_src_tmp_path):
        os.mkdir(new_java_src_tmp_path)
    os.chdir(new_java_src_tmp_path)
    if not os.path.exists('src'):
        os.mkdir('src')

    os.system("rm -rf src/*")
    print("step in :" + filename)

    # 在固态硬盘上的路径java_src_tmp_path里反编译
    for _class in os.listdir(jar_path + filename):
        print('jadx -d src ' + jar_path + filename + '/' + _class)
        jar_command = 'jadx -d src ' + jar_path + filename + '/' + _class

        # 部分反编译会卡死，设置超时时间为1小时，大于该时长，则打算反编译后直接打包
        try:
            child = subprocess.Popen(jar_command, shell=True)
            (msg, errs) = child.communicate(timeout=3600)
            ret_code = child.poll()
            child.wait()
        except subprocess.TimeoutExpired:
            child.kill()
            child.terminate()
        except Exception as e:
            pass

    # 将反编译里的resource文件夹删掉
    jar_command = 'rm -rf src/resources'
    child = subprocess.Popen(jar_command, shell=True)
    child.wait()
    # 将反编译的代码打包成zip文件，存在java_path中
    jar_command = 'zip -r ' + java_path + filename + '.zip src'
    child = subprocess.Popen(jar_command, shell=True)
    child.wait()
    os.system("rm -rf src/")
    os.chdir(java_src_tmp_path)
    os.system("rm -rf " + filename)
