import numpy as np
from byte_tracker import BYTETracker
import os
import re

class Process:
    def __init__(self, folder, track_threshs, match_threshs, track_buffers):
        self.folder = folder
        self.track_threshs = track_threshs
        self.match_threshs = match_threshs
        self.track_buffers = track_buffers
        self.detections_arr = [[] for _ in range(5)]
        np.float=float
        self.fixed_confidences = 1

    def start(self):
        files = os.listdir(self.folder)
        files = sorted(files, key=lambda x: int(re.search(r'\d+', x).group()))
        for file in files:
            lines = self.read_file(os.path.join(self.folder, file))
            self.get_detections(lines)

        total_id_arr = []
        for i in range(5):
            tracks = self.get_tracks(self.detections_arr[i], track_thresh=self.track_threshs[i], match_thresh=self.match_threshs[i], track_buffer=self.track_buffers[i])
            total_id_arr += [self.get_total_id(tracks)]
        return total_id_arr

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

        self.detections_arr[0] += [detection0]
        self.detections_arr[1] += [detection1]
        self.detections_arr[2] += [detection2]
        self.detections_arr[3] += [detection3]
        self.detections_arr[4] += [detection4]

    def read_file(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        return lines

    # 讓 tracker 訓練
    def get_tracks(self, detections, track_thresh, match_thresh, track_buffer):
        class BYTETrackerArgs:
            def __init__(self, track_thresh, match_thresh, track_buffer):
                self.track_thresh = track_thresh
                self.match_thresh = match_thresh
                self.track_buffer = track_buffer
                self.aspect_ratio_thresh = 3.0
                self.min_box_area = 1.0
                self.mot20 = False

        byte_tracker_args = BYTETrackerArgs(track_thresh.get(), match_thresh.get(), track_buffer.get())
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