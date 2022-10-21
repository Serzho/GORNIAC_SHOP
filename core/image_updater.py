from PIL import Image, ImageFilter
from pathlib import Path


def update_images():
    images_dict = {}
    files_list = [file for file in Path('static/images/logo').iterdir() if file.is_file()]
    for file in files_list:
        images_dict.update({file.name: Image.open(file)})

    soldout_template = Image.open("static/images/logo/soldout/soldout.png")
    soldout_mask = Image.open("static/images/logo/soldout/soldout_mask.png").convert('L')

    for img_name in images_dict.keys():
        current_image = images_dict[img_name]
        current_image = current_image.filter(ImageFilter.GaussianBlur(radius=2))
        current_image.paste(soldout_template, (0, 0), soldout_mask)
        current_image.save(f"static/images/logo/soldout/soldout_{img_name}")


if __name__ == "__main__":
    update_images()