
from check import creation_json_yolo_to_coco

annotation_to_elaborate_directory = r"C:\Users\Claudio\PycharmProjects\YolosegmentationtoCocosegmentation\annotation_to_elaborate_directory"
images_to_elaborate_directory = r"C:\Users\Claudio\PycharmProjects\YolosegmentationtoCocosegmentation\images_to_elaborate_directory"
annotation_elaborate_directory = r"C:\Users\Claudio\PycharmProjects\YolosegmentationtoCocosegmentation\annotation_elaborate"


categorie = ["Stomata"]
creation_json_yolo_to_coco(images_to_elaborate_directory,annotation_to_elaborate_directory, annotation_elaborate_directory,
                           categories=categorie, singleormultiple= "m")



