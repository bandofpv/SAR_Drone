#print ("Start simulator (SITL)")

#import dronekit_sitl
import time

# Import DroneKit-Python
from dronekit import connect, VehicleMode

#sitl = dronekit_sitl.start_default()
#connection_string = sitl.connection_string()

# Connect to the Vehicle.
print("Connecting to vehicle on: serial0")
vehicle = connect('/dev/serial0', wait_ready=True, baud=921600)

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print ("Basic pre-arm checks")

    # Check that vehicle is armable
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("\nSet Vehicle.mode = GUIDED (currently: %s)" % vehicle.mode.name)
    #vehicle.mode = VehicleMode("GUIDED")
    while not vehicle.mode.name == 'GUIDED':  # Wait until mode has changed
        print(" Waiting for mode change ...")
        time.sleep(1)

    print ("\nSet Vehicle.armed=True (currently: %s)" % vehicle.armed)
    vehicle.armed = True
    while not vehicle.armed:
        print (" Waiting for arming...")
        time.sleep(1)
    print (" Vehicle is armed: %s" % vehicle.armed)

    print ("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print ("Global Location (relative altitude): %s" % vehicle.location.global_relative_frame)
        print (" Altitude: ", vehicle.location.global_relative_frame.alt)
        #Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95:
            print ("Reached target altitude")
            break
        time.sleep(1)

# Take off to 10m
arm_and_takeoff(10)

print("Take off complete")

# Hover for 10 seconds
time.sleep(10)

print("Now let's land")
vehicle.mode = VehicleMode("LAND")

# Close vehicle object
vehicle.close()
