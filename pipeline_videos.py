#!/usr/bin/env python

import os
import argparse

hf_token = "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"

def main():

    # get arguments from command line
    parser = argparse.ArgumentParser(description='Process videos from a folder and generate .srt, .json and .vrt files')
    parser.add_argument('--input_folder', '-i', type=str, help='folder with videos to process', required=True)
    parser.add_argument('--language', '-l', type=str, help='language of the videos', required=True)

    args = parser.parse_args()

    videos = os.listdir(args.input_folder)
    # loop over videos and process them
    for video in videos:
        if video.endswith(".mp4"):
            # create a folder for each video
            video_folder = os.path.join(args.input_folder, video.split('.')[0])
            if not os.path.exists(video_folder):
                os.mkdir(video_folder)
            # normalize audio and save it in the video folder
            os.system("ffmpeg -y -hide_banner -loglevel error -i " + os.path.join(args.input_folder, video) + " -c:v copy -af loudnorm=I=-23:LRA=7:TP=-2.0:measured_I=-17.31:measured_LRA=5.71:measured_TP=-1.35 "  + os.path.join(video_folder, video.split('.')[0] + ".mp3"))
            # generate json and .srt file
            os.system("whisperx --model large --output_format all --language " + args.language + " --output_dir " + video_folder + " " + os.path.join(video_folder, video.split('.')[0] + ".mp3"))
            # generate .vrt file
            os.system("generate_vrt -i " + os.path.join(video_folder, video.split('.')[0] + ".json") + " -o " + os.path.join(video_folder, video.split('.')[0] + ".vrt"))


if __name__ == "__main__":
    main()