import urllib.request
import time
from random import uniform
from multiprocessing.dummy import Pool as ThreadPool
import requests
import glob
import os
import hashlib

def file_hash(filepath):
	""" Generate MD5 Hash of an file.
	"""
	with open(filepath, 'rb') as f:
		return hashlib.md5(f.read()).hexdigest()

def remove_duplicates():
	""" Remove duplicate images.
	"""
	hashes = []
	for jpgfile in glob.iglob(os.path.join('./images/', "*.jpg")):
		md5_hash = file_hash(jpgfile)
		if md5_hash in hashes: os.remove(jpgfile)
		else: hashes.append(md5_hash)
	return hashes

def download_image(i):
	""" Download image from thispersondoesnotexist.com
	"""

	# This sleep function is of course not really necessary, but since the website generates a new image based on time
	# and not request, we want some delay in our requests to have more unique images. Duplicates get removed anyway.
	time.sleep(uniform(0.1,5))

	print("  > Downloading Image: {0}".format(i+1))
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
	try:
		response = requests.get('https://thispersondoesnotexist.com/image', headers=headers)
		if response.status_code == 200:
			img_path = "images/face_{0}.jpg".format(i)
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
	print("Automate the download of faces from thispersondoesnotexist.com - Author: @curosim\n")


def main():
	banner()

	# It doesnt really make sense to have more threads, 4 is already too much tbh.
	# The website generates new faces based on time, so faster requests make no difference, we just download more duplicates.
	num_threads = 4

	#change to maximum number of images needed
	number_of_images = int(input("[*] Enter number of images: "))

	# Download images with multiple threads
	pool = ThreadPool(num_threads)
	results = pool.map(download_image, range(0, number_of_images))
	pool.close()
	pool.join()

	print("[*] {0} images downloaded".format(number_of_images))
	print("[*] Removing duplicates now")
	hashes = remove_duplicates()
	print("[!] Found {0} unique images, {1} duplicates removed".format(len(hashes), number_of_images-len(hashes)))
	print("[*] Execution finished")

main()