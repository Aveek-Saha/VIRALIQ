import numpy as np
from sklearn.cluster import KMeans
from tqdm import tqdm
import os
import glob
# from image_to_vec import Img2Vec
from sklearn.metrics.pairwise import cosine_similarity

def create_video_embeddings(feats_path, metadata_path):
    if not os.path.isdir(metadata_path):
        os.makedirs(metadata_path)

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
        
    n_clus = 10 
        
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

    best_neighbors = np.array(best_neighbors)
    outfile = os.path.join(metadata_path, 'neighbours.npy')
    np.save(outfile, best_neighbors)

    centers = np.array(centers)
    outfile = os.path.join(metadata_path, 'centers.npy')
    np.save(outfile, centers)

    outfile = os.path.join(metadata_path, 'labels.npy')
    np.save(outfile, labels)



# parser = argparse.ArgumentParser(description="""
# This script Will create a video embeddings for your entire database
# """)
# parser.add_argument("--folder", help="Path of the folder containing videos")

# args = parser.parse_args()

# FOLDER = args.folder


# video_to_image_feats(FOLDER, feats_path, 2)

# create_video_embeddings(feats_path, metadata_path)
