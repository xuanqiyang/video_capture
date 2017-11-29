#!/usr/bin/python3
# -*- coding: utf-8 -*-
import cv2
from multiprocessing import Process
import time
from datetime import *
import random
import os
import sys
import numpy

if sys.getdefaultencoding()!='utf-8':
    reload(sys)#重载sys模块
    sys.setdefaultencoding('utf-8')#将默认编码改成utf-8

OutputDir = 'images' #输出目录
CaptureTime = 1 #截取视频为图片的时间点,单位为秒
ImageType = '.jpg'
CaptureFrameInterval = 1 #截取帧间隔
CaptureImageSize = (704, 358)
OutPutQuality = 60

def getDirAllVideoFile():
    allDirFiles = os.listdir()
    #获取当前文件夹中的视频 支持MP4, FLV, AVI
    videoFiles = [file for file in allDirFiles if os.path.splitext(file)[1].upper() == '.FLV' or os.path.splitext(file)[1].upper() == '.MP4' or os.path.splitext(file)[1].upper() == '.AVI']
    return videoFiles

def capture(videoFile):
    vc = cv2.VideoCapture(videoFile) #载入视频文件
    CaptureFrame = vc.get(cv2.CAP_PROP_FPS) * CaptureTime #获取当前视频的帧率,并设置需要截取的视频帧点
    outPutFileName = (os.path.join(OutputDir,videoFile) + ImageType) #输出图片文件名
    currentFrame = 1 #初始化当前帧为第一帧
    if vc.isOpened():
        rval, frame = vc.read()
    else:
        rval = False
    while rval:
        rval, frame = vc.read()
        if currentFrame == CaptureFrame: #读取到需要截取的视频帧点,就输出图片,并停止继续读取
            resizeImg = cv2.resize(frame, CaptureImageSize, interpolation=cv2.INTER_CUBIC)
            #cv2.imwrite(outPutFileName.decode('utf-8') , resizeImg, [int(cv2.IMWRITE_JPEG_QUALITY), OutPutQuality]) #生成图片,格式为jpg, 图片质量为80%
            cv2.imencode(ImageType ,resizeImg, [int(cv2.IMWRITE_JPEG_QUALITY), OutPutQuality])[1].tofile(outPutFileName)
            break
        currentFrame = currentFrame + CaptureFrameInterval
        cv2.waitKey(1)
    vc.release()

def uniqueName(path):
    nowTime = datetime.now().strftime("%Y%m%d%H%M%S") #生成当前的时间
    randomNum = random.randint(0,100) #生成随机数n,其中0<=n<=100
    if randomNum<=10:
        randomNum = str(0) + str(randomNum)
    uniqueName = str(nowTime) + str(randomNum)
    return uniqueName

def main():
    if not os.path.exists(OutputDir):
        os.mkdir(OutputDir)
    for videoFile in getDirAllVideoFile():
        print(videoFile)
        capture(videoFile)

if __name__ == '__main__':
    main()
