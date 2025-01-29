


# process the 1 minute video and extract one frame every 10 secs. 
# open the video; loop thru and do cv2.save() to a folder. 
# use the content of the folder to process the image with the new_main.py; using only the images.

def split_the_video(videofile):

    print('... input a video file mp4 ')

    cap = cv2.VideoCapture('./sample.mp4')



# read frames
frame_nmr = -1
ret = True
while ret:
    frame_nmr += 1
    ret, frame = cap.read()