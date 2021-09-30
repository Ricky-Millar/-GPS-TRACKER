import asyncio
from mavsdk import System
import pyproj
import math

#TODO Use terminal to exicute following commands, also needs Qcontrol open to make simulation work.
# # Navigate to PX4-Autopilot repo
# cd PX4-Autopilot
# # Build and runs SITL simulation with jMAVSim to test the setup
# make px4_sitl jmavsim

async def run():
    # Init the drone
    drone = System()

    # await drone.connect(system_address='tcp://[192.168.1.65][:5760]')
    await drone.connect()
    print('banana')
    # Start the tasks
    asyncio.ensure_future(print_position(drone))


async def print_position(drone):
    async for position in drone.telemetry.position():
        #Gets the current position from the drone and sends it into the vactor calculator
        asyncio.ensure_future(calculate_vector(position.latitude_deg, position.longitude_deg, position.absolute_altitude_m , 47.39834979992792, 8.54374869374406  , 487.9540100097656))

async def calculate_vector(Dlat, Dlng, Dheight, Plat, Plng, Pheight):
    geodesic = pyproj.Geod(ellps='WGS84')
    #Calculates the azimush angles and the distance between Pilot and Drone
    fwd_azimuth, back_azimuth, distance = geodesic.inv(Dlng, Dlat, Plng, Plat)
    #Calculates the angle between the height of the pilot and the drone.
    height_angle = math.degrees(math.atan((Dheight-Pheight)/distance))  #Tan0 = opposite/adjacent
    print(f"Azamuth angle : {fwd_azimuth}      Elevation angle : {height_angle}")

if __name__ == "__main__":
    # Start the main function
    asyncio.ensure_future(run())

    # Runs the event loop until the program is canceled with e.g. CTRL-C
    asyncio.get_event_loop().run_forever()