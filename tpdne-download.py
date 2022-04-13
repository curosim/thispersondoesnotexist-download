import urllib.request
import time
from random import uniform
from multiprocessing.dummy import Pool as ThreadPool
import requests
import glob
import os
import hashlib

#change to maximum number of images needed
number_of_images = int(input("Enter number of images: "))

def file_hash(filepath):
	with open(filepath, 'rb') as f:
		return hashlib.md5(f.read()).hexdigest()

def remove_duplicates():
	print("[*] Removing duplicates now")
	hashes = []
	for jpgfile in glob.iglob(os.path.join('.', "*.jpg")):
		md5_hash = file_hash(jpgfile)
		if md5_hash in hashes: os.remove(jpgfile)
		else: hashes.append(md5_hash)
	print("[*] {0} unique images in total...".format(len(hashes)))

def download_image(i):
	time.sleep(uniform(0.1,2))
	print("Downloading Image: {0}".format(i))
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/81.{0}'.format(i)}
	try:
		response = requests.get('https://thispersondoesnotexist.com/image', headers=headers)
		if response.status_code == 200:
			img_name = "image{0}.jpg".format(i)
			with open(img_name, 'wb') as f:
				f.write(response.content)
	except: pass

def main():
	# Make the Pool of workers
	pool = ThreadPool(10)

	# Open the URLs in their own threads
	# and return the results
	results = pool.map(download_image, range(0, number_of_images))

	# Close the pool and wait for the work to finish
	pool.close()
	pool.join()

	print("Done...")

	remove_duplicates()


main()


"""
for num in range(0,number_of_images):
	print("downloading image number " + str(num+1))
	#opener = urllib.request.build_opener()
	#opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0')]
	#urllib.request.install_opener(opener)
	#urllib.request.urlretrieve("https://thispersondoesnotexist.com/image", "image" + str(num+1) + ".jpg")
	if num < number_of_images:
		time.sleep(uniform(1.3,3.4))
"""
