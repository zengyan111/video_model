import matplotlib.pylab as plt
from upapy.reconstruction.ubp2d import FastUBP
import numpy as np
import cmaps
import cv2
import os
import datetime
import tempfile


#每2帧图片，总运行时间23s
class video_gray:
    
    def __init__(self, tensor_data, frame_gap,):  
        self.__N = tensor_data[:,:,:]
        img_fps = []
        dict = {}
        
        #视频宽高设置
        width, height = 0, 0

        i = 0
        while i < tensor_data.shape[0]:
            if i % frame_gap == 0:
                #使用previewer重构建图像
                reconstuct=FastUBP()
                reconstuct.set_image_param(35,35,0.0000,-4.1200,50,25)
                reconstuct.set_pa_frame_param()
                reconstuct.set_reconstruction_param(1.4860, 1.4860,0,[0.0000,0.0000,-4.1200,0.0000,0.0000])
                image = reconstuct.reconstruction(tensor_data[i])
            
                #使用临时文件存储图片
                file = tempfile.NamedTemporaryFile(suffix=".png", mode='w+', delete=False)
                with file as temp_file:
                    plt.imsave(temp_file.name, image, cmap="gray")
                    width, height = image.shape

                    #存储文件路径到列表
                    img_fps.append(temp_file.name)
                    #存储时间节点到字典
                    time = os.path.getmtime(temp_file.name)
                    #字典存储时间和图片路径
                    dict[time] = temp_file.name
            i += 1

        #创建视频对象
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter('./tem_storted_gray22.mp4', fourcc, 5, (width, height)) #一秒5帧

        for pn in dict.values():
            # 读取图像
            image = plt.imread(pn, format='png') 
            image = cv2.imread(pn)
   
            # 写入图像到视频
            video.write(image)

        
        # 释放资源
        video.release()

