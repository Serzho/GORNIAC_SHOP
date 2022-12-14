from PIL import Image, ImageFilter
from pathlib import Path
from service import base_logger
from cfg import IN_DOCKER


def log(message: str) -> None:
    module_name = "IMAGE_UPDATER"
    base_logger(msg=message, module_name=module_name)


def update_images():
    images_dict = {}
    images_dir = 'static/images/logo' if not IN_DOCKER else "core/static/images/logo"
    files_list = [file for file in Path(images_dir).iterdir() if file.is_file()]
    for file in files_list:
        images_dict.update({file.name: Image.open(file)})
    log(f"Found {len(images_dict)} images")

    soldout_template = Image.open(f"{images_dir}/soldout/soldout.png")
    soldout_mask = Image.open(f"{images_dir}/soldout/soldout_mask.png").convert('L')

    for img_name in images_dict.keys():
        current_image = images_dict[img_name]
        current_image = current_image.filter(ImageFilter.GaussianBlur(radius=2))
        current_image.paste(soldout_template, (0, 0), soldout_mask)
        current_image.save(f"{images_dir}/soldout/soldout_{img_name}")
        log(f"{img_name} updated")


if __name__ == "__main__":
    update_images()
