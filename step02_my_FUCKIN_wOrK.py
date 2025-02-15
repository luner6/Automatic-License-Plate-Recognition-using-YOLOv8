from ultralytics import YOLO
import cv2
import util
from sort import *
from util import get_car, read_license_plate, write_csv
from glob import glob
from functions import get_frames,display_image_timed
import matplotlib.pyplot as plt




def proccessing_frames_from_videos():
    results = {}

    mot_tracker = Sort()

    # load models
    coco_model = YOLO('yolov8n.pt')
    license_plate_detector = YOLO('license_plate_detector.pt')

    # load video
    cap = cv2.VideoCapture('C:\\plate_reader_frames\\test_video.mp4')

    vehicles = [2, 3, 5, 7]

    # read frames
    frame_nmr = -1
    ret = True
    while ret:
        frame_nmr += 1
        ret, frame = cap.read()
        if ret:
            results[frame_nmr] = {}
            # detect vehicles
            detections = coco_model(frame)[0]
            detections_ = []
            for detection in detections.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = detection
                if int(class_id) in vehicles:
                    detections_.append([x1, y1, x2, y2, score])

            # track vehicles
            track_ids = mot_tracker.update(np.asarray(detections_))

            # detect license plates
            license_plates = license_plate_detector(frame)[0]
            for license_plate in license_plates.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = license_plate

                # assign license plate to car
                xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, track_ids)

                if car_id != -1:

                    # crop license plate
                    license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]

                    # process license plate
                    license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                    _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)

                    # read license plate number
                    license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_thresh)

                    if license_plate_text is not None:
                        results[frame_nmr][car_id] = {'car': {'bbox': [xcar1, ycar1, xcar2, ycar2]},
                                                    'license_plate': {'bbox': [x1, y1, x2, y2],
                                                                        'text': license_plate_text,
                                                                        'bbox_score': score,
                                                                        'text_score': license_plate_text_score}}

    # write results
    write_csv(results, './test.csv')



def proccessing_individual_frames():

    print("... Running License Plate Recognizition on our own.")

    results = {}

    mot_tracker = Sort()

    # load models
    coco_model = YOLO('yolov8n.pt')
    license_plate_detector = YOLO('license_plate_detector.pt')

    # load video
    #cap = cv2.VideoCapture('C:\\plate_reader_frames\\test_video.mp4') 
    #TODO   call to a function that returns a list of images from plate_data
    # use glob.glob
    #frame_list = get_image_list(path to folder with frames)
    
    frame_list = get_frames("/Users/rpglover/AAAPROJ/plate_reader/yolo8_data")
    
    vehicles = [2, 3, 5, 7]

    # read frames
    frame_nmr = -1
    ret = True
    for frame_name in frame_list :
        frame_nmr += 1
        print(f"... proccessing frame {frame_nmr} of {len(frame_list)}")
        frame = cv2.imread(frame_name)
        if frame is not None:
            display_image_timed(frame,1)
            ret = True
        else:
            ret = False
            print(f"Error: Could not load image at {frame_name}")
       
     
            
            
        if ret:
            results[frame_nmr] = {}
            # detect vehicles
            detections = coco_model(frame)[0]
            detections_ = []
            for detection in detections.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = detection
                if int(class_id) in vehicles:
                    detections_.append([x1, y1, x2, y2, score])

            # track vehicles
            track_ids = mot_tracker.update(np.asarray(detections_))

            # detect license plates
            license_plates = license_plate_detector(frame)[0]
            for license_plate in license_plates.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = license_plate

                # assign license plate to car
                xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, track_ids)

                if car_id != -1:

                    # crop license plate
                    license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]

                    # process license plate
                    license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                    _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)

                    # read license plate number
                    license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_thresh)

                    if license_plate_text is not None:
                        results[frame_nmr][car_id] = {'car': {'bbox': [xcar1, ycar1, xcar2, ycar2]},
                                                    'license_plate': {'bbox': [x1, y1, x2, y2],
                                                                        'text': license_plate_text,
                                                                        'bbox_score': score,
                                                                        'text_score': license_plate_text_score}}

# write results
    write_csv(results, './test.csv')




if __name__ == "__main__":

    
    proccessing_individual_frames()

    # proccessing_frames_from_videos()