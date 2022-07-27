# coding=utf-8
import os
from .DirAndFile import DirAndFile
from multiprocessing import Pool


def extract_process(dataset, count, total, filename, ThirdPartyResultPath, JavaResultPath, ManifestPath, outFilePath):
    # print('Extracting dataset: ' + dataset + ', count: ' + str(count) + ', total: ' + str(total))
    if not os.path.exists(outFilePath + filename + '.tokenResult'):
        print('Begin extract file: ' + filename)
        try:
            dirAndFile = DirAndFile(ThirdPartyResultPath, JavaResultPath, ManifestPath, filename, outFilePath)
            count_java_file = dirAndFile.extractToken(ifRandomSample=True)
            print("Extract Files count: " + str(count_java_file))
            dirAndFile.writeResult()
        except Exception as e:
            print("Extract error: " + str(e))
    else:
        # print('File already exist: ' + outFilePath + filename + '.tokenResult')
        pass


def extract_token(dataset, ThirdPartyResultPath, JavaResultPath, ManifestPath, outFilePath, total_process):
    filenames = os.listdir(ManifestPath)
    count = 0
    total = len(filenames)
    pool = Pool(processes=total_process)
    for filename in filenames:
        count += 1
        # extract_process(dataset, count, total, filename, ThirdPartyResultPath, JavaResultPath, ManifestPath, outFilePath,)
        pool.apply_async(extract_process, (dataset, count, total, filename, ThirdPartyResultPath, JavaResultPath, ManifestPath, outFilePath,))
    pool.close()
    pool.join()

