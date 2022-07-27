# coding=utf-8
import os
import numpy as np
import re
import xgboost
import joblib

def load_feature(feature_file):
    filelist = []
    label = []
    feature = []

    fi = open(feature_file)
    while True:
        lines = fi.readlines(10000)
        if not lines:
            break
        for line in lines:
            parts = line.strip().split(',')
            filelist.append(parts[0])
            label.append(1 if parts[1] == 'b' else 0)
            feature.append([float(tk) for tk in parts[2].split(' ')])

    return filelist, label, feature


def train_xgb(labels, feature, model_cla_path, lr=0.2):

    # print('start: ' + below_num + ' ' + above_len + ' ' + str(lsi_len) + ' ')
    # if (os.path.exists('./apk_train_xgbooost_lsi_' + str(lsi_len) + '_myblack_train_result_below_' + below_num + '_above_' + above_len + '_permission.model')):
    #     return
    # print(feature[1])
    # print(len(feature[-1]))
    # for featur in feature:
    #     if len(featur) != 559:
    #         print(len(featur))

    x = np.array(feature)
    y = np.array(labels)
    # print(x)
    # print(y.shape)
    print('data count: ' + str(len(y)))

    n_msp = 2
    n_gamma = 0
    n_tree = 80
    n_f = 12
    subS = 1
    # lr = lr
    col = 0.6

    clf = xgboost.XGBClassifier(base_score=0.5, colsample_bylevel=1, colsample_bytree=col,
                                gamma=n_gamma, learning_rate=lr, max_delta_step=0, max_depth=n_f,
                                min_child_weight=1, n_estimators=n_tree, nthread=-1,
                                objective='reg:logistic', reg_alpha=0, reg_lambda=0.1,
                                scale_pos_weight=1, seed=66, silent=1, subsample=subS)
    # print(x)
    clf.fit(x, y)
    # joblib.dump(clf, 'apk_train_xgbooost_lsi_' + str(
    #     lsi_len) + '_myblack_train_result_below_' + below_num + '_above_' + above_len + '_permission.model')
    joblib.dump(clf, model_cla_path)
    print('Trainging Finished')


# clf: xgboot.XGBClassifier, data: np.array, labels: np.array(取值为0,1 或w,b)
def test_xgb(model_cla_path, data, labels):
    clf = joblib.load(model_cla_path)
    if len(labels) == 0:
        print('No data')
        return
    result = clf.predict(data)
    TP = 0
    FP = 0
    TN = 0
    FN = 0
    for i in range(len(result)):
        if result[i] == 0 and (labels[i] == 0 or labels[i] == 'w'):
            TN += 1
        elif result[i] == 0 and (labels[i] == 1 or labels[i] == 'b'):
            FN += 1
        elif result[i] == 1 and (labels[i] == 0 or labels[i] == 'w'):
            FP += 1
        elif result[i] == 1 and (labels[i] == 1 or labels[i] == 'b'):
            TP += 1
    accuracy = float(TP + TN) / (len(result))
    recall = float(TP) / (TP + FN)
    precision = float(TP) / (TP + FP)
    F1 = 2 * recall * precision / (recall + precision)
    print('TP: ' + str(TP) + ', FP: ' + str(FP) + ', TN: ' + str(TN) + ', FN: ' + str(FN))
    print('accuacy: ' + str(accuracy) + ', precision: ' + str(precision) + ', recall: ' + str(recall) + ', F1: ' + str(F1))
    return accuracy


def test_xgb_model(feature_file, model_cla_path):
    filelist, labels, feature = load_feature(feature_file)
    accuracy = test_xgb(model_cla_path, np.array(feature), np.array(labels))
    return accuracy


def train_xgb_model(feature_file, model_cla_path, lr = 0.2):
    filelist, labels, feature = load_feature(feature_file)
    print(len(feature))
    train_xgb(labels, feature, model_cla_path, lr=lr)
    test_xgb(model_cla_path, np.array(feature), np.array(labels))


