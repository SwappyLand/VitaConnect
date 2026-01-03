/**
 * VitaConnect Medical License Scanner
 * -----------------------------------
 * Scans a doctor's license image using Azure AI Document Intelligence.
 * Extracts: License Number & Expiry Date.
 * returns: { success: boolean, data: object, message: string }
 */

// 1. CONFIGURATION (Replace with your actual keys from Azure Portal)
const CONFIG = {
  endpoint: "YOUR_OCR_ENDPOINT", // e.g., https://vitaconnect-ocr.cognitiveservices.azure.com/
  apiKey: "YOUR_OCR_KEY",        // Found in "Keys and Endpoint" blade
  modelId: "med-license-v1",     // The EXACT name you gave your model during training
  apiVersion: "2023-07-31"       // Stable version for Custom Models
};

export async function verifyLicense(fileObject) {
  try {
    console.log("🔵 Starting License Scan...");

    // ---------------------------------------------------------
    // STEP 1: SUBMIT THE FILE TO AZURE
    // ---------------------------------------------------------
    const analyzeUrl = `${CONFIG.endpoint}/documentintelligence/documentModels/${CONFIG.modelId}:analyze?api-version=${CONFIG.apiVersion}`;

    const submitResponse = await fetch(analyzeUrl, {
      method: "POST",
      headers: {
        "Ocp-Apim-Subscription-Key": CONFIG.apiKey,
        "Content-Type": fileObject.type, // e.g., "image/jpeg" or "application/pdf"
      },
      body: fileObject, // The raw file from the input
    });

    if (!submitResponse.ok) {
      const errorText = await submitResponse.text();
      throw new Error(`Submission Failed: ${errorText}`);
    }

    // Azure doesn't give the answer immediately. It gives us a "Receipt URL" to check later.
    const operationUrl = submitResponse.headers.get("Operation-Location");
    if (!operationUrl) throw new Error("No operation URL returned from Azure.");

    // ---------------------------------------------------------
    // STEP 2: POLL FOR RESULTS (Wait for AI to finish)
    // ---------------------------------------------------------
    let result = null;
    let status = "running";

    console.log("⏳ AI is reading the document...");

    while (status === "running" || status === "notStarted") {
      // Wait 1 second before asking again
      await new Promise((resolve) => setTimeout(resolve, 1000));

      const statusResponse = await fetch(operationUrl, {
        headers: { "Ocp-Apim-Subscription-Key": CONFIG.apiKey },
      });

      if (!statusResponse.ok) throw new Error("Status check failed");

      result = await statusResponse.json();
      status = result.status;
      
      // Safety break: If it takes longer than 30 seconds, stop.
      // (You can add a counter here if you want to be strict)
    }

    if (status === "failed") {
      throw new Error("AI analysis failed to process the document.");
    }

    console.log("✅ AI Analysis Complete!");

    // ---------------------------------------------------------
    // STEP 3: EXTRACT YOUR CUSTOM DATA
    // ---------------------------------------------------------
    // "documents[0]" is the first page of the uploaded file
    const fields = result.analyzeResult?.documents?.[0]?.fields;

    if (!fields) {
      return { success: false, message: "No text found on this document." };
    }

    // Get the values based on the TAGS you created in the Studio
    // Note: We use optional chaining (?.) just in case the AI missed a field
    const licenseNumber = fields.LicenseNumber?.content || null;
    const expiryDateString = fields.ExpiryDate?.valueDate || fields.ExpiryDate?.content || null;

    console.log(`🔍 Found - License: ${licenseNumber}, Expiry: ${expiryDateString}`);

    // ---------------------------------------------------------
    // STEP 4: LOGIC CHECK (Is it expired?)
    // ---------------------------------------------------------
    
    if (!licenseNumber) {
      return { success: false, message: "Could not read License Number. Please upload a clearer image." };
    }

    if (!expiryDateString) {
      // NOTE: Some older licenses don't have expiry dates. You can decide to allow this or not.
      return { success: false, message: "Could not find Expiry Date on this license." };
    }

    // Check Date Validity
    const expiryDate = new Date(expiryDateString);
    const today = new Date();
    
    // Reset time to midnight for fair comparison
    today.setHours(0, 0, 0, 0);

    if (expiryDate < today) {
      return { 
        success: false, 
        message: `License expired on ${expiryDate.toDateString()}. Verification Failed.` 
      };
    }

    // SUCCESS!
    return {
      success: true,
      message: "Verification Successful",
      data: {
        licenseNumber: licenseNumber,
        expiryDate: expiryDateString,
        isVerified: true
      }
    };

  } catch (error) {
    console.error("❌ Error in verifyLicense:", error);
    return { success: false, message: error.message };
  }
}