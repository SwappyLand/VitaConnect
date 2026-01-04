import os
from azure.communication.email import EmailClient

def send_confirmation_email(patient_email, patient_name, doctor_name, date, time):
    try:
        # Load connection string from environment variable for security
        connection_string = "endpoint=https://vitaconnect-comm-resource.india.communication.azure.com/;accesskey=3F9EFca1Oft3QupDKmg4bFMhHWfAOPGSoA1AkSZkjjTD7WQTwElvJQQJ99CAACULyCpYdi65AAAAAZCS54tY" 
        
        # Initialize the Client
        client = EmailClient.from_connection_string(connection_string)

        # Your "From" address must match the domain in Azure
        # Example: "DoNotReply@812308-123-123.azurecomm.net"
        sender_address = "DoNotReply@327923ad-f17d-4558-91da-071888cb4d92.azurecomm.net"

        message = {
            "senderAddress": sender_address,
            "recipients":  {
                "to": [{"address": patient_email}]
            },
            "content": {
                "subject": "Appointment Confirmed - VitaConnect",
                "plainText": f"Hello {patient_name}, your appointment with Dr. {doctor_name} is confirmed for {date} at {time}.",
                "html": f"""
                <html>
                    <body style="font-family: Arial, sans-serif; color: #333;">
                        <h2 style="color: #0078D4;">VitaConnect</h2>
                        <p>Hello <strong>{patient_name}</strong>,</p>
                        <p>Your appointment has been successfully booked.</p>
                        <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px;">
                            <p><strong>Doctor:</strong> Dr. {doctor_name}</p>
                            <p><strong>Date:</strong> {date}</p>
                            <p><strong>Time:</strong> {time}</p>
                        </div>
                        <p style="margin-top: 20px;">Please arrive 10 minutes early with your ID.</p>
                    </body>
                </html>
                """
            }
        }

        # Send the email
        poller = client.begin_send(message)
        result = poller.result()
        
        print(f"Email sent successfully! Message ID: {result['id']}")
        return True

    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

# --- TEST BLOCK ---
if __name__ == "__main__":
    # Replace this with your actual email to test
    send_confirmation_email(
        patient_email="swapniledake27@gmail.com", 
        patient_name="Swapnil Edake", 
        doctor_name="Aradhya Modak", 
        date="2026-01-10", 
        time="10:00 AM"
    )