from flask import Flask, request, send_file, jsonify
from fpdf import FPDF
from io import BytesIO
from flask_cors import CORS
import os
import base64
import uuid
import tempfile
from datetime import datetime, timedelta
import shutil

app = Flask(__name__)
CORS(app)  # CORS-ondersteuning toevoegen

# Eenvoudige API-sleutel authenticatie
API_KEY = os.environ.get('API_KEY', 'test_key')  # Standaard test_key, verander dit in productie

# Map om tijdelijke PDF's op te slaan - gebruik een persistente map in plaats van /tmp
TEMP_DIR = os.path.join(os.getcwd(), 'pdf_files')
os.makedirs(TEMP_DIR, exist_ok=True)

# Opslag voor tijdelijke PDF's met verlooptijd
temp_pdfs = {}

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Custom GPT PDF', 0, 1, 'C')
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')

def verify_api_key():
    api_key = request.headers.get('X-API-Key')
    if not api_key or api_key != API_KEY:
        return False
    return True

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    # API-sleutel verificatie
    if not verify_api_key():
        return jsonify({"error": "Ongeldige of ontbrekende API-sleutel"}), 401
        
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Geen tekst meegegeven"}), 400

    text = data['text']
    
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    
    # Correcte manier om BytesIO te gebruiken met FPDF
    pdf_content = pdf.output(dest='S')
    
    # Converteer PDF naar base64
    pdf_base64 = base64.b64encode(pdf_content.encode('latin-1')).decode('utf-8')
    
    # Geef JSON-respons terug met base64-gecodeerde PDF
    return jsonify({
        "success": True,
        "filename": "output.pdf",
        "content_type": "application/pdf",
        "pdf_data": pdf_base64
    })

@app.route('/generate_pdf_url', methods=['POST'])
def generate_pdf_url():
    # API-sleutel verificatie
    if not verify_api_key():
        return jsonify({"error": "Ongeldige of ontbrekende API-sleutel"}), 401
        
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Geen tekst meegegeven"}), 400

    text = data['text']
    
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    
    # Genereer unieke bestandsnaam
    pdf_id = str(uuid.uuid4())
    filename = f"{pdf_id}.pdf"
    filepath = os.path.join(TEMP_DIR, filename)
    
    # Sla PDF op als bestand
    pdf_content = pdf.output(dest='S')
    with open(filepath, 'wb') as f:
        f.write(pdf_content.encode('latin-1'))
    
    # Sla informatie op met verlooptijd (bijv. 1 uur)
    expiry_time = datetime.now() + timedelta(hours=1)
    temp_pdfs[pdf_id] = {
        'filepath': filepath,
        'expires_at': expiry_time
    }
    
    # Genereer downloadbare URL
    base_url = request.host_url.rstrip('/')
    download_url = f"{base_url}/download_pdf/{pdf_id}"
    
    return jsonify({
        "success": True,
        "filename": "output.pdf",
        "download_url": download_url,
        "expires_at": expiry_time.isoformat()
    })

@app.route('/download_pdf/<pdf_id>', methods=['GET'])
def download_pdf(pdf_id):
    # Controleer of PDF bestaat en niet verlopen is
    if pdf_id not in temp_pdfs:
        return jsonify({"error": "PDF niet gevonden"}), 404
        
    if datetime.now() > temp_pdfs[pdf_id]['expires_at']:
        # Verwijder verlopen PDF
        try:
            filepath = temp_pdfs[pdf_id]['filepath']
            if os.path.exists(filepath):
                os.remove(filepath)
            del temp_pdfs[pdf_id]
        except Exception as e:
            print(f"Fout bij het verwijderen van verlopen PDF: {str(e)}")
        return jsonify({"error": "PDF is verlopen"}), 410
    
    filepath = temp_pdfs[pdf_id]['filepath']
    
    # Controleer of het bestand daadwerkelijk bestaat
    if not os.path.exists(filepath):
        print(f"Bestand niet gevonden: {filepath}")
        return jsonify({"error": "PDF-bestand niet gevonden op de server"}), 404
    
    try:
        return send_file(filepath, as_attachment=True, download_name="output.pdf", mimetype="application/pdf")
    except Exception as e:
        print(f"Fout bij het verzenden van het bestand: {str(e)}")
        return jsonify({"error": f"Fout bij het downloaden van de PDF: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint voor health checks door Render"""
    # Ruim verlopen PDF's op
    cleanup_expired_pdfs()
    return jsonify({"status": "healthy"}), 200

def cleanup_expired_pdfs():
    """Verwijder verlopen PDF's"""
    now = datetime.now()
    expired_ids = [pdf_id for pdf_id, info in temp_pdfs.items() if now > info['expires_at']]
    
    for pdf_id in expired_ids:
        try:
            filepath = temp_pdfs[pdf_id]['filepath']
            if os.path.exists(filepath):
                os.remove(filepath)
            del temp_pdfs[pdf_id]
        except Exception as e:
            print(f"Fout bij het verwijderen van verlopen PDF {pdf_id}: {str(e)}")

# Bij het afsluiten van de applicatie, verwijder alle tijdelijke bestanden
@app.teardown_appcontext
def cleanup_temp_files(exception):
    try:
        # Verwijder alle bestanden in de tijdelijke map, maar behoud de map zelf
        for filename in os.listdir(TEMP_DIR):
            file_path = os.path.join(TEMP_DIR, filename)
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Fout bij het verwijderen van {file_path}: {str(e)}")
    except Exception as e:
        print(f"Fout bij cleanup: {str(e)}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port) 