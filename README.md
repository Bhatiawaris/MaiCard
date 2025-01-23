# LeftoverMaster
"Hey, want to add me on Instagram?"
"Sorry, I don’t trust the Zucc. How about X?"
"Nah, I don’t do X after the incident. What about Viber?"
"What's a Viber? What about Myspace?"
"That’s funny. No. What about Bluesky?"
"Nah, I don’t even know what that is. BeReal?"
"Missed the notification. LinkedIn?"
"Seriously? Snapchat?"
"Deleted that in 2016. WhatsApp?"
"Too much drama."

As avid **NETWORKERS**, we have all scrambled to get our phones out trying to get everybody on the networking social to type in their LinkedIn/Instagram/WhatsApp etc. WHAT IF there was a near-instant way to receive all the socials of every new person you meet?
Introducing **MaiCard**, a minimal and easily accessible web application to supercharge your networking prowess. Curate your own social business cards with your personal links and embed them in QR codes. Save others' profiles with a single scan. Find your most compatible peers with our ML-powered compatibility scores.

## Stack and Implementation
Maicard was built with a *FastApi* web API handling *Postgres* CRUD operations, text embeddings, and compatibility score generation with *Hugging Face*. The UI was developed in *React* to provide users with an intuitive and responsive interface (desktop/mobile). The QR code reader was integrated using the *html5-qrcode* package

## Usage
```docker compose up --build``` to start all services to run the application locally.

## What's Next
Implement login, redirection link within QR codes, UUID for profiles.
