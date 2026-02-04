'''
Evaluate IoU, DICE, and F1 score
**Segmentation file name must match the ground truth image name exactly.**
'''
import numpy as np
import cv2
import pandas as pd
import os

def read_mask(path:str):
    mask = cv2.imread(path)
    if mask is None: raise ValueError
    
    return mask > 0
    
    
def evaluation_metric(gt:np.ndarray, seg:np.ndarray) -> dict:
    # return {iou, DICE, f1score, accuracy, recall, precision, TP, FN, FP, TN}
    
    tp = np.logical_and(gt, seg).sum()
    fn = np.logical_and(gt, ~seg).sum()
    fp = np.logical_and(~gt, seg).sum()
    tn = np.logical_and(~gt, ~seg).sum()
    
    accuracy = (tp+tn)/(tp+fn+fp+tn)
    recall = tp/(tp+fn)
    precision = tp/(tp+fp)
    
    f1score = 2*precision*recall/(precision+recall) if (precision+recall)!=0 else 0
    iou = tp/(tp+fn+fp) if (tp+fn+fp)!=0 else 0
    dice = 2*tp/(2*tp+fn+fp) if (2*tp+fn+fp)!=0 else 0
    
    return {
        "iou":iou,
        "dice":dice,
        "f1_score":f1score, 
        "accuracy": accuracy, 
        "recall": recall, 
        "precision": precision, 
        "tp": tp, 
        "fn": fn, 
        "fp": fp, 
        "tn": tn
        }


GT_DIR  = 'D:\mc\py\pakineeRNV\data\drac_split_gt';    # ground truth folder
SEG_DIR = 'D:\mc\py\pakineeRNV\data\gvf\median\segmentation';   # segmentation folder

valid_filenames = []
evaluations = []

for filename in os.listdir(GT_DIR):
    gt_path = os.path.join(GT_DIR, filename)
    
    # If you use different names for gt and segment, you will need to change this logic na kubb.
    seg_path = os.path.join(SEG_DIR, filename)
    
    if not os.path.exists(seg_path):
        print(f"missing segmentation for {filename} gt")
        continue
    
    gt, seg = read_mask(gt_path), read_mask(seg_path)
    evaluations.append(evaluation_metric(gt, seg))
    valid_filenames.append(filename)

df = pd.DataFrame({
    "filename":valid_filenames,
})
df_f1 = pd.DataFrame(evaluations)

df = pd.concat([df, df_f1], axis=1)
df.to_csv("evaluation.csv")