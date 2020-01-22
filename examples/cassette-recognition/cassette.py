from edgetpu.classification.engine import ClassificationEngine
from PIL import Image
import cv2
import re
import os
import click
from oscpy.client import OSCClient
from operator import itemgetter

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

# This function parses the labels.txt and puts it in a python dictionary


def loadLabels(labelPath):
    p = re.compile(r'\s*(\d+)(.+)')
    with open(labelPath, 'r', encoding='utf-8') as labelFile:
        lines = (p.match(line).groups() for line in labelFile.readlines())
        return {int(num): text.strip() for num, text in lines}

# This function takes in a PIL Image from any source or path you choose


def classifyImage(image, engine):
    # Classify and ouptut inference
    classifications = engine.classify_with_image(image)
    return classifications


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    '-ip', '--ip-address', 'ip_address',
    default=None,
    required=True,
    help="Used to specify the port that's listening for request on the OSC server handling these OSC messages."
)
@click.option(
    '-p', '--port', 'port',
    default=None,
    required=True,
    help="Used to specify the port that's listening for request on the OSC server handling these OSC messages."
)
@click.option(
    '--path', 'path',
    default='/',
    required=True,
    help="Path (endpoint) at which the OSC server is listening for requests."
)
@click.option(
    '--model', 'model_path',
    default='./model.tflite',
    required=True,
    help="Path to the Tensorflow Lite model file (*.tflite)."
)
@click.option(
    '--labels', 'labels_path',
    default='./labels.txt',
    required=True,
    help="Path to the labels file for the model (*.txt)."
)
def main(ip_address, port, path, model_path, labels_path):
    # Setup the OSC Client
    osc = OSCClient(ip_address, int(port), encoding="utf8")

    # Load your model onto your Coral Edgetpu
    engine = ClassificationEngine(model_path)
    labels = loadLabels(labels_path)

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Format the image into a PIL Image so its compatable with Edge TPU
        cv2_im = frame
        pil_im = Image.fromarray(cv2_im)

        # Resize and flip image so its a square and matches training
        pil_im.resize((224, 224))
        pil_im.transpose(Image.FLIP_LEFT_RIGHT)

        # Classify and display image
        results = classifyImage(pil_im, engine)
        cv2.imshow('frame', cv2_im)

        print(results)
        bestResult = max(results, key=itemgetter(1))
        if (bestResult[0] == 0 and bestResult[1] > 0.9):
            print("Cassette")
            osc.send_message(path, "ON")
        else:
            print("No Cassette")
            osc.send_message(path, "OFF")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
