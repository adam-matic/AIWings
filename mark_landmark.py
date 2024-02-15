import sys
import warnings
import glob
import deeplabcut as dlc
import pandas as pd

def get_index(data, scorer, img_name):
    for i in range(len(data)):
        if data.iloc[i][scorer].name == img_name: return i
    return None


def get_folder():
    from tkinter import filedialog
    from tkinter import Tk
    
    root = Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    folder_selected = folder_selected.replace("/", "\\")
    return folder_selected


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    model_folder = "C:/Users/LUPA/Documents/AI_wings_dlc/"

    folder = get_folder()
    print("Analyzing " + folder)
    subfolders = glob.glob(folder + "\\*\\")

    for s in subfolders:
        dlc.analyze_time_lapse_frames(model_folder + "config.yaml", s, frametype=".tif", shuffle=1, trainingsetindex=0, gputouse=None)
        
        data_file = glob.glob(s + "\\*.h5")[0]
        data = pd.read_hdf(data_file)
        tps_file_name = s + folder[folder.rfind("\\")+1:] + "_AI.TPS"
        f = open(tps_file_name, "w")
        scorer = data.columns[0][0]
        
        
        #data.sort_values(by="name")
        
        for id in range(len(data)):
            image_fn = data.iloc[id].name
            f.write("LM=15\n")
            idx = get_index(data, scorer, image_fn)
            if idx is None: continue
            for k in range(15):
                x = data.iloc[idx][scorer].iloc[k*3]
                y = data.iloc[idx][scorer].iloc[k*3 + 1]
                y = 1920 - y
                f.write(f"{x:.5f} {y:.5f}\n")
            f.write(f"IMAGE={image_fn}\n")
            f.write(f"ID={id}\n")

        f.close()