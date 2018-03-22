# -- coding: utf-8 --

import numpy as np

#运动估计，计算序列LR图像与参考帧之间的移位
def estimate_shift(s,n):

    nr = len(s)
    delta_est = np.zeros((nr, 2))
    p = [n, n]      #只有图像中心的 n * n 像素部分（无混叠）用于移位估计
    sz = s[0].shape
    S1 = np.fft.fftshift(np.fft.fft2(s[0]))     #参考图像的傅立叶变换

    for i in range(1, nr):
        S2 = np.fft.fftshift(np.fft.fft2(s[i]))     #LR图像序列的傅立叶变换

        for i in range(S2.shape[0]):
            for k in range(S2.shape[1]):
                if(S2[i][k] == 0.0 + 0.0j):
                    S2[i][k] = 1e-10 + 0.0j

        Q = S1 * 1.0 / S2
        A = np.angle(Q)     #计算两幅图像之间的相位差

        # 确定要使用的图像频谱中心部分的位置
        beginy = np.floor(sz[0] * 1.0 / 2) - p[0] + 1
        endy = np.floor(sz[0] * 1.0 / 2) + p[0] + 1
        beginx = np.floor(sz[1] * 1.0 / 2) - p[1] + 1
        endx = np.floor(sz[1] * 1.0 / 2) + p[0] + 1

        # 计算像素的x坐标和y坐标
        tempx = np.matrix(range(beginx, endx + 1))
        tempy = np.matrix(range(beginy, endy + 1))
        x = np.ones((endy - beginy + 1, 1)) * tempx
        x = x.reshape((x.shape[0] * x.shape[1], 1))
        y = tempy.T * np.ones(1, endx - beginx + 1)
        y = y.reshape((y.shape[0] * y.shape[1], 1))
        v = A[beginy:endy + 1, beginx:endx + 1]
        v = v.reshape((v.shape[0] * v.shape[1], 1))

        # 计算相位差平面斜率的最小二乘解
        M_A = x
        M_A = np.column_stack((M_A, y))
        M_A = np.column_stack((M_A, np.ones((x.shape[0],1))))
        r = M_A.I * v
        delta_est[i,:] = np.multiply(-[r[1], r[0]]*1.0, sz) / 2 / np.pi

    return delta_est