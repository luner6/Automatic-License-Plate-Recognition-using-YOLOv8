
# region Imports

import numpy as np
import cv2
from glob import glob
import os
import matplotlib.pyplot as plt


#region Functions

def  video_splitter(Video_path):
    cap = cv2.VideoCapture(Video_path)
   
    # Get frames per second (FPS) and initialize frame number
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_number = 0
   
    # list of all the frames 
    Frame_list = []

    # Check if the video opened successfully
    if not cap.isOpened():
        print("Error opening video file")
        return None

   

    while True:
        # Set,read and store the frame 
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        fname = f"C:\\plate_reader_frames\\image_{frame_number}.png"
        print(f"saving file to {fname}")
        
        
        if not ret:
            print("End of video or error reading frame")
            break 

        cv2.imwrite(fname,frame) 

        # Move to the next frame (1-second interval)
        frame_number += fps

    # stops using the video, stops memory leaks
    cap.release()
    
    
def get_frames(folder_path):
   
    return glob(os.path.join(folder_path, "*.png"))


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


def main():

    print("... Running License Plate Recognizition on our own.")

    video_splitter("C:\\plate_reader_frames\\test_video.mp4")




if __name__ == "__main__":
    main()
