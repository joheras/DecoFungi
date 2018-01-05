from django import forms
from PIL import Image

class Formulario(forms.Form):
	image=forms.ImageField()


class Formulario2(forms.Form):
	image=forms.ImageField()
	control_image = forms.ImageField()

class FormularioZip(forms.Form):
	zip_file=forms.FileField()