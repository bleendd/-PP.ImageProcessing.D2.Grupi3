import glob
import os
import multiprocessing as mp
import psutil
import time
import datetime
from PIL import Image
from random import randint

process_count = 8

def make_image_thumbnail(worker: int) -> None:
	p = psutil.Process()
	image_files = glob.glob("Images/*.jpg")
	p.cpu_affinity([worker])
	image_files = image_files[worker::process_count]
	for filename in image_files:
		base_filename, file_extension = os.path.splitext(filename)
		thumbnail_filename = f"Images_{process_count}/{randint(0, 99999999)}{file_extension}"
		image = Image.open(filename)
		image.thumbnail(size=(128, 128))
		image.save(thumbnail_filename, "JPEG")


def child(worker: int) -> None:
    p = psutil.Process()
    print(f"Child #{worker}: {p}, affinity {p.cpu_affinity()}", flush=True)
    time.sleep(1)
    p.cpu_affinity([worker])
    print(f"Child #{worker}: Set my affinity to {worker}, affinity now {p.cpu_affinity()}", flush=True)

    time.sleep(1 + 3 * worker)
    print(f"Child #{worker}: Starting CPU intensive task now for 4 seconds on {p.cpu_affinity()}...", flush=True)
    t_end = time.perf_counter() + 4
    while time.perf_counter() < t_end:
        pass
    print(f"Child #{worker}: Finished CPU intensive task on {p.cpu_affinity()}", flush=True)


if __name__ == "__main__" :
	run_detyra_2 = True
	start = datetime.datetime.now()
	if(run_detyra_2):
		with mp.Pool() as pool:
			workers: int = process_count
			print(f"Running pool with {workers} cores")
			for i in range(workers):
			    pool.apply_async(make_image_thumbnail, (i,))
			pool.close()
			pool.join()
		pass
	else:
		with mp.Pool() as pool:
			workers: int = pool._processes
			print(f"Running pool with {workers} cores")
			for i in range(workers):
			    pool.apply_async(child, (i,))
			pool.close()
			pool.join()
		pass
	end = datetime.datetime.now()
	delta = end - start
	print(delta)