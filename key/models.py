from django.db import models
from django.conf import settings
import os
import json
import hmac
import hashlib
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Europe/Minsk")
CONFIG_DIR = os.path.join(settings.BASE_DIR, 'code_generator', 'config')
CONFIG_PATH = os.path.join(CONFIG_DIR, "secret.json")
APPEND = "OLEG"  # Secret key
INTERVAL = 30  # Update interval in seconds
SIZE_KODE = 6  # Code length

class CodeGenerator:
    def __init__(self):
        self.last_secret = ""
        self.last_code = "—"
        self.time_left = INTERVAL
        os.makedirs(CONFIG_DIR, exist_ok=True)
        self.load_config()

    def load_config(self):
        try:
            if os.path.exists(CONFIG_PATH):
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.last_secret = data.get("secret", "")
        except (FileNotFoundError, json.JSONDecodeError, PermissionError) as e:
            print(f"Error loading config: {e}")

    def save_config(self):
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump({
                    "secret": self.last_secret,
                }, f, ensure_ascii=False, indent=2)
        except (IOError, PermissionError) as e:
            print(f"Error saving config: {e}")

    def update_code(self, secret=None):
        if secret is not None and secret != self.last_secret:
            self.last_secret = secret
            self.save_config()

        now = datetime.now(TZ)
        t_sec = int(now.astimezone(timezone.utc).timestamp())
        self.time_left = INTERVAL - (t_sec % INTERVAL)
        self.last_code = self.generate_code(self.last_secret)
        return self.last_code

    def generate_code(self, secret, digits=SIZE_KODE):
        if not secret:
            return "0" * digits

        now = datetime.now(TZ)
        slot = int(now.astimezone(timezone.utc).timestamp()) // INTERVAL
        msg = f"{secret}:{APPEND}:{slot}".encode()
        hm = hmac.new(secret.encode(), msg, hashlib.sha256).digest()
        return f"{int.from_bytes(hm[:4], 'big') % (10 ** digits):0{digits}d}"

    def verify_code(self, code_to_verify):
        current_code = self.update_code()
        return code_to_verify == current_code