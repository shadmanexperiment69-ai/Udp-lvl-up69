# ==================== STANDARD IMPORTS ====================
import sys
import asyncio
import httpx
import random
import json
import socket
import struct
import time
import os
import uuid
import itertools
import contextvars
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# ==================== ORIGINAL IMPORTS ====================
from google_play_scraper import app as play_scraper
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from protobuf_decoder.protobuf_decoder import Parser
from message_ids import MESSAGE_ID_TO_NAME
import thunderFF_pb2

# ==================== WEB DASHBOARD ====================
from dashboard_server import bot_state, start_web_dashboard

# ==================== CONFIGURATION ====================
WEB_HOST = "0.0.0.0"
WEB_PORT = int(os.environ.get("PORT", 8182))  # ✅ Railway uses $PORT env variable

# ✅ FIX: Absolute paths — works from ANY working directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# ✅ AUTO MULTI-FILE: accounts.json, accounts2.json, accounts3.json ... (root directory)
def get_all_account_files():
    """Root-এ যত accounts*.json আছে সব অটো ডিটেক্ট করে"""
    import glob
    pattern = os.path.join(BASE_DIR, "accounts*.json")
    files = sorted(glob.glob(pattern))
    if not files:
        files = [os.path.join(BASE_DIR, "accounts.json")]
    return files
TOKEN_CACHE_FILE = os.path.join(BASE_DIR, "data", "token_cache.json")
DEVICES_FILE = os.path.join(BASE_DIR, "data", "devices.json")
TOKEN_CACHE_TTL = 3600

# 🔥 Match control
# ✅ FIX: LW interval 18s → 15s, speed সামান্য বাড়বে (ENV দিয়ে override করা যাবে)
START_MATCH_INTERVAL = float(os.environ.get("START_MATCH_INTERVAL", "15"))
# BR matchmaking queue LW-er cheye onek slow. 3s por por abar StartMatch pathale queue reset hoye jay,
# tai BR-er jonno alada (boro) interval. Railway Variable diye override kora jay.
BR_START_MATCH_INTERVAL = float(os.environ.get("BR_START_MATCH_INTERVAL", "20"))   # prothom file-er moto 3s
BR_DOUBLE_SEARCH = os.environ.get("BR_DOUBLE_SEARCH", "0") == "1"
BR_KEEPALIVE_INTERVAL = 5.0
BR_IDLE_LIMIT = 300   # x0.5s = 150s (LW: 80 = 40s)
NEW_MATCH_DELAY = float(os.environ.get("NEW_MATCH_DELAY", "12"))   
MAX_MATCH_DURATION = 700
MATCH_IDLE_TIMEOUT = 8.0
# Thunder+Sharma pathanor koto second por match "shesh" dhore socket bondho kore notun match shuru hobe.
# Server jodi bondho na kore continuous packet pathay (OB55), tokhon ei timer match quick cycle kore.
# Railway Variable: QUICK_FINISH_SECONDS (0 dile bondho, default 15)
try:
    QUICK_FINISH_SECONDS = float(os.environ.get("QUICK_FINISH_SECONDS", "45"))
except Exception:
    QUICK_FINISH_SECONDS = 15.0
# EXP koto second por por server theke refresh hobe (default 30, ager 90 chilo)
try:
    EXP_REFRESH_SECONDS = max(10.0, float(os.environ.get("EXP_REFRESH_SECONDS", "30")))
except Exception:
    EXP_REFRESH_SECONDS = 30.0
PRIORITY_REGIONS = ["BD","IND", "SG", "TH", "PH", "VN", "MY", "ID", "HK", "TW"]

# 🔥 Cache invalidation thresholds
MAX_CONSECUTIVE_PARSE_FAILURES = 5.0     
NON_MATCH_RECONNECT_DELAY = 1.0       

FALLBACK_UID = ""
FALLBACK_PASSWORD = ""


# ==================== ULTRA SAFE PERSISTENT DEVICE RANDOMIZER ====================
# ✅ FIX: In-memory cache — 500 accounts-এ প্রতিবার file read/write করা বন্ধ করে
# এটি disk I/O race condition এবং Railway crash ঠিক করে
_DEVICES_MEMORY_CACHE: Dict[str, dict] = {}
_DEVICES_CACHE_LOADED: bool = False
_DEVICES_DIRTY: bool = False  # True হলে save দরকার


def _load_devices_cache_once():
    """একবারই file থেকে load করে memory-তে রাখে"""
    global _DEVICES_MEMORY_CACHE, _DEVICES_CACHE_LOADED
    if _DEVICES_CACHE_LOADED:
        return
    if os.path.exists(DEVICES_FILE):
        try:
            with open(DEVICES_FILE, "r", encoding="utf-8") as f:
                _DEVICES_MEMORY_CACHE = json.load(f)
        except Exception:
            _DEVICES_MEMORY_CACHE = {}
    _DEVICES_CACHE_LOADED = True


def _save_devices_cache():
    """Memory cache-কে file-এ save করে"""
    global _DEVICES_DIRTY
    try:
        os.makedirs(os.path.dirname(DEVICES_FILE), exist_ok=True)
        tmp_file = DEVICES_FILE + ".tmp"
        with open(tmp_file, "w", encoding="utf-8") as f:
            json.dump(_DEVICES_MEMORY_CACHE, f, indent=4)
        os.replace(tmp_file, DEVICES_FILE)
        _DEVICES_DIRTY = False
    except Exception as e:
        print(f"[WARN] Failed to save devices cache: {e}")


def get_device_for_account(account_identifier: str) -> dict:
    """
    Ensures 1 ID = 1 Specific Device.
    ✅ FIX: File এখন শুধু একবার load হয়, 500x file I/O আর হবে না।
    """
    global _DEVICES_DIRTY
    _load_devices_cache_once()

    acc_key = str(account_identifier)
    
    # ✅ FIX: Memory cache থেকে চেক করো, file থেকে নয়
    if acc_key in _DEVICES_MEMORY_CACHE:
        return _DEVICES_MEMORY_CACHE[acc_key]
        
    # Generate new device profile for this account
    device_list = [
        ("Samsung", "SM-G998B", "Adreno (TM) 660", "Android OS 12 / API-31"),
        ("Xiaomi", "2201122G", "Adreno (TM) 730", "Android OS 13 / API-33"),
        ("Realme", "RMX3700", "Mali-G710", "Android OS 14 / API-34"),
        ("OnePlus", "CPH2451", "Adreno (TM) 740", "Android OS 13 / API-33"),
        ("OPPO", "CPH2611", "Adreno (TM) 720", "Android OS 14 / API-34"),
        ("Vivo", "V2203", "Mali-G710", "Android OS 12 / API-31"),
        ("Poco", "M2102J20SG", "Adreno (TM) 660", "Android OS 13 / API-33"),
    ]
    brand, model, gpu, os_ver = random.choice(device_list)
    
    new_device = {
        "unique_device_id": f"Google|{str(uuid.uuid4())}",
        "brand": brand,
        "model": model,
        "gpu_renderer": gpu,
        "system_software": os_ver,
        "screen_width": random.choice([1080, 1440, 720, 1280]),
        "screen_height": random.choice([2400, 3200, 1600, 2400]),
        "screen_dpi": str(random.randint(300, 420)),
        "memory": random.randint(2800, 6500),
        "processor_details": f"ARM64 FP ASIMD AES VMH | {random.randint(2200, 3200)} | {random.randint(6, 12)}",
        "client_ip": f"{random.randint(103, 223)}.{random.randint(10, 250)}.{random.randint(10, 250)}.{random.randint(10, 250)}"
    }
    
    # ✅ FIX: Memory-তে save করো, file-এ এখনই লেখো না
    _DEVICES_MEMORY_CACHE[acc_key] = new_device
    _DEVICES_DIRTY = True
    
    # ✅ FIX: Background-এ save — blocking করে না, I/O storm হয় না
    try:
        _save_devices_cache()
    except Exception as e:
        pass  # Background save fail হলেও memory cache থেকে কাজ চলবে
        
    return new_device


# ==================== CLOUDFLARE DNS RESOLVER & SOCKET OPTIMIZERS ====================
CLOUDFLARE_PRIMARY_DNS = "1.1.1.1"
CLOUDFLARE_SECONDARY_DNS = "1.0.0.1"
_DNS_CACHE: Dict[str, Tuple[str, float]] = {}
_DNS_CACHE_TTL = 300.0  # 5 minutes DNS cache

async def resolve_host_cloudflare(hostname: str) -> str:
    if not hostname:
        return hostname

    parts = hostname.split('.')
    if len(parts) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parts):
        return hostname

    now = time.time()
    if hostname in _DNS_CACHE:
        ip, exp = _DNS_CACHE[hostname]
        if now < exp:
            return ip

    def _query_cloudflare(server_ip: str) -> Optional[str]:
        s = None
        try:
            tx_id = random.randint(1000, 65535)
            header = struct.pack(">HHHHHH", tx_id, 0x0100, 1, 0, 0, 0)
            qname = b"".join(bytes([len(part)]) + part.encode('ascii') for part in hostname.split('.')) + b"\x00"
            query_pkt = header + qname + struct.pack(">HH", 1, 1)

            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(1.2)
            s.sendto(query_pkt, (server_ip, 53))
            resp, _ = s.recvfrom(1024)

            if len(resp) >= 12:
                ancount = struct.unpack(">H", resp[6:8])[0]
                if ancount > 0:
                    offset = 12 + len(qname) + 4
                    for _ in range(ancount):
                        if offset >= len(resp):
                            break
                        if (resp[offset] & 0xC0) == 0xC0:
                            offset += 2
                        else:
                            while offset < len(resp) and resp[offset] != 0:
                                offset += 1 + resp[offset]
                            offset += 1
                        if offset + 10 > len(resp):
                            break
                        rtype, rclass, ttl, rdlen = struct.unpack(">HHIH", resp[offset:offset+10])
                        offset += 10
                        if rtype == 1 and rdlen == 4 and offset + 4 <= len(resp):
                            return socket.inet_ntoa(resp[offset:offset+4])
                        offset += rdlen
        except Exception:
            pass
        finally:
            if s:
                try:
                    s.close()
                except Exception:
                    pass
        return None

    loop = asyncio.get_running_loop()
    ip = await loop.run_in_executor(None, _query_cloudflare, CLOUDFLARE_PRIMARY_DNS)
    if not ip:
        ip = await loop.run_in_executor(None, _query_cloudflare, CLOUDFLARE_SECONDARY_DNS)
    if not ip:
        try:
            ip_info = await loop.getaddrinfo(hostname, None, family=socket.AF_INET)
            if ip_info:
                ip = ip_info[0][4][0]
        except Exception:
            ip = hostname

    if ip:
        _DNS_CACHE[hostname] = (ip, now + _DNS_CACHE_TTL)
    return ip or hostname


def optimize_tcp_socket(sock: socket.socket):
    try:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)
    except Exception:
        pass


def optimize_udp_socket(sock: socket.socket):
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 131072)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 131072)
        if hasattr(socket, 'SIO_UDP_CONNRESET') and os.name == 'nt':
            try:
                sock.ioctl(socket.SIO_UDP_CONNRESET, False)
            except Exception:
                pass
    except Exception:
        pass


# ==================== NETWORK & CRYPTO ====================
client = httpx.AsyncClient(
    verify=False,
    timeout=15.0,
    limits=httpx.Limits(
        max_connections=1000,
        max_keepalive_connections=300,
        keepalive_expiry=30
    )
)

# ✅ FIX: Login semaphore — একসাথে সর্বোচ্চ LOGIN_CONCURRENCY টি account লগইন করতে পারবে
# version_config_cached থাকায় এখন 20 safe — Play Store scrape আর bottleneck নয়
# ENV দিয়ে override করা যাবে: LOGIN_CONCURRENCY=30
# ✅ FIX: 20→30 — তাড়াতাড়ি connect হবে, server rate limit এখনো safe
_LOGIN_CONCURRENCY = int(os.environ.get("LOGIN_CONCURRENCY", "30"))
_LOGIN_SEMAPHORE = asyncio.Semaphore(_LOGIN_CONCURRENCY)

headers = {
    'User-Agent': 'UnityPlayer/2018.4.12f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Expect': '100-continue',
    'X-Unity-Version': '2018.4.12f1',
    'X-GA-SV': '1789535859',
    'X-GA': 'v1 1',
    'ReleaseVersion': 'OB55'
}

AES_KEY = b'Yg&tc%DEuh6%Zc^8'
AES_IV = b'6oyZDr22E3ychjM%'

CRC7_TABLE = bytes([
    0, 9, 18, 27, 36, 45, 54, 63, 72, 65, 90, 83, 108, 101, 126, 119,
    25, 16, 11, 2, 61, 52, 47, 38, 81, 88, 67, 74, 117, 124, 103, 110,
    50, 59, 32, 41, 22, 31, 4, 13, 122, 115, 104, 97, 94, 87, 76, 69,
    43, 34, 57, 48, 15, 6, 29, 20, 99, 106, 113, 120, 71, 78, 85, 92,
    100, 109, 118, 127, 64, 73, 82, 91, 44, 37, 62, 55, 8, 1, 26, 19,
    125, 116, 111, 102, 89, 80, 75, 66, 53, 60, 39, 46, 17, 24, 3, 10,
    86, 95, 68, 77, 114, 123, 96, 105, 30, 23, 12, 5, 58, 51, 40, 33,
    79, 70, 93, 84, 107, 98, 121, 112, 7, 14, 21, 28, 35, 42, 49, 56,
    65, 72, 83, 90, 101, 108, 119, 126, 9, 0, 27, 18, 45, 36, 63, 54,
    88, 81, 74, 67, 124, 117, 110, 103, 16, 25, 2, 11, 52, 61, 38, 47,
    115, 122, 97, 104, 87, 94, 69, 76, 59, 50, 41, 32, 31, 22, 13, 4,
    106, 99, 120, 113, 78, 71, 92, 85, 34, 43, 48, 57, 6, 15, 20, 29,
    37, 44, 55, 62, 1, 8, 19, 26, 109, 100, 127, 118, 73, 64, 91, 82,
    60, 53, 46, 39, 24, 17, 10, 3, 116, 125, 102, 111, 80, 89, 66, 75,
    23, 30, 5, 12, 51, 58, 33, 40, 95, 86, 77, 68, 123, 114, 105, 96,
    14, 7, 28, 21, 42, 35, 56, 49, 70, 79, 84, 93, 98, 107, 112, 121,
])

_DELTA = 0x9E3779B9
_ROUNDS = 16
_FIELD_SIZES = {0: 1, 1: 2, 2: 2, 3: 1, 4: 2}
_FIELD_NAMES = {0: "sendOption", 1: "cmd", 2: "orderId", 3: "flags", 4: "length"}

sai_tail_dul = bytes.fromhex(
    "0101030101045452000103000100000410312e3133302e3232"
    "1432303139313231303430ca0163736f7665727365612e737472"
    "6f6e67686f6c642e66726565666972656d6f62696c652e636f6d"
    "3b302e302e302e303b33342e3132362e37362e34353b33342e38"
    "372e3137372e31343b33342e38372e3137302e3233303b33352e"
    "3138352e3138332e353700000000000001000000000000000000"
    "0000000100000000000100000000000100b8eeec91c5d7ffde110200"
)

headers = {
    'User-Agent': 'UnityPlayer/2018.4.12f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Expect': '100-continue',
    'X-Unity-Version': '2018.4.12f1',
    'X-GA-SV': '1789535859',
    'X-GA': 'v1 1',
    'ReleaseVersion': 'OB55'
}

class Colors:
    HEADER = '\033[95m'
    GREEN = '\033[92m'
    FAIL = '\033[91m'
    WARNING = '\033[93m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    ENDC = '\033[0m'

def print_colored(text, color=Colors.WHITE):
    try:
        print(f"{color}{text}{Colors.ENDC}")
    except Exception:
        try:
            print(f"{color}{text.encode('ascii', errors='replace').decode('ascii')}{Colors.ENDC}")
        except Exception:
            pass

def print_success(text):
    print_colored(f"[+] {text}", Colors.GREEN)
    try:
        bot_state.log(text, "success")
    except Exception:
        pass

def print_error(text):
    print_colored(f"[-] {text}", Colors.FAIL)
    try:
        bot_state.log(text, "error")
    except Exception:
        pass

def print_warning(text):
    print_colored(f"[!] {text}", Colors.WARNING)
    try:
        bot_state.log(text, "warning")
    except Exception:
        pass

def print_info(text):
    print_colored(f"[i] {text}", Colors.CYAN)
    try:
        bot_state.log(text, "info")
    except Exception:
        pass

def get_proto_field(d, key, default=None):
    if not d or not isinstance(d, dict):
        return default
    if key in d:
        val = d[key].get('data')
        return val if val is not None else default
    if str(key) in d:
        val = d[str(key)].get('data')
        return val if val is not None else default
    return default


# ==================== PER-ACCOUNT MATCH COUNTER ====================
_match_counters: Dict[str, int] = {}
_match_counter_lock = asyncio.Lock()

async def _inc_match(uid: str) -> int:
    async with _match_counter_lock:
        _match_counters[uid] = _match_counters.get(uid, 0) + 1
        return _match_counters[uid]

async def _dec_match(uid: str) -> int:
    async with _match_counter_lock:
        if uid in _match_counters and _match_counters[uid] > 0:
            _match_counters[uid] -= 1
        return _match_counters.get(uid, 0)

async def _get_match_count(uid: str) -> int:
    async with _match_counter_lock:
        return _match_counters.get(uid, 0)

async def _get_total_match_count() -> int:
    async with _match_counter_lock:
        return sum(_match_counters.values())


# ==================== TOKEN CACHE ====================
_token_cache_memo: Dict[str, Any] = {}
_token_cache_memo_time: float = 0.0
_TOKEN_CACHE_MEMO_TTL = 5.0

def _json_serializer(obj):
    if isinstance(obj, (bytes, bytearray)):
        return {"__bytes_hex__": bytes(obj).hex()}
    raise TypeError(f"Type {type(obj)} not serializable")

def _json_deserializer(obj):
    if isinstance(obj, dict):
        if "__bytes_hex__" in obj and len(obj) == 1:
            try:
                return bytes.fromhex(obj["__bytes_hex__"])
            except Exception:
                return b""
        return {k: _json_deserializer(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_json_deserializer(x) for x in obj]
    return obj

def _load_token_cache() -> Dict[str, Any]:
    global _token_cache_memo, _token_cache_memo_time
    now = time.time()
    if _token_cache_memo and (now - _token_cache_memo_time) < _TOKEN_CACHE_MEMO_TTL:
        return _token_cache_memo

    if not os.path.exists(TOKEN_CACHE_FILE):
        return {}
    try:
        with open(TOKEN_CACHE_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if not content:
            return {}
        data = json.loads(content)
        if not isinstance(data, dict):
            raise ValueError("Cache root must be dict")
        parsed = _json_deserializer(data)
        _token_cache_memo = parsed
        _token_cache_memo_time = now
        return parsed
    except Exception as e:
        print_error(f"Token cache corrupt → deleting: {e}")
        try:
            os.remove(TOKEN_CACHE_FILE)
        except Exception:
            pass
        return {}

def _save_token_cache(cache: Dict[str, Any]):
    global _token_cache_memo, _token_cache_memo_time
    try:
        os.makedirs(os.path.dirname(TOKEN_CACHE_FILE), exist_ok=True)
        tmp_file = TOKEN_CACHE_FILE + ".tmp"
        with open(tmp_file, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2, default=_json_serializer)
        os.replace(tmp_file, TOKEN_CACHE_FILE)
        _token_cache_memo = cache
        _token_cache_memo_time = time.time()
    except Exception as e:
        print_error(f"Token cache save error: {e}")

def cache_get(uid: str) -> Optional[Dict]:
    cache = _load_token_cache()
    entry = cache.get(str(uid))
    if not entry:
        return None
    if time.time() - entry.get("cached_at", 0) > TOKEN_CACHE_TTL:
        print_info(f"[CACHE] UID {uid} expired. Re-login needed.")
        cache_invalidate(uid)
        return None
    if str(entry.get("account_id", "")).isdigit():
        entry["account_id"] = int(entry["account_id"])
    if not isinstance(entry.get("login_payload_data"), (bytes, bytearray)):
        print_warning(f"[CACHE] UID {uid} missing payload → invalidating")
        cache_invalidate(uid)
        return None
    return entry

def cache_set(uid: str, account_data: Dict):
    cache = _load_token_cache()
    entry = dict(account_data)
    # ✅ FIX: TTL jitter — সব 500 token একসাথে expire হলে mass re-login হয়
    # Random jitter দিলে expire ছড়িয়ে যায়, thundering herd বন্ধ হয়
    jitter = random.uniform(-TOKEN_CACHE_TTL * 0.20, TOKEN_CACHE_TTL * 0.20)
    entry["cached_at"] = time.time() + jitter  # ±20% random offset
    cache[str(uid)] = entry
    _save_token_cache(cache)
    print_success(f"[CACHE] Saved credentials for UID {uid}")

def cache_invalidate(uid: str):
    cache = _load_token_cache()
    if str(uid) in cache:
        del cache[str(uid)]
        _save_token_cache(cache)
        print_warning(f"[CACHE] Invalidated: {uid}")


# ==================== ENCRYPTION & PROTOBUF ====================

async def aes_encrypt(payload, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(payload, AES.block_size))


_current_login_uid = contextvars.ContextVar("current_login_uid", default=None)

def report_fail(uid, stage: str, detail: str = "", generic: bool = False):
    """Login failure-er asol karon console + dashboard log + account card-e dekhay"""
    if uid is None:
        uid = _current_login_uid.get()
    msg = f"[LOGIN FAIL] {stage}" + (f" -> {detail}" if detail else "")
    print_error(msg)
    try:
        bot_state.log(msg, "error", str(uid) if uid is not None else None)
        if uid is not None:
            acc = bot_state.accounts.get(str(uid))
            # generic (summary) message ashol karon-ke overwrite korbe na
            if not (generic and acc and acc.get("last_error")):
                bot_state.set_error(str(uid), f"{stage}" + (f" -> {detail}" if detail else ""))
    except Exception:
        pass

async def get_playstore_version():
    # Railway Variable diye override kora jay: FF_APP_VERSION (jemon 1.120.1)
    env_ver = os.environ.get("FF_APP_VERSION", "").strip()
    if env_ver:
        return env_ver
    loop = asyncio.get_running_loop()
    for country in ("id", "bd", "in", "us"):
        try:
            result = await asyncio.wait_for(
                loop.run_in_executor(
                    None,
                    lambda c=country: play_scraper('com.dts.freefireth', lang='hi', country=c)
                ),
                timeout=20
            )
            ver = (result or {}).get("version")
            if ver and any(ch.isdigit() for ch in str(ver)):
                return ver
            report_fail(None, f"Play Store version invalid ({country})", str(ver))
        except Exception as e:
            report_fail(None, f"Play Store scrape failed ({country})", repr(e)[:150])
    return None

async def version_config():
    app_version = await get_playstore_version()
    if not app_version:
        report_fail(None, "App version paoa jayni", "Railway Variables-e FF_APP_VERSION din (jemon 1.120.1)")
        return None
    api_url = (
        "https://version.ggwhitehawk.com/live/ver.php"
        f"?version={app_version}"
        "&lang=hi&device=android&channel=android"
        "&appstore=googleplay&region=BD"
        "&whitelist_version=1.3.0&whitelist_sp_version=1.0.0"
    )
    try:
        response = await client.get(api_url)
        response.raise_for_status()
        data = response.json()
        server_url = data.get("server_url")
        remote_version = data.get("remote_version")
        latest_release_version = data.get("latest_release_version")
        if not server_url or not remote_version or not latest_release_version:
            report_fail(None, "ver.php incomplete response", f"app_version={app_version} data={str(data)[:200]}")
            return None
        return latest_release_version, remote_version, server_url
    except Exception as e:
        report_fail(None, "ver.php request failed", repr(e)[:200])
        return None


# ✅ FIX: version_config shared cache — সব accounts একটাই Play Store scrape শেয়ার করবে
# নতুন deploy-এ 500 accounts একসাথে login করলে প্রতিটা আলাদা scrape করত (500x slow!)
# এখন একটাই scrape হবে, বাকি সব cache থেকে পাবে → fast connect
_version_config_cache: Optional[tuple] = None
_version_config_cache_time: float = 0.0
_VERSION_CONFIG_CACHE_TTL = 3600.0  # ১ ঘণ্টা valid থাকবে
_version_config_lock: Optional[asyncio.Lock] = None

def _get_version_config_lock():
    global _version_config_lock
    if _version_config_lock is None:
        _version_config_lock = asyncio.Lock()
    return _version_config_lock

async def version_config_cached():
    """✅ সব accounts-এর জন্য একটাই version_config call — Railway fast connect"""
    global _version_config_cache, _version_config_cache_time
    now = time.time()
    # Cache আছে এবং valid → সরাসরি return
    if _version_config_cache and (now - _version_config_cache_time) < _VERSION_CONFIG_CACHE_TTL:
        return _version_config_cache
    # Lock নিয়ে double-check (thundering herd বন্ধ করে)
    async with _get_version_config_lock():
        now = time.time()
        if _version_config_cache and (now - _version_config_cache_time) < _VERSION_CONFIG_CACHE_TTL:
            return _version_config_cache
        print_info("[VERSION] Fetching version config (shared for all accounts)...")
        result = await version_config()
        if result:
            _version_config_cache = result
            _version_config_cache_time = time.time()
            print_success(f"[VERSION] Cached: {result[0]} / {result[1]}")
        return result

async def get_access_token(uid, password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    hdrs = {
        "Host": "100067.connect.garena.com",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 12; SM-G998B Build/SP1A.210812.016)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"
    }
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"
    }
    last_err = ""
    for attempt in range(5):
        try:
            response = await client.post(url, headers=hdrs, data=data)
            last_err = f"HTTP {response.status_code} {response.text[:150]}"
            if response.status_code == 200:
                response_data = response.json()
                open_id = response_data.get("open_id")
                access_token = response_data.get("access_token")
                platform = response_data.get("platform", 4)
                if open_id and access_token:
                    return open_id, access_token, platform
            if response.status_code == 429:
                await asyncio.sleep(1)
                continue
        except Exception as e:
            last_err = repr(e)[:150]
        await asyncio.sleep(0.5)
    report_fail(uid, "Garena guest token grant failed (UID/Password thik ache? IP block?)", last_err)
    return None

async def parse_results(parsed_results):
    result_dict = {}
    for result in parsed_results:
        field_data = {"wire_type": result.wire_type}
        if result.wire_type == "varint":
            field_data["data"] = result.data
        elif result.wire_type == "string":
            field_data["data"] = result.data
        elif result.wire_type == "bytes":
            field_data["data"] = result.data
        elif result.wire_type == "length_delimited":
            field_data["data"] = await parse_results(result.data.results)
        result_dict[result.field] = field_data
    return result_dict

async def decode_protobuf(data):
    parsed_results = Parser().parse(data)
    parsed_results_dict = await parse_results(parsed_results)
    return json.dumps(parsed_results_dict)

async def build_majorlogin_payload_legacy(open_id, access_token, platform, client_version, device_info):
    try:
        proto = thunderFF_pb2.MajorLoginReq()
        proto.event_time = str(datetime.now())[:-7]
        proto.game_name = "free fire"
        proto.platform_id = 1 if str(platform) in ["1", "4"] else int(platform)
        proto.client_version = client_version
        proto.client_version_code = "2019121229"
        
        # --- INJECTING PERSISTENT DYNAMIC DEVICE DATA ---
        proto.system_software = device_info.get("system_software", "Android OS 12 / API-31 (SP1A.210812.016.C2/user.dxu.20260701.180839)")
        proto.system_hardware = device_info.get("brand", "Handheld")
        proto.device_type = device_info.get("model", "Handheld")
        proto.screen_width = int(device_info.get("screen_width", 1600))
        proto.screen_height = int(device_info.get("screen_height", 900))
        proto.screen_dpi = str(device_info.get("screen_dpi", "300"))
        proto.processor_details = device_info.get("processor_details", "x86-64 SSE3 SSE4.1 SSE4.2 AVX | 2400 | 4")
        proto.memory = int(device_info.get("memory", 5951))
        proto.gpu_renderer = device_info.get("gpu_renderer", "Adreno (TM) 640")
        proto.unique_device_id = device_info.get("unique_device_id", "Google|725030d8-6585-4f55-bcca-a6df7e59935b")
        proto.client_ip = device_info.get("client_ip", "103.145.112.210")
        # ------------------------------------------------
        
        proto.telecom_operator = "Citycell"
        proto.network_operator_a = "Citycell"
        proto.network_type = "WIFI"
        proto.network_type_a = "WIFI"
        proto.cpu_type = 2
        proto.cpu_architecture = "64"
        proto.gpu_version = "OpenGL ES 3.2"
        proto.graphics_api = "OpenGLES2"
        proto.language = "en"
        proto.open_id = open_id
        proto.open_id_type = str(platform)
        proto.login_open_id_type = int(platform)
        proto.access_token = access_token
        proto.login_by = 3
        proto.platform_sdk_id = 2
        proto.origin_platform_type = str(platform)
        proto.primary_platform_type = str(platform)
        proto.reg_avatar = 1
        proto.channel_type = 3
        
        memory_available = proto.memory_available
        memory_available.version = 55
        memory_available.hidden_value = 81
        
        proto.external_storage_total = 34308
        proto.external_storage_available = 30777
        proto.internal_storage_total = 2519
        proto.internal_storage_available = 243
        proto.game_disk_storage_total = 34308
        proto.game_disk_storage_available = 32224
        proto.external_sdcard_total_storage = 34308
        proto.external_sdcard_avail_storage = 32224
        
        proto.library_path = "/data/app/~~UKDdGuy32C5yOa0KZe_ROA==/com.dts.freefireth-UAKF1gjDbXSGfpA07JDTKQ==/lib/arm64"
        proto.library_token = "b8e0cd5e295eee42f5860d3c86e483dd|/data/app/~~UKDdGuy32C5yOa0KZe_ROA==/com.dts.freefireth-UAKF1gjDbXSGfpA07JDTKQ==/base.apk"
        proto.client_using_version = "7428b253defc164018c604a1ebbfebdf"
        proto.supported_astc_bitset = 4095
        proto.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWAUOUgsvA1snWlBaO1kFYg=="
        proto.loading_time = 14582
        proto.release_channel = "android"
        proto.extra_info = "KqsHT4tDHGqm9PQ3syB24XA4N6SWy/Q/HfMFTQM+SgxmVqsgPK138ajtCFyVNW/Q7p6hxoenpRjeZ2NphiIosCZ3YDkONB5NAa+zTwNo7iabx/mj"
        proto.android_engine_init_flag = 111207
        proto.if_push = 1
        proto.is_vpn = 0
        
        payload = proto.SerializeToString()
        return await aes_encrypt(payload, AES_KEY, AES_IV)
    except Exception:
        return None

# ==================== MAJORLOGIN PAYLOAD (REAL CLIENT LAYOUT) ====================
# Real game client-er MajorLogin packet-er field layout onujayi banano.
# Ager version-e 25 no. field ke message (memory_available) hishebe pathano hoto,
# kintu real client ekhane String (device name) pathay. Aro kichu field
# (85, 90, 91, 96, 102, 104-107) chilo na. Eigulo mismatch hoyei server
# BR_AUTH_ABNORMAL_GAME_CLIENT dicchilo.
def _pb_varint(n: int) -> bytes:
    n = int(n)
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            out.append(b | 0x80)
        else:
            out.append(b)
            break
    return bytes(out)


def _pb_encode_fields(fields: Dict[int, Any]) -> bytes:
    """{field_no: int|str|bytes} -> protobuf bytes (field number order-e, real client-er moto)"""
    out = bytearray()
    for num in sorted(fields):
        val = fields[num]
        if val is None:
            continue
        if isinstance(val, bool):
            val = int(val)
        if isinstance(val, int):
            out += _pb_varint((num << 3) | 0) + _pb_varint(val)
        else:
            data = val if isinstance(val, (bytes, bytearray)) else str(val).encode("utf-8")
            out += _pb_varint((num << 3) | 2) + _pb_varint(len(data)) + bytes(data)
    return bytes(out)


# Device profile: real client theke paoa consistent hardware set (OS, GPU, CPU, storage ek sathe mele)
REAL_CLIENT_PROFILE = {
    8:  "Android OS 10 / API-29 (QQ3A.200805.001/135998ea76)",
    9:  "Handheld",
    12: 1666,
    13: 750,
    14: "408",
    15: "ARM64 FP ASIMD AES | 2304 | 8",
    16: 5602,
    17: "Adreno (TM) 618",
    18: "OpenGL ES 3.2 V@415.0 (GIT@29668c6, I386ada412e, 1599643163) (Date:09/09/20)",
    24: "Handheld",
    25: "Xiaomi POCO X3",
    57: "7428b253defc164018c604a1ebbfebdf",
    60: 107339, 61: 91837, 62: 2477, 63: 673,
    64: 91965, 65: 107339, 66: 91965, 67: 107339,
    74: "/data/app/com.dts.freefireth-TuO5diNOf-gtts9f6fYPrw==/lib/arm64",
    77: "b8e0cd5e295eee42f5860d3c86e483dd|/data/app/com.dts.freefireth-TuO5diNOf-gtts9f6fYPrw==/base.apk",
    90: "Mymensingh",
    94: "KqsHT0N1+u1eoAb9dbApLv6MaRbAHgNLk8LWJCNlXGaeEMxOzf5uIIvCld3lpffwqvZs3PmP2ew0lv6zlTP9Cp5+xQxEZshOAQTHmdY5mZL5v8q1",
    96: '{"cur_rate":[30,50,60,90,120],"support_etc2":false}',
    102: "40 06 41 47 56 55 5f 01 61",
    104: 50212,
    106: "https://dl-bs.ggpolarbear.com/live/ABHotUpdates/|https://core-bs.ggpolarbear.com/live/ABHotUpdates/|211c933168f55902c7dfbfd8c4e2957d",
    107: "1.27aa7af0fc56d172",
}


def _build_majorlogin_raw(open_id, access_token, platform, client_version, device_info) -> bytes:
    plat = str(platform)
    f: Dict[int, Any] = dict(REAL_CLIENT_PROFILE)
    f.update({
        3:  str(datetime.now())[:-7],
        4:  "free fire",
        5:  1 if plat in ("1", "4") else int(platform),
        7:  client_version,
        11: "WIFI",
        19: (device_info or {}).get("unique_device_id") or f"Google|{uuid.uuid4()}",
        20: (device_info or {}).get("client_ip") or "27.123.253.211",
        21: "en",
        22: open_id,
        23: plat,
        29: access_token,
        30: 1,
        42: "WIFI",
        73: 2,
        76: 1,
        78: 3,
        79: 2,
        81: "64",
        83: "2019121229",
        85: 3,
        86: "OpenGLES2",
        87: 4095,
        88: int(platform),
        91: "H",
        92: random.randint(5000, 9000),
        93: "android",
        95: 111207,
        97: 1,
        98: 1,
        99: plat,
        100: plat,
        105: 1,
    })
    return _pb_encode_fields(f)


async def build_majorlogin_payload(open_id, access_token, platform, client_version, device_info):
    try:
        if os.environ.get("FF_LEGACY_PAYLOAD") == "1":
            return await build_majorlogin_payload_legacy(open_id, access_token, platform, client_version, device_info)
        payload = _build_majorlogin_raw(open_id, access_token, platform, client_version, device_info)
        return await aes_encrypt(payload, AES_KEY, AES_IV)
    except Exception as e:
        report_fail(None, "MajorLogin payload build exception", repr(e)[:200])
        return None


async def send_majorlogin(data, release_version, server_url):
    try:
        url = f"{server_url}MajorLogin"
        req_headers = headers.copy()
        req_headers["ReleaseVersion"] = release_version
        response = await client.post(url, headers=req_headers, data=data)
        if response.status_code != 200:
            report_fail(None, f"MajorLogin HTTP {response.status_code}", f"url={url} body={response.text[:150]}")
            return None
        response_content = response.content
        if len(response_content) < 40:
            report_fail(None, "MajorLogin response too short", f"{len(response_content)} bytes: {response_content[:60]!r}")
            return None

        # 1. Direct parse
        res_proto = thunderFF_pb2.MajorLoginRes()
        try:
            res_proto.ParseFromString(response_content)
            if res_proto.region and res_proto.token:
                return res_proto
        except Exception:
            pass

        # 2. OB55 64-byte header offset check
        if len(response_content) > 64:
            try:
                res_proto = thunderFF_pb2.MajorLoginRes()
                res_proto.ParseFromString(response_content[64:])
                if res_proto.region and res_proto.token:
                    return res_proto
            except Exception:
                pass

        # 3. Dynamic offset search for OB55 compatibility
        for offset in range(min(128, len(response_content))):
            try:
                candidate = thunderFF_pb2.MajorLoginRes()
                candidate.ParseFromString(response_content[offset:])
                if candidate.region and candidate.token:
                    return candidate
            except Exception:
                pass

        res_proto = thunderFF_pb2.MajorLoginRes()
        res_proto.ParseFromString(response_content)
        if not res_proto.token:
            report_fail(None, "MajorLogin token khali (version/payload mismatch hote pare)", f"{len(response_content)} bytes")
            return None
        return res_proto
    except Exception as e:
        report_fail(None, "MajorLogin exception", repr(e)[:200])
        return None

async def send_getlogin(data, base_url, token, release_version):
    try:
        url = f"{base_url.rstrip('/')}/GetLoginData"
        req_headers = headers.copy()
        req_headers["ReleaseVersion"] = release_version
        req_headers['Authorization'] = f"Bearer {token}"
        req_headers['Host'] = "clientbp.ppmainecoonghj.com"
        response = await client.post(url, headers=req_headers, data=data)
        if response.status_code != 200:
            report_fail(None, f"GetLoginData HTTP {response.status_code}", f"url={url} body={response.text[:150]}")
            return None
        response_content = response.content

        res_proto = thunderFF_pb2.GetLoginDataRes()
        parsed_successfully = False
        try:
            res_proto.ParseFromString(response_content)
            if res_proto.functional_addrs or res_proto.informational_addrs:
                parsed_successfully = True
        except Exception:
            pass

        if not parsed_successfully:
            for offset in range(min(128, len(response_content))):
                try:
                    candidate = thunderFF_pb2.GetLoginDataRes()
                    candidate.ParseFromString(response_content[offset:])
                    if candidate.functional_addrs or candidate.informational_addrs:
                        res_proto = candidate
                        break
                except Exception:
                    pass

        dict_res = {}
        try:
            parsed = Parser().parse(response_content.hex())
            dict_res = await parse_results(parsed)
        except Exception:
            pass

        return res_proto, dict_res
    except Exception as e:
        report_fail(None, "GetLoginData exception", repr(e)[:200])
        return None

async def build_tcp_startup_packet(account_id, token, server_time, key, iv, region="BD", typ='OnLine'):
    uid_hex = f"{int(account_id):016x}"
    timestamp_hex = f"{int(server_time):08x}"
    encode_token = token.encode()
    encrypted_packet = (await aes_encrypt(encode_token, key, iv)).hex()
    encrypted_packet_length = f"{len(encrypted_packet) // 2:08x}"
    reg = str(region).upper() if region else "BD"
    if typ == 'OnLine':
        prefix = '7119' if reg == 'BD' else ('7114' if reg == 'IND' else '7115')
        return f"{prefix}{uid_hex}{timestamp_hex}00000000{encrypted_packet_length}{encrypted_packet}"
    else:  # ChaT / Informational
        prefix = '9219' if reg == 'BD' else ('9214' if reg == 'IND' else '9215')
        return f"{prefix}{uid_hex}{timestamp_hex}{encrypted_packet_length}{encrypted_packet}"

async def send_keep_alive(region="BD"):
    """Send 2-byte keep-alive pulse to maintain connection in OB55"""
    try:
        reg = str(region).upper() if region else "BD"
        ka_hex = "0219" if reg == "BD" else ("0214" if reg == "IND" else "0215")
        return bytes.fromhex(ka_hex)
    except Exception:
        return bytes.fromhex("0219")


async def start_game_lone_wolf(region, client_version, writer, key, iv):
    packet = bytes.fromhex("080112800a0a010b102b3a110a044944433110aa011a064555524f50453a100a044944433210311a064555524f504540014a0801090a0b1219202758016291090a8001303838463832424630324139363736373032303130313030303030303030303030303136303030313030313530303032323246393745454530463030303030303436373632353134303030303030303030303030303030303030303030303030303030303030303030303030303066663030303030303030636163666131366410241afb02735d5e571400024a775d45414d1a041b1c001f11010449715f4243481a001e1d071c1703004b1a4066785c524570735c51486775421b5c5a4c07504042685a63610816054e19025e75196001477c015165406370195f5547404e4550640103020f1304064863754268676c755f65576e40467e5f0a417a4701026d675d6e73670b1108495a4c6a0b78470b740065645e525a057258425f584a447d4e6759440c11044e7c596d7f4b625f7d04055a47505c4e1d6b5b4107447d7201057d7f0f14084e430457674f7e517d72015172415d027473577c4d615f79535256780911030f4d5e027a797f614165067806505d53777750475e75064257076500460817014e741e7e5078487e7a7c465e7669767153497064605a7376677773550d160148037e18675966787f4c42607a645f577e7b441b460776026b18685d0b110205490060020f70676175654674706671797f41067346677c4e06585e780f15074c57047b40517075415f6364027259674b5b0166407f7340600407770a22047a5d5c52300b3a0a167305067162727516134208312e3133302e3232480350015ae90403626253513635686e556f4e36416456324b796f566c636f477776484f624e56526c4d727073504b4f43654177616848494176795556497273743752737149734a7a786b3247525268377a2f637664626d504f6a73552f79626d38547a4c69586d2f474351696d494b53486833447955726f39515152756c34545350626d6d624b7949565937545671577059455372323646572f59624578507338514f706d317372785455736c30796a434144444d4f34616a654b615753366361496c554b4963797a494e396d52516f715277687939797257476d337a644345337a6a61436f492f5a585233656f65365a42647a64677654636b6b665733356e4d4c6a6a565072564b6433523172756174394e50514150724a5546627859696c4c5a3859707336654d5447666b6649793574666a526c314d4648706b51774c6373374439656378566c41636f374e664f6d2b30654756466c4434744478706771385533595973587645384842502f70666c767a737138316a32524f4d7857437556445442492f684735625462773166456e4249725162762b636144775147696f74554e316d4c4b77734379456f4766706746614251457645672b736a764c4c78704743334c304a5344532f74526169504354553344374e6249306547516651622f5a466f4c36455630775a324d6f583932414c572f5049752f56634663584e70596b356f7966326151416a536971486a2f363276354843644f525551303578754e6171795251625653704654303137655237675255636b4966366c6f447476342b514e4a4670766d74757077707774396a5a5974437a4b56743657726d6e36785837706658456251555434684f3758a201050803108703a201050804108103a20105080510c001a20105081d10cc01a2010408161078a20105080e10af01a201020815")
    proto = thunderFF_pb2.StartMatch()
    proto.ParseFromString(packet)
    if hasattr(proto.main, 'region_list') and len(proto.main.region_list) > 0:
        proto.main.region_list[0].region = region
        if len(proto.main.region_list) > 1:
            proto.main.region_list[1].region = region
    if hasattr(proto.main, 'client_version'):
        proto.main.client_version.remote_version = client_version
    packet = proto.SerializeToString()
    encrypted_packet = (await aes_encrypt(packet, key, iv)).hex()
    packet_length = len(encrypted_packet) // 2
    hex_length = hex(packet_length)[2:]
    hex_length = hex_length if len(hex_length) > 1 else "0" + hex_length
    reg = str(region).upper() if region else "BD"
    reg_prefix = "031900" if reg == "BD" else ("031400" if reg == "IND" else "031500")
    final_packet = reg_prefix + "0" * (6 - len(hex_length)) + hex_length + encrypted_packet
    writer.write(bytes.fromhex(final_packet))
    await writer.drain()
    bot_state.log(f"[🐺] Lone Wolf Match Search Packet Sent | Region: {region}", "info")


async def start_game_battle_royale(region, client_version, writer, key, iv):
    """BR (Battle Royale) ম্যাচ সার্চ প্যাকেট — BR-UDP থেকে নেওয়া হয়েছে"""
    packet = bytes.fromhex("080112800a0a010110013a110a044944433110aa011a064555524f50453a100a044944433210311a064555524f504540014a0801090a0b1219202758016291090a8001303838463832424630324139363736373032303130313030303030303030303030303136303030313030313530303032323246393745454530463030303030303436373632353134303030303030303030303030303030303030303030303030303030303030303030303030303066663030303030303030636163666131366410241afb02735d5e571400024a775d45414d1a041b1c001f11010449715f4243481a001e1d071c1703004b1a4066785c524570735c51486775421b5c5a4c07504042685a63610816054e19025e75196001477c015165406370195f5547404e4550640103020f1304064863754268676c755f65576e40467e5f0a417a4701026d675d6e73670b1108495a4c6a0b78470b740065645e525a057258425f584a447d4e6759440c11044e7c596d7f4b625f7d04055a47505c4e1d6b5b4107447d7201057d7f0f14084e430457674f7e517d72015172415d027473577c4d615f79535256780911030f4d5e027a797f614165067806505d53777750475e75064257076500460817014e741e7e5078487e7a7c465e7669767153497064605a7376677773550d160148037e18675966787f4c42607a645f577e7b441b460776026b18685d0b110205490060020f70676175654674706671797f41067346677c4e06585e780f15074c57047b40517075415f6364027259674b5b0166407f7340600407770a22047a5d5c52300b3a0a167305067162727516134208312e3133302e3232480350015ae90403626253513635686e556f4e36416456324b796f566c636f477776484f624e56526c4d727073504b4f43654177616848494176795556497273743752737149734a7a786b3247525268377a2f637664626d504f6a73552f79626d38547a4c69586d2f474351696d494b53486833447955726f39515152756c34545350626d6d624b7949565937545671577059455372323646572f59624578507338514f706d317372785455736c30796a434144444d4f34616a654b615753366361496c554b4963797a494e396d52516f715277687939797257476d337a644345337a6a61436f492f5a585233656f65365a42647a64677654636b6b665733356e4d4c6a6a565072564b6433523172756174394e50514150724a5546627859696c4c5a3859707336654d5447666b6649793574666a526c314d4648706b51774c6373374439656378566c41636f374e664f6d2b30654756466c4434744478706771385533595973587645384842502f70666c767a737138316a32524f4d7857437556445442492f684735625462773166456e4249725162762b636144775147696f74554e316d4c4b77734379456f4766706746614251457645672b736a764c4c78704743334c304a5344532f74526169504354553344374e6249306547516651622f5a466f4c36455630775a324d6f583932414c572f5049752f56634663584e70596b356f7966326151416a536971486a2f363276354843644f525551303578754e6171795251625653704654303137655237675255636b4966366c6f447476342b514e4a4670766d74757077707774396a5a5974437a4b56743657726d6e36785837706658456251555434684f3758a201050803108703a201050804108103a20105080510c001a20105081d10cc01a2010408161078a20105080e10af01a201020815")
    proto = thunderFF_pb2.StartMatch()
    proto.ParseFromString(packet)
    if hasattr(proto.main, 'region_list') and len(proto.main.region_list) > 0:
        proto.main.region_list[0].region = region
        if len(proto.main.region_list) > 1:
            proto.main.region_list[1].region = region
    if hasattr(proto.main, 'client_version'):
        proto.main.client_version.remote_version = client_version
    packet = proto.SerializeToString()
    encrypted_packet = (await aes_encrypt(packet, key, iv)).hex()
    packet_length = len(encrypted_packet) // 2
    hex_length = hex(packet_length)[2:]
    hex_length = hex_length if len(hex_length) > 1 else "0" + hex_length
    reg = str(region).upper() if region else "BD"
    reg_prefix = "031900" if reg == "BD" else ("031400" if reg == "IND" else "031500")
    final_packet = reg_prefix + "0" * (6 - len(hex_length)) + hex_length + encrypted_packet
    writer.write(bytes.fromhex(final_packet))
    await writer.drain()
    bot_state.log(f"[⚔] Battle Royale Match Search Packet Sent ({packet_length} bytes) | Region: {region}", "info")

async def has_ssan_zig(n):
    z = (n << 1) & 0xFFFFFFFFFFFFFFFF
    out = bytearray()
    while z >= 0x80:
        out.append((z & 0x7F) | 0x80)
        z >>= 7
    out.append(z)
    return bytes(out)

async def uleb_encode(n):
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            b |= 0x80
        out.append(b)
        if not n:
            break
    return bytes(out)

async def tea_enc(v0, v1, k0, k1, k2, k3):
    s = 0
    for _ in range(_ROUNDS):
        s = (s + _DELTA) & 0xFFFFFFFF
        v0 = (v0 + (((((v1 << 4) & 0xFFFFFFFF) + k0) & 0xFFFFFFFF ^
                      ((v1 + s) & 0xFFFFFFFF) ^
                      (((v1 >> 5) + k1) & 0xFFFFFFFF)))) & 0xFFFFFFFF
        v1 = (v1 + (((((v0 << 4) & 0xFFFFFFFF) + k2) & 0xFFFFFFFF ^
                      ((v0 + s) & 0xFFFFFFFF) ^
                      (((v0 >> 5) + k3) & 0xFFFFFFFF)))) & 0xFFFFFFFF
    return v0, v1

async def tea_dec(v0, v1, k0, k1, k2, k3):
    s = (_DELTA * _ROUNDS) & 0xFFFFFFFF
    for _ in range(_ROUNDS):
        v1 = (v1 - (((((v0 << 4) & 0xFFFFFFFF) + k2) & 0xFFFFFFFF ^
                      ((v0 + s) & 0xFFFFFFFF) ^
                      (((v0 >> 5) + k3) & 0xFFFFFFFF)))) & 0xFFFFFFFF
        v0 = (v0 - (((((v1 << 4) & 0xFFFFFFFF) + k0) & 0xFFFFFFFF ^
                      ((v1 + s) & 0xFFFFFFFF) ^
                      (((v1 >> 5) + k1) & 0xFFFFFFFF)))) & 0xFFFFFFFF
        s = (s - _DELTA) & 0xFFFFFFFF
    return v0, v1

async def tea_cbc_encrypt(padded, key_bytes):
    k0, k1, k2, k3 = (struct.unpack_from("<I", key_bytes, o)[0] for o in (0, 4, 8, 12))
    out = bytearray(len(padded))
    prev_cipher = bytearray(8)
    prev_intermediate = bytearray(8)
    for i in range(0, len(padded), 8):
        xored = bytearray(8)
        for j in range(8):
            xored[j] = padded[i + j] ^ prev_cipher[j]
        e0, e1 = await tea_enc(
            struct.unpack_from("<I", xored, 0)[0],
            struct.unpack_from("<I", xored, 4)[0],
            k0, k1, k2, k3,
        )
        enc = bytearray(8)
        struct.pack_into("<I", enc, 0, e0)
        struct.pack_into("<I", enc, 4, e1)
        for j in range(8):
            out[i + j] = enc[j] ^ prev_intermediate[j]
        prev_cipher[:] = out[i:i + 8]
        prev_intermediate[:] = xored
    return bytes(out)

async def build_padded(content):
    pad_len = (8 - (len(content) + 10) % 8) % 8
    return bytes([pad_len, 0, 0]) + b"\x00" * pad_len + content + b"\x00" * 7

async def encode_header(layout, send_option, cmd, order_id, flags, length, k, v80):
    out = bytearray()
    for code in layout:
        value = {0: send_option, 1: cmd, 2: order_id, 3: flags, 4: length}[code]
        if _FIELD_SIZES[code] == 1:
            out.append((value & 0xFF) ^ k)
        else:
            v = ((value & 0xFFFF) ^ v80) & 0xFFFF
            out.append(v & 0xFF)
            out.append((v >> 8) & 0xFF)
    return bytes(out)

async def crc7_buff(crc, buf):
    c = crc & 0x7F
    for b in buf:
        c = CRC7_TABLE[((2 * (c & 0xFF)) ^ (b & 0xFF)) & 0xFF] & 0x7F
    return c & 0x7F

async def sv_frame(msg_key, layout, send_option, cmd, order_id, flags, content, key, encrypted=True):
    k = key[0]
    v80 = ((k << 8) | k) & 0xFFFF
    body = await tea_cbc_encrypt(await build_padded(content), key) if encrypted else content
    hdr = bytearray([msg_key, 0]) + await encode_header(layout, send_option, cmd, order_id, flags, len(body), k, v80)
    packet = bytearray(hdr + body)
    packet[1] = await crc7_buff(0, bytes(packet[2:])) & 0x7F
    return bytes(packet)

async def build_match_startup_packets(token, udp_key, match_code, account_id, block_val,
                                      server_ip="", region="BD", client_version="1.132.6",
                                      client_version_code="2019121229", access_token="",
                                      mode="LONE_WOLF"):
    token = token.strip()
    udp_key = bytes.fromhex(udp_key)
    match_code = [int(ch) for ch in str(match_code).strip()]
    
    # OB55 splits JWT match token at 660 bytes
    thunder_jwt = token[:660] if len(token) > 660 else token
    sharma_jwt = token[660:] if len(token) > 660 else ""
    encoded_thunder_jwt = thunder_jwt.encode() if isinstance(thunder_jwt, str) else thunder_jwt
    encoded_sharma_jwt = sharma_jwt.encode() if isinstance(sharma_jwt, str) else sharma_jwt
    
    garena420 = await has_ssan_zig(len(encoded_thunder_jwt)) + encoded_thunder_jwt
    
    # OB55 Sharma payload structure matching Wireshark capture
    reg = str(region).upper() if region else "BD"
    # Mode-dependent Sharma payload (BR-UDP reference theke): BR ar LW-er UDP join packet alada
    if str(mode).upper() == "BR":
        csoversea_block = bytes.fromhex(
            "ca0163736f7665727365612e7374726f6e67686f6c642e66726565666972656d6f62696c652e636f6d"
            "3b302e302e302e303b33342e3132362e37362e34353b33342e38372e3137372e31343b33342e38372e"
            "3137302e3233303b33352e3138352e3138332e35370000000000000100000000000000000000000001"
            "00000000000100010000000100b09df8c5fad88bdf110200"
        )
        m_val1, m_val2 = 1, 1
    else:
        csoversea_block = bytes.fromhex(
            "ca0163736f7665727365612e7374726f6e67686f6c642e66726565666972656d6f62696c652e636f6d"
            "3b302e302e302e303b33342e3132362e37362e34353b33342e38372e3137372e31343b33342e38372e"
            "3137302e3233303b33352e3138352e3138332e35370000000000000100000000000000000000000001"
            "00000800000100000000000100a8a2d7bebd8d8bdf110200"
        )
        m_val1, m_val2 = 43, 11

    mid = bytes.fromhex('0000000001000102030101') + await has_ssan_zig(len(reg)) + reg.encode()
    mid += bytes.fromhex('0001030003000004')
    mid += await has_ssan_zig(len(client_version)) + client_version.encode()
    mid += await has_ssan_zig(len(client_version_code)) + client_version_code.encode()
    mid += csoversea_block
    
    clean_ip = server_ip.split(':')[0] if server_ip else "0.0.0.0"
    mid += await has_ssan_zig(len(clean_ip)) + clean_ip.encode()
    
    clean_acc_tok = access_token.strip() if access_token else ""
    if clean_acc_tok:
        mid += await has_ssan_zig(len(clean_acc_tok)) + clean_acc_tok.encode()
        
    mid += await has_ssan_zig(len(encoded_sharma_jwt)) + encoded_sharma_jwt
    
    tg_garena420 = (
        await uleb_encode(int(account_id)) +
        await uleb_encode(int(block_val)) +
        await uleb_encode(1) +
        await uleb_encode(m_val1) +
        await uleb_encode(int(block_val)) +
        await uleb_encode(m_val2) +
        mid
    )
    
    process = await sv_frame(0x5E, match_code, 2, 447, 0, 1, garena420, udp_key)
    loading = await sv_frame(0x5A, match_code, 2, 448, 1, 1, tg_garena420, udp_key)
    return process.hex(), loading.hex()

async def produce_xor_key(secret_key):
    k = secret_key[0] if secret_key and len(secret_key) > 0 else 10
    return k, ((k << 8) | k) & 0xFFFF

async def parse_layout(layout):
    if isinstance(layout, str):
        return [int(ch) for ch in layout.strip()]
    return list(layout)

async def tea_cbc_decrypt(body, key_bytes):
    k0, k1, k2, k3 = (struct.unpack_from("<I", key_bytes, o)[0] for o in (0, 4, 8, 12))
    out = bytearray(len(body))
    prev_intermediate = bytearray(8)
    prev_cipher = bytearray(8)
    xored = bytearray(8)
    dec = bytearray(8)
    for i in range(0, len(body), 8):
        for j in range(8):
            xored[j] = body[i + j] ^ prev_intermediate[j]
        d0, d1 = await tea_dec(
            struct.unpack_from("<I", xored, 0)[0],
            struct.unpack_from("<I", xored, 4)[0],
            k0, k1, k2, k3
        )
        struct.pack_into("<I", dec, 0, d0)
        struct.pack_into("<I", dec, 4, d1)
        for j in range(8):
            out[i + j] = dec[j] ^ prev_cipher[j]
        prev_cipher[:] = body[i:i + 8]
        prev_intermediate[:] = dec
    return bytes(out)

async def build_hello_packet(text, key, layout):
    data = text.encode("utf-8")
    if len(data) > 25:
        raise ValueError(f"Text is too long ({len(data)} bytes)")
    content = b"\x10\x00\x00\x00" + data + b"\x00" * (29 - 4 - len(data))
    k, v80 = await produce_xor_key(key)
    layout = await parse_layout(layout)
    padded = await build_padded(content)
    enc_body = await tea_cbc_encrypt(padded, key)
    header_bytes = await encode_header(layout, 1, 1, 0, 1, len(enc_body), k, v80)
    packet = bytearray([0x63, 0x00]) + header_bytes + enc_body
    packet[1] = await crc7_buff(0, packet[2:]) & 0x7F
    return bytes(packet).hex()

async def classify(frame):
    cmd = frame["cmd"]
    msg_name = MESSAGE_ID_TO_NAME.get(cmd, f"UNKNOWN_{cmd}")
    if msg_name == "UDP_HELLO":
        return "HELLO"
    if msg_name == "UDP_ACK":
        return "ACK"
    if msg_name == "UDP_PING":
        return "PING"
    if msg_name == "RUDP_JOIN_MATCH":
        return "JOIN_MATCH"
    if msg_name.startswith("RUDP_"):
        return msg_name
    if msg_name.startswith("UDP_"):
        return msg_name
    return "DATA"

async def build_packet(msg_key, layout, send_option, cmd, order_id, flags, content, key, encrypted=True):
    k = key[0]
    v80 = ((k << 8) | k) & 0xFFFF
    body = await tea_cbc_encrypt(await build_padded(content), key) if encrypted else content
    hdr = bytearray([msg_key, 0])
    for code in layout:
        value = {0: send_option, 1: cmd, 2: order_id, 3: flags, 4: len(body)}[code]
        if _FIELD_SIZES[code] == 1:
            hdr.append((value & 0xFF) ^ k)
        else:
            v = ((value & 0xFFFF) ^ v80) & 0xFFFF
            hdr.append(v & 0xFF)
            hdr.append((v >> 8) & 0xFF)
    packet = bytearray(hdr + body)
    packet[1] = await crc7_buff(0, bytes(packet[2:])) & 0x7F
    return bytes(packet)

async def layouts_from_mask(mask):
    ru = [int(c) for c in str(mask).strip()]
    nr = [c for c in ru if c != 2]
    return ru, nr

async def reply_for(frame, key, mask, ack_key=0x68, ping_key=0x6D, hello_key=0x5B, ack_style="short"):
    ru, nr = await layouts_from_mask(mask)
    typ = await classify(frame)
    if typ == "HELLO":
        if ack_style == "echo":
            content = frame["content"] if frame["content"] else b"\x10\x00\x00\x00"
            return typ, await build_packet(hello_key, nr, 1, 1, None, 1, content, key)
        return typ, await build_packet(ack_key, nr, 0, 2, None, 1, b"\x01\x00", key)
    if typ == "ACK":
        content = frame["content"] if frame["content"] else b"\x01\x00"
        return typ, await build_packet(ack_key, nr, 0, 2, None, 1, content, key)
    if typ == "PING":
        c = frame["content"]
        counter = c[:4] if len(c) >= 4 else c
        return typ, await build_packet(ping_key, nr, 0, 3, None, 0, counter + b"\x00\x00\x00", key, encrypted=False)
    if typ == "JOIN_MATCH":
        return typ, await build_packet(ack_key, nr, 0, 2, None, 1, b"\x02\x00", key)
    return typ, None

async def keepalive_ping(sock, ip, port, key_bytes, mask, stop_event):
    nr = (await layouts_from_mask(mask))[1]
    ping_keys = [0x66, 0x6D, 0x69, 0x6C, 0x6B, 0x6E, 0x6F, 0x70]
    i = 0
    while not stop_event.is_set():
        pk = ping_keys[i % len(ping_keys)]
        counter = int(time.time() * 1000) & 0xFFFFFFFF
        pkt = await build_packet(pk, nr, 0, 3, None, 0,
                                  struct.pack("<I", counter) + b"\x00\x00\x00",
                                  key_bytes, encrypted=False)
        try:
            await udp_sendto(sock, pkt, (ip, port))
        except Exception:
            pass
        i += 1
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=3.0)
        except asyncio.TimeoutError:
            pass

async def try_header(buf, layout, k, v80):
    off = 2
    out = {}
    for code in layout:
        size = _FIELD_SIZES[code]
        if off + size > len(buf):
            return None
        out[_FIELD_NAMES[code]] = (buf[off] ^ k) if size == 1 else ((buf[off] | (buf[off + 1] << 8)) ^ v80) & 0xFFFF
        off += size
    out["headerLen"] = off
    return out

async def oicq_unpad(padded):
    if not padded or len(padded) < 8:
        return None
    if not all(padded[-1 - i] == 0 for i in range(7)):
        return None
    pad_len = padded[0] & 0x07
    s = 3 + pad_len
    e = len(padded) - 7
    return padded[s:e] if s < e else b""

async def decode_packet(packet, key, mask=None):
    data = bytes(packet) if isinstance(packet, bytes) else bytes.fromhex(packet)
    if len(data) < 8:
        return None
    k = key[0]
    v80 = ((k << 8) | k) & 0xFFFF
    crc_ok = (data[1] & 0x7F) == await crc7_buff(0, data[2:])
    candidates = []
    if mask:
        ru, nr = await layouts_from_mask(mask)
        layouts = [("RUDP", ru), ("nonRUDP", nr)]
    else:
        layouts = [("RUDP", list(p)) for p in itertools.permutations([0, 1, 2, 3, 4])]
        layouts += [("nonRUDP", list(p)) for p in itertools.permutations([0, 1, 3, 4])]
    for kind, layout in layouts:
        f = await try_header(data, layout, k, v80)
        if not f:
            continue
        if f["flags"] > 7 or f["sendOption"] > 7:
            continue
        if f["length"] != len(data) - f["headerLen"]:
            continue
        body = data[f["headerLen"]:f["headerLen"] + f["length"]]
        content = None
        padded = None
        if f["flags"] & 1:
            if len(body) < 8 or len(body) % 8 != 0:
                continue
            padded = await tea_cbc_decrypt(body, key)
            content = await oicq_unpad(padded)
            if content is None:
                continue
        else:
            content = body
        score = (1 if crc_ok else 0) + (1 if content is not None else 0)
        candidates.append({
            "kind": kind, "layout": layout, "headerLen": f["headerLen"],
            "msgKey": data[0], "cmd": f["cmd"], "flags": f["flags"],
            "sendOption": f["sendOption"], "orderId": f.get("orderId"),
            "length": f["length"], "content": content, "crcOk": crc_ok,
            "padded": padded, "score": score, "total": len(data),
        })
    if not candidates:
        return None
    candidates.sort(key=lambda c: (c["kind"] == "RUDP" or c["kind"] == "nonRUDP", c["score"]), reverse=True)
    return candidates[0]



async def udp_sendto(sock, data, addr):
    """Windows compatible UDP send"""
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, sock.sendto, data, addr)

async def udp_recvfrom(sock, size=65535):
    """Windows compatible UDP recv"""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, sock.recvfrom, size)


# ============================================================
# 🎮 ANTI-AFK (BR-UDP theke) — sudhu BR match-e; BR_ANTI_AFK=0 dile bondho
# ============================================================
BR_ANTI_AFK = os.environ.get("BR_ANTI_AFK", "1") != "0"
# BR match-e dhukle SESH porjonto thakte hobe: majh pothe cheye dile server account-ke "match-e ache" dhore
# ar notun BR search-e queue ack dey kintu kokhono match dey na. Tai lomba duration + lomba idle timeout.
BR_MATCH_DURATION = float(os.environ.get("BR_MATCH_DURATION", "700"))    # prothom file-er moto
BR_IDLE_TIMEOUT = float(os.environ.get("BR_IDLE_TIMEOUT", "25"))          # ✅ FIX: 8→25s, BR-e server onek sময় quiet thake
BR_HOLD_MATCH = os.environ.get("BR_HOLD_MATCH", "0") == "1"             # 1 dile BR match shesh na hoa porjonto notun search hobe na
LAST_MATCH_NOTE: Dict[str, str] = {}   # dashboard card-e last match-er summary dekhanor jonno

async def anti_afk_worker(sock, resolved_ip, port, udp_key_bytes, match_code,
                          account_id, stop_event, match_index):
    server_addr = (resolved_ip, port)
    fires = moves = 0
    try:
        nr = (await layouts_from_mask(match_code))[1]
        try:
            pid = int(account_id) & 0xFFFFFFFF
        except Exception:
            pid = 0
        await asyncio.sleep(2.5)
        while not stop_event.is_set():
            try:
                ts = int(time.time() * 1000) & 0xFFFFFFFF
                if random.random() < 0.5:
                    wid = random.choice([101, 102, 103, 201, 202])
                    pkt = await build_packet(0x68, nr, 0, 104, None, 0,
                                             struct.pack("<IIHB", pid, ts, wid, 1), udp_key_bytes, encrypted=False)
                    await udp_sendto(sock, pkt, server_addr)
                    await asyncio.sleep(random.uniform(0.15, 0.30))
                    pkt = await build_packet(0x68, nr, 0, 105, None, 0,
                                             struct.pack("<IIHB", pid, ts + 200, wid, 0), udp_key_bytes, encrypted=False)
                    await udp_sendto(sock, pkt, server_addr)
                    fires += 1
                else:
                    body = struct.pack("<IIiiiH", pid, ts, random.randint(-100, 100),
                                       random.randint(-50, 50), random.randint(-100, 100), 1)
                    pkt = await build_packet(0x6B, nr, 0, 2001, None, 0, body, udp_key_bytes, encrypted=False)
                    await udp_sendto(sock, pkt, server_addr)
                    moves += 1
                try:
                    await asyncio.wait_for(stop_event.wait(), timeout=random.uniform(2.5, 4.5))
                    break
                except asyncio.TimeoutError:
                    pass
            except asyncio.CancelledError:
                break
            except Exception:
                await asyncio.sleep(1.0)
    except asyncio.CancelledError:
        pass
    finally:
        if fires + moves:
            print_info(f"[🎮] Anti-AFK #{match_index} | Fires: {fires} | Moves: {moves}")

# ============================================================
# play_game — UDP MATCH (FIXED & DNS OPTIMIZED)
# ============================================================
async def play_game(server_ip_port, thunder, sharma, udp_key, match_code,
                    account_id, player_region, client_version, key, iv,
                    match_index: int, dash_uid: str = None, mode: str = "LONE_WOLF"):
    match_start_time = time.time()
    is_br_match = (str(mode).upper() == "BR")
    afk_task = None
    ping_task = None
    sock = None
    ping_stop = asyncio.Event()
    # bookkeeping (dashboard/match counter) always dashboard-er key diye; protocol-e account_id
    uid_str = str(dash_uid or account_id)
    completed_cleanly = False
    dbg = {"pkts": 0, "undecoded": 0, "cmds": {}, "state": "start", "err": "", "reason": "", "last_report": 0.0}

    def _info(msg: str):
        try:
            bot_state.set_info(uid_str, f"Match #{match_index}: {msg}")
        except Exception:
            pass

    def _report(force: bool = False):
        now_t = time.time()
        if not force and now_t - dbg["last_report"] < 4.0:
            return
        dbg["last_report"] = now_t
        cmds = ",".join(f"{k}x{v}" for k, v in list(dbg["cmds"].items())[:8])
        _info(f"state={dbg['state']} pkts={dbg['pkts']} undecoded={dbg['undecoded']} cmds=[{cmds}] t={int(now_t - match_start_time)}s" + (f" err={dbg['err']}" if dbg["err"] else ""))

    try:
        ip, port = server_ip_port.split(":")
        port = int(port)
        resolved_ip = await resolve_host_cloudflare(ip)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        optimize_udp_socket(sock)
        sock.settimeout(2.0)  # blocking timeout for run_in_executor

        udp_key_bytes = bytes.fromhex(udp_key)
        hello_packet = await build_hello_packet(
            f"{account_id}_2585", udp_key_bytes, match_code
        )
        await udp_sendto(sock, bytes.fromhex(hello_packet), (resolved_ip, port))

        ack_state = "waiting_for_hello_reply"
        thunder_sent = False
        sharma_sent = False
        join_match_received = False
        local_closed = False
        send_lock = asyncio.Lock()

        ping_task = asyncio.create_task(
            keepalive_ping(sock, resolved_ip, port, udp_key_bytes, match_code, ping_stop)
        )
        if is_br_match and BR_ANTI_AFK:
            afk_task = asyncio.create_task(
                anti_afk_worker(sock, resolved_ip, port, udp_key_bytes, match_code,
                                account_id, ping_stop, match_index)
            )
        last_activity = time.time()
        MAX_IDLE_BEFORE_HELLO_RESEND = 7.0

        print_colored(
            f"[MATCH #{match_index}] UDP started -> {server_ip_port} (DNS: {resolved_ip})",
            Colors.MAGENTA
        )

        async def send_thunder_sharma_inline():
            nonlocal ack_state, thunder_sent, sharma_sent
            if thunder_sent:
                return
            async with send_lock:
                if thunder_sent:
                    return
                try:
                    await udp_sendto(sock, bytes.fromhex(thunder), (resolved_ip, port))
                    thunder_sent = True
                    await asyncio.sleep(0.1)
                    prepare_ack = await build_packet(
                        0x68, (await layouts_from_mask(match_code))[1],
                        0, 2, None, 1, b"\x01\x00", udp_key_bytes
                    )
                    await udp_sendto(sock, prepare_ack, (resolved_ip, port))
                    await asyncio.sleep(0.2)
                    await udp_sendto(sock, bytes.fromhex(sharma), (resolved_ip, port))
                    sharma_sent = True
                    ack_state = "thunder_sharma_sent"
                    dbg["thunder_t"] = time.time()
                    bot_state.log(f"[MATCH #{match_index}] Thunder+Sharma sent!", "success")
                except Exception as e:
                    print_error(f"[MATCH #{match_index}] send error: {e}")

        _info("UDP hello pathano hoyeche, server reply-er opekkha")
        while not local_closed:
            dbg["state"] = ack_state
            _report()
            if time.time() - match_start_time > (BR_MATCH_DURATION if is_br_match else MAX_MATCH_DURATION):
                dbg["reason"] = "max duration"
                if is_br_match and dbg.get("thunder_t"):
                    completed_cleanly = True
                break
            # ✅ FIX: BR-তে quick_finish বন্ধ — EXP পেতে death/end packet (cmd 103/107) পর্যন্ত অপেক্ষা করতে হবে।
            # LW-এ ১৫s পরে server EXP দেয়, কিন্তু BR-এ ১৫s-এ disconnect করলে EXP আসে না।
            if (not is_br_match and QUICK_FINISH_SECONDS > 0 and dbg.get("thunder_t")
                    and time.time() - dbg["thunder_t"] >= QUICK_FINISH_SECONDS):
                dbg["reason"] = f"quick finish ({int(QUICK_FINISH_SECONDS)}s after thunder)"
                bot_state.log(f"[MATCH #{match_index}] Quick finish after {int(QUICK_FINISH_SECONDS)}s", "success")
                completed_cleanly = True
                break
            try:
                response, server_addr = await asyncio.wait_for(
                    udp_recvfrom(sock, 65535), timeout=1.5
                )
                if response:
                    last_activity = time.time()
                    dbg["pkts"] += 1
                    frame = await decode_packet(response, udp_key_bytes, match_code)
                    if not frame:
                        dbg["undecoded"] += 1
                    if frame:
                        dbg["cmds"][frame['cmd']] = dbg["cmds"].get(frame['cmd'], 0) + 1
                        ptype = await classify(frame)

                        if frame['cmd'] in [103, 107]:
                            bot_state.log(f"[MATCH #{match_index}] Completed (cmd {frame['cmd']})", "success")
                            dbg["reason"] = f"Completed (cmd {frame['cmd']})"
                            completed_cleanly = True
                            local_closed = True
                            continue

                        if frame['cmd'] == 101:
                            try:
                                ack_pkt = await build_packet(
                                    0x68, (await layouts_from_mask(match_code))[1],
                                    0, 2, None, 1, b"\x01\x00", udp_key_bytes
                                )
                                await udp_sendto(sock, ack_pkt, server_addr)
                            except Exception:
                                pass
                            continue

                        if ptype in ["ACK", "PING", "HELLO", "JOIN_MATCH"]:
                            if ptype == "HELLO" and ack_state == "waiting_for_hello_reply":
                                typ, reply = await reply_for(
                                    frame, udp_key_bytes, match_code, ack_style="short"
                                )
                                if reply:
                                    await udp_sendto(sock, reply, server_addr)
                                ack_state = "ack_sent_waiting"
                            elif ptype == "ACK":
                                if ack_state in ("waiting_for_hello_reply", "ack_sent_waiting"):
                                    typ, reply = await reply_for(frame, udp_key_bytes, match_code)
                                    if reply:
                                        await udp_sendto(sock, reply, server_addr)
                                    ack_state = "ready_to_send_thunder"
                                else:
                                    typ, reply = await reply_for(frame, udp_key_bytes, match_code)
                                    if reply:
                                        await udp_sendto(sock, reply, server_addr)
                            elif ptype == "PING":
                                typ, reply = await reply_for(frame, udp_key_bytes, match_code)
                                if reply:
                                    await udp_sendto(sock, reply, server_addr)
                            elif ptype == "JOIN_MATCH" and not join_match_received:
                                typ, reply = await reply_for(frame, udp_key_bytes, match_code)
                                if reply:
                                    await udp_sendto(sock, reply, server_addr)
                                    join_match_received = True

            except asyncio.TimeoutError:
                if ack_state == "ready_to_send_thunder" and not thunder_sent:
                    await send_thunder_sharma_inline()
                elif ack_state == "waiting_for_hello_reply":
                    if (time.time() - last_activity) > MAX_IDLE_BEFORE_HELLO_RESEND:
                        try:
                            pkt = await build_hello_packet(
                                f"{account_id}_2585", udp_key_bytes, match_code
                            )
                            await udp_sendto(sock, bytes.fromhex(pkt), (resolved_ip, port))
                        except Exception:
                            pass
                        last_activity = time.time()
                    if (time.time() - match_start_time) > 25.0:
                        bot_state.log(f"[MATCH #{match_index}] Handshake timeout", "warning")
                        dbg["reason"] = "Handshake timeout (server reply pai ni)"
                        break
                elif ack_state == "thunder_sharma_sent":
                    if (time.time() - last_activity) > (BR_IDLE_TIMEOUT if is_br_match else MATCH_IDLE_TIMEOUT):
                        bot_state.log(f"[MATCH #{match_index}] Finished naturally", "success")
                        dbg["reason"] = "Finished naturally (idle)"
                        completed_cleanly = True
                        break
                continue
            except Exception as _e:
                dbg["err"] = repr(_e)[:80]
                await asyncio.sleep(0.2)
                continue

            if ack_state == "ready_to_send_thunder" and not thunder_sent:
                await send_thunder_sharma_inline()

        return f"match #{match_index} finished"

    except Exception as e:
        print_error(f"[MATCH #{match_index}] error: {e}")
        dbg["reason"] = f"exception: {repr(e)[:100]}"
        return f"match #{match_index} error"
    finally:
        _note = (f"{'BR' if is_br_match else 'LW'} #{match_index} {dbg['reason'] or 'cancelled'} "
                 f"| {int(time.time() - match_start_time)}s pkts={dbg['pkts']} undec={dbg['undecoded']} "
                 f"cmds={dict(list(dbg['cmds'].items())[:6])} ok={completed_cleanly}")
        LAST_MATCH_NOTE[uid_str] = _note
        _info(f"SESH - {dbg['reason'] or 'cancelled'} | pkts={dbg['pkts']} undecoded={dbg['undecoded']} cmds={dict(list(dbg['cmds'].items())[:8])} clean={completed_cleanly}")
        bot_state.log(f"[MATCH #{match_index}] SESH → {_note}", "info", uid_str)
        if completed_cleanly:
            try:
                bot_state.increment_match(uid_str)
            except Exception:
                pass

            async def _refresh_exp_later():
                try:
                    await asyncio.sleep(6)
                    await refresh_account_profile(uid_str)
                    if is_br_match:
                        # ✅ FIX: BR-e EXP settlement deri hoy — 30s + 90s por refresh
                        await asyncio.sleep(30)
                        await refresh_account_profile(uid_str)
                        await asyncio.sleep(90)
                        await refresh_account_profile(uid_str)
                except Exception:
                    pass
            try:
                asyncio.create_task(_refresh_exp_later())
            except Exception:
                pass
        ping_stop.set()
        if afk_task:
            afk_task.cancel()
            try:
                await afk_task
            except (asyncio.CancelledError, Exception):
                pass
        if ping_task:
            ping_task.cancel()
            try:
                await ping_task
            except asyncio.CancelledError:
                pass
        if sock:
            try:
                sock.close()
            except Exception:
                pass
        remaining = await _dec_match(uid_str)
        total = await _get_total_match_count()
        bot_state.log(f"[MATCH #{match_index}] Closed. UID active: {remaining} | Total active: {total}", "info")
        try:
            bot_state.update_status(uid_str, "IN_MATCH" if remaining > 0 else "ONLINE", remaining)
        except Exception:
            pass


# ============================================================
# 🔥 functional_lone_wolf — TRUE Parallel + Smart Cache + DNS
# ============================================================
async def functional_lone_wolf(addrs, starter_packet, account_region, client_version,
                                key, iv, account_id="", account_data=None,
                                max_reconnects=10):
    reconnects = 0
    ip, port = addrs.split(":")
    play_matches: List[asyncio.Task] = []
    no_response_count = 0
    search_attempts = 0
    last_start_time = 0.0
    uid_str = str(account_id)

    consecutive_parse_failures = 0

    current_token = starter_packet
    current_key = key
    current_iv = iv
    current_account_data = account_data
    last_sent_type = None
    last_ka_time = 0.0
    gw = {"pkts": 0, "queue": 0, "big": 0, "last": "-"}

    try:
        while True:
            writer = None

            # BR: match cholche thakle notun search pathabo na (server account-ke "match-e ache" dhore).
            # Match shesh hole (dead / match end / timeout) tarpor-i notun search.
            while BR_HOLD_MATCH and bot_state.get_match_type(uid_str) == "BR":
                play_matches[:] = [m for m in play_matches if not m.done()]
                if not play_matches:
                    break
                try:
                    bot_state.update_status(uid_str, "IN_MATCH", len(play_matches))
                except Exception:
                    pass
                await asyncio.sleep(1.0)

            try:
                if current_account_data:
                    fresh = None
                    if current_account_data.get('auth_type') == 'guest' and current_account_data.get('auth_uid'):
                        fresh = cache_get(str(current_account_data['auth_uid']))
                    elif current_account_data.get('auth_type') == 'token' and current_account_data.get('auth_token'):
                        fresh = cache_get(f"tok_{current_account_data['auth_token'][:20]}")

                    if fresh:
                        current_account_data = fresh
                        current_key = fresh['aes_ak']
                        current_iv = fresh['iv_i']
                        current_token = await build_tcp_startup_packet(
                            fresh['account_id'],
                            fresh['token'],
                            fresh['server_time'],
                            current_key,
                            current_iv,
                            region=fresh.get('region', account_region),
                            typ='OnLine'
                        )
                    else:
                        print_warning(f"[FUNCTIONAL] Cache miss for {uid_str} → re-login needed")
                        try:
                            if current_account_data.get('auth_uid'):
                                cache_invalidate(str(current_account_data['auth_uid']))
                            if current_account_data.get('auth_token'):
                                cache_invalidate(f"tok_{current_account_data['auth_token'][:20]}")
                        except Exception:
                            pass
                        raise ConnectionError("Cache expired, triggering fresh login")

                resolved_ip = await resolve_host_cloudflare(ip)
                reader, writer = await asyncio.open_connection(resolved_ip, int(port))
                
                raw_sock = writer.get_extra_info('socket')
                if raw_sock:
                    optimize_tcp_socket(raw_sock)
                
                writer.write(bytes.fromhex(current_token))
                await writer.drain()

                # Send initial keepalive pulse right after connecting in OB55
                try:
                    init_ka = await send_keep_alive(account_region)
                    if init_ka and writer and not writer.is_closing():
                        writer.write(init_ka)
                        await asyncio.wait_for(writer.drain(), timeout=3)
                except Exception:
                    pass

                bot_state.log(f"[FUNCTIONAL] TCP Gateway Connected for UID: {uid_str} (DNS: {resolved_ip})", "success")
                reconnects = 0
                no_response_count = 0
                last_start_time = 0.0
                last_sent_type = None
                last_ka_time = 0.0

                async def send_start_match():
                    nonlocal search_attempts, last_start_time, last_sent_type
                    # ✅ Global OFF হলে match search করবে না
                    if not bot_state.global_running:
                        last_start_time = asyncio.get_running_loop().time()
                        return
                    search_attempts += 1
                    current_region = "BD"
                    # ✅ Dashboard থেকে সিলেক্ট করা match type পড়া হচ্ছে
                    selected_type = bot_state.get_match_type(uid_str)
                    last_sent_type = selected_type
                    try:
                        # ✅ FIX: Pre-search delay কমানো হয়েছে (2-6s → 1-3s)
                        # Speed বাড়ানোর জন্য, তবু human-like থাকবে (ban-safe)
                        human_delay = random.uniform(1.0, 3.0)
                        await asyncio.sleep(human_delay)
                        if selected_type == "BR":
                            bot_state.log(f"[⚔] BR Match Search #{search_attempts} | UID: {uid_str} | Region: {current_region}", "info")
                            await start_game_battle_royale(
                                current_region, client_version, writer,
                                current_key, current_iv
                            )
                            try:
                                bot_state.set_info(uid_str, f"BR Match Search #{search_attempts} — waiting for match... (gw pkts={gw['pkts']} queue={gw['queue']} big={gw['big']} last={gw['last']})" + (f" || LAST: {LAST_MATCH_NOTE[uid_str]}" if uid_str in LAST_MATCH_NOTE else ""))
                            except Exception:
                                pass
                        else:
                            bot_state.log(f"[🐺] Lone Wolf Search #{search_attempts} | UID: {uid_str} | Region: {current_region}", "info")
                            await start_game_lone_wolf(
                                current_region, client_version, writer,
                                current_key, current_iv
                            )
                            try:
                                bot_state.set_info(uid_str, f"Lone Wolf Search #{search_attempts} — waiting for match...")
                            except Exception:
                                pass
                        active = await _get_match_count(uid_str)
                        try:
                            bot_state.update_status(uid_str, f"SEARCHING ({selected_type})", active)
                        except Exception:
                            pass
                    except Exception as e:
                        print_error(f"send_start_match error ({selected_type}): {e}")
                    last_start_time = asyncio.get_running_loop().time()

                await send_start_match()

                while True:
                    play_matches[:] = [m for m in play_matches if not m.done()]

                    active_count = await _get_match_count(uid_str)

                    # ✅ Global OFF → PAUSED; ON → normal status
                    if not bot_state.global_running:
                        try:
                            bot_state.update_status(uid_str, "PAUSED", active_count)
                        except Exception:
                            pass
                        await asyncio.sleep(1.0)
                        last_start_time = asyncio.get_running_loop().time()
                        last_sent_type = None  # force re-search when resumed
                        continue

                    try:
                        bot_state.update_status(
                            uid_str,
                            "ONLINE" if active_count == 0 else "IN_MATCH",
                            active_count
                        )
                    except Exception:
                        pass

                    now = asyncio.get_running_loop().time()
                    cur_type = bot_state.get_match_type(uid_str)
                    is_br = (cur_type == "BR")
                    if is_br and BR_HOLD_MATCH and any(not m.done() for m in play_matches):
                        # BR match cholche — search bondho, sudhu connection dhore rakho
                        await asyncio.sleep(0.5)
                        continue
                    if cur_type != last_sent_type:
                        # Dashboard theke mode change hole sathe sathe notun search
                        last_sent_type = cur_type
                        await send_start_match()
                    elif now - last_start_time >= (BR_START_MATCH_INTERVAL if is_br else START_MATCH_INTERVAL):
                        await send_start_match()
                        if is_br and BR_DOUBLE_SEARCH:
                            await asyncio.sleep(0.5)
                            await send_start_match()

                    # ✅ FIX: BR + LW উভয়তেই keepalive — LW connection drop ঠিক করে
                    # LW-এ keepalive না থাকলে server 30-40s পর connection বন্ধ করে দেয়
                    LW_KEEPALIVE_INTERVAL = 8.0  # LW-এ 8s পর পর keepalive
                    ka_interval = BR_KEEPALIVE_INTERVAL if is_br else LW_KEEPALIVE_INTERVAL
                    if now - last_ka_time >= ka_interval:
                        last_ka_time = now
                        try:
                            ka = await send_keep_alive(account_region)
                            if ka and writer and not writer.is_closing():
                                writer.write(ka)
                                await asyncio.wait_for(writer.drain(), timeout=3)
                        except Exception:
                            pass

                    try:
                        data = await asyncio.wait_for(reader.read(8192), timeout=0.5)
                    except asyncio.TimeoutError:
                        no_response_count += 1
                        # ✅ FIX: LW idle limit 80→240 (0.5s×240=120s), BR আগের মতো 300
                        # আগে ছিল 40s-এ reconnect, এখন 120s পর্যন্ত অপেক্ষা করবে
                        LW_IDLE_LIMIT = 240
                        if no_response_count > (BR_IDLE_LIMIT if is_br else LW_IDLE_LIMIT):
                            bot_state.log(f"[FUNCTIONAL] Gateway silent ({uid_str}). Reconnecting...", "warning")
                            raise ConnectionError("Gateway idle timeout")
                        continue

                    if not data:
                        raise ConnectionError("Connection closed by server")

                    hex_data = data.hex()
                    packet_length = len(data)
                    no_response_count = 0

                    gw["pkts"] += 1
                    gw["last"] = f"{packet_length}B/{hex_data[:8]}"
                    if is_br:
                        if hex_data.startswith("0300") and 10 < packet_length < 30:
                            gw["queue"] += 1
                        elif packet_length >= 300:
                            gw["big"] += 1
                        bot_state.log(f"[BR-DEBUG] gateway pkt len={packet_length} head={hex_data[:24]}", "info", uid_str)
                        try:
                            bot_state.set_info(uid_str, f"BR Search #{search_attempts} | gw pkts={gw['pkts']} queue={gw['queue']} big={gw['big']} last={gw['last']}" + (f" || LAST: {LAST_MATCH_NOTE[uid_str]}" if uid_str in LAST_MATCH_NOTE else ""))
                        except Exception:
                            pass

                    if hex_data.startswith("0300") and 10 < packet_length < 30:
                        bot_state.log("Match starting, please wait...", "info")
                        continue

                    if hex_data.startswith("0300") and packet_length >= 300:
                        bot_state.log("MATCH FOUND! Loading...", "success")
                        try:
                            bot_state.set_info(uid_str, "MATCH FOUND, UDP shuru hocche...")
                        except Exception:
                            pass

                        try:
                            res = json.loads(await decode_protobuf(hex_data[10:]))
                            token = None
                            udp_key = None
                            match_code = None
                            server_ip_port = None
                            match_account_id = None
                            block_val = None

                            if '42' in res and 'data' in res['42']:
                                match_code = res['42']['data']
                            if '5' in res and 'data' in res['5']:
                                res_field5 = res['5']['data']
                                server_ip_port = res_field5.get('2', {}).get('data')
                                udp_key = res_field5.get('3', {}).get('data')
                                token = res_field5.get('4', {}).get('data')
                                if '42' in res_field5:
                                    match_code = res_field5['42']['data']
                            if '1' in res and 'data' in res['1']:
                                match_account_id = res['1']['data']
                            if '5' in res and 'data' in res['5']:
                                block_val = res['5']['data'].get('1', {}).get('data')

                            effective_acc_id = match_account_id or account_id or "BD_BOT"

                            if token and udp_key and match_code and server_ip_port:
                                acc_tok = ""
                                if current_account_data:
                                    acc_tok = current_account_data.get('access_token', '') or ""
                                thunder, sharma = await build_match_startup_packets(
                                    token, udp_key, match_code, effective_acc_id, block_val or 0,
                                    server_ip=server_ip_port,
                                    region=account_region,
                                    client_version=client_version,
                                    access_token=acc_tok,
                                    mode=("BR" if bot_state.get_match_type(uid_str) == "BR" else "LONE_WOLF")
                                )

                                match_index = await _inc_match(uid_str)
                                total = await _get_total_match_count()
                                bot_state.log(f"🚀 [MATCH #{match_index}] UDP starting → {server_ip_port} (background)", "info")
                                bot_state.log(f"[FUNCTIONAL] UDP task started. UID active: {match_index} | Total: {total}", "success")

                                new_match = asyncio.create_task(
                                    play_game(
                                        server_ip_port,
                                        thunder,
                                        sharma,
                                        udp_key,
                                        match_code,
                                        effective_acc_id,
                                        "BD",
                                        client_version,
                                        current_key,
                                        current_iv,
                                        match_index=match_index,
                                        dash_uid=uid_str,
                                        mode=("BR" if bot_state.get_match_type(uid_str) == "BR" else "LONE_WOLF")
                                    )
                                )
                                play_matches.append(new_match)

                                consecutive_parse_failures = 0

                                try:
                                    writer.close()
                                    await writer.wait_closed()
                                except Exception:
                                    pass

                                # ✅ FIX: Post-match cooldown কমানো হয়েছে (12+5~20s → 8+3~8s)
                                # NEW_MATCH_DELAY default 12s → এখন 8s এ সেট, ENV দিয়ে override করা যাবে
                                post_match_wait = max(8.0, NEW_MATCH_DELAY - 4.0) + random.uniform(3.0, 8.0)
                                bot_state.log(f"[SAFE] Post-match cooldown {post_match_wait:.1f}s before next search", "info")
                                await asyncio.sleep(post_match_wait)
                                reconnects = 0
                                break 

                            elif bot_state.get_match_type(uid_str) == "BR":
                                bot_state.log(f"[BR] config packet ({packet_length}B) — queue-te-i thakchi", "info", uid_str)
                                continue
                            else:
                                consecutive_parse_failures += 1
                                bot_state.log(f"[FUNCTIONAL] Non-match big packet (#{consecutive_parse_failures}/{MAX_CONSECUTIVE_PARSE_FAILURES}) → reconnecting", "warning")

                                if consecutive_parse_failures >= MAX_CONSECUTIVE_PARSE_FAILURES:
                                    bot_state.log(f"[FUNCTIONAL] {MAX_CONSECUTIVE_PARSE_FAILURES}x parse failures → invalidating cache for fresh login", "error")
                                    if current_account_data:
                                        try:
                                            if current_account_data.get('auth_uid'):
                                                cache_invalidate(str(current_account_data['auth_uid']))
                                            if current_account_data.get('auth_token'):
                                                cache_invalidate(f"tok_{current_account_data['auth_token'][:20]}")
                                        except Exception:
                                            pass
                                    consecutive_parse_failures = 0

                                try:
                                    writer.close()
                                    await writer.wait_closed()
                                except Exception:
                                    pass
                                await asyncio.sleep(NON_MATCH_RECONNECT_DELAY)
                                break

                        except Exception as e:
                            print_error(f"[FUNCTIONAL] Match packet error: {e}")
                            consecutive_parse_failures += 1
                            if consecutive_parse_failures >= MAX_CONSECUTIVE_PARSE_FAILURES:
                                if current_account_data:
                                    try:
                                        if current_account_data.get('auth_uid'):
                                            cache_invalidate(str(current_account_data['auth_uid']))
                                        if current_account_data.get('auth_token'):
                                            cache_invalidate(f"tok_{current_account_data['auth_token'][:20]}")
                                    except Exception:
                                        pass
                                consecutive_parse_failures = 0
                            try:
                                writer.close()
                                await writer.wait_closed()
                            except Exception:
                                pass
                            await asyncio.sleep(NON_MATCH_RECONNECT_DELAY)
                            break

                    if 30 <= packet_length <= 40:
                        continue

            except asyncio.CancelledError:
                bot_state.log(f"[FUNCTIONAL] Cancelled — cancelling {len(play_matches)} UDP matches", "warning")
                for m in play_matches:
                    if not m.done():
                        m.cancel()
                if play_matches:
                    await asyncio.gather(*play_matches, return_exceptions=True)
                play_matches.clear()
                raise
            except Exception as e:
                print_error(f"[FUNCTIONAL] TCP state ({uid_str}): {e}")

                play_matches[:] = [m for m in play_matches if not m.done()]

                if writer:
                    try:
                        writer.close()
                        await writer.wait_closed()
                    except Exception:
                        pass

                if "Cache expired" in str(e):
                    print_warning(f"[FUNCTIONAL] Triggering re-login for {uid_str}")
                    break

                reconnects += 1
                if reconnects > max_reconnects:
                    print_error("[FUNCTIONAL] Max reconnects reached, retrying...")
                    reconnects = 0
                    await asyncio.sleep(3)
                    continue

                await asyncio.sleep(min(reconnects, 2))

    except asyncio.CancelledError:
        print_warning(f"[FUNCTIONAL] Outer cancelled. {len(play_matches)} UDP matches still running.")
        for m in play_matches:
            if not m.done():
                m.cancel()
        if play_matches:
            await asyncio.gather(*play_matches, return_exceptions=True)
        play_matches.clear()
        raise


async def informational(addrs, starter_packet, key, iv, region="BD", max_reconnects=3):
    reconnects = 0
    ip, port = addrs.split(":")
    while True:
        writer = None
        ping_task = None
        try:
            resolved_ip = await resolve_host_cloudflare(ip)
            reader, writer = await asyncio.open_connection(resolved_ip, int(port))
            
            raw_sock = writer.get_extra_info('socket')
            if raw_sock:
                optimize_tcp_socket(raw_sock)
                
            writer.write(bytes.fromhex(starter_packet))
            await writer.drain()
            reconnects = 0

            # Initial keepalive right after connecting
            try:
                init_ka = await send_keep_alive(region)
                if init_ka and writer and not writer.is_closing():
                    writer.write(init_ka)
                    await asyncio.wait_for(writer.drain(), timeout=3)
            except Exception:
                pass

            async def info_keepalive():
                ka_bytes = await send_keep_alive(region)
                while True:
                    await asyncio.sleep(5)
                    try:
                        if writer and not writer.is_closing():
                            writer.write(ka_bytes)
                            await writer.drain()
                    except Exception:
                        break

            ping_task = asyncio.create_task(info_keepalive())

            while True:
                data = await reader.read(8192)
                if not data:
                    raise ConnectionError("Connection closed")
        except asyncio.CancelledError:
            if ping_task:
                ping_task.cancel()
            if writer:
                try:
                    writer.close()
                    await writer.wait_closed()
                except Exception:
                    pass
            raise
        except Exception:
            if ping_task:
                ping_task.cancel()
            if writer:
                try:
                    writer.close()
                    await writer.wait_closed()
                except Exception:
                    pass
            reconnects += 1
            if reconnects > max_reconnects:
                await asyncio.sleep(3)
                reconnects = 0
            else:
                await asyncio.sleep(1)


# ==================== ACCOUNT PROCESSORS ====================

def _register_credentials(account_data: Dict):
    try:
        acc_id = str(account_data['account_id'])
        bot_state.account_credentials[acc_id] = account_data
        if account_data.get('auth_uid'):
            bot_state.account_credentials[str(account_data['auth_uid'])] = account_data
        if account_data.get('auth_token'):
            bot_state.account_credentials[f"tok_{account_data['auth_token'][:20]}"] = account_data
    except Exception:
        pass


async def refresh_account_profile(account_data_or_uid: Any):
    try:
        if isinstance(account_data_or_uid, str):
            uid = str(account_data_or_uid)
            account_data = bot_state.account_credentials.get(uid)
        else:
            account_data = account_data_or_uid
            uid = str(account_data.get('account_id'))

        if not account_data:
            return

        url = account_data.get('server_url')
        token = account_data.get('token')
        release_version = account_data.get('release_version')
        payload = account_data.get('login_payload_data')

        if not (url and token and release_version and payload):
            return

        res = await send_getlogin(payload, url, token, release_version)
        if res:
            res_proto, dict_res = res
            level = int(get_proto_field(dict_res, 6, 1))
            exp = int(get_proto_field(dict_res, 7, 0))
            likes = int(get_proto_field(dict_res, 8, 0))
            nickname = res_proto.nickname or get_proto_field(dict_res, 4, "")

            acc_id = str(account_data['account_id'])
            # ✅ FIX: exp >= 0 — 0 EXP-ও valid (নতুন account), শুধু None/negative block করো
            if exp >= 0:
                bot_state.update_exp(acc_id, exp, level)
            if likes > 0 and acc_id in bot_state.accounts:
                bot_state.accounts[acc_id]["likes"] = likes
            if nickname and acc_id in bot_state.accounts:
                bot_state.accounts[acc_id]["nickname"] = nickname
            bot_state.log(f"[EXP-REFRESH] UID {acc_id} -> Level: {level}, EXP: {exp}", "info")
    except Exception as e:
        print_error(f"refresh_account_profile error: {e}")


async def process_account_uid_pass(uid: str, password: str) -> Optional[Dict]:
    _current_login_uid.set(str(uid))
    _acc = bot_state.accounts.get(str(uid))
    if _acc:
        _acc.pop("last_error", None)
    cached = cache_get(uid)
    if cached:
        print_success(f"[CACHE HIT] UID {uid} loaded from token_cache.json (no login)")
        acc_id = str(cached['account_id'])
        bot_state.register_account(
            uid=acc_id,
            nickname=cached.get('nickname', f"Player_{acc_id}"),
            region=cached.get('region', 'BD'),
            level=cached.get('level', 1),
            exp=cached.get('exp', 0),
            likes=cached.get('likes', 0)
        )
        _register_credentials(cached)
        return cached

    print_info(f"[LOGIN] Full login for UID {uid}...")
    # ✅ FIX: Semaphore দিয়ে একসাথে সর্বোচ্চ LOGIN_CONCURRENCY টি login — server rate limit এড়ানো
    async with _LOGIN_SEMAPHORE:
      try:
        # ✅ FIX: version_config_cached — প্রতিটা account আলাদা scrape করে না
        verconfig_res = await version_config_cached()
        if verconfig_res is None:
            report_fail(uid, "Version config failed", generic=True)
            return None
        release_version, client_version, server_url = verconfig_res
        
        tokengrant_response = await get_access_token(uid, password)
        if tokengrant_response is None:
            return None
        open_id, access_token, platform = tokengrant_response
        
        # 🔥 1ta id 1ta Device Injection
        device_info = get_device_for_account(uid)
        
        login_payload_data = await build_majorlogin_payload(open_id, access_token, platform, client_version, device_info)
        if login_payload_data is None:
            report_fail(uid, "MajorLogin payload build failed", generic=True)
            return None
        majorlogin_response = await send_majorlogin(login_payload_data, release_version, server_url)
        if majorlogin_response is None:
            report_fail(uid, "MajorLogin failed", generic=True)
            return None
        getlogin_result = await send_getlogin(login_payload_data, majorlogin_response.url, majorlogin_response.token, release_version)
        if getlogin_result is None:
            report_fail(uid, "GetLoginData failed", generic=True)
            return None
        res_proto, dict_res = getlogin_result

        acc_id = str(majorlogin_response.account_id)
        level = int(get_proto_field(dict_res, 6, 1))
        exp = int(get_proto_field(dict_res, 7, 0))
        likes = int(get_proto_field(dict_res, 8, 0))
        nickname = res_proto.nickname or get_proto_field(dict_res, 4, f"Player_{acc_id}")
        region = majorlogin_response.region or get_proto_field(dict_res, 3, "BD")

        bot_state.register_account(uid=acc_id, nickname=nickname, region=region, level=level, exp=exp, likes=likes)

        account_data = {
            'account_id': majorlogin_response.account_id,
            'nickname': nickname,
            'region': region,
            'level': level,
            'exp': exp,
            'likes': likes,
            'open_id': open_id,
            'access_token': access_token,
            'platform': str(platform),
            'token': majorlogin_response.token,
            'server_time': majorlogin_response.server_time,
            'aes_ak': majorlogin_response.aes_ak,
            'iv_i': majorlogin_response.iv_i,
            'functional_addrs': res_proto.functional_addrs or get_proto_field(dict_res, 14),
            'informational_addrs': res_proto.informational_addrs or get_proto_field(dict_res, 32),
            'release_version': release_version,
            'client_version': client_version,
            'server_url': majorlogin_response.url,
            'login_payload_data': login_payload_data,
            'auth_type': 'guest',
            'auth_uid': uid,
            'auth_password': password
        }
        _register_credentials(account_data)
        cache_set(uid, account_data)
        return account_data
      except Exception as e:
        report_fail(uid, "process_account_uid_pass exception", repr(e)[:250])
        return None


async def process_account_token(access_token: str) -> Optional[Dict]:
    cache_key = f"tok_{access_token[:20]}"
    cached = cache_get(cache_key)
    if cached:
        print_success(f"[CACHE HIT] Token {access_token[:10]}... loaded from cache")
        acc_id = str(cached['account_id'])
        bot_state.register_account(
            uid=acc_id,
            nickname=cached.get('nickname', f"Player_{acc_id}"),
            region=cached.get('region', 'BD'),
            level=cached.get('level', 1),
            exp=cached.get('exp', 0),
            likes=cached.get('likes', 0)
        )
        _register_credentials(cached)
        return cached

    print_info("[LOGIN] Full login with Access Token...")
    # ✅ FIX: Semaphore দিয়ে concurrent login control
    async with _LOGIN_SEMAPHORE:
      try:
        # ✅ FIX: version_config_cached — প্রতিটা token আলাদা scrape করে না
        verconfig_res = await version_config_cached()
        if verconfig_res is None:
            return None
        release_version, client_version, server_url = verconfig_res

        # ✅ FIX: requests (sync/blocking) → httpx async — event loop block হবে না
        url = f"https://100067.connect.garena.com/oauth/token/inspect?token={access_token}"
        hdrs = {
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "close",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "100067.connect.garena.com",
            "User-Agent": "GarenaMSDK/4.0.19P4(G011A ;Android 9;en;US;)"
        }
        resp = await client.get(url, headers=hdrs)
        data = resp.json()

        if 'error' in data:
            return None

        open_id = data.get('open_id')
        platform = data.get('platform', 4)

        if not open_id:
            return None

        # 🔥 1ta id 1ta Device Injection (using unique open_id as the key)
        device_info = get_device_for_account(open_id)

        login_payload_data = await build_majorlogin_payload(open_id, access_token, str(platform), client_version, device_info)
        if not login_payload_data:
            return None

        majorlogin_response = await send_majorlogin(login_payload_data, release_version, server_url)
        if majorlogin_response is None:
            return None

        getlogin_result = await send_getlogin(
            login_payload_data,
            majorlogin_response.url,
            majorlogin_response.token,
            release_version
        )
        if getlogin_result is None:
            return None

        res_proto, dict_res = getlogin_result
        acc_id = str(majorlogin_response.account_id)
        level = int(get_proto_field(dict_res, 6, 1))
        exp = int(get_proto_field(dict_res, 7, 0))
        likes = int(get_proto_field(dict_res, 8, 0))
        nickname = res_proto.nickname or get_proto_field(dict_res, 4, f"Player_{acc_id}")
        region = majorlogin_response.region or get_proto_field(dict_res, 3, "BD")

        bot_state.register_account(uid=acc_id, nickname=nickname, region=region, level=level, exp=exp, likes=likes)

        account_data = {
            'account_id': majorlogin_response.account_id,
            'nickname': nickname,
            'region': region,
            'level': level,
            'exp': exp,
            'likes': likes,
            'open_id': open_id,
            'access_token': access_token,
            'platform': str(platform),
            'token': majorlogin_response.token,
            'server_time': majorlogin_response.server_time,
            'aes_ak': majorlogin_response.aes_ak,
            'iv_i': majorlogin_response.iv_i,
            'functional_addrs': res_proto.functional_addrs or get_proto_field(dict_res, 14),
            'informational_addrs': res_proto.informational_addrs or get_proto_field(dict_res, 32),
            'release_version': release_version,
            'client_version': client_version,
            'server_url': majorlogin_response.url,
            'login_payload_data': login_payload_data,
            'platform': platform,
            'auth_type': 'token',
            'auth_token': access_token
        }
        _register_credentials(account_data)
        cache_set(cache_key, account_data)
        return account_data
      except Exception as e:
        print_error(f"process_account_token error: {e}")
        return None


async def run_account_worker(account_data: Dict, label: str):
    acc_id = str(account_data['account_id'])
    informational_task = None
    exp_task = None
    try:
        # ✅ FIX: Worker শুরু হলেই ONLINE — functional task শেষ না হলেও দেখাবে
        bot_state.update_status(acc_id, "ONLINE")
        reg = account_data.get('region', 'BD')
        tcp_packet_online = await build_tcp_startup_packet(
            account_data['account_id'],
            account_data['token'],
            account_data['server_time'],
            account_data['aes_ak'],
            account_data['iv_i'],
            region=reg,
            typ='OnLine'
        )

        tcp_packet_chat = await build_tcp_startup_packet(
            account_data['account_id'],
            account_data['token'],
            account_data['server_time'],
            account_data['aes_ak'],
            account_data['iv_i'],
            region=reg,
            typ='ChaT'
        )

        informational_task = asyncio.create_task(
            informational(
                account_data['informational_addrs'],
                tcp_packet_chat,
                account_data['aes_ak'],
                account_data['iv_i'],
                region=reg
            )
        )

        async def exp_refresher():
            while True:
                await asyncio.sleep(EXP_REFRESH_SECONDS)
                fresh = bot_state.account_credentials.get(acc_id)
                if fresh:
                    await refresh_account_profile(fresh)

        exp_task = asyncio.create_task(exp_refresher())

        functional_task = asyncio.create_task(
            functional_lone_wolf(
                account_data['functional_addrs'],
                tcp_packet_online,
                account_data['region'],
                account_data['client_version'],
                account_data['aes_ak'],
                account_data['iv_i'],
                account_id=acc_id,
                account_data=account_data
            )
        )

        await functional_task

    except asyncio.CancelledError:
        raise
    except Exception as e:
        print_error(f"run_account_worker error for {label}: {e}")
    finally:
        for t in (informational_task, exp_task):
            if t and not t.done():
                t.cancel()
        for t in (informational_task, exp_task):
            if t:
                try:
                    await t
                except (asyncio.CancelledError, Exception):
                    pass


async def account_loop_guest(uid: str, password: str):
    uid_str = str(uid)

    # display_uid = bot_state.accounts এ যে key দিয়ে track হচ্ছে
    # প্রথমে guest UID, login এর পর real account_id হয়
    display_uid = uid_str

    if uid_str not in bot_state.accounts:
        bot_state.register_account(
            uid=uid_str,
            nickname=f"Player_{uid_str[:6]}",
            region="BD",
            level=1,
            exp=0
        )
    bot_state.update_status(uid_str, "CONNECTING")

    while True:
        # ROOT FIX: প্রতিটি loop শুরুতে blacklist চেক
        # Worker cancel না হলেও এই চেক দিয়ে নিজে থামবে
        if uid_str in bot_state.deleted_uids or display_uid in bot_state.deleted_uids:
            print_warning(f"[BLACKLIST] Worker for {uid} self-terminated.")
            # ✅ FIX: update_status("OFFLINE") না করে সরাসরি accounts থেকে সরাও
            # — dashboard-এ "Offline" দেখাবে না
            bot_state.accounts.pop(display_uid, None)
            bot_state.recalc_totals()
            break

        try:
            print_info(f"[LOGIN] Starting login for Guest UID: {uid}...")
            bot_state.update_status(display_uid, "CONNECTING")

            account_data = await process_account_uid_pass(uid, password)
            if not account_data:
                print_error(f"Login failed for UID: {uid}. Retrying in 15-30 seconds...")
                bot_state.update_status(display_uid, "ERROR")
                # ✅ FIX: 30-60s → 15-30s — তাড়াতাড়ি retry, তবু ban-safe
                await asyncio.sleep(random.uniform(15.0, 30.0))
                continue

            real_acc_id = str(account_data.get('account_id', uid_str))

            if real_acc_id != display_uid:
                # real_acc_id ও blacklist এ আছে কিনা চেক
                if real_acc_id in bot_state.deleted_uids:
                    print_warning(f"[BLACKLIST] Real ID {real_acc_id} blacklisted. Worker stopping.")
                    # ✅ FIX: update_status("OFFLINE") করলে guest UID dashboard-এ "Offline" দেখায়।
                    # সরাসরি accounts থেকে pop করো — status update করার দরকার নেই।
                    bot_state.accounts.pop(display_uid, None)
                    bot_state.recalc_totals()
                    bot_state._remove_from_json(display_uid)   # accounts.json থেকেও মুছো
                    bot_state.deleted_uids.add(display_uid)    # পরের redeploy-এ আর login করবে না
                    bot_state._save_deleted_uids()
                    break

                # ROOT FIX: Worker key পুরনো guest UID থেকে real_acc_id তে সরাও
                # এটাই মূল সমস্যা ছিল — dashboard real_acc_id দিয়ে cancel করত
                # কিন্তু worker store ছিল guest UID দিয়ে → cancel কাজ করত না
                if display_uid in bot_state.account_workers:
                    running_task = bot_state.account_workers.pop(display_uid)
                    bot_state.account_workers[real_acc_id] = running_task
                # guest UID → real account id (Reload এ চলমান আইডি চিনতে লাগে)
                bot_state.guest_alias[uid_str] = real_acc_id

                if display_uid in bot_state.accounts:
                    del bot_state.accounts[display_uid]

                bot_state.register_account(
                    uid=real_acc_id,
                    nickname=account_data.get('nickname', f"Player_{real_acc_id[:6]}"),
                    region=account_data.get('region', 'BD'),
                    level=account_data.get('level', 1),
                    exp=account_data.get('exp', 0),
                    likes=account_data.get('likes', 0)
                )
                # display_uid আপডেট — পরের status update সঠিক key তে যাবে
                display_uid = real_acc_id
                # ✅ FIX: real_acc_id-এ ONLINE সেট — না করলে "Connecting"-এ আটকে থাকে
                bot_state.update_status(display_uid, "ONLINE")

            elif display_uid in bot_state.accounts:
                entry = bot_state.accounts[display_uid]
                entry['nickname']    = account_data.get('nickname', entry['nickname'])
                entry['region']      = account_data.get('region',   entry['region'])
                entry['level']       = account_data.get('level',    entry['level'])
                entry['current_exp'] = account_data.get('exp',      entry['current_exp'])
                entry['likes']       = account_data.get('likes',    entry['likes'])
                entry['status']      = 'ONLINE'
                entry['last_updated'] = time.strftime("%H:%M:%S")
                bot_state.recalc_totals()
                bot_state.check_level_limit(display_uid)

            await run_account_worker(account_data, uid)
            print_warning(f"Session finished for {uid}. Reconnecting in 10-25s...")
            bot_state.update_status(display_uid, "CONNECTING")
            # ✅ SAFE: Random reconnect delay like a real player closing and reopening the game
            await asyncio.sleep(random.uniform(10.0, 25.0))
        except asyncio.CancelledError:
            print_warning(f"Worker for {uid} stopped.")
            bot_state.update_status(display_uid, "OFFLINE")
            break
        except Exception as e:
            print_error(f"Error for UID {uid}: {e}. Retrying in 10s...")
            bot_state.update_status(display_uid, "ERROR")
            bot_state.set_error(display_uid, f"Worker exception: {repr(e)[:200]}")
            await asyncio.sleep(10)


async def account_loop_token(token: str):
    token_label = token[:10]
    placeholder_uid = f"tok_{token_label}"
    if placeholder_uid not in bot_state.accounts:
        bot_state.register_account(
            uid=placeholder_uid,
            nickname=f"Token_{token_label}",
            region="BD",
            level=1,
            exp=0
        )
    bot_state.update_status(placeholder_uid, "CONNECTING")

    while True:
        # ROOT FIX: প্রতিটি loop শুরুতে blacklist চেক
        if placeholder_uid in bot_state.deleted_uids or token_label in bot_state.deleted_uids:
            print_warning(f"[BLACKLIST] Token worker {token_label} self-terminated.")
            bot_state.update_status(placeholder_uid, "OFFLINE")
            break

        try:
            print_info("[LOGIN] Starting login with Access Token...")
            bot_state.update_status(placeholder_uid, "CONNECTING")

            account_data = await process_account_token(token)
            if not account_data:
                print_error("Login failed for Token. Retrying in 15 seconds...")
                bot_state.update_status(placeholder_uid, "ERROR")
                # ✅ FIX: Add random jitter to avoid simultaneous retries
                await asyncio.sleep(15 + random.uniform(0, 10))
                continue

            acc_id = str(account_data['account_id'])

            # ✅ FIX: Update placeholder entry with real data
            if placeholder_uid in bot_state.accounts:
                entry = bot_state.accounts[placeholder_uid]
                entry['nickname']    = account_data.get('nickname', entry['nickname'])
                entry['region']      = account_data.get('region',   entry['region'])
                entry['level']       = account_data.get('level',    entry['level'])
                entry['current_exp'] = account_data.get('exp',      entry['current_exp'])
                entry['likes']       = account_data.get('likes',    entry['likes'])
                entry['last_updated'] = time.strftime("%H:%M:%S")
                bot_state.recalc_totals()
                bot_state.check_level_limit(placeholder_uid)
            # ✅ FIX: update_status দিয়ে ONLINE — Online counter সঠিক হবে
            bot_state.update_status(placeholder_uid, "ONLINE")

            await run_account_worker(account_data, acc_id)
            print_warning("Token session finished. Reconnecting in 3s...")
            bot_state.update_status(placeholder_uid, "CONNECTING")
            await asyncio.sleep(3)
        except asyncio.CancelledError:
            print_warning(f"Worker for token {token_label} stopped.")
            bot_state.update_status(placeholder_uid, "OFFLINE")
            break
        except Exception as e:
            print_error(f"Token error: {e}. Retrying in 10s...")
            bot_state.update_status(placeholder_uid, "ERROR")
            await asyncio.sleep(10)


# ==================== ACCOUNTS LOADER ====================

def load_accounts():
    """accounts*.json সব ফাইল থেকে অটো লোড করে — duplicate বাদ দেয়"""
    accounts = []
    seen_uids = set()
    seen_tokens = set()
    
    files = get_all_account_files()
    for filepath in files:
        if not os.path.exists(filepath):
            continue
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                continue
            fname = os.path.basename(filepath)
            loaded = 0
            for acc in data:
                if "token" in acc and acc["token"]:
                    tok = str(acc["token"]).strip()
                    if tok not in seen_tokens:
                        seen_tokens.add(tok)
                        accounts.append(acc)
                        loaded += 1
                elif "uid" in acc and "password" in acc and acc["uid"]:
                    uid = str(acc["uid"]).strip()
                    if uid not in seen_uids:
                        seen_uids.add(uid)
                        accounts.append(acc)
                        loaded += 1
            print_success(f"[LOADER] {fname} → {loaded} account(s) loaded")
        except Exception as e:
            print_error(f"Could not load {filepath}: {e}")

    if not accounts and FALLBACK_UID and FALLBACK_PASSWORD:
        accounts.append({"uid": FALLBACK_UID, "password": FALLBACK_PASSWORD})

    print_info(f"[LOADER] Total accounts loaded: {len(accounts)} (from {len(files)} file(s))")
    return accounts


# ==================== MAIN ====================

async def _periodic_device_saver():
    """✅ FIX: প্রতি 60s-এ dirty devices cache file-এ save করে — I/O storm বন্ধ করে"""
    while True:
        await asyncio.sleep(60)
        if _DEVICES_DIRTY:
            try:
                _save_devices_cache()
            except Exception:
                pass


async def main():
    print_colored("=" * 60, Colors.CYAN)
    print_info(f"Start Match Interval: {START_MATCH_INTERVAL}s")
    print_info(f"Offline Wait: {NEW_MATCH_DELAY}s (after match found)")
    print_info(f"Non-match Reconnect: {NON_MATCH_RECONNECT_DELAY}s")
    print_info(f"Cache Invalidation Threshold: {MAX_CONSECUTIVE_PARSE_FAILURES}x")
    print_info(f"Parallel Matches: UNLIMITED (background)")
    print_info(f"Cache TTL: {TOKEN_CACHE_TTL}s ({TOKEN_CACHE_TTL//60} min)")
    print_info(f"Priority Regions: {PRIORITY_REGIONS}")
    print_info("Device System: 1 ID = 1 Persistent Device ID (data/devices.json)")
    print_info(f"Login Concurrency: {_LOGIN_CONCURRENCY} (ENV: LOGIN_CONCURRENCY)")
    print_colored("=" * 60, Colors.CYAN)

    # ✅ FIX: Device cache একবারই load করো — 500 আইডির জন্য file I/O আর হবে না
    _load_devices_cache_once()
    # Background periodic saver চালু করো
    asyncio.create_task(_periodic_device_saver())

    # ✅ FIX: Auto-free port if already in use (kills old stuck process)
    try:
        import subprocess, signal
        result = subprocess.run(
            ["fuser", f"{WEB_PORT}/tcp"],
            capture_output=True, text=True
        )
        pids = result.stdout.strip().split()
        for pid_str in pids:
            try:
                pid = int(pid_str)
                if pid != os.getpid():
                    os.kill(pid, signal.SIGKILL)
                    print_warning(f"Killed old process on port {WEB_PORT} (PID: {pid})")
                    await asyncio.sleep(1)
            except Exception:
                pass
    except Exception:
        pass

    try:
        await start_web_dashboard(host=WEB_HOST, port=WEB_PORT)
        print_success(f"Web Dashboard live at http://localhost:{WEB_PORT}")
    except Exception as e:
        print_error(f"Could not start web dashboard: {e}")
        # Last resort: try killing with fuser and retry once
        try:
            import subprocess
            subprocess.run(["fuser", "-k", f"{WEB_PORT}/tcp"], capture_output=True)
            await asyncio.sleep(2)
            await start_web_dashboard(host=WEB_HOST, port=WEB_PORT)
            print_success(f"Web Dashboard live at http://localhost:{WEB_PORT} (retry OK)")
        except Exception as e2:
            print_error(f"Dashboard could not start even after retry: {e2}")

    async def on_account_added_handler(data):
        if "token" in data and data["token"]:
            t = str(data["token"]).strip()
            placeholder = f"tok_{t[:10]}"
            # ✅ Re-add করলে blacklist থেকে সরাও
            bot_state.deleted_uids.discard(t[:10])
            bot_state.deleted_uids.discard(placeholder)
            if placeholder not in bot_state.accounts:
                bot_state.register_account(uid=placeholder, nickname=f"Token_{t[:10]}", region="BD", level=1, exp=0)
            bot_state.update_status(placeholder, "CONNECTING")
            await asyncio.sleep(random.uniform(0.5, 2.0))
            task = asyncio.create_task(account_loop_token(t))
            bot_state.account_workers[t[:10]] = task
        elif "uid" in data and "password" in data:
            u = str(data["uid"]).strip()
            p = str(data["password"]).strip()
            # ✅ Re-add করলে blacklist থেকে সরাও
            bot_state.deleted_uids.discard(u)
            if u not in bot_state.accounts:
                bot_state.register_account(uid=u, nickname=f"Player_{u[:6]}", region="BD", level=1, exp=0)
            bot_state.update_status(u, "CONNECTING")
            await asyncio.sleep(random.uniform(0.5, 2.0))
            task = asyncio.create_task(account_loop_guest(u, p))
            bot_state.account_workers[u] = task

    async def on_refresh_account_handler(uid):
        await refresh_account_profile(uid)

    async def on_reload_accounts_handler():
        """
        accounts*.json reload করে — ইতিমধ্যে চলমান নয় এমন accounts চালু করে।
        deleted_uids আগেই dashboard_server.py-তে clear করা হয়েছে।
        """
        fresh_accounts = load_accounts()
        started = 0
        for acc in fresh_accounts:
            if "token" in acc and acc["token"]:
                t = str(acc["token"]).strip()
                key = t[:10]
                placeholder = f"tok_{key}"
                # ইতিমধ্যে চলমান হলে skip
                if key in bot_state.account_workers and not bot_state.account_workers[key].done():
                    continue
                bot_state.deleted_uids.discard(key)
                bot_state.deleted_uids.discard(placeholder)
                if placeholder not in bot_state.accounts:
                    bot_state.register_account(uid=placeholder, nickname=f"Token_{key}", region="BD", level=1, exp=0)
                bot_state.update_status(placeholder, "CONNECTING")
                await asyncio.sleep(random.uniform(0.3, 1.0))
                task = asyncio.create_task(account_loop_token(t))
                bot_state.account_workers[key] = task
                started += 1
            elif "uid" in acc and "password" in acc and acc["uid"]:
                u = str(acc["uid"]).strip()
                p = str(acc["password"]).strip()
                # ইতিমধ্যে চলমান হলে skip (worker key login-এর পর real account id হয়ে যায়, তাই alias-ও দেখা হয়)
                real_key = bot_state.guest_alias.get(u, u)
                if any(k in bot_state.account_workers and not bot_state.account_workers[k].done() for k in (u, real_key)):
                    continue
                bot_state.deleted_uids.discard(u)
                bot_state.deleted_uids.discard(real_key)
                if u not in bot_state.accounts:
                    bot_state.register_account(uid=u, nickname=f"Player_{u[:6]}", region="BD", level=1, exp=0)
                bot_state.update_status(u, "CONNECTING")
                await asyncio.sleep(random.uniform(0.3, 1.0))
                task = asyncio.create_task(account_loop_guest(u, p))
                bot_state.account_workers[u] = task
                started += 1
        return started

    bot_state.refresh_callbacks["on_account_added"] = on_account_added_handler
    bot_state.refresh_callbacks["on_refresh_account"] = on_refresh_account_handler
    bot_state.refresh_callbacks["on_reload_accounts"] = on_reload_accounts_handler

    accounts = load_accounts()

    if not accounts:
        print_warning(f"No accounts found in any accounts*.json file! Add accounts from Web Dashboard.")
        print_warning(f"Open: http://localhost:{WEB_PORT}")

    # ✅ FIX: Pre-register ALL accounts immediately so dashboard shows them from startup
    # ✅ FIX2: deleted_uids-এ থাকলে skip — redeploy-এর পর level-limit আইডি আর "Connecting" দেখাবে না
    for acc in accounts:
        if "token" in acc and acc["token"]:
            placeholder = f"tok_{acc['token'][:10]}"
            if placeholder in bot_state.deleted_uids:
                continue
            bot_state.register_account(uid=placeholder, nickname=f"Token_{acc['token'][:10]}", region="BD", level=1, exp=0)
            bot_state.update_status(placeholder, "CONNECTING")
        elif "uid" in acc and "password" in acc and acc["uid"]:
            u = str(acc["uid"])
            if u in bot_state.deleted_uids:
                continue
            bot_state.register_account(uid=u, nickname=f"Player_{u[:6]}", region="BD", level=1, exp=0)
            bot_state.update_status(u, "CONNECTING")

    # ✅ FIX: BATCH LAUNCH SYSTEM — 500 আইডির জন্য smart batch system
    # প্রতি batch-এ BATCH_SIZE টি account একসাথে launch হয়
    # Batch-এর মধ্যে BATCH_DELAY সেকেন্ড gap দেওয়া হয়
    # এটি Railway-তে memory spike বন্ধ করে এবং crash ঠিক করে
    # ✅ FIX: Batch size বাড়ানো 10→20, delay কমানো 5.0→2.0
    # version_config_cached থাকায় এখন বড় batch safe — একটাই version scrape হয়
    BATCH_SIZE = int(os.environ.get("LAUNCH_BATCH_SIZE", "20"))
    BATCH_DELAY = float(os.environ.get("LAUNCH_BATCH_DELAY", "2.0"))

    total = len(accounts)
    print_info(f"[LAUNCHER] Starting {total} accounts in batches of {BATCH_SIZE} (delay: {BATCH_DELAY}s between batches)")

    for batch_start in range(0, total, BATCH_SIZE):
        batch = accounts[batch_start: batch_start + BATCH_SIZE]
        batch_num = batch_start // BATCH_SIZE + 1
        total_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE

        for acc in batch:
            if "token" in acc and acc["token"]:
                t_key = acc["token"][:10]
                placeholder = f"tok_{t_key}"
                # ✅ FIX: deleted_uids-এ থাকলে worker শুরু করবে না
                if placeholder in bot_state.deleted_uids or t_key in bot_state.deleted_uids:
                    continue
                t = asyncio.create_task(account_loop_token(acc["token"]))
                bot_state.account_workers[t_key] = t
            elif "uid" in acc and "password" in acc and acc["uid"]:
                u = str(acc["uid"])
                # ✅ FIX: deleted_uids-এ থাকলে worker শুরু করবে না
                if u in bot_state.deleted_uids:
                    continue
                t = asyncio.create_task(account_loop_guest(u, acc["password"]))
                bot_state.account_workers[u] = t

        print_info(f"[LAUNCHER] Batch {batch_num}/{total_batches} launched ({len(batch)} accounts)")

        # Last batch-এর পর আর sleep নেই
        if batch_start + BATCH_SIZE < total:
            await asyncio.sleep(BATCH_DELAY)

    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, asyncio.CancelledError):
        print_warning("\n[STOP] Shutting down all accounts...")
        for t in list(bot_state.account_workers.values()):
            t.cancel()
        await asyncio.gather(*bot_state.account_workers.values(), return_exceptions=True)
        print_success("All sessions cleanly closed.")


if __name__ == "__main__":
    try:
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
    except KeyboardInterrupt:
        print_warning("\nProgram stopped by user.")
