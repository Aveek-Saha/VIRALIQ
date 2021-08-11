# Graph Based Temporal Aggregation for Video Retrieval

[![PWC](https://img.shields.io/endpoint.svg?url=https://paperswithcode.com/badge/graph-based-temporal-aggregation-for-video/video-retrieval-on-msr-vtt)](https://paperswithcode.com/sota/video-retrieval-on-msr-vtt?p=graph-based-temporal-aggregation-for-video)

**VIRALIQ**: **VI**deo Retrev**AL** through **I**mage **Q**ueries

<!-- 1. Cluster the whole database
2. Cluster every video separately -->

# Dependencies

## Python dependencies
All python packages required can be installed from `requirements.txt`

```
pip install -r requirements.txt
```

## FFmpeg

FFmpeg is required for extracting frames from videos. Download links can be found [here](https://ffmpeg.org/download.html).

**Note:** Windows users will have to add the FFmpeg bin folder to the PATH variable.

# Instructions for execution

1. Create cluster embeddings
1. Perform image queries