from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a0201893b879e3cff472febaf92f6260a98a1357200f225d'

app = Flask(__name__)


# FUNCIÓN PRINCIPAL DE PREDICCIÓN
def predictFunction(text, modelo, threshold):
	# CARGA ETIQUETAS DE CONJUNTO DE DATOS
	import pandas as pd
	import csv
	domain_labels = pd.read_csv('/home/iberanuncios/TFM/etiquetas/domainLabels_Nov2022.csv').values.tolist()
	domain_labels = [i for row in domain_labels for i in row] # Flat
	domain_labels = sorted(list(domain_labels))

	import torch
	import numpy as np
	
	model_ckpt= "PlanTL-GOB-ES/roberta-base-bne"

	# Vectorización
	from transformers import AutoTokenizer

	# Se especifica el tipo de clasificación multietiqueta
	tokenizer = AutoTokenizer.from_pretrained(model_ckpt, problem_type="multi_label_classification")
	
	# Se utiliza el modelo seleccionado
	from transformers import AutoModelForSequenceClassification
	model = AutoModelForSequenceClassification.from_pretrained(modelo) # modelo elegible en formulario
	
	# Predicción
	encoding = tokenizer(text, return_tensors="pt")
	encoding = {k: v.to(model.device) for k,v in encoding.items()}
	outputs = model(**encoding)	
	logits = outputs.logits
	
	sigmoid = torch.nn.Sigmoid()
	probs = sigmoid(logits.squeeze().cpu())
	predictions = np.zeros(probs.shape)
	predictions[np.where(probs >= threshold)] = 1 # theshold ajustable en formulario
	
	# Convierte id en nombre de etiqueta
	# Cambiada sintaxis de bucle por compatibilidad con Flask
	predicted_labels=[]
	for idx, label in enumerate(predictions):
		if label == 1:
			for idx2, label2 in enumerate(domain_labels):
				if idx == idx2:
					predicted_labels.append(domain_labels[idx2])
	
	# SALIDA JSON PARA INTEGRACIÓN CON OTROS SERVICIOS
	import json
	json_str = json.dumps(predicted_labels)

	return json_str


@app.route('/')
def index():
    return render_template('index.html')

# PRECCIONES VÍA FORMULARIO WEB
@app.route('/predict', methods=["POST"])
def predict():
	text = request.form.get("tituloOferta")
	modelo = request.form.get("modelo")
	
	if not modelo:
		modelo="/home/iberanuncios/TFM/modelos/checkpointNov2022"
	
	threshold = request.form.get("threshold")
	if not threshold:
		threshold=0.5
	else:
		threshold = float(threshold)
		
	return render_template('predict.html', prediction = predictFunction(text, modelo, threshold), tituloOferta = text)
	

# PRECCIONES ORIENTADAS A WEB SERVICE (API)
@app.route('/predictService', methods=["POST"])
def predictService():
	text = request.form.get("tituloOferta")
	modelo = request.form.get("modelo")
	
	if not modelo:
		modelo="/home/iberanuncios/TFM/modelos/checkpointNov2022"
	
	threshold = request.form.get("threshold")
	if not threshold:
		threshold=0.5
	else:
		threshold = float(threshold)
		
	return predictFunction(text, modelo, threshold)
