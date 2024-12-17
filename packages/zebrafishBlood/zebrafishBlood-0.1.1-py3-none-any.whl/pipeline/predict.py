import numpy as np
from ultralytics import YOLO

def predict(MODEL, IPATH, devicenum):
    # results = MODEL(source=IPATH, device=devicenum, max_det=1000, save=True, save_txt=True, save_conf=True, line_width=1, verbose=False)
    results = MODEL(source=IPATH, device=devicenum, max_det=1000, verbose=False)
    # return results[0].save_dir
    return np.unique(results[0].boxes.cls.cpu().numpy(), return_counts=True)