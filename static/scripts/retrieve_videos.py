from sklearn.metrics.pairwise import cosine_similarity
from image_to_vec import Img2Vec
import numpy as np
import glob
import os
import sys
from tqdm import tqdm
import time

img2vec = Img2Vec()

root = os.path.join(os.path.expanduser('~'), ".viraliq")

def get_video_ranks(query_image, embeds_path):
    
    video_list = glob.glob(os.path.join(embeds_path, '*.npy'))

    video_ranks = dict()
    
    for video_feats in video_list:
        
        video_id = video_feats.split(os.path.sep)[-1].split(".")[0]
        video_embedding = np.load(video_feats)
        
        similarities = np.zeros((len(video_embedding)))
    
        i = 0
        for vec in video_embedding:
            similarities[i] = cosine_similarity(query_image, vec.reshape(1, -1))
            i += 1
        
        video_ranks[video_id] = max(similarities)
    
    return video_ranks


def main():
    
    query_image_path = sys.argv[1]
    print(query_image_path)
    query_image = img2vec.get_vec(query_image_path).reshape(1, -1)

    x1 = time.time()
    
    video_ranks = get_video_ranks(query_image, os.path.join(root, "data", "embeds", "resnet50"))

    x2 = time.time()
    
    return video_ranks

    

vr = main()


ranks = []
for i in sorted(vr) : 
    ranks.append((i, vr[i]))
    
ranks.sort(key = lambda x: x[1], reverse = True)
print('ranks', ",".join([x + ":" + str(y) for (x, y) in ranks]))

    
