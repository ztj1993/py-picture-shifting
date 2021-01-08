# -*- coding: utf-8 -*-
# Intro: 图片偏移量计算
# Author: Ztj
# Email: ztj1993@gmail.com
# Version: 0.0.1
# Date: 2020-01-07

import cv2
import numpy as np

__version__ = '0.0.1'


class Shifting(object):

    def __init__(self, big_picture, small_picture):
        self.big_picture = big_picture
        self.small_picture = small_picture
        self.cache = dict()

    def read_small_picture(self):
        """读取小文件"""
        picture = self.cache.get('small')
        if picture is not None:
            return picture

        picture = cv2.imread(self.small_picture, 0)
        self.cache['small'] = picture
        return picture

    def get_big_size(self):
        big_read = self.read_big_picture()
        height, width = big_read.shape[:2]
        return width, height

    def get_small_size(self):
        small_read = self.read_small_picture()
        height, width = small_read.shape[:2]
        return width, height

    def read_big_picture(self):
        """读取大文件"""
        picture = self.cache.get('big')
        if picture is not None:
            return picture

        picture = cv2.imread(self.big_picture, 0)
        self.cache['big'] = picture
        return picture

    def match_template(self):
        """特征匹配"""
        match = self.cache.get('match')
        if match is not None:
            return match

        small_read = self.read_small_picture()
        big_read = self.read_big_picture()

        match = cv2.matchTemplate(
            small_read,
            big_read,
            cv2.TM_CCOEFF_NORMED
        )
        self.cache['match'] = match
        return match

    def normalize(self):
        """偏移量"""
        normalize = self.cache.get('normalize')
        if normalize is not None:
            return normalize

        match = self.match_template()
        cv2.normalize(match, match, 0, 1, cv2.NORM_MINMAX, -1)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
        normalize = max_loc
        self.cache['normalize'] = normalize
        return normalize

    def merge_picture(self):
        """合并图像"""
        merge = self.cache.get('merge')
        if merge is not None:
            return merge

        merge = self.read_big_picture().copy()
        small_width, small_height = self.get_small_size()
        x_offset, y_offset = self.normalize()

        cv2.rectangle(
            merge,
            (x_offset, y_offset),
            (x_offset + small_width, y_offset + small_height),
            (0, 0, 255),
            2
        )
        self.cache['merge'] = merge
        return merge

    def stack_picture(self):
        """显示图片"""
        width, height = self.get_big_size()
        big = self.read_big_picture()
        small = self.read_small_picture()
        merge = self.merge_picture()

        im_stack = np.hstack([
            cv2.resize(big, (width, height)),
            cv2.resize(small, (height, height)),
            cv2.resize(merge, (width, height)),
        ])
        cv2.imshow('stack', im_stack)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def save_small(self, filename):
        cv2.imwrite(filename, self.read_small_picture())

    def save_big(self, filename):
        cv2.imwrite(filename, self.read_big_picture())

    def save_merge(self, filename):
        cv2.imwrite(filename, self.merge_picture())

    def x_offset(self):
        return self.normalize()[0]

    def y_offset(self):
        return self.normalize()[1]
