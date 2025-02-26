# PDF Generator API

Een eenvoudige Flask-applicatie die PDF's genereert op basis van tekst.

## Functionaliteit

De applicatie biedt een API-endpoint dat tekst accepteert en een PDF-document retourneert.

### API Endpoint

- **URL**: `/generate_pdf`
- **Methode**: POST
- **Body**: JSON met een `text` veld
- **Respons**: PDF-bestand

## Lokaal gebruik

1. Installeer de vereiste packages:
   ```
   pip install -r requirements.txt
   ```

2. Start de applicatie:
   ```
   python pdf.py
   ```

3. De server draait nu op `http://localhost:5000`

## Voorbeeld gebruik

```python
import requests
import json

url = "http://localhost:5000/generate_pdf"
data = {"text": "Dit is een voorbeeld tekst voor mijn PDF."}
headers = {"Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(data), headers=headers)

# Sla de PDF op
with open("output.pdf", "wb") as f:
    f.write(response.content)
```

## Deployment op Render

Deze applicatie is geconfigureerd voor eenvoudige deployment op Render. 