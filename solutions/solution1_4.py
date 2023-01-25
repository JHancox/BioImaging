%%time
import threading
import time
from cucim import CuImage
import numpy as np

# TODO Try changing the number of threads and see what effect
# it has on the overall run time
num_threads = 32
level = 1

input_file = "data/patient_100_node_0.tif"
cuslide = CuImage(input_file)
sizes=cuslide.metadata["cucim"]["resolutions"]
width = sizes["level_dimensions"][level][0]
height = sizes["level_dimensions"][level][1]

# create the array to contain the whole image
img = np.zeros((width,height,3), dtype=np.uint8)
print(img.shape)

class loaderThread (threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        x = (width // num_threads) * (self.threadID)
        img_s = cuslide.read_region((x,0),(width//num_threads, height), level)
        img[x:x+(width//num_threads),:,:] = np.swapaxes(np.array(img_s),0,1)

threads = []

print("Starting Threads")
for i in range(num_threads):
    # Create new threads
    thread = loaderThread(i)
    thread.start()
    threads.append(thread)

# Wait for all threads to complete
for t in threads:
    t.join()
    
print("Exited Threads")
