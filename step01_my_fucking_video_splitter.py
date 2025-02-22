
# region Imports

import numpy as np
import cv2
from glob import glob
import os
import matplotlib.pyplot as plt
import argparse
import json

#region variables


#region Functions

def  video_splitter(video_path, output_folder):
    
    cap = cv2.VideoCapture(video_path)

    #TODO  ouput folder shall be cleaned for OS independence
   
    # Get frames per second (FPS) and initialize frame number
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_number = 0

    
    if not cap.isOpened():
        print("Error opening video file")
        return None

   

    while True:
        # Set,read and store the frame 
       
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        fname = os.path.join(output_folder, f"frame_{frame_number}.png")
        

        print(f"saving file to {fname}")
        
        
        if not ret:
            print("End of video or error reading frame")
            break 

        cv2.imwrite(fname,frame) 

        # Move to the next frame (1-second interval)
        frame_number += fps

    # stops using the video, stops memory leaks
    cap.release()
    

def get_frames(output_folder):
   
    return glob(os.path.join(output_folder, "*.png"))


def display_image_timed(img, duration=3):
    """
    Display an image for a specified duration using matplotlib.
    
    Parameters:
    image_path (str): Path to the image file
    duration (float): Time in seconds to display the image (default: 3)
    """
    # Read and display the image
    plt.clf()
    plt.imshow(img)
    
    # Remove axes for cleaner display
    plt.axis('off')
    
    # Show the image without blocking
    plt.draw()
    plt.pause(duration)
    plt.close("all")

    
# endregion


def load_config(config_path="config.json"):
    with open(config_path, "r") as file:
        return json.load(file)
    

def main():

    print("... Running License Plate Recognizition of our own.")
    
    parser = argparse.ArgumentParser(description="Process input and output folder paths along with a filename.")
    parser.add_argument("-uc", "--use_config", action="store_true", help="Flag to use the config file or not.")
    parser.add_argument("-if", "--input_folder", default="./input", help="Path to the input folder (default: ./input)")
    parser.add_argument("-of", "--output_folder", default="./output", help="Path to the output folder (default: ./output)")
    parser.add_argument("-fname", "--filename", default="default.mp4", help="Filename to process (default: default.txt)")

    args = parser.parse_args()

    if args.use_config:
        config = load_config()
        default_input_folder = config["input_folder"] 
        default_output_folder = config["output_folder"]
        default_file_name = config["filename"]
    
    else:
       
        default_input_folder = args.input_folder 
        default_output_folder = args.output_folder
        default_file_name = args.filename

    source_video_path = os.path.join(default_input_folder, default_file_name)
    destination_frame_path = os.path.join(default_output_folder)
    
    print(f"Input File Path: {source_video_path}")
    print(f"Output File Path: {destination_frame_path}")

    video_splitter(source_video_path, destination_frame_path)


if __name__ == "__main__":
    main()
