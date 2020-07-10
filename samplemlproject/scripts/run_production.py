#####     Run Production     #####
from os.path import join, splitext, basename
import numpy as np
from tensorflow.keras.preprocessing import image
import time
# import opcua
# from opcua import Client, ua
import os
from tensorflow.keras.models import load_model
import click
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class PredictionClass(object):

    def __init__(self, model_path: str, threshold: float = 0.5):
        self.model_path = model_path
        self.counter = 0
        self.loaded_model = None
        self.threshold = threshold

    def predict(self, path, timeSec):

        # Bild laden
        test_image = image.load_img(path, target_size=(512, 512))
        test_image = image.img_to_array(test_image)
        # 1 / 255
        test_image *= 0.00392156862745098
        test_image = np.expand_dims(test_image, axis=0)

        result = self.loaded_model.predict(test_image)
        result_val = result[0][0]
        self.counter = self.counter + 1

        # vorher auf == 1 abgefragt
        if result_val >= self.threshold:
            time.sleep(0.001)
            prediction = 'schlecht'
            cl_prefix = "_R1_"
        else:
            time.sleep(0.001)
            prediction = 'gut'
            cl_prefix = "_R0_"
        file_path, ext = splitext(path)
        os.rename(path, f"{file_path}{cl_prefix}{result_val:0.4f}{ext}")

        # Definition der aktuellen Zeit
        duration = time.time() - timeSec
        # Berechnung der benötigten Zeit und Ausgabe des Ergebnisses auf der Konsole
        print(f"{basename(path)} Duration: {duration:0.3f} Image: {self.counter} Result: {prediction} {result_val:0.4f}")

    def load_model(self):
        if self.loaded_model is None:
            self.loaded_model = load_model(self.model_path)
            print(f"Modell geladen: {self.model_path}")


# Klassen-Definition "MyFileSystemHandler"
class MyFileSystemHandler(FileSystemEventHandler):
    counting = 0
    Kamera_Online = 0

    def __init__(self, predictor: PredictionClass):
        self.predictor = predictor

    def on_created(self, event):
        # Festlegen der Startzeit der Verarbeitung
        start_time = time.time()
        if self.counting == 0:
            self.predictor.load_model()
            self.counting = 1
            self.Kamera_Online = 1
            return

        try:
            self.predictor.predict(event.src_path, start_time)
        except PermissionError:
            while True:
                try:
                    self.predictor.predict(event.src_path, start_time)
                    break
                except PermissionError:
                    pass


@click.command()
@click.argument("image_path")
@click.argument("model_path")
def run(image_path, model_path):
    # Instanziieren der PredictionClass
    predictor = PredictionClass(model_path=model_path)
    event_handler = MyFileSystemHandler(predictor)
    observer = Observer()
    lock_file = join(image_path, "loading.txt")
    # Angabe des zu überwachenden Pfades
    observer.schedule(event_handler, path=image_path, recursive=False)
    observer.start()
    file = open(lock_file, "w")
    file.close()
    time.sleep(3)
    os.remove(lock_file)

    try:
        while True:
            time.sleep(0.001)
    except KeyboardInterrupt:
        observer.stop()
        print('Stop KeyboardInterrupt')
    observer.join()


if __name__ == "__main__":
    run()
