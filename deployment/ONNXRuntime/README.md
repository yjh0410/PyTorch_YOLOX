## FreeYOLO ONNXRuntime

### Download FreeYOLO ONNX file
Main results on COCO-val:

| Model          |  Scale  |  FLOPs   |  Params  |    AP    |    AP50    |  ONNX  |
|----------------|---------|----------|----------|----------|------------|----------|
| FreeYOLO-Nano  |  416    |   1.2 G  |  1.0 M   |      |        |  |
| FreeYOLO-Tiny  |  416    |   5.9 G  |  6.2 M   |      |        |  |
| FreeYOLO-Large |  640    |  144.8 G |  44.1 M  |      |        |  |
| FreeYOLO-Huge  |  640    |  257.8 G |  78.9 M  |      |        |  |


### Convert Your Model to ONNX

First, you should move to <FreeYOLO_HOME> by:
```shell
cd <FreeYOLO_HOME>
cd tools/
```
Then, you can:

1. Convert a standard FreeYOLO model by:
```shell
python3 export_onnx.py --output-name yolo_free_large.onnx -n yolo_free_large --weight ../weight/coco/yolo_free_large/yolo_free_large.pth --no_decode
```

Notes:
* -n: specify a model name. The model name must be one of the [yolox-s,m,l,x and yolox-nano, yolox-tiny, yolov3]
* -c: the model you have trained
* -o: opset version, default 11. **However, if you will further convert your onnx model to [OpenVINO](https://github.com/Megvii-BaseDetection/YOLOX/demo/OpenVINO/), please specify the opset version to 10.**
* --no-onnxsim: disable onnxsim
* To customize an input shape for onnx model,  modify the following code in tools/export_onnx.py:

    ```python
    dummy_input = torch.randn(args.batch_size, 3, cfg['test_size'], cfg['test_size'])
    ```

### ONNXRuntime Demo

Step1.
```shell
cd <YOLOX_HOME>/deployment/ONNXRuntime
```

Step2. 
```shell
python3 onnx_inference.py --weight ../../weights/onnx/11/yolo_free_large.onnx -i ../test_image.jp -s 0.3 --img_size 640
```
Notes:
* --weight: your converted onnx model
* -i: input_image
* -s: score threshold for visualization.
* --img_size: should be consistent with the shape you used for onnx convertion.