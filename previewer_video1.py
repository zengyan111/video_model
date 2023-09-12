import matplotlib.pylab as plt
from upapy.reconstruction.ubp2d import FastUBP
import numpy as np
import cmaps
import cv2
import os
import datetime


#每隔2帧图片，运行20s
class video_gray:
    def __init__(self, tensor_data, frame_gap,):   
        self.__N = tensor_data[:,:,:]
        
        #创建本地文件夹
        folder_path = 'test_folder'
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
            
        i = 0
        while i < tensor_data.shape[0]:
            if i % frame_gap == 0:
                #使用previewer重构建图像
                reconstuct=FastUBP()
                reconstuct.set_image_param(35,35,0.0000,-4.1200,50,25)
                reconstuct.set_pa_frame_param()
                reconstuct.set_reconstruction_param(1.4860, 1.4860,0,[0.0000,0.0000,-4.1200,0.0000,0.0000])
                image = reconstuct.reconstruction(tensor_data[i])
                
                #存储文件到 folder_path              
                plt.imsave(f'test_folder/{i}.png', image, cmap="gray")
            i += 1

                
            # 获取图像列表
        a = [img for img in os.listdir(folder_path) if img.endswith('.png')]
        images = sorted(a, key=lambda x: int(x[0:-4]))

            # 读取图像
        frame = cv2.imread(os.path.join(folder_path, images[0]))
        height, width, layers = frame.shape

            # 创建视频对象
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter('./unfiled_previewer_gray.mp4', fourcc, 5, (width,height)) #一秒2帧

            # 写入图像到视频
        for image in images:
            frame = cv2.imread(os.path.join(folder_path, image))
            video.write(frame)

            # 释放资源
        cv2.destroyAllWindows()
        video.release()

