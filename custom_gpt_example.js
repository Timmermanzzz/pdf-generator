// Voorbeeld van hoe een Custom GPT de PDF-generator API kan gebruiken
// Dit is een voorbeeld van code die je kunt gebruiken in je Custom GPT

// Functie om een PDF te genereren met de API (base64-methode)
async function generatePDFWithBase64(text) {
  try {
    const response = await fetch('https://pdf-generator-hril.onrender.com/generate_pdf', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': 'jouw_api_sleutel' // Vervang dit door je echte API-sleutel
      },
      body: JSON.stringify({ text: text })
    });

    // Verwerk de JSON-respons
    const data = await response.json();
    
    if (data.success) {
      // De PDF is beschikbaar als base64-gecodeerde string in data.pdf_data
      return {
        success: true,
        message: "PDF succesvol gegenereerd!",
        filename: data.filename,
        pdfData: data.pdf_data
      };
    } else {
      return {
        success: false,
        message: "Er is een fout opgetreden bij het genereren van de PDF."
      };
    }
  } catch (error) {
    return {
      success: false,
      message: `Er is een fout opgetreden: ${error.message}`
    };
  }
}

// Functie om een PDF te genereren met de API (downloadlink-methode)
async function generatePDFWithDownloadLink(text) {
  try {
    const response = await fetch('https://pdf-generator-hril.onrender.com/generate_pdf_url', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': 'jouw_api_sleutel' // Vervang dit door je echte API-sleutel
      },
      body: JSON.stringify({ text: text })
    });

    // Verwerk de JSON-respons
    const data = await response.json();
    
    if (data.success) {
      // De downloadlink is beschikbaar in data.download_url
      return {
        success: true,
        message: "PDF succesvol gegenereerd!",
        filename: data.filename,
        downloadUrl: data.download_url,
        expiresAt: data.expires_at
      };
    } else {
      return {
        success: false,
        message: "Er is een fout opgetreden bij het genereren van de PDF."
      };
    }
  } catch (error) {
    return {
      success: false,
      message: `Er is een fout opgetreden: ${error.message}`
    };
  }
}

// Voorbeeld van hoe je de functie kunt gebruiken in je Custom GPT
async function handlePDFRequest(userText) {
  // Genereer de PDF met downloadlink
  const result = await generatePDFWithDownloadLink(userText);
  
  if (result.success) {
    // Hier kun je de gebruiker informeren dat de PDF is gegenereerd
    // en een downloadlink aanbieden
    
    // Formatteer de vervaldatum
    const expiryDate = new Date(result.expiresAt);
    const formattedExpiryDate = expiryDate.toLocaleString();
    
    // Voorbeeld van een bericht aan de gebruiker:
    return `
      De PDF-generatie is gelukt! ✅
      
      Je kunt de gegenereerde PDF downloaden via deze link:
      [Download PDF](${result.downloadUrl})
      
      Let op: Deze link verloopt op ${formattedExpiryDate}.
    `;
  } else {
    // Informeer de gebruiker over de fout
    return `Er is een probleem opgetreden bij het genereren van de PDF: ${result.message}`;
  }
}

// Voorbeeld van hoe je dit kunt integreren in je Custom GPT
// Dit is een voorbeeld en moet worden aangepast aan je specifieke implementatie
async function onUserMessage(userMessage) {
  if (userMessage.includes("genereer een pdf") || userMessage.includes("maak een pdf")) {
    // Haal de tekst op die in de PDF moet worden opgenomen
    const textForPDF = userMessage.replace(/genereer een pdf|maak een pdf/gi, "").trim();
    
    // Genereer de PDF en geef een antwoord aan de gebruiker
    const response = await handlePDFRequest(textForPDF);
    return response;
  }
  
  // Verwerk andere berichten zoals gewoonlijk
  return "Ik kan een PDF voor je genereren. Vraag me gewoon om 'een pdf te genereren met [je tekst]'.";
} 