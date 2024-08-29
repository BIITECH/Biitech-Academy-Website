from mailjet_rest import Client

class AdminUpdate:
    def __init__(self):
        self.api_key = '614f1d5db217f5a35c8ed583bbf4f09c'
        self.api_secret = '118dec95ed600a827d6400f210f3a524'
        self.sender_email = 'contact@biitechacademy.com'
        self.subject = 'New User Sign Up'

    def send_admin_mail(self, recipient_email, recipient_name):
        message = '''<div style="width: 100%; display: flex; height: auto; margin: auto; justify-content: center; align-items: center; background-color: #f0f0f0;">
                        <div style="width: 100%; max-width: 600px; justify-content: center; align-items: center; height: 100%; max-height: 600px; background: #000; border-radius: 10px; margin: 10px; padding: 20px;">
                          <div style="text-align: center; margin-bottom: 20px;">
                            <h2 style="font-size: 1.8em; font-weight: bold; color: #fff;">New User Enrollment Success</h2>
                            <p style="font-size: 1.2em; font-weight: 500; color: #fff;">Notification from BIITECH ACADEMY</p>
                          </div>
                          
                          <div style="text-align: center;">
                            <p style="font-size: 1em; font-weight: 500; color: #fff;">Dear Admin,<br />We are pleased to inform you that a new user has successfully enrolled in BIITECH ACADEMY.</p>
                          </div>
                        </div>
                      </div>'''
        try:
            mailjet = Client(auth=(self.api_key, self.api_secret), version='v3.1')

            data = {
                'Messages': [
                    {
                        "From": {
                            "Email": self.sender_email,
                            "Name": "BIITECH ACADEMY"
                        },
                        "To": [
                            {
                                "Email": '',
                                "Name": 'C.E.O BIITECH ACADEMY',
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
                print(f"Failed to send the email. MailJet API response: {result.json()}")
        except Exception as e:
            print(f"Error occurred while sending the automated response: {e}")
