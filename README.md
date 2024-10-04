# WeWomen
 
This project is an Emergency SMS application built using Kivy and Firebase. It allows users to send predefined emergency messages to a list of contacts stored in Firebase.

## Features

- User authentication with Firebase
- Store and manage contacts in Firebase
- Send predefined emergency SMS to selected contacts
- User-friendly interface with Kivy
- Dynamic background and responsive layout

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x
- Kivy library
- Firebase Admin SDK
- python-dotenv library (for environment variable management)
- Access to a Twilio account (or another SMS service) to send messages

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/emergency-sms-app.git
   cd emergency-sms-app
   ```

2. **Install required libraries:**

   Use pip to install the necessary dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Firebase:**

   - Create a Firebase project and set up the Firebase Admin SDK.
   - Download the `firebase-cred.json` file and place it in the project root.

4. **Create a `.env` file:**

   In the project root, create a `.env` file and add your Firebase and Twilio credentials:

   ```env
   FIREBASE_API_KEY=your_firebase_api_key
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   TWILIO_PHONE_NUMBER=your_twilio_phone_number
   ```

## Usage

1. **Run the application:**

   To start the application, use the following command:

   ```bash
   python main.py
   ```

2. **Add Contacts:**

   Navigate to the Add Contact screen to input the names and phone numbers of your emergency contacts. 

3. **Send SMS:**

   - Select the contacts to whom you want to send an emergency message.
   - Press the "Send" button to dispatch the predefined message.

## Code Structure

```
/emergency-sms-app
│
├── main.py                # Main application file
├── firebase-cred.json     # Firebase credentials
├── .env                   # Environment variables
├── requirements.txt       # Python dependencies
└── Screens                # Directory containing Kivy screen classes
    ├── AddContactScreen.py # Screen for adding contacts
    └── EmergencyButton.py  # Emergency button functionality
```

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Kivy Documentation](https://kivy.org/doc/stable/)
- [Firebase Documentation](https://firebase.google.com/docs)
- [Twilio API Documentation](https://www.twilio.com/docs/usage/api)
