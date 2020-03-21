import shutil
import subprocess
import glob
from tqdm import tqdm
import numpy as np
import os

import torch

from img2vec_keras import Img2Vec
img2vec = Img2Vec()

C, H, W = 3, 224, 224


def extract_frames(video, dst):
    with open(os.devnull, "w") as ffmpeg_log:
        if os.path.exists(dst):
            print(" cleanup: " + dst + "/")
            shutil.rmtree(dst)
        os.makedirs(dst)
        print('{0}/%06d.jpg'.format(dst))
        video_to_frames_command = ["ffmpeg",
                                   # (optional) overwrite output file if it exists
                                   '-y',
                                   '-i', video,  # input file
                                   '-vf', "scale=400:300",  # input file
                                   '-qscale:v', "2",  # quality for JPEG
                                   '{0}/%06d.jpg'.format(dst)]
        subprocess.call(video_to_frames_command,
                        stdout=ffmpeg_log, stderr=ffmpeg_log)


def extract_feats(params, model, load_image_fn):
    global C, H, W
    model.eval()

    dir_fc = params['output_dir']
    if not os.path.isdir(dir_fc):
        os.mkdir(dir_fc)
    print("save video feats to %s" % (dir_fc))
    video_list = glob.glob(os.path.join(params['video_path'], '*.mp4'))
    for video in tqdm(video_list):
        video_id = video.split("/")[-1].split(".")[0]
        dst = params['model'] + '_' + video_id
        extract_frames(video, dst)

        video_length = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", video],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
        
        image_list = sorted(glob.glob(os.path.join(dst, '*.jpg')))
        samples = np.round(np.linspace(
            0, len(image_list) - 1, int(video_length.stdout[:2]) * params['frames_per_sec']))
        
        
        image_list = [image_list[int(sample)] for sample in samples]
            
        fc_feats = []
        for i in range(len(image_list)):
            with torch.no_grad():
                #print(images)
                fc_feats.append(img2vec.get_vec(image_list[i]))
                
        img_feats = np.array(fc_feats)
        # Save the inception features
        outfile = os.path.join(dir_fc, video_id + '.npy')
        np.save(outfile, img_feats)
        # cleanup
        shutil.rmtree(dst)

def video_to_image_feats(video_path, feats_path, frames_per_sec):
    
    params = {'output_dir':feats_path, 'video_path':video_path, 'model':'resnet50', 'frames_per_sec':frames_per_sec}
    
    extract_feats(params)
