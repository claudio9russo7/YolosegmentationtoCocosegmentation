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
    x_coord = []
    y_coord = []
    for point in list_of_point:
        x_point = point[0]
        x_coord.append(x_point)
    for point in list_of_point:
        y_point = point[1]
        y_coord.append(y_point)
    min_x = min(x_coord)
    min_y = min(y_coord)
    max_x = max(x_coord)
    max_y = max(y_coord)
    width = round(max_x - min_x, 2)
    height = round(max_y - min_y, 2)
    return [min_x, min_y, width, height]


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


def creation_json_yolo_to_coco(images_directory, annotation_directory, categories, singleormultiple):
    codified_categories = creates_categories(categories)
    if singleormultiple == "m":
        for file in os.listdir(images_directory):
            base_json = {"licenses": [{"name": "", "id": 0, "url": ""}], "info": {"contributor": "", "date_created": "",
                                                                                  "description": "", "url": "",
                                                                                  "version": "",
                                                                                  "year": ""},
                         "categories": codified_categories,
                         "images": [],
                         "annotations": []
                         }
            image = {"id": 1, "width": "", "height": "", "file_name": "", "license": 0,
                     "flickr_url": "", "coco_url": "", "date_captured": 0}
            im = Image.open(os.path.join(images_directory, file))
            w, h = im.size
            image["width"] = w
            image["height"] = h
            image["file_name"] = file
            base_json["images"].append(image)
            annotation_file = os.path.splitext(file)[0] + ".txt"
            new_file = open(os.path.join(annotation_directory, annotation_file), "r")
            id_annotation = 1
            for line in new_file:
                annotation = {"id": "", "image_id": 1, "category_id": "", "segmentation": [],
                              "area": "", "bbox": [], "iscrowd": 0, "attributes": {"occluded": False}}
                ann = line.split()
                point_in_coco_format = yolo_coord_to_coco(list_of_value=ann, width=w, height=h)
                annotation["category_id"] = int(ann[0]) + 1
                annotation["segmentation"] = [[x for t in point_in_coco_format for x in t]]
                annotation["bbox"] = bbox_coco(point_in_coco_format)
                annotation["area"] = area_calculator(list_of_value=point_in_coco_format)
                annotation["id"] = id_annotation
                id_annotation += 1
                base_json["annotations"].append(annotation)

            with open(f"{annotation_file[:-4]}.json", "w") as outfile:
                json.dump(base_json, outfile)
    elif singleormultiple == "s":
        image_id = 1
        base_json = {"licenses": [{"name": "", "id": 0, "url": ""}], "info": {"contributor": "", "date_created": "",
                                                                              "description": "", "url": "",
                                                                              "version": "",
                                                                              "year": ""},
                     "categories": codified_categories,
                     "images": [],
                     "annotations": []
                     }
        for file in os.listdir(images_directory):
            image = {"id": image_id, "width": "", "height": "", "file_name": "", "license": 0,
                     "flickr_url": "", "coco_url": "", "date_captured": 0}
            im = Image.open(os.path.join(images_directory, file))
            w, h = im.size
            image["width"] = w
            image["height"] = h
            image["file_name"] = file
            base_json["images"].append(image)
            annotation_file = os.path.splitext(file)[0] + ".txt"
            new_file = open(os.path.join(annotation_directory, annotation_file), "r")
            id_annotation = 1
            for line in new_file:
                annotation = {"id": "", "image_id": image_id, "category_id": "", "segmentation": [],
                              "area": "", "bbox": [], "iscrowd": 0, "attributes": {"occluded": False}}
                ann = line.split()
                point_in_coco_format = yolo_coord_to_coco(list_of_value=ann, width=w, height=h)
                annotation["category_id"] = int(ann[0]) + 1
                annotation["segmentation"] = [[x for t in point_in_coco_format for x in t]]
                annotation["bbox"] = bbox_coco(point_in_coco_format)
                annotation["area"] = area_calculator(list_of_value=point_in_coco_format)
                annotation["id"] = id_annotation
                id_annotation += 1
                base_json["annotations"].append(annotation)
            image_id += 1
        name_file = input("How do you want to call the final file?")
        with open(f"{name_file}.json", "w") as outfile:
            json.dump(base_json, outfile)
    else:
        print("Remember to select the mode for the json output:\n"
              "'m' = if you want multiple file, so a file for every yolo_annotation\n"
              "'s' = if you want a single file for all yolo_annotation")









































