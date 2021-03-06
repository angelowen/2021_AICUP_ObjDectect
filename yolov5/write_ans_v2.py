import argparse
import time,os
from pathlib import Path
import re
import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random
import numpy as np
from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path, save_one_box
from utils.plots import colors, plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized

def extract_peek_ranges_from_array(array_vals, minimun_val=500, minimun_range=20):
    # print(array_vals)
    start_i = None
    end_i = None
    peek_ranges = []
    #enumerate() 函數用於將數據對象組合為一個索引序列，同時列出數據和數據下標
    for i, val in enumerate(array_vals):
        if val > minimun_val and start_i is None:
            start_i = i
        elif val > minimun_val and start_i is not None:
            pass
        elif val < minimun_val and start_i is not None:
            end_i = i
            if end_i - start_i >= minimun_range:
                peek_ranges.append((start_i, end_i))
            start_i = None
            end_i = None
        elif val < minimun_val and start_i is None:
            pass
        else:
            raise ValueError("cannot parse this case...")
    return peek_ranges

def x_crop(img,xyxy):
    # img = cv2.imread('data/images/img_3.jpg')
    c_img = img[int(xyxy[1]):int(xyxy[3]),int(xyxy[0]):int(xyxy[2])] # [y1:y2,x1:x2]
    x_l  = int(xyxy[0])
    y_up = int(xyxy[1])
    
    gray_img = cv2.cvtColor(c_img, cv2.COLOR_BGR2GRAY)
    bilateral = cv2.bilateralFilter(gray_img, 11, 75, 75)
    blur = cv2.GaussianBlur(bilateral,(5,5),1)
    adaptive_threshold = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,11, 2)

    vertical_sum = np.sum(adaptive_threshold, axis=0)
    horizontal_sum = np.sum(adaptive_threshold, axis=1)

    line_seg_adaptive_threshold = np.copy(adaptive_threshold)
    peek_ranges = extract_peek_ranges_from_array(vertical_sum)
    # print("peek:",peek_ranges)
    small_blocks=[]
    for i, peek_range in enumerate(peek_ranges):
        x = peek_range[0]
        y = 0
        w = peek_range[1] - x
        h = line_seg_adaptive_threshold.shape[0]
        pt1 = (x_l + x, y_up + y)
        pt2 = (x_l + x + w, y_up + y + h)
        # print(pt1 ,";", pt2,"\n")
        small_blocks.append(pt1)
        small_blocks.append(pt2)
        #cv2.rectangle(影像, 頂點座標, 對向頂點座標, 顏色, 線條寬度)
        cv2.rectangle(img, pt1, pt2, (0,0,255),2)
    return small_blocks


def y_crop(img,xyxy):
    # img = cv2.imread('data/images/img_3.jpg')
    c_img = img[int(xyxy[1]):int(xyxy[3]),int(xyxy[0]):int(xyxy[2])] # [y1:y2,x1:x2]
    x_l  = int(xyxy[0])
    y_up = int(xyxy[1])
    
    gray_img = cv2.cvtColor(c_img, cv2.COLOR_BGR2GRAY)
    bilateral = cv2.bilateralFilter(gray_img, 11, 75, 75)
    blur = cv2.GaussianBlur(bilateral,(5,5),1) # 7, 7 ,1
    adaptive_threshold = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,11, 2)# 3,2

    vertical_sum = np.sum(adaptive_threshold, axis=0)
    horizontal_sum = np.sum(adaptive_threshold, axis=1)

    line_seg_adaptive_threshold = np.copy(adaptive_threshold)
    peek_ranges = extract_peek_ranges_from_array(vertical_sum)
    small_blocks=[]
    # print("rect positions: ")
    for i, peek_range in enumerate(peek_ranges):
        x = 0
        y = peek_range[0]
        w = line_seg_adaptive_threshold.shape[1]
        h = peek_range[1] - y
        pt1 = (x_l + x, y_up + y)
        pt2 = (x_l + x + w, y_up + y + h)
        # print(pt1 ,";", pt2,"\n")
        small_blocks.append(pt1)
        small_blocks.append(pt2)
        #cv2.rectangle(影像, 頂點座標, 對向頂點座標, 顏色, 線條寬度)
        cv2.rectangle(img, pt1, pt2, (0,0,255),4)
        # print(pt1,pt2)
    return small_blocks

def detect(opt):
    source, weights, view_img, save_txt, imgsz = opt.source, opt.weights, opt.view_img, opt.save_txt, opt.img_size
    save_img = not opt.nosave and not source.endswith('.txt')  # save inference images
    webcam = source.isnumeric() or source.endswith('.txt') or source.lower().startswith(
        ('rtsp://', 'rtmp://', 'http://', 'https://'))

    # Directories
    save_dir = increment_path(Path(opt.project) / opt.name, exist_ok=opt.exist_ok)  # increment run
    (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

    # Initialize
    set_logging()
    device = select_device(opt.device)
    half = device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    model = attempt_load(weights, map_location=device)  # load FP32 model
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(imgsz, s=stride)  # check img_size
    names = model.module.names if hasattr(model, 'module') else model.names  # get class names
    if half:
        model.half()  # to FP16

    # Second-stage classifier
    classify = False
    if classify:
        modelc = load_classifier(name='resnet101', n=2)  # initialize
        modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=device)['model']).to(device).eval()

    # Set Dataloader
    vid_path, vid_writer = None, None
    if webcam:
        view_img = check_imshow()
        cudnn.benchmark = True  # set True to speed up constant image size inference
        dataset = LoadStreams(source, img_size=imgsz, stride=stride)
    else:
        dataset = LoadImages(source, img_size=imgsz, stride=stride)

    # Run inference
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
    t0 = time.time()
    filepath = 'answer.csv'
    if os.path.isfile(filepath):
        os.remove(filepath)
    with open(filepath, 'a') as f:
        for path, img, im0s, vid_cap in dataset:
            img = torch.from_numpy(img).to(device)
            img = img.half() if half else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)


            # Inference
            t1 = time_synchronized()
            pred = model(img, augment=opt.augment)[0]

            # Apply NMS
            pred = non_max_suppression(pred, opt.conf_thres, opt.iou_thres, classes=opt.classes, agnostic=opt.agnostic_nms)
            t2 = time_synchronized()

            # Apply Classifier
            if classify:
                pred = apply_classifier(pred, modelc, img, im0s)

            # Process detections
            for i, det in enumerate(pred):  # detections per image
                if webcam:  # batch_size >= 1
                    p, s, im0, frame = path[i], '%g: ' % i, im0s[i].copy(), dataset.count
                else:
                    p, s, im0, frame = path, '', im0s.copy(), getattr(dataset, 'frame', 0)

                p = Path(p)  # to Path
                save_path = str(save_dir / p.name)  # img.jpg
                txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # img.txt
                s += '%gx%g ' % img.shape[2:]  # print string
                gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                if len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                    # Print results
                    for c in det[:, -1].unique():
                        n = (det[:, -1] == c).sum()  # detections per class
                        s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string
                    
                    # Write results
                    for *xyxy, conf, cls in reversed(det):
                        # cls is group id
                        if save_txt:  # Write to file
                        
                            points = []
                            f.write(str(re.split('_|\.',txt_path)[1])+',')
                            # for num in xyxy:
                            points.append(xyxy[0])# x_l
                            points.append(xyxy[1])# y_up
                            points.append(xyxy[2])
                            points.append(xyxy[1])# y_d
                            points.append(xyxy[2])
                            points.append(xyxy[3])# y_d
                            points.append(xyxy[0])# x_l
                            points.append(xyxy[3])# y_d
                            for num in points:
                                f.write(f"{int(num)},")
                            f.write(f'{conf}\n')

                            
                            if (int(cls)==0):
                                h = xyxy[3] - xyxy[1]
                                w = xyxy[2] - xyxy[0]
                                if(w>h):
                                    # run x_crop
                                    small_blocks = x_crop(im0,xyxy)
                                    for a,b in zip(small_blocks[0::2], small_blocks[1::2]): # data[0::2] means create subset collection of elements that (index % 2 == 0)
                                        f.write(str(re.split('_|\.',txt_path)[1])+',')
                                        f.write(f"{a[0]},{a[1]},{b[0]},{a[1]},{b[0]},{b[1]},{a[0]},{b[1]},")
                                        f.write(f'0.5\n')
                                else:
                                    # run y_crop
                                    small_blocks = y_crop(im0,xyxy)
                                    for a,b in zip(small_blocks[0::2], small_blocks[1::2]): # data[0::2] means create subset collection of elements that (index % 2 == 0)
                                        f.write(str(re.split('_|\.',txt_path)[1])+',')
                                        f.write(f"{a[0]},{a[1]},{b[0]},{a[1]},{b[0]},{b[1]},{a[0]},{b[1]},")
                                        f.write(f'0.5\n')

                        if save_img or opt.save_crop or view_img:  # Add bbox to image
                            c = int(cls)  # integer class
                            label = None if opt.hide_labels else (names[c] if opt.hide_conf else f'{names[c]} {conf:.2f}')

                            plot_one_box(xyxy, im0, label=label, color=colors(c, True), line_thickness=opt.line_thickness)
                            if opt.save_crop:
                                save_one_box(xyxy, im0s, file=save_dir / 'crops' / names[c] / f'{p.stem}.jpg', BGR=True)

                # Print time (inference + NMS)
                print(f'{s}Done. ({t2 - t1:.3f}s)')

                # Stream results
                if view_img:
                    cv2.imshow(str(p), im0)
                    cv2.waitKey(1)  # 1 millisecond

                # Save results (image with detections)
                if save_img:
                    if dataset.mode == 'image':
                        cv2.imwrite(save_path, im0)
                    else:  # 'video' or 'stream'
                        if vid_path != save_path:  # new video
                            vid_path = save_path
                            if isinstance(vid_writer, cv2.VideoWriter):
                                vid_writer.release()  # release previous video writer
                            if vid_cap:  # video
                                fps = vid_cap.get(cv2.CAP_PROP_FPS)
                                w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                                h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                            else:  # stream
                                fps, w, h = 30, im0.shape[1], im0.shape[0]
                                save_path += '.mp4'
                            vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
                        vid_writer.write(im0)

        if save_txt or save_img:
            s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ''
            print(f"Results saved to {save_dir}{s}")

        print(f'Done. ({time.time() - t0:.3f}s)')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default='yolov5s.pt', help='model.pt path(s)')
    parser.add_argument('--source', type=str, default='data/images', help='source')  # file/folder, 0 for webcam
    parser.add_argument('--img-size', type=int, default=640, help='inference size (pixels)')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='IOU threshold for NMS')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='display results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
    parser.add_argument('--save-crop', action='store_true', help='save cropped prediction boxes')
    parser.add_argument('--nosave', action='store_true', help='do not save images/videos')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--update', action='store_true', help='update all models')
    parser.add_argument('--project', default='runs/detect', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    parser.add_argument('--line-thickness', default=3, type=int, help='bounding box thickness (pixels)')
    parser.add_argument('--hide-labels', default=False, action='store_true', help='hide labels')
    parser.add_argument('--hide-conf', default=False, action='store_true', help='hide confidences')
    opt = parser.parse_args()
    print(opt)
    check_requirements(exclude=('tensorboard', 'pycocotools', 'thop'))

    with torch.no_grad():
        if opt.update:  # update all models (to fix SourceChangeWarning)
            for opt.weights in ['yolov5s.pt', 'yolov5m.pt', 'yolov5l.pt', 'yolov5x.pt']:
                detect(opt=opt)
                strip_optimizer(opt.weights)
        else:
            detect(opt=opt)
