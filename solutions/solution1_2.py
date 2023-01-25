%%time
import multiprocessing
import time

num_processes = 16 # experiment with this setting

class loaderProcess(multiprocessing.Process):
    def __init__(self, processID):
        # Class initialisation - set its ID
        multiprocessing.Process.__init__(self)
        self.processID = processID

    def run(self):
        print("Starting process {}".format(self.processID))
        start = timer()
        width, height = slide.level_dimensions[2]
        x = (width // num_processes) * (1-self.processID)
        img = slide.read_region((x,0), 2,(width//num_processes, height))
        end = timer()
        print("Exiting process {}, running time = {}".format(self.processID, str(end-start)))

processes = []

for i in range(num_processes):
    # Create new threads
    process = loaderProcess(i)
    process.start()
    processes.append(process)

# Wait for all threads to complete
for p in processes:
    p.join()
    
print("Exiting Main Process")