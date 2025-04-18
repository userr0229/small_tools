# This program needs to be in the same directory as data.json
#
# File structure should be:
# 
# └── your_folder/
#     ├── ip_notifier.py
#     └── data.json
#
# In data.json, you need to have the following content:
# {
#     "token": "your_discord_bot_token",
#     "channel_id": "your_discord_channel_id"
# }

import discord
import requests
import os
import time
from pywifi import PyWiFi, const
import sys
import json


# Path to JSON file
FILE_NAME = "data.json"
CURRENT_FOLDER = os.path.dirname(__file__)
json_file = os.path.join(CURRENT_FOLDER, FILE_NAME)

def handle_json(operation='read', token=None, channel_id=None, new_ip=None):
    """
    Handle all JSON file operations
    operation: 'read' - read JSON, 'write' - write token and channel_id, 'update_ip' - update IP
    """
    try:
        if operation == 'read':
            with open(json_file, 'r') as file:
                return json.load(file)
        elif operation == 'write':
            data = {'token': token, 'channel_id': channel_id}
            with open(json_file, 'w') as file:
                json.dump(data, file, indent=4)
            print("Data written to JSON file.")
        elif operation == 'update_ip':
            data = handle_json('read')
            if data is None:
                data = {}
            if new_ip is not None:
                data['ip'] = new_ip
            with open(json_file, 'w') as file:
                json.dump(data, file, indent=4)
            print("JSON file updated.")
    except FileNotFoundError:
        print("JSON file not found.")
        return None

data = handle_json('read')

# Discord Bot Token and Channel ID (replace with your Token and Channel ID)
TOKEN = data['token']  # Read Token from JSON file
CHANNEL_ID = data['channel_id']  # Read Channel ID from JSON file

# Initialize Discord Client
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# Get external IP
def get_external_ip():
    try:
        return requests.get("https://api.ipify.org").text.strip()
    except requests.RequestException:
        return None

# Save new IP
def save_current_ip(ip):
    handle_json('update_ip', new_ip=ip)  # Update IP in JSON file

# Check IP and notify on startup
async def check_ip_and_notify():
    try:
        previous_ip = data.get('ip')  # Use get() method, returns None if ip doesn't exist
        current_ip = get_external_ip()

        if current_ip and current_ip != previous_ip:
            save_current_ip(current_ip)
            channel = client.get_channel(CHANNEL_ID)
            if channel:
                await channel.send(f"⚠️ IP change detected on startup:")
                await channel.send(f"{current_ip}")
            print(f"IP address changed: {current_ip}")
        else:
            print("IP has not changed")
    except Exception as e:
        print(f"Error checking IP: {str(e)}")
        if current_ip:  # If we can at least get the current IP, save it
            save_current_ip(current_ip)

@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')
    await check_ip_and_notify()
    await client.close()  # Close Bot after execution

def get_connected_wifi():
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]  # Get first wireless interface

    if iface.status() == const.IFACE_CONNECTED:
        profile = iface.network_profiles()
        if profile:
            return profile[0].ssid
    return None

# Start Bot
def on_wifi_connected(ssid):
    print(f"Connected to WiFi: {ssid}")
    # Define actions to execute here
    # if ssid == "dlink-897B":  # Replace with target WiFi name
    client.run(TOKEN)
    time.sleep(1)
    print("Specific actions completed, program will exit.")
    sys.exit(0)

def monitor_wifi():
    last_ssid = None
    while True:
        current_ssid = get_connected_wifi()
        if current_ssid != last_ssid:
            if current_ssid:
                on_wifi_connected(current_ssid)
            else:
                print("WiFi connection lost")
            last_ssid = current_ssid
        time.sleep(2)  # Check WiFi status every 2 seconds

if __name__ == "__main__":
    print("Starting WiFi connection monitoring...")
    monitor_wifi()
