import os
import json


def duplicate_image_names(coco_file_paths):
    message = None
    all_image_names = []
    for coco_file in coco_file_paths:
        with open(coco_file, "r") as f:
            json_file = json.load(f)
        for image_dict in json_file["images"]:
            image_name = image_dict["file_name"]
            all_image_names.append(image_name)
    n_duplicate_names = len(all_image_names) - len(set(all_image_names))
    if n_duplicate_names:
        duplicate_list = [all_image_names.count(i) for i in all_image_names]
        duplicate_dict = {
            i: j for i, j in zip(all_image_names, duplicate_list) if j > 1
        }
        duplicate_names = list(duplicate_dict.keys())
        # TODO: Print out the coco files to check too if duplicates are found
        message = (
            f"{n_duplicate_names} duplicate image names detected"
            f"in COCO files.\n Duplicates found for files: {duplicate_names}."
        )
    return message


def coco_validator(coco, file_path):
    messages = []
    file_base_name = os.path.basename(file_path)
    missing_keys, n_missing_keys = check_coco_keys(coco)
    if n_missing_keys:
        messages.append(
            f"COCO file {file_base_name} was missing"
            f" {n_missing_keys} key(s) in the file. "
            f"The following are the missing keys:"
            f"{missing_keys}"
        )
    try:
        category_message, result = check_coco_categories(coco["categories"])
        if result:
            messages.append(
                f"COCO file {file_base_name} has a problematic categories object "
                f"with the following message: {category_message}"
            )
        images_message, result = check_coco_images(coco["images"])
        if result:
            messages.append(
                f"COCO file {file_base_name} has a problematic images object"
                f"with the following message: {images_message}"
            )
        annotations_message, result = check_coco_annotations(coco["annotations"])
        if result:
            messages.append(
                f"COCO file {file_base_name} has a problematic annotations object"  # noqa
                f"with the following message: {annotations_message}"
            )
    except Exception as e:
        messages.append(
            "Error encountered while going through COCO file "
            f"{file_base_name} with arguments {e.args}"
        )
        pass
    return messages


def check_coco_keys(coco):
    needed_keys = {"info", "categories", "images", "annotations"}
    existing_keys = set(coco.keys())
    missing_keys = needed_keys - existing_keys
    n_missing_keys = len(needed_keys - existing_keys)
    return missing_keys, n_missing_keys


def check_coco_categories(categories_list):
    needed_keys = {"id", "name"}
    ids = []
    for category_dict in categories_list:
        ids.append(int(category_dict["id"]))
        existing_keys = set(category_dict.keys())
        missing_keys = needed_keys - existing_keys
        n_missing_keys = len(missing_keys)
        if n_missing_keys:
            return f"Missing keys: {missing_keys}", True
    if max(ids) != len(categories_list):
        return "IDs of categories don't match #items", True
    return "", False


def check_coco_images(images_list):
    needed_keys = {"id", "file_name", "height", "width"}
    ids = []
    for images_dict in images_list:
        ids.append(int(images_dict["id"]))
        existing_keys = set(images_dict.keys())
        missing_keys = needed_keys - existing_keys
        n_missing_keys = len(missing_keys)
        if n_missing_keys:
            return f"Missing keys: {missing_keys}", True
    if max(ids) != len(images_list):
        return "IDs of images don't match #items", True
    return "", False


def check_coco_annotations(annotations_list):
    needed_keys = {
        "id",
        "image_id",
        "category_id",
        "bbox",
        "area",
        "segmentation",
        "iscrowd",
    }
    ids = []
    for annotations_dict in annotations_list:
        ids.append(int(annotations_dict["id"]))
        existing_keys = set(annotations_dict.keys())
        missing_keys = needed_keys - existing_keys
        n_missing_keys = len(missing_keys)
        if n_missing_keys:
            return f"Missing keys: {missing_keys}", True
    if (max(ids) + 1) != len(annotations_list):
        return "IDs of annotations don't match #items", True
    return "", False
