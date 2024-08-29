from mailjet_rest import Client


class OtpSender:
    def __init__(self):
        self.api_key = '614f1d5db217f5a35c8ed583bbf4f09c'
        self.api_secret = '118dec95ed600a827d6400f210f3a524'
        self.sender_email = 'contact@biitechacademy.com'
        self.subject = 'Confirmation of Your Account Creation'

    def send_otp_email(self, recipient_email, recipient_name, otp):
        message = '''<div style="width: 100%; display: flex; height: auto; margin: auto; justify-content: center; align-items: center; background-color: #f0f0f0;">
                        <div style="width: 100%; max-width: 600px; height: 100%; justify-content: center; align-items: center; max-height: 600px; background-color: #000; border-radius: 10px; margin: 10px auto; padding: 20px;">
                          <div style="justify-content: center; align-items: center; margin: auto; padding: 0 15px;">
                            <h2 style="font-size: 1.8em; font-weight: bold; color: #fff; text-align: center;">Enrollment Confirmation</h2>
                            <p style="font-size: 1.2em; font-weight: 500; color: #fff; text-align: center;">Welcome to BIITECH Academy</p>
                          </div>

                          <div style="justify-content: center; align-items: center; margin: auto;">
                            <p style="font-size: 1em; font-weight: 500; color: #fff; text-align: center;">Dear {recipient_name},</p>
                            <p style="font-size: 1em; font-weight: 500; color: #fff; text-align: center;">We are delighted to welcome you to BIITECH Academy. Prepare to embark on a rewarding learning journey with us. A representative will contact you shortly. In the meantime, please enter the OTP below to get started:</p>
                            <p style="font-size: 1em; font-weight: 500; color: #fff; text-align: center; font-family: monospace;">{otp}</p>
                            <a href="https://www.biitechacademy.com/auth/user/account" style="width: max-content; padding: 10px 20px; margin: auto; height: auto; display: flex; justify-content: center; align-items: center; background-color: #fff; color: #000; font-size: 1em; font-weight: 500; border-radius: 10px; text-decoration: none;">Get Started Here</a>
                          </div>
                        </div>
                    </div>'''

        try:
            mailjet = Client(
                auth=(self.api_key, self.api_secret), version='v3.1')

            data = {
                'Messages': [
                    {
                        "From": {
                            "Email": self.sender_email,
                            "Name": "Biitech Academy"
                        },
                        "To": [
                            {
                                "Email": recipient_email,
                                "Name": recipient_name,
                            }
                        ],
                        "Subject": self.subject,
                        "TextPart": "",
                        "HTMLPart": message,
                        "CustomID": "AppGettingStartedTest"
                    }
                ]
            }

            result = mailjet.send.create(data=data)

            # Check if the request was successful (status code 2xx)
            if result.status_code != 200:
                print(
                    f"Failed to send the email. MailJet API response: {result.json()}")
        except Exception as e:
            print(f"Error occurred while sending the automated response: {e}")
