# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 23:23:06 2018

@author: ghn
"""


# -*- coding: utf-8 -*-
'''
kalman2d - 2D Kalman filter using OpenCV
Based on http://jayrambhia.wordpress.com/2012/07/26/kalman-filter/
Copyright (C) 2014 Simon D. Levy
This code is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.
This code is distributed in the hope that it will be useful,
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU Lesser General Public License
along with this code. If not, see <http://www.gnu.org/licenses/>.
'''
 
from cv2 import cv
 
class Kalman2D(object):
    '''
    A class for 2D Kalman filtering
    '''
 
    def __init__(self, processNoiseCovariance=1e-4, measurementNoiseCovariance=1e-1, errorCovariancePost=0.1):
        '''
        Constructs a new Kalman2D object.  
        For explanation of the error covariances see
        http://en.wikipedia.org/wiki/Kalman_filter
        '''
        # 状态空间：位置--2d,速度--2d
        self.kalman = cv.CreateKalman(4, 2, 0)
        self.kalman_state = cv.CreateMat(4, 1, cv.CV_32FC1)
        self.kalman_process_noise = cv.CreateMat(4, 1, cv.CV_32FC1)
        self.kalman_measurement = cv.CreateMat(2, 1, cv.CV_32FC1)
 
        for j in range(4):
            for k in range(4):
                self.kalman.transition_matrix[j,k] = 0
            self.kalman.transition_matrix[j,j] = 1
        #加入速度 x = x + vx, y = y + vy
        # 1,0,1,0,   0,1,0,1,  0,0,1,0,  0,0,0,1
        #如果把下面两句注释掉，那么位置跟踪kalman滤波器的状态模型就是没有使用速度信息
#        self.kalman.transition_matrix[0, 2]=1
#        self.kalman.transition_matrix[1, 3]=1
        
        cv.SetIdentity(self.kalman.measurement_matrix)
        #初始化带尺度的单位矩阵
        cv.SetIdentity(self.kalman.process_noise_cov, cv.RealScalar(processNoiseCovariance))
        cv.SetIdentity(self.kalman.measurement_noise_cov, cv.RealScalar(measurementNoiseCovariance))
        cv.SetIdentity(self.kalman.error_cov_post, cv.RealScalar(errorCovariancePost))
 
        self.predicted = None
        self.esitmated = None
 
    def update(self, x, y):
        '''
        Updates the filter with a new X,Y measurement
        '''
 
        self.kalman_measurement[0, 0] = x
        self.kalman_measurement[1, 0] = y
 
        self.predicted = cv.KalmanPredict(self.kalman)
        self.corrected = cv.KalmanCorrect(self.kalman, self.kalman_measurement)
 
    def getEstimate(self):
        '''
        Returns the current X,Y estimate.
        '''
 
        return self.corrected[0,0], self.corrected[1,0]
 
    def getPrediction(self):
        '''
        Returns the current X,Y prediction.
        '''
 
        return self.predicted[0,0], self.predicted[1,0]