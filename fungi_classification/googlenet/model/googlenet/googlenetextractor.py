# import the necessary packages

from sklearn_theano.feature_extraction.caffe.googlenet import GoogLeNetTransformer

class GoogleNetExtractor:
	def __init__(self):
		# store the layer number and initialize the Overfeat transformer
		#self.layerNum = layerNum
		self.of = GoogLeNetTransformer()

	def describe(self, data):
		# apply the Overfeat transfrom to the images
		return self.of.transform(data)

