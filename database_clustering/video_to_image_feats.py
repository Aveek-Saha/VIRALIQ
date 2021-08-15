import shutil
import subprocess
import glob
from tqdm import tqdm
import numpy as np
import os

from .image_to_vec import Img2Vec
img2vec = Img2Vec()

C, H, W = 3, 224, 224

root = os.path.join(os.path.expanduser('~'), ".viraliq")
if not os.path.exists(root):
    os.makedirs(root)

def extract_frames(video, dst, fps):
    with open(os.devnull, "w") as ffmpeg_log:
        if os.path.exists(dst):
            shutil.rmtree(dst)
        os.makedirs(dst)
        # print('{0}'.format(dst) + os.sep + '%06d.jpg')
        video_to_frames_command = ["ffmpeg",
                                   # (optional) overwrite output file if it exists
                                   '-y',
                                   '-i', video,  # input file
                                   '-vf', "scale=224:224",  # input file
                                   '-r', '{0}'.format(fps),
                                   '-qscale:v', "2",  # quality for JPEG
                                   '{0}\%06d.jpg'.format(dst)]
        subprocess.call(video_to_frames_command,
                        stdout=ffmpeg_log, stderr=ffmpeg_log)


def extract_feats(params):
    global C, H, W

    dir_fc = params['output_dir']
    if not os.path.isdir(dir_fc):
        os.makedirs(dir_fc)
    # print("save video feats to %s" % (dir_fc))
    video_list = glob.glob(os.path.join(params['video_path'], '*.mp4'))
    # print(video_list)
    count = 0
    for video in tqdm(video_list):
        count+= 1
        video_id = video.split(os.path.sep)[-1].split(".")[0]
        dst = os.path.join(root, params['model'] + '_' + video_id)
        
        extract_frames(video, dst, params['frames_per_sec'])

        # video_length = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
        #                      "format=duration", "-of",
        #                      "default=noprint_wrappers=1:nokey=1", video],
        # stdout=subprocess.PIPE,
        # stderr=subprocess.STDOUT)
        
        image_list = sorted(glob.glob(os.path.join(dst, '*.jpg')))
        # samples = np.round(np.linspace(
        #     0, len(image_list) - 1, int(float((video_length.stdout[:2]))) * params['frames_per_sec']))
        
        # image_list = [image_list[int(sample)] for sample in samples]
            
        # fc_feats = []
        frames = []
        for image in image_list:
            frames.append(image)
        # fc_feats.append(img2vec.get_vec(frames))
        img_feats = img2vec.get_vec(frames)

        # img_feats = np.array(fc_feats)
        # Save the inception features
        outfile = os.path.join(dir_fc, video_id + '.npy')
        np.save(outfile, img_feats)
        # cleanup
        shutil.rmtree(dst)
        # print('Finished,', count/len(video_list))

def video_to_image_feats(video_path, feats_path, frames_per_sec):
    
    params = {'output_dir':feats_path, 'video_path':video_path, 'model':'resnet152', 'frames_per_sec':frames_per_sec}
    
    extract_feats(params)