import torch
import torch.nn.functional as F
from sklearn.cluster import spectral_clustering


def graph_cuts(fg_embed, edge_index, num_cg, bandwidth=1.0, kernel='rbf', device=torch.device(0), random_state=None):
    affinity = compute_affinity(fg_embed, edge_index, bandwidth, kernel, device)
    # print(affinity)
    pred_cg_idx = spectral_clustering(affinity.cpu().numpy(), n_clusters=num_cg, assign_labels='discretize',
                                          random_state=random_state)

    return pred_cg_idx, affinity


def graph_cuts_with_adj(adj, num_cg, random_state=None):
    pred_cg_idx = spectral_clustering(adj.cpu().numpy(), n_clusters=num_cg, assign_labels='discretize',
                                      random_state=random_state)
    return pred_cg_idx


def compute_affinity(fg_embed, edge_index, bandwidth=1.0, kernel='rbf', device=torch.device(0)):
    if kernel == 'rbf':
        num_nodes = fg_embed.shape[0]
        fg_embed = fg_embed.to(device)
        pairwise_dist = torch.norm(fg_embed[edge_index[0]] - fg_embed[edge_index[1]], dim=1).to(torch.device(0))
        # pairwise_dist = torch.norm(fg_embed.reshape(n, 1, d) - fg_embed.reshape(1, n, d), dim=2).to(torch.device(0))

        pairwise_dist = pairwise_dist ** 2
        affinity = torch.exp(-pairwise_dist / (2 * bandwidth ** 2))
        # affinity = affinity * adj
        affinity = torch.sparse.LongTensor(edge_index, affinity, (num_nodes, num_nodes)).to_dense()
    elif kernel == 'linear':
        affinity = F.relu(fg_embed @ fg_embed.t())
    else:
        assert False

    return affinity
