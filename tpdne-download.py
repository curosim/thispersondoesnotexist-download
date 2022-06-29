import time
from random import uniform
from multiprocessing.dummy import Pool as ThreadPool
import requests
import glob
import os
import hashlib

# Appendix for image file names, simply so we wont overwrite images from previous executions.
timestamp = int(time.time())

def file_hash(filepath):
	""" Generate MD5 Hash of a file.
	"""
	with open(filepath, 'rb') as f:
		return hashlib.md5(f.read()).hexdigest()

def remove_duplicates():
	""" Remove duplicate images, duplicates are found with MD5 Hash.
	"""
	total_removed = 0
	hashes = []

	# Find all JPG Files with the appendix of this execution (timestamp)
	for jpgfile in glob.iglob(os.path.join('./images/', "{0}*.jpg".format(timestamp))):
		
		# Calculate a MD5 Hash of the file
		md5_hash = file_hash(jpgfile)
		if md5_hash in hashes:

			# Remove the file
			os.remove(jpgfile)
			total_removed = total_removed+1
		else: hashes.append(md5_hash)
	total_images = len(hashes)
	return total_images, total_removed

def download_image(i):
	""" Download image from thispersondoesnotexist.com and save it as JPG.
	"""

	# This sleep function is of course not really necessary, but since the website generates a new image based on time
	# and not request, we want some delay in our requests to have more unique images. Duplicates get removed anyway.
	time.sleep(uniform(0.1,3))

	print("  > Downloading Image: {0}".format(i+1))
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
	try:
		# Download image and save it as a file
		response = requests.get('https://thispersondoesnotexist.com/image', headers=headers)
		if response.status_code == 200:
			img_path = "images/{0}_face_{1}.jpg".format(timestamp, i)
			with open(img_path, 'wb') as f:
				f.write(response.content)
	except: pass

def banner():
	print("  __________  ____  _   ________   ____                      __                __")
	print(" /_  __/ __ \\/ __ \\/ | / / ____/  / __ \\____ _      ______  / /___  ____ _____/ /")
	print("  / / / /_/ / / / /  |/ / __/    / / / / __ \\ | /| / / __ \\/ / __ \\/ __ `/ __  / ")
	print(" / / / ____/ /_/ / /|  / /___   / /_/ / /_/ / |/ |/ / / / / / /_/ / /_/ / /_/ /  ")
	print("/_/ /_/   /_____/_/ |_/_____/  /_____/\\____/|__/|__/_/ /_/_/\\____/\\__,_/\\__,_/   ")
	print("                                                                                 ")
	print("Automated download of faces from thispersondoesnotexist.com - Author: @curosim\n")


def main():
	banner()

	# It doesnt really make sense to have more threads, 4 is already too much tbh.
	# The website generates new faces based on time, so faster requests make no difference, we just download more duplicates.
	num_threads = 4
	
	number_of_images = int(input("[*] Enter number of images: "))
	
	# Create directory if it doesnt exist
	os.makedirs('./images/', exist_ok=True)

	# Start image download in multiple threads
	pool = ThreadPool(num_threads)
	results = pool.map(download_image, range(0, number_of_images))
	pool.close()
	pool.join()

	print("[*] {0} images downloaded".format(number_of_images))
	print("[*] Removing duplicates now")
	total_images, total_removed = remove_duplicates()
	print("[!] Found {0} unique images, {1} duplicates removed".format(total_images, total_removed))
	print("[*] Execution finished")

main()
