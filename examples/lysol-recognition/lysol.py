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


def get_details_of_best_result(results, labels):
    best_result = max(results, key=itemgetter(1))
    best_result_label_index = best_result[0]
    best_result_score = best_result[1]
    return {"label": labels[best_result_label_index], "score": best_result_score}


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

        # Get the label of the best result and send it with OSC
        details_of_best_result = get_details_of_best_result(results, labels)
        print(details_of_best_result)
        osc.send_message(path, details_of_best_result["label"])

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
