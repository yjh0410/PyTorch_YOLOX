#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) Megvii, Inc. and its affiliates.

import argparse
import os

import cv2
import time
import numpy as np
import sys
sys.path.append('../../')

import onnxruntime
from dataset.transforms import ValTransforms
from utils.post_process import PostProcessor
from utils.vis_tools import visualize


def make_parser():
    parser = argparse.ArgumentParser("onnxruntime inference sample")
    parser.add_argument("--weight", type=str, default="../../weight/onnx/yolo_free.onnx",
                        help="Input your onnx model.")
    parser.add_argument("-i", "--image_path", type=str, default='../test_image.jpg',
                        help="Path to your input image.")
    parser.add_argument("-o", "--output_dir", type=str, default='../../det_results/onnx/',
                        help="Path to your output directory.")
    parser.add_argument("-s", "--score_thr", type=float, default=0.3,
                        help="Score threshould to filter the result.")
    parser.add_argument("-size", "--img_size", type=int, default=640,
                        help="Specify an input shape for inference.")
    return parser


if __name__ == '__main__':
    args = make_parser().parse_args()

    # class color for better visualization
    np.random.seed(0)
    class_colors = [(np.random.randint(255),
                     np.random.randint(255),
                     np.random.randint(255)) for _ in range(80)]

    # preprocessor
    prepocess = ValTransforms(img_size=args.img_size, adaptive=False)

    # postprocessor
    postprocess = PostProcessor(
        img_size=args.img_size, strides=[8, 16, 32],
        num_classes=80, conf_thresh=args.score_thr, nms_thresh=0.5)

    # read an image
    input_shape = tuple(args.img_size, args.img_size)
    origin_img = cv2.imread(args.image_path)

    # preprocess
    x = prepocess(origin_img)[0]
    x = x.unsqueeze(0)

    t0 = time.time()
    # inference
    session = onnxruntime.InferenceSession(args.weight)

    ort_inputs = {session.get_inputs()[0].name: x}
    output = session.run(None, ort_inputs)
    print("inference time: {:.1f} ms", (time.time() - t0)*100)

    t0 = time.time()
    # post process
    bboxes, scores, labels = postprocess(output)
    print("post-process time: {:.1f} ms", (time.time() - t0)*100)

    # visualize detection
    origin_img = visualize(
        img=origin_img,
        bboxes=bboxes,
        scores=scores,
        labels=labels,
        vis_thresh=args.score_thr,
        class_colors=class_colors
        )

    # save results
    os.makedirs(args.output_dir, exist_ok=True)
    output_path = os.path.join(args.output_dir, os.path.basename(args.image_path))
    cv2.imwrite(output_path, origin_img)
