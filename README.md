# PDF Generator API

Een eenvoudige Flask-applicatie die PDF's genereert op basis van tekst.

## Functionaliteit

De applicatie biedt een API-endpoint dat tekst accepteert en een PDF-document retourneert.

### API Endpoint

- **URL**: `/generate_pdf`
- **Methode**: POST
- **Headers**: 
  - `Content-Type: application/json`
  - `X-API-Key: jouw_api_sleutel`
- **Body**: JSON met een `text` veld
- **Respons**: PDF-bestand

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

url = "http://localhost:5000/generate_pdf"
data = {"text": "Dit is een voorbeeld tekst voor mijn PDF."}
headers = {
    "Content-Type": "application/json",
    "X-API-Key": "test_key"  # Gebruik de juiste API-sleutel
}

response = requests.post(url, data=json.dumps(data), headers=headers)

# Sla de PDF op
with open("output.pdf", "wb") as f:
    f.write(response.content)
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

// Verwerk de PDF-respons
const pdfBlob = await response.blob();
``` 