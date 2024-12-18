import math
from ultralytics import YOLO
from PIL import Image


def load_ai_model(model_path):
    model = YOLO(model_path)
    return model

# Accident Predicion
def accPredict(image):
    model = load_ai_model('traffic_light/accAI.pt')
    prediction = model.predict(source=image,imgsz=650,conf=0.4, save=True)
    visualize(prediction)
    return prediction

# Cngestion Predicion
def conPredict(image):
    model = load_ai_model('traffic_light/conAI.pt')
    prediction = model.predict(source=image, imgsz=650, conf=0.5, save=True)
    visualize(prediction)
    return prediction

def visualize(results):
    for i, r in enumerate(results):
        # Plot results image
        im_bgr = r.plot()  # BGR-order numpy array
        im_rgb = Image.fromarray(im_bgr[..., ::-1])  # RGB-order PIL image

        # Save results to disk
        r.save(filename=f'traffic_light/static/traffic_light/img/results{i}.jpg')


def density(number_of_vehicles):
    # return 0 if number_of_vehicles < 9 else (1)
  return "Low" if number_of_vehicles < 9 else ("Medium" if number_of_vehicles <= 20 else "High")

def green_signal_time(number_of_vehicles):
    # Average times for cars to pass the intersection
    carTime = 3
    # number of lanes
    numLanes = 4
    # Default minimum and maximum green light time
    defaultMinimum = 5
    defaultMaximum = 30
    # Calculate the green light time
    GLT = math.ceil((number_of_vehicles * carTime)/(numLanes+1))
    if(GLT<defaultMinimum):
      GLT = defaultMinimum
    elif(GLT>defaultMaximum):
      GLT = defaultMaximum
    return GLT