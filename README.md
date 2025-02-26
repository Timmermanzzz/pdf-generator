# PDF Generator API

Een eenvoudige Flask-applicatie die PDF's genereert op basis van tekst.

## Functionaliteit

De applicatie biedt een API-endpoint dat tekst accepteert en een JSON-respons retourneert met een base64-gecodeerde PDF.

### API Endpoint

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

### Health Check Endpoint

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

### Voorbeeld API-aanroep in Custom GPT

```javascript
// Voorbeeld van een API-aanroep in een Custom GPT
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