import json
from check import creates_categories, creation_json_yolo_to_coco

annotation_directory = r"C:\Users\Claudio\PycharmProjects\texturetriangle\Annotations"
images_directory = r"C:\Users\Claudio\PycharmProjects\texturetriangle\Images"



categorie = ["Stomata"]
creation_json_yolo_to_coco(images_directory,annotation_directory, categories=categorie)



