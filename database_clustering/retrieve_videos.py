from sklearn.metrics.pairwise import cosine_similarity
from .image_to_vec import Img2Vec
import numpy as np
import glob
import os
from tqdm import tqdm
import copy

img2vec = Img2Vec()

root = os.path.join(os.path.expanduser('~'), ".viraliq")


def remove_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def get_video_ranks(query_image_path, feats_path, metadata_path):

    query_image = img2vec.get_vec_single(query_image_path).reshape(1, -1)

    feats_list = glob.glob(os.path.join(feats_path, '*.npy'))
    best_neighbors = np.load(os.path.join(metadata_path, 'neighbours.npy'))
    centers = list(np.load(os.path.join(
        metadata_path, 'centers.npy'), allow_pickle=True))
    labels = np.load(os.path.join(metadata_path, 'labels.npy'))

    embeddings = []
    feat_to_video = dict()

    video_lengths = []

    for video_feats in tqdm(feats_list):
        video_id = video_feats.split(os.sep)[-1]
        vex = np.load(video_feats)

        video_lengths.append(len(vex))

        for feat in vex:
            feat_to_video[tuple(feat)] = video_id

        embeddings.extend(vex)

    original_centers = copy.deepcopy(centers)

    centers.sort(key=lambda x: cosine_similarity(
        query_image, x[1].reshape(1, -1)), reverse=True)

    rel_clusters = [centers[0][0]]
    for ni in best_neighbors[centers[0][0]][1:4]:
        rel_clusters.append(original_centers[ni][0])

    rel_feats = [embeddings[i]
                 for i in range(len(embeddings)) if labels[i] in rel_clusters]

    rel_feats.sort(key=lambda x: cosine_similarity(
        query_image, x.reshape(1, -1)), reverse=True)

    rel_videos = [feat_to_video[tuple(x)] for x in rel_feats]

    rel_videos = remove_duplicates(rel_videos)

    return rel_videos


# def main():
#     parser = argparse.ArgumentParser(description="""
#     This script retrieve videos based on an image query
#     """)
#     parser.add_argument("--image", help="Path of the image")

#     args = parser.parse_args()

#     IMAGE = args.image
#     query_image_path = IMAGE
#     print(query_image_path)

#     x1 = time.time()

#     video_ranks = get_video_ranks(query_image_path, os.path.join(
#         root, "data", "feats", "resnet152"), os.path.join(root, "metadata"))

#     x2 = time.time()

#     print(x2 - x1)

#     return video_ranks


# vr = main()
# print(vr)

# ranks = []
# for i in sorted(vr) :
#     ranks.append((i, vr[i]))

# ranks.sort(key = lambda x: x[1], reverse = True)
# print('ranks', ",".join([x + ":" + str(y) for (x, y) in ranks][:5]))
