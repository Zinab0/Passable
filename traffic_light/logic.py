# # Default values of signal times
# import math

# timeElapsed = 0

# currentGreen = 0 # Indicates which signal is green
# nextGreen = (currentGreen+1)% noOfSignals
# currentYellow = 0
# # Indicates whether yellow signal is on or off

# vehicles = {'right': {0:[], 1:[], 2:[], 'crossed':0}, 'down': {0:[], 1:[], 2:[], 'crossed':0}, 'left': {0:[], 1:[], 2:[], 'crossed':0}, 'up': {0:[], 1:[], 2:[], 'crossed':0}}
# vehicleTypes = {0:'car', 1:'bus', 2:'truck', 3:'rickshaw', 4:'bike'}
# directionNumbers = {0:'right', 1:'down', 2:'left', 3:'up'}


# # Red signal time at which cars will be detected at a signal
# detectionTime = 5
# speeds = {'car':2.25, 'bus' :1.8, 'truck' :1.8, 'rickshaw' :2, 'bike' :2.5} # average speeds of vehicles

# def setTime():
#     global noOfCars, noOfBikes, noOfBuses, noOfTrucks, noOfRickshaws, noOfLanes
#     global carTime, busTime, truckTime, rickshawTime, bikeTime
#     print("say detecting vehicles, "+directionNumbers[(currentGreen+1)%noOfSignals])
#     noOfCars, noOfBuses, noOfTrucks, noOfRickshaws, noOfBikes = 0,0,0,0,0
#     for j in range(len(vehicles[directionNumbers[nextGreen]][0])):
#         vehicle = vehicles[directionNumbers[nextGreen]][0][j]
#         if(vehicle.crossed==0):
#             vclass = vehicle.vehicleClass
#             noOfBikes += 1
#     for i in range(1,3):
#         for j in range(len(vehicles[directionNumbers[nextGreen]][i])):
#             vehicle = vehicles[directionNumbers[nextGreen]][i][j]
#             if(vehicle.crossed==0):
#                 vclass = vehicle.vehicleClass
#                 # print(vclass)
#                 if(vclass=='car'):
#                     noOfCars += 1
#                 elif(vclass=='bus'):
#                     noOfBuses += 1
#                 elif(vclass=='truck'):
#                     noOfTrucks += 1
#                 elif(vclass=='rickshaw'):
#                     noOfRickshaws += 1
#     # print(noOfCars)
#     greenTime = math.ceil(((noOfCars*carTime) + (noOfRickshaws*rickshawTime) + (noOfBuses*busTime) + (noOfTrucks*truckTime)+ (noOfBikes*bikeTime))/(noOfLanes+1))
#     # greenTime = math.ceil((noOfVehicles)/noOfLanes) 
#     print('Green Time: ',greenTime)
#     if(greenTime<defaultGreenMinimum):
#         greenTime = defaultGreenMinimum
#     elif(greenTime>defaultGreenMaximum):
#         greenTime = defaultGreenMaximum
#     # greenTime = random.randint(15,50)
#     signals[(currentGreen+1)%(noOfSignals)].green = greenTime

import math
import random
import time

defaultRed = 150
defaultYellow = 2
defaultGreen = 10
defaultGreenMinimum = 5
defaultGreenMaximum = 30
signals = [ ]
noOfSignals = 4
carTime = 2.25
noOfLanes = 4
simTime = 300 # change this to change time of simulation -> 300 seconds (i.e 5 minutes)
is_accident = 0
######### ADD TRAFIC ID #############
class TrafficSignal:
    def __init__(self, red=defaultRed, yellow=defaultYellow, green=defaultGreen, is_accident=0):
        self.red = red
        self.yellow = yellow
        self.green = green
        self.green_min = defaultGreenMinimum
        self.green_max = defaultGreenMaximum
        self.is_accident = is_accident

    def update_signal(self, cars, is_accident):
        # Adjust green light time based on number of cars
        self.green = math.ceil((cars*carTime) / (noOfLanes+1))
        
        # Make sure green light time stays within limits
        self.green = max(self.green, self.green_min)
        self.green = min(self.green, self.green_max)

        # Update is_accident attribute
        self.is_accident = is_accident

    def display_signal(self):
        print(f"Green: {self.green} seconds, Yellow: {self.yellow} seconds, Red: {self.red} seconds. Accident: {self.is_accident}")

def simulate_traffic(signals, sim_time):
    start_time = time.time()
    current_time = 0
    while current_time < sim_time:
        print("\n")
        print("Time:", current_time)
        for signal in signals:
            signal.display_signal()
        time.sleep(10)  # Simulate one second passing
        current_time = int(time.time() - start_time)

        # Update signal based on traffic conditions (random for now)
        for signal in signals:
            cars = random.randint(0, 50)  # Simulate number of cars
            is_accident = random.randint(0, 1)  # Simulate if there's an accident
            print(f"Updating signal with {cars} cars and accident: {is_accident}")
            signal.update_signal(cars, is_accident)

def main():
    signals = [TrafficSignal() for _ in range(noOfSignals)]
    simulate_traffic(signals, simTime)

if __name__ == "__main__":
    main()
