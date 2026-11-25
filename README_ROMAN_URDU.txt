PRODINNA AI BUSINESS AGENT - STARTER VERSION

YE VERSION KYA KARTA HAI?
1. Laptop par local website chatbot chalata hai.
2. Services, quotation aur contact ke basic sawalat ka jawab deta hai.
3. Inquiry form se leads ko leads.csv mein save karta hai.
4. WhatsApp webhook ka starter endpoint included hai, lekin Meta credentials ke baghair WhatsApp messages receive/send nahi karega.

STEP 1 - PYTHON INSTALL KAREIN
1. https://www.python.org/downloads/ open karein.
2. Python 3.11 ya newer download karein.
3. Installer ke first screen par "Add Python to PATH" ko tick karein.
4. Install Now click karein.

STEP 2 - PROJECT OPEN KAREIN
1. ZIP extract karein.
2. Extracted folder "prodinna_ai_agent" open karein.
3. Folder ke address bar mein cmd type karke Enter press karein.

STEP 3 - COMMANDS CHALAYEIN
Pehle:
py -m venv .venv

Phir:
.venv\Scripts\activate

Phir:
py -m pip install -r requirements.txt

Phir:
py app.py

STEP 4 - BOT TEST KAREIN
Chrome mein ye address open karein:
http://127.0.0.1:5000

Chat mein test karein:
- Salam
- What services do you offer?
- I need a quotation

Lead form fill karein. Project folder mein leads.csv file ban jayegi.

IMPORTANT
Ye pehla working local prototype hai; abhi public internet par live nahi hai.
WhatsApp ke liye Meta WhatsApp Business Platform account, access token, phone number ID, verify token aur public HTTPS webhook chahiye. Tokens kisi ke saath share na karein.
Local AI add karne ke liye next stage mein Ollama install/configure kiya ja sakta hai. 8GB RAM par small model use karein; speed hardware par depend karegi.
