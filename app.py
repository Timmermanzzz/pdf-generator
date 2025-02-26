from flask import Flask, request, send_file, jsonify
from fpdf import FPDF
from io import BytesIO
from flask_cors import CORS
import os
import base64

app = Flask(__name__)
CORS(app)  # CORS-ondersteuning toevoegen

# Eenvoudige API-sleutel authenticatie
API_KEY = os.environ.get('API_KEY', 'test_key')  # Standaard test_key, verander dit in productie

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

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint voor health checks door Render"""
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port) 