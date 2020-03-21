from sklearn.metrics.pairwise import cosine_similarity
from img2vec_keras import Img2Vec
import numpy as np
import glob
import os
from tqdm import tqdm

img2vec = Img2Vec()

def get_video_ranks(query_image, embeds_path):
    
    video_list = glob.glob(os.path.join(embeds_path, '*.npy'))

    video_ranks = dict()
    
    for video_feats in tqdm(video_list):
        
        video_id = video_feats.split("/")[-1].split(".")[0]
        video_embedding = np.load(video_feats)
        
        similarities = np.zeros((len(video_embedding)))
    
        i = 0
        for vec in video_embedding:
            similarities[i] = cosine_similarity(query_image, vec.reshape(1, -1))
            i += 1
        
        video_ranks[video_id] = max(similarities)
    
    return video_ranks


def main():
    
    query_image_path = "queries/cheetah.png"
    query_image = img2vec.get_vec(query_image_path).reshape(1, -1)
    
    video_ranks = get_video_ranks(query_image, "data/embeds/resnet50")
    
    print(video_ranks)

main()