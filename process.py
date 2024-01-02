import numpy as np
from byte_tracker import BYTETracker
import os
import re

class Process:
    def __init__(self):
        self.test_folder = "/Users/lvyijing/Desktop/final/Deep_Learning_Final_Project_IDK/test"
        self.detections0 = []
        self.detections1 = []
        self.detections2 = []
        self.detections3 = []
        self.detections4 = []
        np.float=float
        self.fixed_confidences = 1

    def start(self):
        files = os.listdir(self.test_folder)
        files = sorted(files, key=lambda x: int(re.search(r'\d+', x).group()))
        for file in files:
            lines = self.read_file(os.path.join(self.test_folder, file))
            self.get_detections(lines)

        tracks0 = self.get_tracks(self.detections0)
        tracks1 = self.get_tracks(self.detections1)
        tracks2 = self.get_tracks(self.detections2)
        tracks3 = self.get_tracks(self.detections3)
        tracks4 = self.get_tracks(self.detections4)
        print('0: ', self.get_total_id(tracks0))
        print('1: ', self.get_total_id(tracks1))
        print('2: ', self.get_total_id(tracks2))
        print('3: ', self.get_total_id(tracks3))
        print('4: ', self.get_total_id(tracks4))

    # 取得物體的數量
    def get_total_id(self, tracks):
        max = 0
        for track in tracks:
            if (track.track_id > max):
                max = track.track_id
        return max
        
    # 對每個 frame 抓出各物體的座標、confidence 資訊，整理到 detections
    def get_detections(self, lines):
        detection0 = []
        detection1 = []
        detection2 = []
        detection3 = []
        detection4 = []

        for line in lines:
            parts = line.strip().split()
            label = int(parts[0])
            confidences = self.fixed_confidences
            coord = [float(x) for x in parts[1:5]]
            l, t = float(coord[0]), float(coord[1])
            r, b = float(coord[2]), float(coord[3])
            if label == 0:
                detection0.append([l, t, r, b, confidences])
            elif label == 1:
                detection1.append([l, t, r, b, confidences])
            elif label == 2:
                detection2.append([l, t, r, b, confidences])
            elif label == 3:
                detection3.append([l, t, r, b, confidences])
            elif label == 4:
                detection4.append([l, t, r, b, confidences])

        self.detections0 += [detection0]
        self.detections1 += [detection1]
        self.detections2 += [detection2]
        self.detections3 += [detection3]
        self.detections4 += [detection4]

    def read_file(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        return lines

    # 讓 tracker 訓練
    def get_tracks(self, detections):
        class BYTETrackerArgs:
            def __init__(self):
                self.track_thresh = 0.25
                self.track_buffer = 30 # To-do: 不同物體，使用合理的 buffer
                self.match_thresh = 0.8
                self.aspect_ratio_thresh = 3.0
                self.min_box_area = 1.0
                self.mot20 = False

        byte_tracker_args = BYTETrackerArgs()
        byte_tracker = BYTETracker(byte_tracker_args)

        tracks = []
        for detection in detections:
            np_arr_det = np.array(detection, dtype=float)

            # 若此 frame 沒有物體，放入 0 array
            if (np_arr_det.ndim == 1):
                np_arr_det = np.array([[0, 0, 0, 0, 0]])
                
            # To-do: 設定正確的 img_info, img_size
            track = byte_tracker.update(output_results=np.array(np_arr_det, dtype=float), img_info=(1000, 1000), img_size=(1000, 1000))
            tracks = tracks + track
            # print('next frame---------------')
            # for trac in track:
            #     print('track: frame: ', trac.frame_id)
            #     print('loc ', trac.location)
            #     print('time ', trac.time_since_update)
            #     print('id ', trac.track_id)

        return tracks