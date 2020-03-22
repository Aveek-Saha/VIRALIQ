import numpy as np
from sklearn.cluster import KMeans
from tqdm import tqdm
import os
import glob

from video_to_image_feats import video_to_image_feats


def get_video_embedding(feats_path):
    vex = np.load(feats_path)
    
    n_clus = len(vex)//10
    
    kmeans = KMeans(n_clusters=n_clus, random_state=0).fit(vex)
    centers = kmeans.cluster_centers_
    
    
    adj_mat = np.zeros((n_clus,n_clus))
    for i in range(len(kmeans.labels_)-1):
        if(kmeans.labels_[i] != kmeans.labels_[i+1]):
            adj_mat[kmeans.labels_[i]][kmeans.labels_[i+1]] += 1
            adj_mat[kmeans.labels_[i+1]][kmeans.labels_[i]] += 1
            
    for i in range(n_clus):
        adj_mat[i][i] = 1
    
    neighs = np.matmul(adj_mat, centers)
    
    for x in range(len(neighs)):
        neighs[x] /= sum(adj_mat[x])
        
    final_embed = np.add(centers, neighs)
    final_embed /= 2
    
    return final_embed

def create_video_embeddings(feats_path, embeds_path):
    
    feats_list = glob.glob(os.path.join(feats_path, '*.npy'))
    
    for video_feats in tqdm(feats_list):
        video_id = video_feats.split("/")[-1]
        embedding = get_video_embedding(video_feats)
        np.save(os.path.join(embeds_path, video_id), embedding)

      
video_to_image_feats("data/train-video", "data/feats/resnet50", 2)

create_video_embeddings("data/feats/resnet50", "data/embeds/resnet50")
