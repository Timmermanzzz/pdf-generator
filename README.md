# PDF Generator API

Een eenvoudige Flask-applicatie die PDF's genereert op basis van tekst.

## Functionaliteit

De applicatie biedt twee API-endpoints voor het genereren van PDF's:

1. Een endpoint dat een base64-gecodeerde PDF retourneert in een JSON-respons
2. Een endpoint dat een tijdelijke downloadlink genereert voor de PDF

### API Endpoints

#### 1. PDF met Base64-encoding

- **URL**: `/generate_pdf`
- **Methode**: POST
- **Headers**: 
  - `Content-Type: application/json`
  - `X-API-Key: jouw_api_sleutel`
- **Body**: JSON met een `text` veld
- **Respons**: JSON met de volgende velden:
  - `success`: Boolean die aangeeft of de PDF-generatie succesvol was
  - `filename`: De naam van het gegenereerde PDF-bestand
  - `content_type`: Het MIME-type van het bestand (application/pdf)
  - `pdf_data`: De base64-gecodeerde inhoud van het PDF-bestand

#### 2. PDF met Downloadlink

- **URL**: `/generate_pdf_url`
- **Methode**: POST
- **Headers**: 
  - `Content-Type: application/json`
  - `X-API-Key: jouw_api_sleutel`
- **Body**: JSON met een `text` veld
- **Respons**: JSON met de volgende velden:
  - `success`: Boolean die aangeeft of de PDF-generatie succesvol was
  - `filename`: De naam van het gegenereerde PDF-bestand
  - `download_url`: De URL om de PDF te downloaden
  - `expires_at`: De datum en tijd waarop de downloadlink verloopt

#### 3. PDF Downloaden

- **URL**: `/download_pdf/{pdf_id}`
- **Methode**: GET
- **Respons**: PDF-bestand

#### 4. Health Check

- **URL**: `/health`
- **Methode**: GET
- **Respons**: JSON met status informatie

## Lokaal gebruik

1. Installeer de vereiste packages:
   ```
   pip install -r requirements.txt
   ```

2. Start de applicatie:
   ```
   python app.py
   ```

3. De server draait nu op `http://localhost:5000`

## Voorbeeld gebruik

### Voorbeeld 1: PDF met Base64-encoding

```python
import requests
import json
import base64

url = "http://localhost:5000/generate_pdf"
data = {"text": "Dit is een voorbeeld tekst voor mijn PDF."}
headers = {
    "Content-Type": "application/json",
    "X-API-Key": "test_key"  # Gebruik de juiste API-sleutel
}

response = requests.post(url, data=json.dumps(data), headers=headers)
response_data = response.json()

if response_data["success"]:
    # Decodeer de base64-gecodeerde PDF
    pdf_data = base64.b64decode(response_data["pdf_data"])
    
    # Sla de PDF op
    with open("output.pdf", "wb") as f:
        f.write(pdf_data)
    print(f"PDF opgeslagen als {response_data['filename']}")
else:
    print("Fout bij het genereren van de PDF")
```

### Voorbeeld 2: PDF met Downloadlink

```python
import requests
import json
import webbrowser

url = "http://localhost:5000/generate_pdf_url"
data = {"text": "Dit is een voorbeeld tekst voor mijn PDF."}
headers = {
    "Content-Type": "application/json",
    "X-API-Key": "test_key"  # Gebruik de juiste API-sleutel
}

response = requests.post(url, data=json.dumps(data), headers=headers)
response_data = response.json()

if response_data["success"]:
    print(f"PDF gegenereerd! Download URL: {response_data['download_url']}")
    print(f"Deze link verloopt op: {response_data['expires_at']}")
    
    # Open de download URL in de browser
    webbrowser.open(response_data['download_url'])
else:
    print("Fout bij het genereren van de PDF")
```

## Deployment op Render

Deze applicatie is geconfigureerd voor eenvoudige deployment op Render:

1. Maak een nieuw Web Service aan op Render
2. Verbind je GitHub repository
3. Render zal automatisch de `render.yaml` configuratie gebruiken
4. De API-sleutel wordt automatisch gegenereerd door Render

## Gebruik met Custom GPT

Om deze API te gebruiken met een Custom GPT:

1. Zorg ervoor dat je de juiste API-sleutel gebruikt in je Custom GPT configuratie
2. Gebruik de volledige URL van je Render deployment in je API-aanroepen
3. De CORS-ondersteuning is al ingebouwd, dus je kunt de API direct aanroepen vanuit je Custom GPT

### Voorbeeld API-aanroep in Custom GPT (Base64-methode)

```javascript
// Voorbeeld van een API-aanroep in een Custom GPT met base64-encoding
const response = await fetch('https://jouw-render-url.onrender.com/generate_pdf', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': 'jouw_api_sleutel'
  },
  body: JSON.stringify({ text: 'Tekst voor in de PDF' })
});

// Verwerk de JSON-respons
const data = await response.json();
if (data.success) {
  // De PDF is beschikbaar als base64-gecodeerde string in data.pdf_data
  // Je kunt deze tonen aan de gebruiker of een downloadlink aanbieden
  console.log(`PDF gegenereerd: ${data.filename}`);
}
```

### Voorbeeld API-aanroep in Custom GPT (Downloadlink-methode)

```javascript
// Voorbeeld van een API-aanroep in een Custom GPT met downloadlink
const response = await fetch('https://jouw-render-url.onrender.com/generate_pdf_url', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': 'jouw_api_sleutel'
  },
  body: JSON.stringify({ text: 'Tekst voor in de PDF' })
});

// Verwerk de JSON-respons
const data = await response.json();
if (data.success) {
  // De downloadlink is beschikbaar in data.download_url
  console.log(`PDF gegenereerd! Download URL: ${data.download_url}`);
  console.log(`Deze link verloopt op: ${data.expires_at}`);
}
``` 