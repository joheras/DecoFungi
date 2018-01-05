# import the necessary packages
import numpy as np
import cv2

def prepare_image(image, fixedSize):
	# convert the image from BGR to RGB, then resize it to a fixed size,
	# ignoring aspect ratio
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	image = cv2.resize(image, tuple(fixedSize))

	# return the image
	return image

def build_batch(paths, fixedSize):
	# load the images from disk, prepare them for extraction, and convert
	# the list to a NumPy array
	images = [prepare_image(cv2.imread(p), fixedSize) for p in paths]
	images = np.array(images, dtype="float")

	# extract the labels from the image paths
	labels = [":".join(p.split("/")[-2:]) for p in paths]

	# return the labels and images
	return (labels, images)

def control_image(path):
	classes = ["azul_acido","azul_brillante","azul_chicago","azul_directo_1","azul_directo_2", "azul_remazol","fucsina",
			   "fucsina_acida_1", "fucsina_acida_2", "fucsina_acida", "indigo_1", "indigo_2", "indigo_carmin", "indigo",
	 "naranja_metilo_2","naranja_metilo","naranja_2", "naranja", "rbbr"]
	for c in classes:
		if c in path:
			return "/home/joheras/Escritorio/Research/Fungi/FungiImages/decoloracion/"+c+"/control.jpg"

def build_batch_control(paths, fixedSize):
	# load the images from disk, prepare them for extraction, and convert
	# the list to a NumPy array
	images = [prepare_image(cv2.imread(control_image(p)), fixedSize) for p in paths]
	images = np.array(images, dtype="float")


	# return the labels and images
	return images

def control_image_evaluation(path):
	print("/home/joheras/Escritorio/Research/Fungi/ControlNewImages" + path + "_control.jpg")
	return "/home/joheras/Escritorio/Research/Fungi/ControlNewImages/" + path + "_control.jpg"


def build_batch_control_evaluation(paths, fixedSize):
	# load the images from disk, prepare them for extraction, and convert
	# the list to a NumPy array
	images = [prepare_image(cv2.imread(control_image_evaluation(im[im.rfind('/')+1:im.rfind('_')])), fixedSize) for im in paths]
	images = np.array(images, dtype="float")# return the labels and images
	return images

def chunk(l, n):
	# loop over the list `l`, yielding chunks of size `n`
	for i in np.arange(0, len(l), n):
		yield l[i:i + n]