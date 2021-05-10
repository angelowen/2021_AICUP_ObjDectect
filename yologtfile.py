import json
import os

wr_dir = "./yologt/"
if not os.path.exists(wr_dir):
    os.makedirs(wr_dir)
json_src = "./TrainDataset/json/"
files = os.listdir(json_src)

for name in files:
    filename = json_src+name ## open filename
    write_name = wr_dir+name.split('.')[0]+'.txt' ## writing filename
    print(filename)
    with open(write_name, 'w') as fw:
        with open(filename,'r') as fr:
            data = json.load(fr)
            H = float(data["imageHeight"])
            W = float(data["imageWidth"])
            for item in data["shapes"]:
                points = []  # xl_up ,yl_up ,xr_up ,yr_up ,xr_dn ,yr_dn ,xl_dn ,yl_dn
                for point in item["points"]:
                    x,y = point
                    points.append(x)
                    points.append(y)
                g_id = item["group_id"]
                ## change don't care item class index
                if g_id == 255:
                    g_id = 6
                ###    
                xl_up ,yl_up ,xr_up ,yr_up ,xr_dn ,yr_dn ,xl_dn ,yl_dn = points
                x_center = (xl_up+xr_dn)/2/W
                y_center = (yl_up+yr_dn)/2/H
                width = max(xr_up - xl_up,xr_dn - xl_dn)/W
                height = max(yl_dn - yl_up,yr_dn - yr_up)/H
                fw.write(f"{g_id} {x_center} {y_center} {width} {height}\n")
