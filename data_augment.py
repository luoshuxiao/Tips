import math
import os
import random

import numpy as np
import cv2
import torchvision
import matplotlib.pyplot as plt
from rename import tongji

#  随机裁剪(完全随机，四个角+中心)  crop
def random_crop(img, scale=[0.8, 1.0], ratio=[3. / 4., 4. / 3.], resize_w=500, resize_h=500):
    """
    随机裁剪
    :param img:
    :param scale: 缩放
    :param ratio:
    :param resize_w:
    :param resize_h:
    :return:
    """
    aspect_ratio = math.sqrt(np.random.uniform(*ratio))
    w = 1. * aspect_ratio
    h = 1. / aspect_ratio
    src_h, src_w = img.shape[:2]

    bound = min((float(src_w) / src_h) / (w ** 2),
                (float(src_h) / src_w) / (h ** 2))
    scale_max = min(scale[1], bound)
    scale_min = min(scale[0], bound)

    target_area = src_h * src_w * np.random.uniform(scale_min,
                                                    scale_max)
    target_size = math.sqrt(target_area)
    w = int(target_size * w)
    h = int(target_size * h)

    i = np.random.randint(0, src_w - w + 1)
    j = np.random.randint(0, src_h - h + 1)

    img = img[j:j + h, i:i + w]
    img = cv2.resize(img, (resize_w, resize_h))
    return img


# 规则裁剪
def rule_crop(img, box_ratio=(3. / 4, 3. / 4), location_type='LT', resize_w=500, resize_h=500):
    """
    按照一定规则进行裁剪, 直接在原图尺寸上操作，不对原图进行
    :param img:
    :param box_ratio: 剪切的 比例：  （宽度上的比例， 高度上的比例）
    :param location_type: 具体在=哪个位置： 以下其中一个：
            LR : 左上角
            RT : 右上角
            LB : 左下角
            RB : 右下角
            CC : 中心
    :param resize_w: 输出图的width
    :param resize_h: 输出图的height
    :return:
    """
    assert location_type in ('LT', 'RT', 'LB', 'RB', 'CC'), 'must have a location .'
    is_gray = False
    if len(img.shape) == 3:
        h, w, c = img.shape
    elif len(img.shape) == 2:
        h, w = img.shape
        is_gray = True

    crop_w, crop_h = int(w * box_ratio[0]), int(h * box_ratio[1])
    crop_img = np.zeros([10, 10])
    if location_type == 'LT':
        crop_img = img[:crop_h, :crop_w, :] if not is_gray else img[:crop_h, :crop_w]
    elif location_type == 'RT':
        crop_img = img[:crop_h:, w - crop_w:, :] if not is_gray else img[:crop_h:, w - crop_w:]
    elif location_type == 'LB':
        crop_img = img[h - crop_h:, :crop_w, :] if not is_gray else img[h - crop_h:, :crop_w]
    elif location_type == 'RB':
        crop_img = img[h - crop_h:, w - crop_w:, :] if not is_gray else img[h - crop_h:, w - crop_w:]
    elif location_type == 'CC':
        start_h = (h - crop_h) // 2
        start_w = (w - crop_w) // 2
        crop_img = img[start_h:start_h + crop_h, start_w:start_w + crop_w, :] if not is_gray else img[
                                                                                                  start_h:start_h + crop_h,
                                                                                                  start_w:start_w + crop_w]

    resize = cv2.resize(crop_img, (resize_w, resize_h))
    return resize


# 水平翻转
def random_flip(img, mode=1):
    """
    随机翻转
    :param img:
    :param model: 1=水平翻转 / 0=垂直 / -1=水平垂直
    :return:
    """
    assert mode in (0, 1, -1), "mode is not right"
    flip = np.random.choice(2) * 2 - 1  # -1 / 1
    if mode == 1:
        img = img[:, ::flip, :]
    elif mode == 0:
        img = img[::flip, :, :]
    elif mode == -1:
        img = img[::flip, ::flip, :]

    return img





# 翻转
def flip(img, mode=1):
    """
    翻转
    :param img:
    :param mode: 1=水平翻转 / 0=垂直 / -1=水平垂直
    :return:
    """
    assert mode in (0, 1, -1), "mode is not right"
    return cv2.flip(img, flipCode=mode)



# 随机锐化增强
def random_USM(img, gamma=0.6):
    """
    USM锐化增强算法可以去除一些细小的干扰细节和图像噪声，比一般直接使用卷积锐化算子得到的图像更可靠。
        output = 原图像−w∗高斯滤波(原图像)/(1−w)
        其中w为上面所述的系数，取值范围为0.1~0.9，一般取0.6。
    :param img:
    :param gamma:
    :return:
    """
    blur = cv2.GaussianBlur(img, (0, 0), 25)
    img_sharp = cv2.addWeighted(img, 1.5, blur, -0.3, gamma)
    return img_sharp


# 噪声(高斯、自定义)
def random_noise(img, rand_range=(3, 20)):
    """
    随机噪声
    :param img:
    :param rand_range: (min, max)
    :return:
    """
    img = np.asarray(img, np.float)
    sigma = random.randint(*rand_range)
    nosie = np.random.normal(0, sigma, size=img.shape)
    img += nosie
    img = np.uint8(np.clip(img, 0, 255))
    return img



# 滤波(高斯、平滑、均值、中值、最大最小值、双边、引导、运动)
# 各种滤波原理介绍：https://blog.csdn.net/hellocsz/article/details/80727972
def gaussianBlue(img, ks=(7, 7), stdev=1.5):
    """
    高斯模糊, 可以对图像进行平滑处理，去除尖锐噪声
    :param img:
    :param ks:  卷积核
    :param stdev: 标准差
    :return:
    """
    return cv2.GaussianBlur(img, (7, 7), 1.5)


# 随机滤波
def ranndom_blur(img, ksize=(3, 3)):
    """
    随机滤波
    :param img:
    :param ksize:
    :return:
    """
    blur_types = ['gaussian', 'median', 'bilateral', 'mean', 'box']
    assert len(blur_types) > 0
    blur_func = None
    blur_index = random.choice(blur_types)
    if blur_index == 0:  # 高斯模糊, 比均值滤波更平滑，边界保留更加好
        blur_func = cv2.GaussianBlur
    elif blur_index == 1:  # 中值滤波, 在边界保存方面好于均值滤波，但在模板变大的时候会存在一些边界的模糊。对于椒盐噪声有效
        blur_func = cv2.medianBlur
    elif blur_index == 2:  # 双边滤波, 非线性滤波，保留较多的高频信息，不能干净的过滤高频噪声，对于低频滤波较好，不能去除脉冲噪声
        blur_func = cv2.bilateralFilter
    elif blur_index == 3:  # 均值滤波, 在去噪的同时去除了很多细节部分，将图像变得模糊
        blur_func = cv2.blur
    elif blur_index == 4:  # 盒滤波器
        blur_func = cv2.boxFilter

    img_blur = blur_func(src=img, ksize=ksize)
    return img_blur


# 直方图均衡化
def equalize_hist(img):
    """
    直方图均衡化
    :param img:
    :return:
    """
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    hist = cv2.equalizeHist(gray)
    rgb = cv2.cvtColor(hist, cv2.COLOR_GRAY2RGB)
    return rgb


# 画直方图
gray_level = 256
def pixel_probability(img):
    """
    计算像素值出现概率
    :param img:
    :return:
    """
    assert isinstance(img, np.ndarray)

    prob = np.zeros(shape=(256))

    for rv in img:
        for cv in rv:
            prob[cv] += 1

    r, c = img.shape
    prob = prob / (r * c)

    return prob


# 根据像素概率将原始图像直方图均衡化
def probability_to_histogram(img, prob):
    """
    根据像素概率将原始图像直方图均衡化
    :param img:
    :param prob:
    :return: 直方图均衡化后的图像
    """
    prob = np.cumsum(prob)  # 累计概率

    img_map = [int(i * prob[i]) for i in range(256)]  # 像素值映射

   # 像素值替换
    assert isinstance(img, np.ndarray)
    r, c = img.shape
    for ri in range(r):
        for ci in range(c):
            img[ri, ci] = img_map[img[ri, ci]]

    return img

# 画直方图
def plot(y, name):
    """
    画直方图，len(y)==gray_level
    :param y: 概率值
    :param name:
    :return:
    """
    plt.figure(num=name)
    plt.bar([i for i in range(gray_level)], y, width=1)


# 旋转
def rotate(img, angle, scale=1.0):
    """
    旋转
    补边：就近像素补边
    黑色补边的影响，不加偏置 ，影响？？
    :param img:
    :param angle: 旋转角度， >0 表示逆时针，
    :param scale:
    :return:
    """
    height, width = img.shape[:2]  # 获取图像的高和宽
    center = (width / 2, height / 2)  # 取图像的中点

    M = cv2.getRotationMatrix2D(center, angle, scale)  # 获得图像绕着某一点的旋转矩阵
    # cv2.warpAffine()的第二个参数是变换矩阵,第三个参数是输出图像的大小
    rotated = cv2.warpAffine(img, M, (height, width))
    return rotated



# 随机旋转
def random_rotate(img, angle_range=(-10, 10)):
    """
    随机旋转
    :param img:
    :param angle_range:  旋转角度范围 (min,max)   >0 表示逆时针，
    :return:
    """
    height, width = img.shape[:2]  # 获取图像的高和宽
    center = (width / 2, height / 2)  # 取图像的中点
    angle = random.randrange(*angle_range, 1)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)  # 获得图像绕着某一点的旋转矩阵
    # cv2.warpAffine()的第二个参数是变换矩阵,第三个参数是输出图像的大小
    rotated = cv2.warpAffine(img, M, (height, width))
    return rotated


# 偏移
def shift(img, x_offset, y_offset):
    """
    偏移，向右 向下
    :param img:
    :param x_offset:  >0表示向右偏移px, <0表示向左
    :param y_offset:  >0表示向下偏移px, <0表示向上
    :return:
    """
    h, w, _ = img.shape
    M = np.array([[1, 0, x_offset], [0, 1, y_offset]], dtype=np.float)
    return cv2.warpAffine(img, M, (w, h))


# 倾斜/缩放
def resize_img(img, resize_w, resize_h):
    height, width = img.shape[:2]  # 获取图片的高和宽
    return cv2.resize(img, (resize_w, resize_h), interpolation=cv2.INTER_CUBIC)


# RGB / BGR->HSV
def rgb2hsv_py(r, g, b):
    # from https://blog.csdn.net/weixin_43360384/article/details/84871521
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    m = mx - mn
    if mx == mn:
        h = 0
    elif mx == r:
        if g >= b:
            h = ((g - b) / m) * 60
        else:
            h = ((g - b) / m) * 60 + 360
    elif mx == g:
        h = ((b - r) / m) * 60 + 120
    elif mx == b:
        h = ((r - g) / m) * 60 + 240
    if mx == 0:
        s = 0
    else:
        s = m / mx
    v = mx

    merged = cv2.merge([h, s, v])
    cv2.imshow("Merged", merged)
    cv2.waitKey(0)
    return h, s, v



def rgb2hsv_cv(img):
    # from https://blog.csdn.net/qq_38332453/article/details/89258058
    h = img.shape[0]
    w = img.shape[1]
    H = np.zeros((h, w), np.float32)
    S = np.zeros((h, w), np.float32)
    V = np.zeros((h, w), np.float32)
    r, g, b = cv2.split(img)
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    for i in range(0, h):
        for j in range(0, w):
            mx = max((b[i, j], g[i, j], r[i, j]))
            mn = min((b[i, j], g[i, j], r[i, j]))
            V[i, j] = mx
            if V[i, j] == 0:
                S[i, j] = 0
            else:
                S[i, j] = (V[i, j] - mn) / V[i, j]
            if mx == mn:
                H[i, j] = 0
            elif V[i, j] == r[i, j]:
                if g[i, j] >= b[i, j]:
                    H[i, j] = (60 * ((g[i, j]) - b[i, j]) / (V[i, j] - mn))
                else:
                    H[i, j] = (60 * ((g[i, j]) - b[i, j]) / (V[i, j] - mn)) + 360
            elif V[i, j] == g[i, j]:
                H[i, j] = 60 * ((b[i, j]) - r[i, j]) / (V[i, j] - mn) + 120
            elif V[i, j] == b[i, j]:
                H[i, j] = 60 * ((r[i, j]) - g[i, j]) / (V[i, j] - mn) + 240
            H[i, j] = H[i, j] / 2
    return H, S, V



# 颜色抖动(亮度\色度\饱和度\对比度)
def adjust_contrast_bright(img, contrast=0.5, brightness=50):
    """
    调整亮度与对比度
    dst = img * contrast + brightness
    :param img:
    :param contrast: 对比度   越大越亮
    :param brightness: 亮度  0~100
    :return:
    """
    # 像素值会超过0-255， 因此需要截断
    return np.uint8(np.clip((contrast * img + brightness), 0, 255))




# gamma 变换,
def gamma_transform(img, gamma=3):
    """
    https://blog.csdn.net/zfjBIT/article/details/85113946
    伽马变换就是用来图像增强，其提升了暗部细节，简单来说就是通过非线性变换，
    让图像从暴光强度的线性响应变得更接近人眼感受的响应，即将漂白（相机曝光）或过暗（曝光不足）的图片，进行矫正
    人眼对外界光源的感光值与输入光强不是呈线性关系的，而是呈指数型关系的。在低照度下，人眼更容易分辨出亮度的变化，随着照度的增加，
    人眼不易分辨出亮度的变化。而摄像机感光与输入光强呈线性关系。
    为能更有效的保存图像亮度信息，需进行Gamma变换,经过Gamma变换后，改善了存储的有效性和效率。
    :param img:
    :param gamma:
        # gamma = random.random() * random.choice([0.5, 1, 3, 5])
        >1, 变暗
        <1, 漂白
    :return:
    """
    assert 0 < gamma < 10.
    # 具体做法先归一化到1，然后gamma作为指数值求出新的像素值再还原
    gamma_table = [np.power(x / 255.0, gamma) * 255.0 for x in range(256)]
    gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
    # 实现映射用的是Opencv的查表函数
    return cv2.LUT(img, gamma_table)

if __name__ == "__main__":
    test_img = cv2.imread('car_test_dz.jpg')
    # img_ = gamma_transform(test_img)
    # cv2.imshow('00', img_)
    cv2.waitKey(0)

# mix up 图片混合 ??
def mixup(batch_x, batch_y, alpha):
    """
    Returns mixed inputs, pairs of targets, and lambda
    :param batch_x:
    :param batch_y:
    :param alpha:
    :return:
    """
    if alpha > 0:
        lam = np.random.beta(alpha, alpha)
    else:
        lam = 1

    batch_size = batch_x.shape[0]
    index = [i for i in range(batch_size)]
    random.shuffle(index)

    mixed_x = lam * batch_x + (1 - lam) * batch_x[index, :]
    y_a, y_b = batch_y, batch_y[index]
    return mixed_x, y_a, y_b, lam


# 角点检测- Harris 角点检测
def jiaodianjiance(img):
    """
    如果在各个方向上移动这个特征的小窗口，窗口内区域的灰度发生了较大的变化，那么就认为在窗口内遇到了角点.
    如果这个特定的窗口在图像各个方向上移动时，窗口内图像的灰度没有发生变化，那么窗口内就不存在角点
    :param img:
    :return:
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    # 输入图像必须是 float32，最后一个参数在 0.04 到 0.05 之间
    dst = cv2.cornerHarris(gray, 2, 3, 0.04)
    # result is dilated for marking the corners, not important
    dst = cv2.dilate(dst, None)
    # Threshold for an optimal value, it may vary depending on the image.
    img[dst > 0.01 * dst.max()] = [0, 0, 255]
    return img



if __name__ == "__main__":
    test_img = cv2.imread('car_test_auto.jpg')
    img_ = jiaodianjiance(test_img)
    cv2.imshow('00', img_)
    cv2.waitKey(0)


    # 单张图片测试
    # test_img_ = cv2.imread('car_test_auto.jpg',0)
    # #
    # prob = pixel_probability(test_img_)
    # plot(prob, "原图直方图")
    # # 直方图均衡化
    # img = probability_to_histogram(test_img_, prob)
    # cv2.imwrite("source_hist.jpg", img)  # 保存图像
    #
    # prob = pixel_probability(img)
    # plot(prob, "直方图均衡化结果")
    #
    # plt.show()






    # id = 0
    # dir_ = tongji(r'E:\00lehongxia\Dataset\vehicle-identification(luozhoujie)\train/')
    # for dirs in dir_:
    #     imgs_dir = os.listdir(dirs)
    #     for img_dir in imgs_dir:
    #         read_dir = dirs+img_dir
    #         read_dir = read_dir.replace('\\','/')
    #         save_dir = dirs + str(id) + img_dir
    #         imgimg = cv2.imdecode(np.fromfile(read_dir, dtype=np.uint8), -1)
    #         img_ = equalize_hist(imgimg)
    #         cv2.imencode('.jpg', img_)[1].tofile(save_dir)
    #         id += 1
    #         print(save_dir)