# Graph Based Temporal Aggregation for Video Retrieval

[![Build/Publish](https://github.com/Aveek-Saha/VIRALIQ/actions/workflows/python-publish.yml/badge.svg)](https://github.com/Aveek-Saha/VIRALIQ/actions/workflows/python-publish.yml)
[![PWC](https://img.shields.io/endpoint.svg?url=https://paperswithcode.com/badge/graph-based-temporal-aggregation-for-video/video-retrieval-on-msr-vtt)](https://paperswithcode.com/sota/video-retrieval-on-msr-vtt?p=graph-based-temporal-aggregation-for-video)

**VIRALIQ**: **VI**deo Retrev**AL** through **I**mage **Q**ueries

## Dependencies

### FFmpeg
FFmpeg is required for extracting frames from videos. Download links can be found [here](https://ffmpeg.org/download.html).

**Note:** Windows users will have to add the FFmpeg bin folder to the PATH variable.


## Installation

Install the package using pip
```
pip install viraliq
```

## CLI usage

### Create embeddings
Create video embeddings
```
viraliq cluster "PATH_TO_VIDEO_DIR"
```

### Search
Search using an image query
```
viraliq search "PATH_TO_VIDEO_DIR" "PATH_TO_IMAGE"
```

## Citing

If you find VIRALIQ useful please cite the following paper:

```
Srinivasan, Arvind, Aprameya Bharadwaj, Aveek Saha, and Subramanyam Natarajan. "Graph Based Temporal Aggregation for Video Retrieval." arXiv preprint arXiv:2011.02426 (2020).
```