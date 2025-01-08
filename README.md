# Yolo-segmentation-to-Coco-segmentation
This script is designed to convert YOLO segmentation annotations into COCO segmentation annotations. \
It utilizes basic Python packages, including json, PIL, and os.

# Requirements
To use this script, you need to specify:

The image directory \
The annotation directory \
The category types
# Modes of Operation
The script can operate in two different modes, controlled by the variable singleormultiple in the creation_json_yolo_to_coco function:

"m" (multiple): Generates a separate JSON file for each image. \
"s" (single): Creates a single JSON file containing annotations for all images.

