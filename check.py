import os
from PIL import Image
import json


def creates_categories(categories):
    cats = []
    id = 1
    for element in categories:
        cat = {"id": id, "name": f"{element}", "supercategory": ""}
        cats.append(cat)
        id += 1
    return cats


def check_annotation(annotation_directory, images_directory):
    number_annotation = len(os.listdir(annotation_directory))
    number_images = len(os.listdir(images_directory))
    annotation_file = []
    images_file = []
    missing_annotation = []
    if number_annotation == number_images:
        print("Good, found all annotation for the images!")
        return True
    else:
        for file in os.listdir(annotation_directory):
            annotation_file.append(file.split(".")[0])
        for file in os.listdir(images_directory):
            images_file.append(file.split(".")[0])
        for image in images_file:
            if not image in annotation_file:
                missing_annotation.append(image)
        print(f"Attention there are some images without annotation: {missing_annotation}")
        return False


def yolo_coord_to_coco(list_of_value, width, height):
    array = list_of_value
    x = list(map(float, array[1::2]))
    y = list(map(float, array[2::2]))
    y_real = [round(i * height, 2) for i in y]
    x_real = [round(i * width, 2) for i in x]
    list_point = list(zip(x_real, y_real))
    return list_point


def bbox_coco(list_of_value):
    list_of_point = list_of_value
    number_of_point = len(list_of_point)
    min_point = [8000, 8000]
    max_point = [0, 0]
    for i in range(0, number_of_point - 1):
        if list_of_point[i][0] < min_point[0]:
            min_point[0] = list_of_point[i][0]
    for i in range(0, number_of_point - 1):
        if list_of_point[i][1] < min_point[1]:
            min_point[1] = list_of_point[i][1]
    for i in range(0, number_of_point - 1):
        if list_of_point[i][0] > max_point[0]:
            max_point[0] = list_of_point[i][0]
    for i in range(0, number_of_point - 1):
        if list_of_point[i][1] > max_point[1]:
            max_point[1] = list_of_point[i][1]
    width = round(max_point[0] - min_point[0], 2)
    height = round(max_point[1] - min_point[1], 2)
    result = []
    for element in min_point:
        result.append(element)
    result.append(width)
    result.append(height)
    return result


def area_calculator(list_of_value):
    list_of_point = list_of_value
    number_of_vertices = len(list_of_point)
    sum_1 = 0.0
    sum_2 = 0.0
    for i in range(0, number_of_vertices - 1):
        sum_1 += list_of_point[i][0] * list_of_point[i + 1][1]
        sum_2 += list_of_point[i][1] * list_of_point[i + 1][0]
    final_sum_1 = sum_1 + list_of_point[number_of_vertices - 1][0] * list_of_point[0][1]
    final_sum_2 = sum_2 + list_of_point[0][0] * list_of_point[number_of_vertices - 1][1]
    final_sum = round(abs((final_sum_1 - final_sum_2)) / 2, 2)
    return final_sum


def creation_json_yolo_to_coco(images_directory, annotation_directory, categories):
    codified_categories = creates_categories(categories)
    base_json = {"licenses": [{"name": "", "id": 0, "url": ""}], "info": {"contributor": "", "date_created": "",
                                                                          "description": "", "url": "", "version": "",
                                                                          "year": ""},
                 "categories": codified_categories,
                 "images": [],
                 "annotations": []
                 }

    for file in os.listdir(images_directory):
        image = {"id": 1, "width": "", "height": "", "file_name": "", "license": 0,
                 "flickr_url": "", "coco_url": "", "date_captured": 0}
        im = Image.open(os.path.join(images_directory, file))
        w, h = im.size
        image["width"] = w
        image["height"] = h
        image["file_name"] = file
        base_json["images"].append(image)
        annotation_file = file[:-3] + "txt"
        new_file = open(os.path.join(annotation_directory, annotation_file), "r")
        id_annotation = 1
        for line in new_file:
            annotation = {"id": "", "image_id": 1, "category_id": "", "segmentation": [],
                          "area": "", "bbox": [], "iscrowd": 0, "attributes": {"occluded": False}}
            ann = line.split()
            point_in_coco_format = yolo_coord_to_coco(list_of_value=ann, width= w, height= h)
            annotation["category_id"] = int(ann[0]) + 1
            annotation["segmentation"] = [[x for t in point_in_coco_format for x in t]]
            annotation["bbox"] = bbox_coco(point_in_coco_format)
            annotation["area"] = area_calculator(list_of_value=point_in_coco_format)
            annotation["id"] = id_annotation
            id_annotation += 1
            base_json["annotations"].append(annotation)

        with open(f"{file[:-4]}.json", "w") as outfile:
            json.dump(base_json, outfile)















































