import numpy as np
from sklearn.cluster import KMeans
from tqdm import tqdm
import os
import glob
from image_to_vec import Img2Vec
from sklearn.metrics.pairwise import cosine_similarity
import json
import re
import copy

feats_path = "testdata/feats/resnet152"

feats_list = glob.glob(os.path.join(feats_path, '*.npy'))

embeddings = []
feat_to_video = dict()

video_lengths = []

for video_feats in tqdm(feats_list):
    video_id = video_feats.split("/")[-1]
    vex = np.load(video_feats)
    
    video_lengths.append(len(vex))
    
    for feat in vex:
        feat_to_video[tuple(feat)] = video_id
    
    embeddings.extend(vex)   
    
n_clus = 200 
    
kmeans = KMeans(n_clusters = n_clus, random_state=0).fit(embeddings)
centers = kmeans.cluster_centers_
labels = kmeans.labels_


adj_mat = np.zeros((n_clus,n_clus))

index = 0
for vl in video_lengths:
    for i in range(vl-1):
        adj_mat[labels[index]][labels[index+1]] += 1
        adj_mat[labels[index+1]][labels[index]] += 1
        index += 1
    index += 1
    
for i in range(n_clus):
    adj_mat[i][i] += 1

neighs = np.matmul(adj_mat, centers)

for x in range(len(neighs)):
    neighs[x] /= sum(adj_mat[x])
    
final_embed = np.add(centers, neighs)
final_embed /= 2

centers = final_embed


centers = list(enumerate(centers))

best_neighbors = []
for i in range(n_clus):
    best = list(enumerate(adj_mat[i]))
    best.sort(key = lambda x: x[1], reverse = True)
    best_neighbors.append([x[0] for x in best])

original_centers = copy.deepcopy(centers)

def remove_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def get_rank_list(query_image_path, query_category_id):
    query_image = img2vec.get_vec(query_image_path).reshape(1, -1)
    centers.sort(key = lambda x: cosine_similarity(query_image, x[1].reshape(1, -1)), reverse = True)
    
    rel_clusters = [centers[0][0]]
    for ni in best_neighbors[centers[0][0]][1:4]:
        rel_clusters.append(original_centers[ni][0])
    
    rel_feats = [embeddings[i] for i in range(len(embeddings)) if labels[i] in rel_clusters]
    
    rel_feats.sort(key = lambda x: cosine_similarity(query_image, x.reshape(1, -1)), reverse = True)
    
    rel_videos = [feat_to_video[tuple(x)] for x in rel_feats]

    rel_videos = remove_duplicates(rel_videos)
    
    return rel_videos

def run_test(query_category_id, query_image_path, K):
    
    fp = open('video_categories.json')
    video_categories = json.loads(fp.read())
    fp.close()
    
    query_image_list = os.listdir(os.path.join("queries", "category_" + str(query_category_id)))
    query_image_list = [os.path.join(query_image_path, "category_" + str(query_category_id), query_image) for query_image in query_image_list if (re.match(r".*\.png", query_image) or re.match(r".*\.jp(e|)g", query_image))]
    query_image_list.sort()
    
    total_map = 0
    p_k = []
    
    for query_image_path in query_image_list:
    
        vr = get_rank_list(query_image_path, query_category_id)
        
        '''
        ranks = []
        for i in sorted(vr) : 
            ranks.append((i, vr[i]))
            
        ranks.sort(key = lambda x: x[1], reverse = True)
        '''
        ranks = vr
        
        #Evaluation
        
        #Top K videos
        
        correct_preds = 0
        for i in range(K):
            if(query_category_id == 16):
                if(video_categories[ranks[i].split('.')[0]] == 17):
                    correct_preds += 1
                    continue
            if(video_categories[ranks[i].split('.')[0]] == query_category_id):
                correct_preds += 1
        
        p = (correct_preds/K) * 100
        p_k.append(p)
        
        total_map += p
        
    map_k = total_map / len(query_image_list)
    
    return map_k, p_k


img2vec = Img2Vec()

fp = open('results_resnet152_graph_final.csv', 'w')
fp.write('category_id,K,map_k,p_k1,p_k2,p_k3,p_k4\n')
for category in range(20):
    for k in [5, 10, 20]:
        map_k, p_k = run_test(query_category_id = category, query_image_path = "queries", K = k)
        write_str = str(category) + "," + str(k) + "," + str(map_k) + "," + ",".join(map(str, p_k)) + "\n"
        fp.write(write_str)
        print("DONE: " + str(category) + " : " + str(k))
fp.close()

    
fp = open('video_categories.json')
video_categories = json.loads(fp.read())
fp.close()