import torch
import copy

# Unversal data loader and reader (can be used for other graph datasets from https://ls11-www.cs.tu-dortmund.de/staff/morris/graphkerneldatasets)
class GraphData(torch.utils.data.Dataset):
    # None means all Train and Test data
    def __init__(self,
                 datareader,
                 split=None):
        self.rnd_state = datareader.rnd_state
        self.split = split
        self.set_fold(datareader.data)

    def set_fold(self, data):
        self.total = len(data['targets'])
        self.N_nodes_max = data['N_nodes_max']
        self.num_classes = data['num_classes']
        self.num_features = data['num_features']
        # None: merge Train and Test
        if not self.split == 'test':
            self.idx = data['splits'][self.split]
        else:
            self.idx = data['splits']['train'] + data['splits']['val']
            self.idx.sort()
        # use deepcopy to make sure we don't alter objects in folds
        # self.labels = copy.deepcopy([data['targets'][i] for i in self.idx])
        # self.adj_list = copy.deepcopy([data['adj_list'][i] for i in self.idx])
        # self.features_onehot = copy.deepcopy([data['features_onehot'][i] for i in self.idx])
        # self.graph_feature = copy.deepcopy([data['graph_feature'][i] for i in self.idx])
        self.labels = [data['targets'][i] for i in self.idx]
        self.adj_list = [data['adj_list'][i] for i in self.idx]
        self.features_onehot = [data['features_onehot'][i] for i in self.idx]
        self.graph_feature = [data['graph_feature'][i] for i in self.idx]
        print('%s: %d/%d' % (self.split, len(self.labels), len(data['targets'])))
        # print(len(self.graph_feature[0]))

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, index):
        # print('_________+++++++++++++++++_______________++++++++++++++++++')
        # print(torch.from_numpy(self.graph_feature[index]).float())
        # convert to torch
        # print(self.graph_feature[index])
        return [torch.from_numpy(self.features_onehot[index]).float(),  # node_features
                torch.from_numpy(self.adj_list[index]).float(),  # adjacency matrix
                int(self.labels[index]),
                torch.from_numpy(self.graph_feature[index]).float()]