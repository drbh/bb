from bb import BearingBuilder, BearingConfig
import time
print("CAD env loaded")

config = BearingConfig(
    number_of_balls=8,
    circle_radius=20,
    ball_diameter=4.1,
    thickness=4,
)
print(config)

bearing = BearingBuilder(config).build()
print(bearing)

start_time = time.time()
print("Start export")
bearing.export_3mf(".")
print("SVG export time: ", time.time() - start_time)
