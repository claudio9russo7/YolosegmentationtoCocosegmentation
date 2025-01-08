# Yolo-segmentation-to-Coco-segmentation
This is a script useful to transform Yolo segmentation annotation in Coco segmentation annotation.\
The script uses basic python package (json, PIL and os).\
In order to use it, it is necessary to define the Image directory, Annotation Directory and type of categories.\
This script in the current form creates for every images an annotation file in COCO format (.json).\
It is designed in this way in order to upload on annotation tool like CVAT the singular annotation file for every images.
