#!/usr/bin/env python

import cv2
import numpy as np


def get_transformed_points(boxes, prespective_transform):
    arr = []
    for i in boxes:
        pnts = np.array([[[int(i[0] + (i[2] * 0.5)), int(i[1] + i[3])]]], dtype="float32")
        bd_pnt = cv2.perspectiveTransform(pnts, prespective_transform)[0][0]
        pnt = [int(bd_pnt[0]), int(bd_pnt[1])]
        arr.append(pnt)

    return arr


def cal_dis(p1, p2, d_w, d_h):
    h = abs(p2[1] - p1[1])
    w = abs(p2[0] - p1[0])

    dis_w = float((w / d_w) * 180)
    dis_h = float((h / d_h) * 180)

    return int(np.sqrt((dis_h ** 2) + (dis_w ** 2)))


def get_distances(boxes1, bottom_points, d_w, d_h):
    dMat = []
    bxs = []

    for i in range(len(bottom_points)):
        for j in range(len(bottom_points)):
            if i != j:
                dist = cal_dis(bottom_points[i], bottom_points[j], d_w, d_h)
                if dist <= 150:
                    closeness = 0
                    dMat.append([bottom_points[i], bottom_points[j], closeness])
                    bxs.append([boxes1[i], boxes1[j], closeness])
                elif dist > 150 and dist <= 180:
                    closeness = 1
                    dMat.append([bottom_points[i], bottom_points[j], closeness])
                    bxs.append([boxes1[i], boxes1[j], closeness])
                else:
                    closeness = 2
                    dMat.append([bottom_points[i], bottom_points[j], closeness])
                    bxs.append([boxes1[i], boxes1[j], closeness])

    return dMat, bxs


def get_scale(W, H):
    dis_w = 400
    dis_h = 600

    return float(dis_w / W), float(dis_h / H)


def get_count(dMat):
    r = []
    g = []
    y = []

    for i in range(len(dMat)):

        if dMat[i][2] == 0:
            if (dMat[i][0] not in r) and (dMat[i][0] not in g) and (dMat[i][0] not in y):
                r.append(dMat[i][0])
            if (dMat[i][1] not in r) and (dMat[i][1] not in g) and (dMat[i][1] not in y):
                r.append(dMat[i][1])

    for i in range(len(dMat)):

        if dMat[i][2] == 1:
            if (dMat[i][0] not in r) and (dMat[i][0] not in g) and (dMat[i][0] not in y):
                y.append(dMat[i][0])
            if (dMat[i][1] not in r) and (dMat[i][1] not in g) and (dMat[i][1] not in y):
                y.append(dMat[i][1])

    for i in range(len(dMat)):

        if dMat[i][2] == 2:
            if (dMat[i][0] not in r) and (dMat[i][0] not in g) and (dMat[i][0] not in y):
                g.append(dMat[i][0])
            if (dMat[i][1] not in r) and (dMat[i][1] not in g) and (dMat[i][1] not in y):
                g.append(dMat[i][1])

    return (len(r), len(y), len(g))









