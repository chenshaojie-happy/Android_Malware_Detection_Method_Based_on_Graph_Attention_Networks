import os
import numpy as np
import argparse
from os.path import join
import sys
sys.path.append('..')
from memory_usage import memory_usage

def split_ids(ids):
    #import random
    n = len(ids)
    train_ids = ids[:int(0.9 * n)]
    #random.shuffle(train_ids)
    test_ids = ids[int(0.9 * n):]

    return train_ids, test_ids



class DataReader():
    '''
    Class to read the txt files containing all data of the dataset.
    Should work for any dataset from https://ls11-www.cs.tu-dortmund.de/staff/morris/graphkerneldatasets
    '''

    def __init__(self,
                 data_dir,  # folder with txt files
                 rnd_state=None,
                 use_cont_node_attr=False,
                 train_test='train_val',
                 use_node_labels=False
                 # use or not additional float valued node attributes available in some datasets
                 ):

        self.data_dir = data_dir
        self.rnd_state = np.random.RandomState() if rnd_state is None else rnd_state
        self.use_cont_node_attr = use_cont_node_attr
        self.use_node_labels = use_node_labels
        files = os.listdir(self.data_dir)
        if train_test == 'train_val':
            file_prefix = '_train_'
        else:
            file_prefix = '_test_'
        data = {}
        nodes, graphs, indexes= self.read_graph_nodes_relations(list(filter(lambda f: f.find(file_prefix + 'graph_indicator.txt') >= 0, files))[0])
        print('+++++++++++++++++1')
        print(memory_usage())
        # data['adj_list'] = {}
        data['adj_list'] = self.read_graph_adj(list(filter(lambda f: f.find(file_prefix + 'A.txt') >= 0, files))[0], nodes, graphs, indexes) #, list(filter(lambda f: f.find(file_prefix + 'A2.txt') >= 0, files))[0])
        print('+++++++++++++++++2')
        print(memory_usage())
        print('Read adj list done!')

        data['targets'] = np.array(
            self.parse_txt_file(list(filter(lambda f: f.find(file_prefix + 'graph_labels') >= 0, files))[0],
                                line_parse_fn=lambda s: int(float(s.strip()))))
        print('+++++++++++++++++3')
        print(memory_usage())
        if self.use_cont_node_attr:
            data['attr'] = self.read_node_features(list(filter(lambda f: f.find(file_prefix + 'node_attributes.txt') >= 0, files))[0],
                                                   nodes, graphs,
                                                   fn=lambda s: np.array(list(map(float, s.strip().split(',')))))
        print('+++++++++++++++++4')
        print(memory_usage())
        print('Read node attri done!')
        data['graph_feature'] = np.array(
            self.parse_txt_file(list(filter(lambda f: f.find(file_prefix + 'graph_attributes.txt') >= 0, files))[0],
                                line_parse_fn=lambda s: [float(z) for z in s.split(',')]))
        print('+++++++++++++++++5')
        print(memory_usage())
        if self.use_node_labels:
            data['features'] = self.read_node_features(list(filter(lambda f: f.find(file_prefix + 'node_labels.txt') >= 0, files))[0], nodes, graphs, fn=lambda s: int(s.strip()))
        print(len(data['attr']))

        features, n_edges, degrees = [], [], []
        for sample_id, adj in enumerate(data['adj_list']):
            N = len(adj)  # number of nodes
            if self.use_node_labels:
                assert N == len(data['features'][sample_id]), (N, len(data['features'][sample_id]))
            # if not np.allclose(adj, adj.T):
            #     print(sample_id, 'not symmetric')
            n = np.sum(adj)  # total sum of edges
            # assert n % 2 == 0, n
            # n_edges.append(int(n / 2))  # undirected edges, so need to divide by 2
            n_edges.append(int(n))
            degrees.extend(list(np.sum(adj, 1)))
            if self.use_node_labels:
                features.append(np.array(data['features'][sample_id]))
        print('+++++++++++++++++6')
        print(memory_usage())
        # Create features over graphs as one-hot vectors for each node
        if self.use_node_labels:
            features_all = np.concatenate(features)
            features_min = features_all.min()
            num_features = int(features_all.max() - features_min + 1)  # number of possible values
        print('+++++++++++++++++7')
        print(memory_usage())
        max_degree = np.max(degrees)
        features_onehot = []
        for sample_id, adj in enumerate(data['adj_list']):
            N = adj.shape[0]
            if self.use_node_labels:
                x = data['features'][sample_id]
                feature_onehot = np.zeros((len(x), num_features))
                for node, value in enumerate(x):
                    feature_onehot[node, value - features_min] = 1
            else:
                feature_onehot = np.empty((N, 0))
            if self.use_cont_node_attr:
                feature_attr = np.array(data['attr'][sample_id])
            else:
                feature_attr = np.empty((N, 0))
            degree_onehot = np.empty((N, 0))
            # print(sample_id)
            # print(feature_onehot.shape, feature_attr.shape, degree_onehot.shape)
            node_features = np.concatenate((feature_onehot, feature_attr, degree_onehot), axis=1)
            if node_features.shape[1] == 0:
                # dummy features for datasets without node labels/attributes
                # node degree features can be used instead
                node_features = np.ones((N, 1))
            features_onehot.append(node_features)
        print('+++++++++++++++++8')
        print(memory_usage())
        num_features = features_onehot[0].shape[1]

        shapes = [len(adj) for adj in data['adj_list']]
        labels = data['targets']  # graph class labels
        labels -= np.min(labels)  # to start from 0

        classes = np.unique(labels)
        num_classes = len(classes)
        print('+++++++++++++++++9')
        print(memory_usage())
        if not np.all(np.diff(classes) == 1):
            print('making labels sequential, otherwise pytorch might crash')
            labels_new = np.zeros(labels.shape, dtype=labels.dtype) - 1
            for lbl in range(num_classes):
                labels_new[labels == classes[lbl]] = lbl
            labels = labels_new
            classes = np.unique(labels)
            assert len(np.unique(labels)) == num_classes, np.unique(labels)

        def stats(x):
            return (np.mean(x), np.std(x), np.min(x), np.max(x))

        print('N nodes avg/std/min/max: \t%.2f/%.2f/%d/%d' % stats(shapes))
        print('N edges avg/std/min/max: \t%.2f/%.2f/%d/%d' % stats(n_edges))
        print('Node degree avg/std/min/max: \t%.2f/%.2f/%d/%d' % stats(degrees))
        print('Node features dim: \t\t%d' % num_features)
        print('N classes: \t\t\t%d' % num_classes)
        print('Classes: \t\t\t%s' % str(classes))
        for lbl in classes:
            print('Class %d: \t\t\t%d samples' % (lbl, np.sum(labels == lbl)))

        print('+++++++++++++++++10')
        print(memory_usage())
        N_graphs = len(labels)  # number of samples (graphs) in data
        print(N_graphs)
        print(len(data['adj_list']))
        print(len(features_onehot))
        assert N_graphs == len(data['adj_list']) == len(features_onehot), 'invalid data'

        # Create train/test sets first
        # if train_test == 'train_val':
        train_ids, val_ids = split_ids(rnd_state.permutation(N_graphs))
        # else:
        #     train_ids, val_ids = split_ids(N_graphs)
        print('+++++++++++++++++11')
        print(memory_usage())
        # Create train sets
        splits = {'train': list(train_ids), 'val': list(val_ids)}

        data['features_onehot'] = features_onehot
        data['targets'] = labels
        data['splits'] = splits
        data['N_nodes_max'] = np.max(shapes)  # max number of nodes
        data['num_features'] = num_features
        data['num_classes'] = num_classes
        print('+++++++++++++++++12')
        print(memory_usage())
        self.data = data

    def parse_txt_file(self, fpath, line_parse_fn=None):
        print(fpath)
        data = []
        count = 0
        with open(join(self.data_dir, fpath), 'r') as f:
        #     lines = f.readlines()
        # print('---')
        # data = [line_parse_fn(s) if line_parse_fn is not None else s for s in lines]
            while True:
                lines = f.readlines(10000)
                if not lines:
                    break
                for line in lines:
                    count += 1
                    if count % 1000000 == 0:
                        print(count)
                    data.append(line_parse_fn(line) if line_parse_fn is not None else line)
        return data
    def parse_txt_file_single(self, fpath, line_parse_fn=None):
        print(fpath)
        data = []
        count = 0
        with open(join(self.data_dir, fpath), 'r') as f:
        #     lines = f.readlines()
        # print('---')
        # data = [line_parse_fn(s) if line_parse_fn is not None else s for s in lines]
            while True:
                lines = f.readlines(10000)
                if not lines:
                    break
                for line in lines:
                    count += 1
                    if count % 1000000 == 0:
                        print(count)
                    yield line_parse_fn(line) if line_parse_fn is not None else line
        # return data

    # graph key is graph_id, value is list of nodes
    def read_graph_adj(self, fpath, nodes, graphs, indexes, fpath2=None):
        # edges = self.parse_txt_file(fpath, line_parse_fn=lambda s: [int(num.strip()) for num in s.split(',')])
        adj_dict = {}
        # 添加每个节点的自环
        # for node in nodes:
        #     edges.append((str(node), str(node)))
        # for edge in edges:
        for edge in self.parse_txt_file_single(fpath, line_parse_fn=lambda s: [int(num.strip()) for num in s.split(',')]):
            # print(edge)
            node1 = edge[0]#int(edge[0].strip())# - 1  # -1 because of zero-indexing in our code
            node2 = edge[1]#int(edge[1].strip())# - 1
            graph_id = nodes[node1]
            assert graph_id == nodes[node2], ('invalid data', graph_id, nodes[node2])
            if graph_id not in adj_dict:
                n = len(graphs[graph_id])
                # adj_dict[graph_id] = np.zeros((n, n))
                adj_dict[graph_id] = np.full((n, n), -1e9)
                # adj_dict[graph_id] = np.array(n * [n * [-1e9]])
                # print(adj_dict[graph_id].shape)
                # raise Exception
                # 添加每个节点的自环
                for i in range(n):
                    adj_dict[graph_id][i, i] = 0
            # ind1 = np.where(graphs[graph_id] == node1)[0]
            # ind2 = np.where(graphs[graph_id] == node2)[0]
            # print(ind2)
            ind1 = np.array([indexes[node1]])
            ind2 = np.array([indexes[node2]])
            # print(ind2)
            assert len(ind1) == len(ind2) == 1, (ind1, ind2)
            adj_dict[graph_id][ind1, ind2] = 0
            # pass

            # 转成无向图
            adj_dict[graph_id][ind2, ind1] = 0
        # print(adj_dict[0])
        # 添加节点特征关联
        # if fpath2 is not None:
        #     for edge in self.parse_txt_file_single(fpath2, line_parse_fn=lambda s: [int(num.strip()) for num in s.split(',')]):
        #
        #         # print(edge)
        #         node1 = edge[0]#int(edge[0].strip())# - 1  # -1 because of zero-indexing in our code
        #         node2 = edge[1]#int(edge[1].strip())# - 1
        #         graph_id = nodes[node1]
        #         assert graph_id == nodes[node2], ('invalid data', graph_id, nodes[node2])
        #         if graph_id not in adj_dict:
        #             n = len(graphs[graph_id])
        #             adj_dict[graph_id] = np.zeros((n, n))
        #         # ind1 = np.where(graphs[graph_id] == node1)[0]
        #         # ind2 = np.where(graphs[graph_id] == node2)[0]
        #         # print(ind2)
        #         ind1 = np.array([indexes[node1]])
        #         ind2 = np.array([indexes[node2]])
        #         # print(ind2)
        #         assert len(ind1) == len(ind2) == 1, (ind1, ind2)
        #         adj_dict[graph_id][ind1, ind2] = 1
        #         pass
        #
        #         # 转成无向图
        #         adj_dict[graph_id][ind2, ind1] = 1
        # print(adj_dict[0])
        for graph_id in graphs.keys():
            if graph_id not in adj_dict:
                n = len(graphs[graph_id])
                adj_dict[graph_id] = np.zeros((n, n))
        adj_list = [adj_dict[graph_id] for graph_id in sorted(list(graphs.keys()))]

        return adj_list

    def read_graph_nodes_relations(self, fpath):
        graph_ids = self.parse_txt_file(fpath, line_parse_fn=lambda s: int(s.rstrip()))
        nodes, graphs = {}, {}
        indexes = [0.0 for i in range(len(graph_ids))]
        for node_id, graph_id in enumerate(graph_ids):
            if graph_id not in graphs:
                graphs[graph_id] = []
            graphs[graph_id].append(node_id)
            nodes[node_id] = graph_id
            indexes[node_id] = len(graphs[graph_id]) - 1
        graph_ids = np.unique(list(graphs.keys()))
        for graph_id in graph_ids:
            graphs[graph_id] = np.array(graphs[graph_id])
        return nodes, graphs, indexes

    def read_node_features(self, fpath, nodes, graphs, fn):
        node_features_all = self.parse_txt_file(fpath, line_parse_fn=fn)
        node_features = {}
        for node_id, x in enumerate(node_features_all):
            graph_id = nodes[node_id]
            if graph_id not in node_features:
                node_features[graph_id] = [None] * len(graphs[graph_id])
            ind = np.where(graphs[graph_id] == node_id)[0]
            assert len(ind) == 1, ind
            assert node_features[graph_id][ind[0]] is None, node_features[graph_id][ind[0]]
            node_features[graph_id][ind[0]] = x
        node_features_lst = [node_features[graph_id] for graph_id in sorted(list(graphs.keys()))]
        return node_features_lst
