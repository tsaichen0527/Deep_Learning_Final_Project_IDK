import tkinter as tk
from tkinter import filedialog
from process import Process
import os

class GUI:
    def __init__(self, master):
        self.num_of_class = 5

        self.master = master
        master.title("Tracker")

        self.objs = [tk.StringVar() for _ in range(self.num_of_class)]
        self.objs[0].set("Pedestrian")
        self.objs[1].set("Car")
        self.objs[2].set("Bicycle")
        self.objs[3].set("Motorcycle")
        self.objs[4].set("Cyclist")

        self.track_threshs = [tk.DoubleVar() for _ in range(self.num_of_class)]
        self.match_threshs = [tk.DoubleVar() for _ in range(self.num_of_class)]
        self.track_buffers = [tk.IntVar() for _ in range(self.num_of_class)]

        self.folder_txt = tk.StringVar()
        self.folder_txt.set("")
        self.result_txt = tk.StringVar()
        self.result_txt.set("")

        tk.Button(master, text="Select Result Folder...", command=self.get_folder).pack()
        tk.Label(master, textvariable=self.folder_txt).pack()

        self.sub_frames = [tk.Frame(self.master) for _ in range(self.num_of_class)]
        for i in range(self.num_of_class):
            tk.Label(self.sub_frames[i], text=(str(i) + "th " + "object: ")).pack(side=tk.LEFT)
            tk.Entry(self.sub_frames[i], textvariable=self.objs[i]).pack(side=tk.LEFT)

            tk.Label(self.sub_frames[i], text=("Track Thresh: ")).pack(side=tk.LEFT)
            tk.Entry(self.sub_frames[i], textvariable=self.track_threshs[i]).pack(side=tk.LEFT)
            self.track_threshs[i].set(0.5)

            tk.Label(self.sub_frames[i], text=("Match Thresh: ")).pack(side=tk.LEFT)
            tk.Entry(self.sub_frames[i], textvariable=self.match_threshs[i]).pack(side=tk.LEFT)
            self.match_threshs[i].set(0.8)

            tk.Label(self.sub_frames[i], text=("Track Buffer: ")).pack(side=tk.LEFT)
            tk.Entry(self.sub_frames[i], textvariable=self.track_buffers[i]).pack(side=tk.LEFT)
            self.track_buffers[i].set(100)
            self.sub_frames[i].pack()
        
        tk.Button(master, text="Start Tracking", command=self.start_tracking).pack()
        tk.Label(master, textvariable=self.result_txt).pack()        
        
    def get_folder(self):
        self.folder = filedialog.askdirectory()
        self.folder_txt.set("Choosen Folder: " + self.folder)
        self.result_txt.set("")
    
    def start_tracking(self):
        process = Process(self.folder, self.track_threshs, self.match_threshs, self.track_buffers)
        self.results = process.start()
        self.result_txt.set("")
        txt = ""
        i = 0
        for result in self.results:
            txt += ("Number Of " + self.objs[i].get() + "s: " + str(result) + os.linesep)
            i += 1
        self.result_txt.set(txt)