import cv2
from twilio.rest import Client

# Twilio credentials
account_sid = 'ACdeb2fa9721a38a209a43b72f70f76757'
auth_token = 'e5cb734e90b3768fccf00e943c3b83d2'
twilio_number = '+1 571 701 1946'  # Your Twilio number
receiver_number = '+91 9500936522'  # Your personal phone number

# Initialize Twilio client
client = Client(account_sid, auth_token)

# Initialize camera
cap = cv2.VideoCapture(0)

# Load Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

sent = False  # To avoid multiple SMS for one detection

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # If face is detected
    if len(faces) > 0 and not sent:
        print("Face detected!")

        # Send SMS
        message = client.messages.create(
            body="Alert: A person has been detected by your security surveillance drone.",
            from_=twilio_number,
            to=receiver_number
        )

        print(f"SMS sent. SID: {message.sid}")
        sent = True

    # Draw rectangles around faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow('Drone Camera', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
