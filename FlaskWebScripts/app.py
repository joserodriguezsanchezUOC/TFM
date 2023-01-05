from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a0201893b879e3cff472febaf92f6260a98a1357200f225d'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/predict', methods=["POST"])
def predict():
	text = request.form.get("tituloOferta")
	threshold = float(request.form.get("threshold"))
	
	"""
	import pandas as pd
	import torch
	import numpy as np
	
	model_ckpt= "PlanTL-GOB-ES/roberta-base-bne"

	# Vectorización
	from transformers import AutoTokenizer

	# para multi etiquetas, se tiene que especificar el tipo de clasificación
	tokenizer = AutoTokenizer.from_pretrained(model_ckpt, problem_type="multi_label_classification")
	
	from transformers import AutoModelForSequenceClassification
	model = AutoModelForSequenceClassification.from_pretrained("/home/iberanuncios/TFM/modelos/checkpointProduccion")

	encoding = tokenizer(text, return_tensors="pt")
	encoding = {k: v.to(model.device) for k,v in encoding.items()}

	outputs = model(**encoding)
	
	logits = outputs.logits

	df = pd.read_csv('/home/iberanuncios/TFM/ofertasNov2022_preClean.csv')
	
	

	from gensim.utils import deaccent
	# Keywords a minúsculas y en un array
	rows = []
	for i, row in df.iterrows():
	  # we sort the array
	  labels = sorted([deaccent(item.strip().lower()) for item in row['label'].split(",")])
	  rows.append({"text":row["text"],"labels": labels, "labels_str": ",".join(labels)})

	df = pd.DataFrame(rows)
	
	domain_labels = set()
	for row in df.itertuples():
	  domain_labels.update(row.labels) # Los sets NO permiten elementos duplicados
	domain_labels = sorted(list(domain_labels))
	
	sigmoid = torch.nn.Sigmoid()
	probs = sigmoid(logits.squeeze().cpu())
	predictions = np.zeros(probs.shape)
	predictions[np.where(probs >= threshold)] = 1 # ajustar theshold
	# turn predicted id's into actual label names
	predicted_labels=[]
	for idx, label in enumerate(predictions):
		if label == 1:
			for idx2, label2 in enumerate(domain_labels):
				if idx == idx2:
					predicted_labels.append(domain_labels[idx2])
					#print(domain_labels[idx2])
	
	return render_template('predict.html', prediction = predicted_labels, tituloOferta = text)
	"""
	return render_template('predict.html', prediction = "etiquetas", tituloOferta = text)



@app.route('/predictFromTitle', methods=["POST"])
def predictFromTitle():
	tituloOferta = request.form.get("tituloOferta")
	
	import torch
	# Para ejecutar en CPU no CUDA
	device = torch.device('cpu')
	# Por defecto se aplica el modelo con Threshold= 0,5 (26824)
	trainer = torch.load('/home/iberanuncios/TFM/modelos/checkpoint-26824/pytorch_model.bin',map_location=torch.device('cpu'))

	# Probando el modelo
	from transformers import pipeline
	# Por defecto se aplica el modelo con Threshold= 0,5 (26824)
	classifier = pipeline("text-classification",model='/home/iberanuncios/TFM/modelos/checkpoint-26824')
	prediction = classifier(tituloOferta, )
	
	f1 = ""
	
	for i in prediction:
		f1 += str(i) +" "
	
	return f1
	#render_template('predict.html', prediction = prediction)
	
