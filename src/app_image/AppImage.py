import subprocess
import os
from PIL import Image
import keras_ocr

class AppImage:
    def __init__(self, adb_host, screenshots_path):
        self.adb_host = adb_host
        self.screenshots_path = screenshots_path
        self.image = None
        
    def take_screenshot(self, file_name: str):
        subprocess.run(["adb", '-s', self.adb_host, "shell", "screencap", "-p", "/sdcard/screen.png"])
        subprocess.run(["adb", '-s', self.adb_host, "pull", "/sdcard/screen.png", os.path.join(self.screenshots_path, file_name + '.png')])
    
    def get_image_color(self, image_name: str, region: tuple):
        self.image = Image.open(os.path.join(self.screenshots_path, image_name + '.png'))
        cropped_image = self._crop_image(region)
        cropped_image.save(os.path.join(self.screenshots_path, image_name + '.png'))
        _image = Image.open(os.path.join(self.screenshots_path, image_name + '.png'))
        width, height = _image.size
        for x in range(width):
            for y in range(height):
                print(_image.getpixel((x, y)))
                r, g, b, a = _image.getpixel((x, y))
                print(f'{r} {g} {b} {a}')
                return f'{r} {g} {b} {a}'

    def get_app_action_from_image(self, image_name: str, region: tuple) -> str:
        self._load_image(image_name)
        cropped_image = self._crop_image(region)
        cropped_image.save(os.path.join(self.screenshots_path, image_name + '.png'))
        print("========= Transforming Image from Text  =========")
        text = self._recognize_text(image_name)
        return text
    
    def _load_image(self, image_name):
        self.image = Image.open(os.path.join(self.screenshots_path, image_name + '.png')).convert('L')
    
    def _crop_image(self, region):
        return self.image.crop(region)
    
    def _recognize_text(self, image_name):
        pipeline = keras_ocr.pipeline.Pipeline()
        img = [
            keras_ocr.tools.read(file) for file in [os.path.join(self.screenshots_path, image_name + '.png')]
        ]
        prediction_groups = pipeline.recognize(img)
        return [text[0] for text in prediction_groups[0]]
