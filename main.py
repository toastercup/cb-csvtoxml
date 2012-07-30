from flask import Flask, views, request, render_template, send_file
import os, csv, codecs
from xml.sax.saxutils import escape
from xml.dom.minidom import Document

#-----------------------------
# App Configuration

class Config:
	ALLOWED_EXTENSIONS = set(['txt', 'csv'])
	SECRET_KEY = 'oQFoCABw458y&%GS'
	DEBUG = False


class DevConfig(Config):
	DEBUG = True

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in Config.ALLOWED_EXTENSIONS

#-----------------------------
# CSV parsing

def parse_csv(csv_file):
	if csv_file and allowed_file(csv_file.filename):
		data = csv.reader(csv_file)
		
		doc = Document()
		dataEle = doc.createElement('data')
		doc.appendChild(dataEle)
		
		rownum = 0
		for row in data:
			if rownum == 0:
				header = row
			else:
				rowEle = doc.createElement('row')
				dataEle.appendChild(rowEle)
				
				colnum = 0
				for col in row:
					tagEle = doc.createElement(escape_csv_text(header[colnum]))
					rowEle.appendChild(tagEle)
					
					tagText = doc.createTextNode(escape_csv_text(col))
					tagEle.appendChild(tagText)
					
					colnum += 1
			rownum += 1
	return doc


def escape_csv_text(data):
	return escape(data.strip().decode('utf-8'))

#-----------------------------
# App

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/csvtoxml/')
def form():
	return render_template('csvtoxml.html')


@app.route('/csvtoxml/', methods=['POST'])
def process_csv():
	csv_file = request.files['formFile']
	parsedXml = parse_csv(csv_file)
	
	fileName = 'output.xml'
	xmlFile=codecs.open(fileName, 'w', 'utf-8')
	parsedXml.writexml(xmlFile)
	xmlFile.close()

	return send_file(fileName, 'text/xml', True, 'output.xml')


@app.route('/')
def index():
	return render_template('index.html')

