# -*- coding: utf-8 -*-
"""
FreeFire Level Up Bot - Professional Web Dashboard & Real-Time EXP Tracker
Embedded Async Web Server (aiohttp)
"""

import asyncio
import json
import os
import time

# Account level eta ba tar beshi hole BR theke automatic Lone Wolf. 0 dile bondho.
try:
    AUTO_LW_LEVEL = int(os.environ.get("AUTO_LW_LEVEL", "3"))
except Exception:
    AUTO_LW_LEVEL = 3
from typing import Dict, List, Any, Optional
from aiohttp import web

# ==================== BASE DIRECTORY (ALWAYS ABSOLUTE) ====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# ✅ AUTO MULTI-FILE SUPPORT - accounts.json, accounts2.json, accounts3.json ...
import glob as _glob

def get_all_account_files_dashboard():
    """Root-এ accounts*.json সব ফাইল অটো ডিটেক্ট করে"""
    files = sorted(_glob.glob(os.path.join(BASE_DIR, "accounts*.json")))
    if not files:
        files = [os.path.join(BASE_DIR, "accounts.json")]
    return files

ACCOUNTS_FILE_PATH = os.path.join(BASE_DIR, "accounts.json")  # default for new adds

# ==================== EMBEDDED HTML DASHBOARD ====================
# HTML is embedded directly — no external file dependency (works on Termux/mobile)
DASHBOARD_HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#0c0f14">
<title>SHADMAN LEVEL UP</title>
<link rel="icon" href="/logo.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=DM+Sans:wght@400;500;600&display=swap">
<style>
:root{--bg:#0c0f14;--s1:#12161d;--s2:#181d26;--s3:#1f2530;--border:rgba(190,205,230,.08);--border2:rgba(134,174,214,.16);
--fire:#5b89b9;--fire2:#dcc29a;--violet:#9a93c9;--violet2:#a9a3d6;--green:#4cc38a;--amber:#cfae72;--red:#d17b86;--blue:#86aed6;
--text:#e6eaf0;--text2:#b1b9c6;--muted:#7d8696;--muted2:#2c3340;--white:#e8ecf2;--rsm:8px;--rmd:11px;--rlg:14px;--ease:cubic-bezier(.4,0,.2,1)}
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:'DM Sans','Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;-webkit-font-smoothing:antialiased;overflow-x:hidden;font-size:13px}
button,input,select{font:inherit}button{cursor:pointer}
::-webkit-scrollbar{width:6px;height:6px}::-webkit-scrollbar-thumb{background:var(--muted2);border-radius:99px}
body{font-variant-numeric:tabular-nums}
.app{display:grid;grid-template-columns:250px 1fr;grid-template-rows:48px 1fr;height:100vh;height:100dvh}
.header{grid-column:1/-1;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:0 20px;background:rgba(12,15,20,.92);border-bottom:1px solid var(--border);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);z-index:100}
.brand{display:flex;align-items:center;gap:9px;min-width:0;flex:1 1 auto}
.brand>div{min-width:0}
.flame{width:22px;height:22px;flex:0 0 auto}
.brand-name{font-family:'Rajdhani','Segoe UI',sans-serif;font-size:16px;font-weight:700;letter-spacing:.05em;white-space:nowrap;line-height:1.1;overflow:hidden;text-overflow:ellipsis;color:var(--fire2)}
.brand-sub{font-size:10.5px;color:var(--muted);margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.header-right{display:flex;align-items:center;gap:10px;flex:0 0 auto}
.live{min-width:64px;justify-content:flex-end;display:flex;align-items:center;gap:6px;font-size:12px;font-weight:500;color:var(--green);white-space:nowrap}
.live i{width:7px;height:7px;border-radius:50%;background:var(--green);animation:pg 2.4s ease-in-out infinite}
.live.off{color:var(--red)}.live.off i{background:var(--red);animation:none}
@keyframes pg{0%,100%{box-shadow:0 0 0 0 rgba(76,195,138,.4)}50%{box-shadow:0 0 0 5px rgba(76,195,138,0)}}
.btn-primary{height:32px;padding:0 14px;background:#4a78a6;color:#fff;border:0;border-radius:var(--rsm);font-size:12.5px;font-weight:600;display:flex;align-items:center;gap:6px;white-space:nowrap;transition:background .2s var(--ease)}
.btn-primary:hover{background:#5886b4}
.btn-icon{width:32px;height:32px;flex:0 0 auto;display:grid;place-items:center;background:var(--s2);border:1px solid var(--border);border-radius:var(--rsm);color:var(--text2);transition:color .2s var(--ease),border-color .2s var(--ease)}
.btn-icon:hover{color:var(--red);border-color:var(--red)}.btn-icon svg{width:15px;height:15px}
.sidebar{background:var(--s1);border-right:1px solid var(--border);padding:10px;overflow-y:auto;display:flex;flex-direction:column;gap:10px}
.slabel{font-family:'Rajdhani','Segoe UI',sans-serif;font-size:11px;font-weight:600;color:var(--white);opacity:.75;letter-spacing:.08em;margin-bottom:6px;text-transform:uppercase}
.exp-hero{background:var(--s2);border:1px solid var(--border);border-radius:var(--rmd);padding:9px 8px;text-align:center}
.exp-hero-num{font-family:'Rajdhani','Segoe UI',sans-serif;font-size:22px;font-weight:700;line-height:1;color:var(--white)}
.exp-hero-num small{font-family:'DM Sans',sans-serif;font-size:12px;font-weight:600;margin-right:6px;opacity:.7;letter-spacing:.04em}
.exp-hero-sub{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-height:1.2em;font-size:11px;color:var(--white);opacity:.7;margin-top:4px}
.stat-grid{display:grid;grid-template-columns:1fr 1fr;gap:5px}
.stat-card{background:var(--s2);border:1px solid var(--border);border-radius:var(--rsm);padding:6px 9px}
.stat-card.wide{grid-column:1/-1}
.stat-card:has(.c-fire){box-shadow:inset 2px 0 0 var(--fire)}
.stat-card:has(.c-green){box-shadow:inset 2px 0 0 var(--blue)}
.stat-card:has(.c-amber){box-shadow:inset 2px 0 0 var(--amber)}
.stat-card:has(.c-red){box-shadow:inset 2px 0 0 var(--red)}
.stat-card:has(.c-muted){box-shadow:inset 2px 0 0 var(--muted)}
.stat-num{min-height:1em;font-family:'Rajdhani','Segoe UI',sans-serif;font-size:17px;font-weight:700;line-height:1;margin-bottom:2px;color:var(--white)}
.stat-lbl{font-size:11px;color:var(--white);opacity:.7}
.c-fire,.c-green,.c-red,.c-amber,.c-muted{color:var(--white)}
.divider{height:1px;background:var(--border)}
.ctrl-toggle{display:none}
.ctrl-stack{display:flex;flex-direction:column;gap:10px}
.row-between{display:flex;align-items:center;justify-content:space-between;background:var(--s2);border:1px solid var(--border);border-radius:var(--rsm);padding:6px 10px}
.row-label{font-size:12.5px;font-weight:500;color:var(--white)}
.tgl{position:relative;width:36px;height:20px}.tgl input{opacity:0;width:0;height:0}
.tgl-track{position:absolute;inset:0;background:var(--muted2);border-radius:99px;cursor:pointer;transition:background .25s var(--ease)}
.tgl-track::before{content:'';position:absolute;width:14px;height:14px;left:3px;top:3px;background:#fff;border-radius:50%;transition:transform .25s var(--ease)}
.tgl input:checked+.tgl-track{background:var(--fire)}.tgl input:checked+.tgl-track::before{transform:translateX(16px)}
.mode-row{display:grid;grid-template-columns:repeat(3,1fr);background:var(--s2);border:1px solid var(--border);border-radius:var(--rsm);overflow:hidden}
.mbtn{padding:8px 4px;font-size:11.5px;font-weight:600;background:transparent;color:var(--text2);border:0;transition:background .2s var(--ease),color .2s var(--ease)}
.mbtn:not(:last-child){border-right:1px solid var(--border)}
.mbtn:hover{background:rgba(255,255,255,.04)}
.mbtn-br.active{background:rgba(220,194,154,.14);color:var(--white)}.mbtn-lw.active{background:rgba(154,147,201,.18);color:var(--white)}.mbtn-auto.active{background:rgba(134,174,214,.16);color:var(--white)}
.input-row{display:flex;gap:6px}
.inp{flex:1;min-width:0;background:var(--s2);border:1px solid var(--border);border-radius:var(--rsm);padding:7px 11px;color:var(--text);font-size:13px;outline:0;transition:border-color .2s var(--ease)}
.inp:focus{border-color:var(--fire)}.inp::placeholder{color:var(--muted)}
.hint{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-height:1.3em;font-size:11px;color:var(--white);opacity:.6;margin-top:5px}
.btn-ghost{height:34px;padding:0 13px;background:var(--s3);border:1px solid var(--border);color:var(--white);border-radius:var(--rsm);font-size:12px;font-weight:600;white-space:nowrap;transition:border-color .2s var(--ease),background .2s var(--ease)}
.btn-ghost:hover{border-color:var(--fire);background:#252c38}
.btn-block{width:100%;height:33px;background:rgba(134,174,214,.08);border:1px solid rgba(134,174,214,.2);color:var(--white);border-radius:var(--rsm);font-size:12px;font-weight:600;transition:background .2s var(--ease)}
.btn-block:hover{background:rgba(134,174,214,.15)}.btn-block:disabled,.btn-ghost:disabled{opacity:.5;cursor:wait}
.main{overflow-y:auto;padding:12px 16px 24px;display:flex;flex-direction:column;gap:16px;min-width:0}
.sec-head{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:10px;flex-wrap:wrap}
.sec-title{font-family:'Rajdhani','Segoe UI',sans-serif;font-size:15px;font-weight:700;color:var(--white)}
.sec-title small{font-family:'DM Sans',sans-serif;font-size:11px;color:var(--white);opacity:.6;font-weight:500;margin-left:8px}
.search{width:220px;max-width:100%;height:30px}
.accounts-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(205px,1fr));gap:8px}
.acard{background:var(--s1);border:1px solid var(--border);border-radius:var(--rmd);padding:9px;position:relative;overflow:hidden;transition:border-color .25s var(--ease),background .25s var(--ease)}
.acard:hover{border-color:rgba(190,205,230,.18);background:#151a22}
.acard::before{content:'';position:absolute;top:0;left:0;right:0;height:2px}
.st-online::before{background:linear-gradient(90deg,var(--blue),transparent)}
.st-match::before{background:linear-gradient(90deg,var(--green),transparent)}
.st-match{border-color:rgba(76,195,138,.30);background:linear-gradient(180deg,rgba(76,195,138,.06),transparent 60%),var(--s1)}
.st-match:hover{border-color:rgba(76,195,138,.46);background:linear-gradient(180deg,rgba(76,195,138,.08),transparent 60%),#151a22}
.st-connecting::before{background:linear-gradient(90deg,var(--amber),transparent)}
.st-offline::before{background:linear-gradient(90deg,var(--red),transparent)}
.st-paused::before{background:linear-gradient(90deg,var(--muted),transparent)}
.card-top{display:flex;align-items:flex-start;gap:8px;margin-bottom:7px}
.avatar{min-width:42px;height:42px;padding:0 6px;border-radius:10px;background:var(--s3);border:1px solid var(--border);display:flex;align-items:center;justify-content:center;flex:0 0 auto}
.lvl{font-family:'Rajdhani','Segoe UI',sans-serif;font-size:28px;font-weight:700;line-height:1;color:var(--white);letter-spacing:.01em;white-space:nowrap;display:flex;align-items:flex-end;gap:1px}
.lvl-tag{font-size:10px;font-weight:600;opacity:.65;margin-bottom:3px;letter-spacing:.04em;font-family:'DM Sans',sans-serif}
.card-info{flex:1;min-width:0}
.nick{font-family:'Rajdhani','Segoe UI',sans-serif;font-size:13.5px;font-weight:700;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:var(--white)}
.uid{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-size:11.5px;font-weight:700;color:var(--white);opacity:.92;margin-top:1px;letter-spacing:.02em}
.badge-row{display:flex;gap:3px;margin-top:4px;flex-wrap:nowrap;overflow:hidden;height:22px}
.badge{white-space:nowrap;flex:0 0 auto}
.badge{font-size:9.5px;font-weight:600;padding:1px 5px;border-radius:5px;border:1px solid var(--border);font-family:inherit;line-height:1.3;color:var(--white);background:rgba(255,255,255,.05);transition:background .2s var(--ease),border-color .2s var(--ease)}
.b-online{background:rgba(134,174,214,.12);border-color:rgba(134,174,214,.28)}
.b-match{background:rgba(76,195,138,.16);border-color:rgba(76,195,138,.40);color:#9ce6c0}
.b-connecting{background:rgba(207,174,114,.12);border-color:rgba(207,174,114,.28)}
.b-offline{background:rgba(209,123,134,.12);border-color:rgba(209,123,134,.28)}
.b-paused{background:rgba(125,134,150,.14);border-color:rgba(125,134,150,.28)}
.b-br{background:rgba(220,194,154,.10);border-color:rgba(220,194,154,.24)}
.b-lw{background:rgba(154,147,201,.11);border-color:rgba(154,147,201,.24)}
.b-reg{background:rgba(255,255,255,.05)}
.badge.st{font-size:11.5px;font-weight:700;padding:1px 6px}
button.badge:hover{background:rgba(255,255,255,.12)}
.exp-row{display:flex;align-items:center;gap:9px;margin-bottom:7px}
.ring-wrap{position:relative;width:36px;height:36px;flex:0 0 auto}
.ring-svg{transform:rotate(-90deg);width:100%;height:100%}
.ring-bg{fill:none;stroke:var(--s3);stroke-width:4.5}
.ring-fill{fill:none;stroke:url(#expGrad);stroke-width:4.5;stroke-linecap:round;transition:stroke-dashoffset 1s var(--ease)}
.ring-pct{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-family:'Rajdhani','Segoe UI',sans-serif;font-size:10px;font-weight:700;color:var(--white)}
.exp-lbl{font-size:10px;color:var(--white);opacity:.7;margin-bottom:2px}
.exp-val{font-family:'Rajdhani','Segoe UI',sans-serif;font-size:15px;font-weight:700;color:var(--white);line-height:1}
.exp-need{font-size:10px;color:var(--white);opacity:.7;margin-top:2px}
.limit{height:3px;background:var(--s3);border-radius:99px;overflow:hidden;margin:-2px 0 9px}
.limit i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--amber),var(--red));transition:width .8s var(--ease)}
.meta{font-size:10.5px;color:var(--white);opacity:.75;margin-bottom:7px;line-height:1.5}
.meta{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.meta b{color:var(--white);font-weight:600;opacity:1}
.note{font-size:11px;line-height:1.4;padding:6px 8px;border-radius:8px;margin-bottom:8px;word-break:break-word;color:var(--text2);background:rgba(255,255,255,.035);border:1px solid var(--border)}
.note.err{color:#e3a6ad;background:rgba(209,123,134,.07);border-color:rgba(209,123,134,.18)}
.note.info{height:60px;overflow:hidden;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical}
.note.info[hidden]{display:-webkit-box;visibility:hidden}
.note.err{max-height:42px;overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
.note.err[hidden]{display:none}
.meta{min-height:3em}
.exp-need,.exp-val{white-space:nowrap}
.card-btns{display:flex;gap:6px}
.cbtn{flex:1;height:24px;background:var(--s2);border:1px solid var(--border);color:var(--white);border-radius:var(--rsm);font-size:10.5px;font-weight:500;transition:border-color .2s var(--ease),background .2s var(--ease)}
.cbtn:hover.ref{border-color:var(--blue);background:rgba(134,174,214,.10)}
.cbtn:hover.del{border-color:var(--red);background:rgba(209,123,134,.10)}
.empty{grid-column:1/-1;text-align:center;color:var(--text2);font-size:13px;padding:44px 20px;border:1px dashed var(--muted2);border-radius:var(--rlg)}
.log-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px}
.log-clear{font-size:11px;color:var(--white);opacity:.6;background:none;border:0;transition:opacity .2s var(--ease)}.log-clear:hover{opacity:1}
.log-box{background:var(--s1);border:1px solid var(--border);border-radius:var(--rmd);padding:10px 12px;max-height:220px;overflow-y:auto;display:flex;flex-direction:column;gap:4px}
.log-entry{display:flex;gap:10px;font-size:11.5px;line-height:1.45}
.log-ts{color:var(--white);opacity:.45;flex:0 0 auto;font-size:11px;font-variant-numeric:tabular-nums}
.log-msg{word-break:break-word;color:var(--text2)}.l-success{color:var(--green)}.l-warning{color:var(--amber)}.l-error{color:var(--red)}.l-info{color:var(--blue)}
.overlay{position:fixed;inset:0;z-index:200;display:none;place-items:center;padding:18px;background:rgba(0,0,0,.7);backdrop-filter:blur(8px)}
.overlay.open{display:grid}
.modal{width:min(420px,100%);max-height:100%;overflow-y:auto;background:var(--s1);border:1px solid var(--border);border-radius:16px;padding:18px}
.modal h2{font-family:'Rajdhani','Segoe UI',sans-serif;font-size:18px;margin-bottom:4px;color:var(--white)}
.modal p{font-size:12px;color:var(--text2);margin-bottom:12px}
.tabs{display:grid;grid-template-columns:1fr 1fr;gap:4px;padding:3px;background:var(--bg);border:1px solid var(--border);border-radius:10px;margin-bottom:12px}
.tab{height:32px;border:0;border-radius:8px;background:transparent;color:var(--text2);font-size:12px;font-weight:600;transition:background .2s var(--ease)}
.tab.active{background:var(--s3);color:var(--white)}
.field{margin-bottom:11px}.field label{display:block;font-size:10.5px;color:var(--white);opacity:.7;text-transform:uppercase;letter-spacing:.06em;margin-bottom:5px}
.field .inp{width:100%;height:38px}
.pane{display:none}.pane.active{display:block}
.modal-foot{display:flex;gap:8px;margin-top:6px}.modal-foot button{flex:1;height:38px}
.toasts{position:fixed;right:18px;bottom:18px;z-index:300;display:flex;flex-direction:column;gap:8px;pointer-events:none}
.toast{max-width:340px;padding:10px 13px;font-size:12px;font-weight:500;color:var(--white);background:var(--s2);border:1px solid var(--border);border-left:3px solid var(--green);border-radius:10px;box-shadow:0 12px 32px rgba(0,0,0,.5)}
.toast.err{border-left-color:var(--red)}
@media(min-width:901px){
.sidebar .log-sec{flex:none;display:flex;flex-direction:column}
.sidebar .log-box{flex:none;height:380px;max-height:380px;padding:8px 9px}
.sidebar .log-entry{flex-direction:column;gap:0}
}
@media(max-width:900px){
.app{display:flex;flex-direction:column;height:auto}
.header{position:sticky;top:0;padding:0 14px}
.sidebar{border-right:0;border-bottom:1px solid var(--border);overflow:visible;gap:12px}
.stat-grid{grid-template-columns:repeat(4,1fr)}.stat-card{padding:8px 8px}.stat-card.wide{grid-column:1/-1}
.ctrl-toggle{display:flex;width:100%;height:36px;align-items:center;justify-content:center;gap:6px;background:var(--s2);border:1px solid var(--border);border-radius:var(--rsm);color:var(--white);font-size:12.5px;font-weight:600}
.ctrl-stack{display:none}.ctrl-stack.open{display:flex}
.main{overflow:visible;padding:14px 14px 36px}
.accounts-grid{grid-template-columns:repeat(auto-fill,minmax(230px,1fr))}
.brand-sub{display:none}
.toasts{left:14px;right:14px}.toast{max-width:none}
}
@media(max-width:520px){
.accounts-grid{grid-template-columns:1fr}.search{width:100%}
.header{gap:8px;padding:0 10px}
.brand{gap:7px}.flame{width:20px;height:20px}
.brand-name{font-size:14px;letter-spacing:.03em}
.header-right{gap:8px}
.live{font-size:11px;gap:5px}
.btn-primary{padding:0 10px;gap:0}.btn-primary .lbl{display:none}
.btn-primary svg{width:15px;height:15px}
.btn-primary{width:32px;justify-content:center;padding:0}
}
.rolechip{font-size:10.5px;font-weight:600;padding:2px 8px;border-radius:99px;border:1px solid var(--border);color:var(--white);background:rgba(255,255,255,.06);white-space:nowrap}
.role-user .ctrl-stack,.role-user .ctrl-toggle,.role-user .card-btns,.role-user .log-clear,.role-user .divider{display:none!important}
.role-user button.badge.mode{pointer-events:none;cursor:default}
@media(max-width:520px){.rolechip{display:none}}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute;pointer-events:none"><defs><linearGradient id="expGrad" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#86aed6"/><stop offset="100%" stop-color="#6fc2ae"/></linearGradient></defs></svg>
<div class="app">
<header class="header">
  <div class="brand">
    <svg class="flame" viewBox="0 0 24 24"><defs><linearGradient id="flGrad" x1="12" y1="2" x2="12" y2="22" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#ecd7b4"/><stop offset="1" stop-color="#c9a572"/></linearGradient></defs><path d="M12 2C10 5 7 9 7.5 13a4.8 4.8 0 001 2.5C8 13 9.5 11 11 10.5c-.5 2 .5 3.5 1 4a4.5 4.5 0 002-3.5c1 1.5 1.5 3 1.5 5A5 5 0 017 16c0-4 2.5-8.5 5-14z" fill="url(#flGrad)"/></svg>
    <div><div class="brand-name">SHADMAN LEVEL UP</div><div class="brand-sub">FreeFire Bot Dashboard</div></div>
  </div>
  <div class="header-right">
    <span class="rolechip" id="roleChip"></span>
    <div class="live" id="live"><i></i><span id="liveTxt">Live</span></div>
    <button class="btn-icon" id="logoutBtn" type="button" title="Logout" aria-label="Logout"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><path d="m16 17 5-5-5-5"/><path d="M21 12H9"/></svg></button>
    <button class="btn-primary" id="openAdd" type="button"><svg width="13" height="13" viewBox="0 0 16 16" fill="currentColor"><path d="M8 2a.5.5 0 01.5.5v5h5a.5.5 0 010 1h-5v5a.5.5 0 01-1 0v-5h-5a.5.5 0 010-1h5v-5A.5.5 0 018 2z"/></svg><span class="lbl">Add Account</span></button>
  </div>
</header>

<aside class="sidebar">
  <div>
    <div class="slabel">Total EXP Farmed</div>
    <div class="exp-hero"><div class="exp-hero-num"><small>EXP</small><span id="totalExp">0</span></div><div class="exp-hero-sub" id="totalSub">0 matches</div></div>
  </div>
  <div>
    <div class="slabel">Accounts</div>
    <div class="stat-grid">
      <div class="stat-card wide"><div class="stat-num c-fire" id="sTotal">0</div><div class="stat-lbl">Total</div></div>
      <div class="stat-card"><div class="stat-num c-green" id="sOnline">0</div><div class="stat-lbl">Online</div></div>
      <div class="stat-card"><div class="stat-num c-amber" id="sConn">0</div><div class="stat-lbl">Connecting</div></div>
      <div class="stat-card"><div class="stat-num c-red" id="sOffline">0</div><div class="stat-lbl">Offline</div></div>
      <div class="stat-card"><div class="stat-num c-muted" id="sPaused">0</div><div class="stat-lbl">Paused</div></div>
    </div>
  </div>
  <button class="ctrl-toggle" id="ctrlToggle" type="button">⚙ Controls ▾</button>
  <div class="divider"></div>
  <div class="ctrl-stack" id="ctrlStack">
    <div class="slabel" style="margin-bottom:-4px">Controls</div>
    <div class="row-between"><span class="row-label">All Bots</span><label class="tgl"><input type="checkbox" id="globalToggle" checked><span class="tgl-track"></span></label></div>
    <div>
      <div class="slabel">Match Mode — All</div>
      <div class="mode-row">
        <button class="mbtn mbtn-br" id="m-BR" type="button">⚔ BR</button>
        <button class="mbtn mbtn-lw" id="m-LONE_WOLF" type="button">🐺 LW</button>
        <button class="mbtn mbtn-auto" id="m-AUTO" type="button">🔄 Auto</button>
      </div>
    </div>
    <div>
      <div class="slabel">EXP Limit (auto-delete)</div>
      <div class="input-row"><input class="inp" type="text" inputmode="numeric" id="limitInp" placeholder="0 = no limit"><button class="btn-ghost" id="limitBtn" type="button">Set</button></div>
      <div class="hint" id="limitHint"></div>
    </div>
    <div>
      <div class="slabel">Level Limit (auto-delete)</div>
      <div class="input-row"><input class="inp" type="text" inputmode="numeric" id="levelInp" placeholder="0 = no limit"><button class="btn-ghost" id="levelBtn" type="button">Set</button></div>
      <div class="hint" id="levelHint"></div>
    </div>
    <div>
      <div class="slabel">User ID Limit (per user)</div>
      <div class="input-row"><input class="inp" type="text" inputmode="numeric" id="userLimitInp" placeholder="0 = no limit"><button class="btn-ghost" id="userLimitBtn" type="button">Set</button></div>
      <div class="hint" id="userLimitHint"></div>
    </div>
    <button class="btn-block" id="reloadBtn" type="button">↺ Reload accounts.json</button>
  </div>
</aside>

<main class="main">
  <section>
    <div class="sec-head">
      <div class="sec-title">Accounts<small id="countTxt"></small></div>
      <input class="inp search" id="search" type="search" placeholder="Search name or UID…" autocomplete="off">
    </div>
    <div class="accounts-grid" id="grid"></div>
  </section>
  <section class="log-sec" id="logSec">
    <div class="log-head"><div class="sec-title">Activity Log</div><button class="log-clear" id="logClear" type="button">Clear</button></div>
    <div class="log-box" id="logBox"></div>
  </section>
</main>
</div>

<div class="overlay" id="overlay">
  <div class="modal" role="dialog" aria-modal="true">
    <h2>Add Account</h2><p>Connect a Free Fire account. It is validated before the bot starts.</p>
    <div class="tabs"><button class="tab active" data-tab="guest" type="button">Guest Account</button><button class="tab" data-tab="token" type="button">Access Token</button></div>
    <div class="pane active" data-pane="guest">
      <div class="field"><label for="fUid">UID</label><input class="inp" id="fUid" inputmode="numeric" autocomplete="off" placeholder="Player UID"></div>
      <div class="field"><label for="fPwd">Password</label><input class="inp" id="fPwd" type="password" autocomplete="off" placeholder="Account password"></div>
    </div>
    <div class="pane" data-pane="token">
      <div class="field"><label for="fTok">Access Token</label><input class="inp" id="fTok" autocomplete="off" placeholder="Paste access token"></div>
    </div>
    <div class="field"><label for="fReg">Server Region</label>
      <select class="inp" id="fReg"><option value="BD">Bangladesh</option><option value="IND">India</option><option value="SG">Singapore</option><option value="ID">Indonesia</option><option value="BR">Brazil</option><option value="US">United States</option></select></div>
    <div class="modal-foot"><button class="btn-ghost" id="addCancel" type="button">Cancel</button><button class="btn-primary" id="addSubmit" type="button" style="justify-content:center">Validate &amp; Start</button></div>
  </div>
</div>
<div class="toasts" id="toasts"></div>

<script>
const EXP_LIST=[0,48,202,544,1012,1844,2792,3800,4870,6004,7192,8448,9760,11140,12566,14060,15610,17224,18902,20632,22424,24278,26192,28166,30200,32294,34448,37804,41274,44870,48582,53394,58566,64096,69994,76260,83506,91128,99322,108092,120144,133266,147472,162760,179126,196572,215368,235316,257010,279860,304056,348318,394982,444044,495508,549364,633756,721744,813336,908522,1041438,1180352,1325266,1476184,1634300,1840946,2056594,2281242,2514880,2757530,3059506,3372284,3699456,4041030,4397002,4829104,5282204,5756304,6251404,6767502,7381324,8043154,8752982,9510808,10316638,11277190,12291748,13360304,14482858,15659418,17026708,18453990,19941280,21488570,23095858,24763138,26490428,28277708,30124996,32032284];
// EXP_LIST[i] = total EXP needed to reach level i+1
const $=id=>document.getElementById(id);
const esc=v=>String(v==null?'':v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmt=v=>{const n=Number(v);return Number.isFinite(n)?n.toLocaleString():'0'};
const num=v=>{const n=Number(v);return Number.isFinite(n)?n:0};
let globalRunning=true,modeChoice=null,limitLoaded=false,limitBusy=false,toggleBusy=false,lastLogSig='',lastData=null,tab='guest';
const cards=new Map();
let levelLoaded=false,levelBusy=false,userLimitLoaded=false,userLimitBusy=false;

function toast(msg,err){const t=document.createElement('div');t.className='toast'+(err?' err':'');t.textContent=msg;$('toasts').appendChild(t);setTimeout(()=>t.remove(),3400)}
async function api(path,body){
  const r=await fetch(path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body||{})});
  if(r.status===401){location.href='/login';throw new Error('Session expired')}
  const d=await r.json().catch(()=>({}));
  if(!r.ok||d.status==='error'||d.success===false)throw new Error(d.error||d.message||'Request failed');
  return d;
}

function status(s){
  const v=String(s||'ONLINE').toUpperCase().replace(/ +/g,'_');
  if(v==='CONNECTING')return{k:'connecting',l:'◌ Connecting',g:'conn'};
  if(v==='SEARCHING'||v==='SEARCH')return{k:'connecting',l:'◌ Searching',g:'on'};
  if(v==='IN_MATCH'||v==='MATCH'||v==='PLAYING')return{k:'match',l:'▶ In Match',g:'on'};
  if(v==='OFFLINE'||v==='DISCONNECTED')return{k:'offline',l:'● Offline',g:'off'};
  if(v==='ERROR'||v==='FAILED')return{k:'offline',l:'● Error',g:'off'};
  if(v==='PAUSED'||v==='STOPPED')return{k:'paused',l:'⏸ Paused',g:'pause'};
  return{k:'online',l:'● Online',g:'on'};
}
function progress(level,exp){
  const lv=Math.max(1,Math.floor(num(level))),cur=EXP_LIST[lv-1],nxt=EXP_LIST[lv];
  if(cur===undefined)return{pct:0,need:0,max:true};
  if(nxt===undefined)return{pct:100,need:0,max:true};
  const pct=Math.min(100,Math.max(0,(num(exp)-cur)/(nxt-cur)*100));
  return{pct,need:Math.max(0,nxt-num(exp)),max:false};
}
function ringSvg(){const r=23.75,c=2*Math.PI*r;return`<svg class="ring-svg" width="54" height="54" viewBox="0 0 54 54"><circle class="ring-bg" cx="27" cy="27" r="${r}"/><circle class="ring-fill" cx="27" cy="27" r="${r}" stroke-dasharray="${c.toFixed(2)}" stroke-dashoffset="${c.toFixed(2)}"/></svg><div class="ring-pct">0%</div>`}

function cardHtml(){return`<div class="card-top"><div class="avatar"><span class="lvl"></span></div><div class="card-info"><div class="nick"></div><div class="uid"></div><div class="badge-row"><span class="badge st"></span><button type="button" class="badge mode" title="Click to switch BR / Lone Wolf"></button><span class="badge b-reg reg"></span></div></div></div>
<div class="exp-row"><div class="ring-wrap">${ringSvg()}</div><div><div class="exp-lbl">EXP this session</div><div class="exp-val"></div><div class="exp-need"></div></div></div>
<div class="limit" hidden><i></i></div>
<div class="meta"></div>
<div class="note err" hidden></div><div class="note info" hidden></div>
<div class="card-btns"><button type="button" class="cbtn ref">↻ Refresh</button><button type="button" class="cbtn del">🗑 Delete</button></div>`}

function makeCard(uid){
  const el=document.createElement('article');
  el.dataset.uid=uid;el.innerHTML=cardHtml();
  el.querySelector('.mode').addEventListener('click',()=>{const a=el._acc;if(a)setMatchType(uid,a.match_type==='BR'?'LONE_WOLF':'BR')});
  el.querySelector('.ref').addEventListener('click',()=>refreshAcc(uid));
  el.querySelector('.del').addEventListener('click',()=>deleteAcc(uid));
  return el;
}
function setText(el,t){if(el.textContent!==t)el.textContent=t}
function updateCard(el,a,limit){
  el._acc=a;
  const st=status(a.status),nick=a.nickname||a.name||'Unknown',uid=String(a.uid),lv=num(a.level)||1;
  const cur=num(a.current_exp??a.exp),gained=a.gained_exp!=null?num(a.gained_exp):Math.max(0,cur-num(a.initial_exp));
  const p=progress(lv,cur),mt=a.match_type==='BR'?'BR':'LONE_WOLF',region=a.region||'—';
  el.className='acard st-'+st.k;
  el.querySelector('.lvl').innerHTML=String(lv)+'<span class="lvl-tag">LV</span>';
  setText(el.querySelector('.nick'),nick);el.querySelector('.nick').title=nick;
  setText(el.querySelector('.uid'),'#'+uid);
  const s=el.querySelector('.st');setText(s,st.l);s.className='badge st b-'+st.k;
  const m=el.querySelector('.mode');setText(m,mt==='BR'?'⚔ BR':'🐺 LW');m.className='badge mode '+(mt==='BR'?'b-br':'b-lw');
  setText(el.querySelector('.reg'),region);
  const circ=2*Math.PI*23.75;
  el.querySelector('.ring-fill').style.strokeDashoffset=(circ-p.pct/100*circ).toFixed(2);
  setText(el.querySelector('.ring-pct'),Math.round(p.pct)+'%');
  setText(el.querySelector('.exp-val'),'+'+fmt(gained));
  setText(el.querySelector('.exp-need'),p.max?'Max level':fmt(p.need)+' to Lv'+(lv+1));
  const lim=el.querySelector('.limit');
  if(limit>0){lim.hidden=false;lim.firstElementChild.style.width=Math.min(100,gained/limit*100)+'%';lim.title='Limit: '+fmt(gained)+' / '+fmt(limit)}else lim.hidden=true;
  const lm=a.last_match_time||'No match yet';
  el.querySelector('.meta').innerHTML='<b>'+fmt(a.matches_played??a.matches)+'</b> matches · Region: '+esc(region)+'<br>EXP '+fmt(num(a.initial_exp))+' → <b>'+fmt(cur)+'</b> · Last match: '+esc(lm);
  const er=el.querySelector('.note.err'),inf=el.querySelector('.note.info');
  er.hidden=!a.last_error;if(a.last_error)setText(er,a.last_error);
  inf.hidden=!a.last_info;if(a.last_info)setText(inf,a.last_info);
  el._search=(nick+' '+uid).toLowerCase();
}

function render(data){
  const accs=Array.isArray(data.accounts)?data.accounts.slice():[];
  // Highest level first; same level → UID order (EXP বদলালে কার্ড জায়গা বদলাবে না)
  accs.sort((a,b)=>num(b.level)-num(a.level)||String(a.uid).localeCompare(String(b.uid)));
  const limit=num(data.exp_limit),grid=$('grid'),q=$('search').value.trim().toLowerCase();
  const seen=new Set();let g={on:0,conn:0,off:0,pause:0};
  accs.forEach((a,i)=>{
    const uid=String(a.uid);seen.add(uid);
    let el=cards.get(uid);if(!el){el=makeCard(uid);cards.set(uid,el)}
    updateCard(el,a,limit);
    g[status(a.status).g]++;
    el.hidden=!!q&&!el._search.includes(q);
    if(grid.children[i]!==el)grid.insertBefore(el,grid.children[i]||null);   // keeps level order, moves only what changed
  });
  cards.forEach((el,uid)=>{if(!seen.has(uid)){el.remove();cards.delete(uid)}});
  let emp=grid.querySelector('.empty');
  if(!accs.length){if(!emp){emp=document.createElement('div');emp.className='empty';emp.textContent='No bots connected. Add a Free Fire account to start.';grid.appendChild(emp)}}else if(emp)emp.remove();
  const shown=q?accs.filter(a=>(String(a.nickname||'')+' '+a.uid).toLowerCase().includes(q)).length:accs.length;
  $('countTxt').textContent=q?shown+' / '+accs.length:accs.length+' total';
  $('totalExp').textContent=fmt(data.total_gained_exp);
  const up=num(data.uptime),h=Math.floor(up/3600),mi=Math.floor(up%3600/60);
  $('totalSub').textContent=fmt(data.total_matches)+' matches · uptime '+(h?h+'h ':'')+mi+'m';
  $('sTotal').textContent=fmt(accs.length);$('sOnline').textContent=fmt(g.on);$('sConn').textContent=fmt(g.conn);$('sOffline').textContent=fmt(g.off);$('sPaused').textContent=fmt(g.pause);
  // global toggle
  if(!toggleBusy&&data.global_running!==undefined){globalRunning=!!data.global_running;$('globalToggle').checked=globalRunning}
  // exp limit
  $('limitHint').textContent=limit>0?'Auto-delete at +'+fmt(limit)+' EXP':'No limit (accounts are never auto-deleted)';
  if(!limitLoaded&&data.exp_limit!==undefined&&!limitBusy){$('limitInp').value=data.exp_limit;limitLoaded=true}
  // role (Admin / User)
  const isUser=data.role==='user';document.body.classList.toggle('role-user',isUser);$('roleChip').textContent=isUser?'User':'Admin';
  // level limit
  const ll=num(data.level_limit);
  $('levelHint').textContent=ll>0?'Auto-delete at Lv'+ll:'No level limit';
  if(!levelLoaded&&data.level_limit!==undefined&&!levelBusy){$('levelInp').value=data.level_limit;levelLoaded=true}
  // user add limit (admin sets how many IDs each user may add)
  const ul=num(data.user_add_limit);
  $('userLimitHint').textContent=ul>0?'Each user can add up to '+ul+' ID(s)':'No limit (users can add unlimited IDs)';
  if(!userLimitLoaded&&data.user_add_limit!==undefined&&!userLimitBusy){$('userLimitInp').value=data.user_add_limit;userLimitLoaded=true}
  // mode highlight
  const mts=accs.map(a=>a.match_type==='BR'?'BR':'LONE_WOLF');
  let act=modeChoice;
  if(act!=='AUTO'&&mts.length){act=mts.every(x=>x==='BR')?'BR':mts.every(x=>x==='LONE_WOLF')?'LONE_WOLF':null}
  ['BR','LONE_WOLF','AUTO'].forEach(k=>$('m-'+k).classList.toggle('active',act===k));
  renderLogs(data.logs);
}

function renderLogs(logs){
  logs=Array.isArray(logs)?logs:[];
  const last=logs[logs.length-1],sig=logs.length+'|'+(last?last.time+last.message:'');
  if(sig===lastLogSig)return;lastLogSig=sig;
  const box=$('logBox'),keepTop=box.scrollTop;
  box.innerHTML=logs.slice().reverse().map(l=>'<div class="log-entry"><span class="log-ts">'+esc(l.time)+'</span><span class="log-msg l-'+esc(l.level||'info')+'">'+esc(l.message)+'</span></div>').join('')||'<div class="log-entry"><span class="log-ts">—</span><span class="log-msg">No activity yet</span></div>';
  box.scrollTop=keepTop;   // রিফ্রেশে স্ক্রল উপরে লাফিয়ে যাবে না
}

async function fetchStats(){
  try{
    const r=await fetch('/api/stats',{cache:'no-store'});
    if(r.status===401){location.href='/login';return}
    if(!r.ok)throw new Error('HTTP '+r.status);
    lastData=await r.json();render(lastData);
    $('live').className='live';$('liveTxt').textContent='Live';
  }catch(e){console.error('Stats error:',e);$('live').className='live off';$('liveTxt').textContent='Disconnected'}
}

async function setMatchType(uid,mt){
  try{await api('/api/account/match-type',{uid,match_type:mt});toast('UID '+uid+' → '+(mt==='BR'?'⚔ Battle Royale':'🐺 Lone Wolf'));modeChoice=null;await fetchStats()}
  catch(e){toast(e.message,true)}
}
async function refreshAcc(uid){try{await api('/api/account/refresh',{uid});toast('Refreshing #'+uid+'…');await fetchStats()}catch(e){toast(e.message,true)}}
async function deleteAcc(uid){
  if(!confirm('Delete account #'+uid+'?'))return;
  try{await api('/api/account/delete',{uid});toast('Account #'+uid+' deleted');await fetchStats()}catch(e){toast(e.message,true)}
}
$('globalToggle').addEventListener('change',async function(){
  const on=this.checked;toggleBusy=true;
  try{await api('/api/bot/toggle',{running:on});globalRunning=on;toast(on?'✅ সব আইডি চালু হয়েছে':'🛑 সব আইডি বন্ধ হয়েছে')}
  catch(e){this.checked=!on;toast(e.message,true)}
  toggleBusy=false;fetchStats();
});
['BR','LONE_WOLF','AUTO'].forEach(mode=>$('m-'+mode).addEventListener('click',async()=>{
  try{await api('/api/accounts/set-all-mode',{mode});modeChoice=mode;toast('✅ সব আইডি → '+(mode==='AUTO'?'🔄 Auto Level Mode':mode==='BR'?'⚔ Battle Royale':'🐺 Lone Wolf'));await fetchStats()}
  catch(e){toast(e.message,true)}
}));
async function setLimit(){
  const n=parseInt($('limitInp').value.trim().replace(/,/g,''),10);
  if(isNaN(n)||n<0){toast('❌ সঠিক সংখ্যা দিন (0 = লিমিট বন্ধ)',true);return}
  limitBusy=true;$('limitBtn').disabled=true;
  try{await api('/api/settings/exp-limit',{exp_limit:n});toast(n?'🎯 EXP লিমিট সেট: '+fmt(n):'🔓 EXP লিমিট বন্ধ');$('limitInp').value=n;limitLoaded=true;await fetchStats()}
  catch(e){toast(e.message,true)}
  limitBusy=false;$('limitBtn').disabled=false;
}
$('limitBtn').addEventListener('click',setLimit);
async function setLevelLimit(){
  const n=parseInt($('levelInp').value.trim(),10);
  if(isNaN(n)||n===1||n<0||n>200){toast('❌ লেভেল দিন 2–200 (0 = লিমিট বন্ধ)',true);return}
  levelBusy=true;$('levelBtn').disabled=true;
  try{await api('/api/settings/level-limit',{level_limit:n});toast(n?'🎚 Level লিমিট সেট: Lv'+n:'🔓 Level লিমিট বন্ধ');$('levelInp').value=n;levelLoaded=true;await fetchStats()}
  catch(e){toast(e.message,true)}
  levelBusy=false;$('levelBtn').disabled=false;
}
$('levelBtn').addEventListener('click',setLevelLimit);
async function setUserLimit(){
  const n=parseInt($('userLimitInp').value.trim(),10);
  if(isNaN(n)||n<0||n>100000){toast('❌ সঠিক সংখ্যা দিন (0 = লিমিট বন্ধ)',true);return}
  userLimitBusy=true;$('userLimitBtn').disabled=true;
  try{await api('/api/settings/user-limit',{user_add_limit:n});toast(n?'👤 প্রতি User সর্বোচ্চ '+n+'টি আইডি':'🔓 User ID লিমিট বন্ধ');$('userLimitInp').value=n;userLimitLoaded=true;await fetchStats()}
  catch(e){toast(e.message,true)}
  userLimitBusy=false;$('userLimitBtn').disabled=false;
}
$('userLimitBtn').addEventListener('click',setUserLimit);
$('userLimitInp').addEventListener('keydown',e=>{if(e.key==='Enter')setUserLimit()});
$('levelInp').addEventListener('keydown',e=>{if(e.key==='Enter')setLevelLimit()});
$('limitInp').addEventListener('keydown',e=>{if(e.key==='Enter')setLimit()});
function resetDashboard(){
  cards.forEach(el=>el.remove());cards.clear();
  const emp=$('grid').querySelector('.empty');if(emp)emp.remove();
  lastLogSig='';limitLoaded=false;levelLoaded=false;userLimitLoaded=false;modeChoice=null;lastData=null;
}
$('reloadBtn').addEventListener('click',async function(){
  const btn=this,old=btn.textContent;
  if(btn.disabled)return;
  btn.disabled=true;btn.textContent='↺ Reloading…';
  try{
    const d=await api('/api/accounts/reload');
    resetDashboard();                 // পুরনো কার্ড, লগ ও সেটিংস পরিষ্কার করে নতুন করে আঁকবে
    toast(d.message||'Accounts reloaded');
    await fetchStats();
    [1500,4000,8000].forEach(ms=>setTimeout(fetchStats,ms));   // নতুন চালু হওয়া আইডি ধরতে কয়েকবার রিফ্রেশ
  }catch(e){toast(e.message,true)}
  btn.disabled=false;btn.textContent=old;
});
$('logClear').addEventListener('click',async()=>{try{await api('/api/logs/clear');lastLogSig='';await fetchStats()}catch(e){toast(e.message,true)}});
$('search').addEventListener('input',()=>{if(lastData)render(lastData)});
$('ctrlToggle').addEventListener('click',()=>{const o=$('ctrlStack').classList.toggle('open');$('ctrlToggle').textContent='⚙ Controls '+(o?'▴':'▾')});

function openAdd(){$('overlay').classList.add('open');setTimeout(()=>{(tab==='guest'?$('fUid'):$('fTok')).focus()},50)}
function closeAdd(){$('overlay').classList.remove('open');['fUid','fPwd','fTok'].forEach(i=>$(i).value='')}
$('openAdd').addEventListener('click',openAdd);
(function(){const mq=matchMedia('(min-width:901px)');const place=()=>{const l=$('logSec');if(mq.matches)$('ctrlStack').after(l);else document.querySelector('.main').appendChild(l)};place();mq.addEventListener('change',place)})();$('addCancel').addEventListener('click',closeAdd);
$('overlay').addEventListener('click',e=>{if(e.target===$('overlay'))closeAdd()});
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeAdd()});
document.querySelectorAll('.tab').forEach(b=>b.addEventListener('click',()=>{
  tab=b.dataset.tab;
  document.querySelectorAll('.tab').forEach(x=>x.classList.toggle('active',x===b));
  document.querySelectorAll('.pane').forEach(p=>p.classList.toggle('active',p.dataset.pane===tab));
}));
$('addSubmit').addEventListener('click',async function(){
  const region=$('fReg').value,p={type:tab,region};
  if(tab==='guest'){p.uid=$('fUid').value.trim();p.password=$('fPwd').value.trim();if(!p.uid||!p.password){toast('UID এবং Password দিন',true);return}}
  else{p.token=$('fTok').value.trim();if(!p.token){toast('Access token দিন',true);return}}
  this.disabled=true;this.textContent='Validating…';
  try{await api('/api/account/add',p);toast('Account added — starting bot');closeAdd();await fetchStats()}
  catch(e){toast(e.message,true)}
  this.disabled=false;this.textContent='Validate & Start';
});

$('logoutBtn').addEventListener('click',async()=>{try{await fetch('/api/logout',{method:'POST'})}catch(e){}location.href='/login'});
fetchStats();setInterval(fetchStats,4000);
</script>
</body>
</html>
"""


# ==================== LOGIN / ACCESS KEY ====================
# Dashboard-e dhukte Access Key lagbe. Default key: SHADMAN-LEVEL
# Railway-te alada key chaile Variables-e DASHBOARD_KEY set korun (code change lagbe na).
import hmac as _hmac
import hashlib as _hashlib
import base64 as _b64

# ✅ ROLES: Admin = সব কাজ | User = শুধু দেখা + Add Account
#   Admin key  → ADMIN_KEY (না থাকলে DASHBOARD_KEY, ডিফল্ট SHADMAN-LEVEL)
#   User key   → USER_KEY  (ডিফল্ট AFX-USER)
DASHBOARD_KEY = (os.environ.get("ADMIN_KEY") or os.environ.get("DASHBOARD_KEY") or "SHADMAN-LEVEL").strip()
USER_KEY = (os.environ.get("USER_KEY") or "AFX-USER").strip()
USER_ALLOWED_PATHS = {"/", "/api/stats", "/api/account/add", "/api/logout"}
SESSION_COOKIE = "afx_session"
SESSION_DAYS = 30
_SESSION_SECRET = _hashlib.sha256(("afx-dashboard|" + DASHBOARD_KEY + "|" + USER_KEY).encode("utf-8")).digest()
_LOGIN_FAILS: Dict[str, Any] = {}   # ip -> {"n": fail_count, "until": lock_until_ts}
_MAX_FAILS = 5
_LOCK_SECONDS = 60

LOGO_JPG = _b64.b64decode("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")

LOGIN_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#0a0d12">
<title>SHADMAN LEVEL UP — Access</title>
<link rel="icon" href="/logo.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=DM+Sans:wght@400;500;600&display=swap">
<style>
:root{--bg:#0a0d12;--fire:#5b89b9;--fire2:#dcc29a;--violet:#9a93c9;--violet2:#a9a3d6;--red:#d17b86;--green:#4cc38a;--text:#e6eaf0;--muted:#7d8696}
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
html,body{height:100%}
body{font-family:'DM Sans','Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--text);-webkit-font-smoothing:antialiased;overflow:hidden;
background-image:radial-gradient(60% 50% at 12% 100%,rgba(91,137,185,.16),transparent 70%),radial-gradient(55% 45% at 92% 0%,rgba(154,147,201,.18),transparent 70%)}
body::before{content:'';position:fixed;inset:0;pointer-events:none;
background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);
background-size:44px 44px;-webkit-mask-image:radial-gradient(ellipse at center,#000 15%,transparent 70%);mask-image:radial-gradient(ellipse at center,#000 15%,transparent 70%)}
#fx{position:fixed;inset:0;width:100%;height:100%;pointer-events:none}
.scan{position:fixed;left:0;right:0;height:140px;top:-140px;pointer-events:none;background:linear-gradient(180deg,transparent,rgba(91,137,185,.05),transparent);animation:scan 7s linear infinite}
@keyframes scan{to{transform:translateY(calc(100vh + 280px))}}

.wrap{position:relative;z-index:2;min-height:100%;min-height:100dvh;display:flex;align-items:center;justify-content:center;padding:24px 18px;overflow-y:auto}
.card{position:relative;width:min(400px,100%);padding:78px 26px 26px;margin-top:64px;border-radius:26px;text-align:center;
background:linear-gradient(180deg,rgba(20,25,33,.80),rgba(12,16,22,.84));border:1px solid rgba(154,147,201,.22);
box-shadow:0 30px 90px rgba(0,0,0,.65),0 0 0 1px rgba(255,255,255,.02) inset;backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);
animation:rise .9s cubic-bezier(.22,1,.36,1) both}
@keyframes rise{from{opacity:0;transform:translateY(26px) scale(.97)}to{opacity:1;transform:none}}
.card::before{content:'';position:absolute;top:0;left:12%;right:12%;height:2px;background:linear-gradient(90deg,transparent,var(--fire),var(--violet),transparent);border-radius:2px}
.corner{position:absolute;width:16px;height:16px;border:2px solid rgba(220,194,154,.55)}
.c1{top:12px;left:12px;border-right:0;border-bottom:0;border-top-left-radius:8px}
.c2{top:12px;right:12px;border-left:0;border-bottom:0;border-top-right-radius:8px}
.c3{bottom:12px;left:12px;border-right:0;border-top:0;border-bottom-left-radius:8px}
.c4{bottom:12px;right:12px;border-left:0;border-top:0;border-bottom-right-radius:8px}

.logo{position:absolute;left:50%;top:0;width:136px;height:136px;transform:translate(-50%,-50%);border-radius:50%;padding:4px}
.logo::before{content:'';position:absolute;inset:0;border-radius:50%;background:conic-gradient(from 0deg,var(--fire),var(--violet),var(--fire2),#2a3140,var(--fire));animation:spin 5s linear infinite}
.logo::after{content:'';position:absolute;inset:-14px;border-radius:50%;background:radial-gradient(circle,rgba(91,137,185,.38),rgba(154,147,201,.22) 55%,transparent 72%);filter:blur(12px);z-index:-1;animation:breathe 3.6s ease-in-out infinite}
.logo img{position:relative;z-index:1;width:100%;height:100%;border-radius:50%;display:block;background:#000;border:3px solid #0a0d12}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes breathe{0%,100%{opacity:.65;transform:scale(.96)}50%{opacity:1;transform:scale(1.06)}}

h1{font-family:'Rajdhani','Segoe UI',sans-serif;font-size:29px;font-weight:700;letter-spacing:.14em;line-height:1;background:linear-gradient(90deg,#9cbfe3,#e8ecf2,#dcc29a);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.sub{margin-top:9px;font-size:10.5px;letter-spacing:.34em;color:var(--muted);text-transform:uppercase;font-weight:500}
.lock-line{display:flex;align-items:center;gap:10px;margin:22px 0 18px;color:var(--muted);font-size:11px;letter-spacing:.08em}
.lock-line::before,.lock-line::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,transparent,rgba(154,147,201,.35))}
.lock-line::after{transform:scaleX(-1)}

form{text-align:left}
label{display:block;font-family:'Rajdhani','Segoe UI',sans-serif;font-size:11px;font-weight:600;letter-spacing:.16em;color:var(--muted);margin-bottom:8px}
.field{position:relative;display:flex;align-items:center;height:52px;background:rgba(10,13,18,.7);border:1px solid rgba(154,147,201,.22);border-radius:14px;transition:border-color .2s,box-shadow .2s}
.field:focus-within{border-color:var(--fire);box-shadow:0 0 0 4px rgba(91,137,185,.12),0 0 28px rgba(91,137,185,.12)}
.field svg{flex:0 0 auto}
.field .ico{width:18px;height:18px;margin-left:15px;color:var(--muted);transition:color .2s}
.field:focus-within .ico{color:var(--fire2)}
.field input{flex:1;min-width:0;height:100%;padding:0 10px 0 12px;background:transparent;border:0;outline:0;color:var(--text);font-family:ui-monospace,'SF Mono',Menlo,Consolas,monospace;font-size:16px;letter-spacing:.22em;text-transform:uppercase}
.field input::placeholder{letter-spacing:.12em;text-transform:none;color:#4a5366;font-family:'DM Sans',sans-serif;font-size:14px}
.eye{width:44px;height:100%;background:none;border:0;color:var(--muted);cursor:pointer;display:grid;place-items:center;transition:color .2s}
.eye:hover{color:var(--text)}.eye svg{width:19px;height:19px}
.err{min-height:20px;margin:9px 2px 0;font-size:12px;color:var(--red);font-weight:500}
.btn{position:relative;width:100%;height:52px;margin-top:6px;border:0;border-radius:14px;cursor:pointer;overflow:hidden;color:#fff;font-family:'Rajdhani','Segoe UI',sans-serif;font-size:16px;font-weight:700;letter-spacing:.16em;display:flex;align-items:center;justify-content:center;gap:10px;
background:linear-gradient(100deg,#4a78a6,#6a96c4);box-shadow:0 10px 30px rgba(91,137,185,.28);transition:transform .15s,box-shadow .2s,filter .2s}
.btn::after{content:'';position:absolute;top:0;bottom:0;width:60px;left:-80px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.35),transparent);transform:skewX(-20deg);transition:left .6s}
.btn:hover{transform:translateY(-2px);box-shadow:0 14px 38px rgba(91,137,185,.42)}.btn:hover::after{left:120%}
.btn:active{transform:scale(.98)}.btn:disabled{cursor:wait;filter:saturate(.7) brightness(.9)}
.btn svg{width:18px;height:18px;transition:transform .2s}.btn:hover svg{transform:translateX(3px)}
.spin{width:18px;height:18px;border:2.5px solid rgba(255,255,255,.35);border-top-color:#fff;border-radius:50%;animation:spin .7s linear infinite}
.tag{margin-top:24px;display:flex;justify-content:center;align-items:center;gap:9px;font-size:10.5px;letter-spacing:.24em;color:var(--muted);font-weight:600;white-space:nowrap}
.tag i{width:4px;height:4px;border-radius:50%;background:var(--fire)}

.shake{animation:shake .5s cubic-bezier(.36,.07,.19,.97)}
@keyframes shake{10%,90%{transform:translateX(-2px)}20%,80%{transform:translateX(4px)}30%,50%,70%{transform:translateX(-7px)}40%,60%{transform:translateX(7px)}}
.card.ok{animation:ok .8s cubic-bezier(.22,1,.36,1) forwards;border-color:rgba(76,195,138,.55)}
.card.ok .logo::before{animation-duration:.8s}
@keyframes ok{to{opacity:0;transform:scale(1.06) translateY(-10px);filter:blur(4px)}}
.flash{position:fixed;inset:0;z-index:5;pointer-events:none;background:radial-gradient(circle at 50% 40%,rgba(76,195,138,.28),transparent 60%);opacity:0;transition:opacity .5s}
.flash.on{opacity:1}
@media(max-width:380px){.card{padding-left:18px;padding-right:18px}h1{font-size:25px}.tag{letter-spacing:.14em}}
@media(max-height:620px){.card{margin-top:78px}}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}}
</style>
</head>
<body>
<canvas id="fx"></canvas>
<div class="scan"></div>
<div class="flash" id="flash"></div>

<div class="wrap">
  <main class="card" id="card">
    <i class="corner c1"></i><i class="corner c2"></i><i class="corner c3"></i><i class="corner c4"></i>
    <div class="logo"><img src="/logo.jpg" alt="SHADMAN" width="128" height="128"></div>

    <h1>SHADMAN LEVEL UP</h1>
    <div class="sub">Secure Access</div>
    <div class="lock-line">ENTER YOUR ACCESS KEY</div>

    <form id="form" autocomplete="off">
      <label for="key">ACCESS KEY</label>
      <div class="field" id="field">
        <svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="15" r="4"/><path d="M10.8 12.2 20 3"/><path d="m16 7 3 3"/><path d="m14 9 2 2"/></svg>
        <input id="key" name="key" type="password" placeholder="Type your key" autocomplete="off" autocapitalize="characters" autocorrect="off" spellcheck="false" maxlength="64" required>
        <button class="eye" id="eye" type="button" aria-label="Show key">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/></svg>
        </button>
      </div>
      <div class="err" id="err" role="alert" aria-live="polite"></div>
      <button class="btn" id="btn" type="submit"><span id="btnTxt">UNLOCK DASHBOARD</span>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m13 6 6 6-6 6"/></svg>
      </button>
    </form>

    <div class="tag"><span>TRUSTED</span><i></i><span>FAST</span><i></i><span>ALWAYS</span></div>
  </main>
</div>

<script>
const $=id=>document.getElementById(id);
const card=$('card'),key=$('key'),err=$('err'),btn=$('btn'),btnTxt=$('btnTxt');
let busy=false,lockTimer=null;

$('eye').addEventListener('click',()=>{const show=key.type==='password';key.type=show?'text':'password';$('eye').setAttribute('aria-label',show?'Hide key':'Show key');key.focus()});
key.addEventListener('input',()=>{err.textContent=''});

function fail(msg){
  err.textContent=msg;
  card.classList.remove('shake');void card.offsetWidth;card.classList.add('shake');
  key.select();
}
function startLock(sec){
  clearInterval(lockTimer);
  btn.disabled=true;
  const tick=()=>{if(sec<=0){clearInterval(lockTimer);btn.disabled=false;err.textContent='';btnTxt.textContent='UNLOCK DASHBOARD';return}
    btnTxt.textContent='LOCKED · '+sec+'s';err.textContent='Too many wrong attempts. Please wait.';sec--};
  tick();lockTimer=setInterval(tick,1000);
}

$('form').addEventListener('submit',async e=>{
  e.preventDefault();
  const v=key.value.trim();
  if(busy||btn.disabled)return;
  if(!v){fail('Please enter your access key.');return}
  busy=true;btn.disabled=true;err.textContent='';
  const old=btn.innerHTML;btn.innerHTML='<span class="spin"></span><span>VERIFYING…</span>';
  try{
    const r=await fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({key:v}),credentials:'same-origin'});
    const d=await r.json().catch(()=>({}));
    if(r.ok&&d.status==='ok'){
      $('flash').classList.add('on');card.classList.add('ok');
      setTimeout(()=>{location.replace('/')},650);
      return;
    }
    btn.innerHTML=old;busy=false;
    if(r.status===429){startLock(Math.max(1,Math.ceil(d.retry_after||60)));return}
    btn.disabled=false;fail(d.error||'Wrong access key. Try again.');
  }catch(ex){
    btn.innerHTML=old;busy=false;btn.disabled=false;fail('Cannot reach the server. Check your connection.');
  }
});
key.focus();

/* ember particles */
(function(){
  if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  const c=$('fx'),x=c.getContext('2d');let W,H,dpr,P=[];
  function size(){dpr=Math.min(devicePixelRatio||1,2);W=innerWidth;H=innerHeight;c.width=W*dpr;c.height=H*dpr;x.setTransform(dpr,0,0,dpr,0,0)}
  function mk(init){return{x:Math.random()*W,y:init?Math.random()*H:H+10,r:Math.random()*1.8+.5,v:Math.random()*.5+.25,d:(Math.random()-.5)*.35,a:Math.random()*.5+.25,h:Math.random()<.72?'134,174,214':'220,194,154',t:Math.random()*6.28}}
  size();addEventListener('resize',size);
  const N=Math.round(Math.min(70,Math.max(28,W*H/20000)));
  for(let i=0;i<N;i++)P.push(mk(true));
  (function loop(){
    x.clearRect(0,0,W,H);
    for(const p of P){
      p.y-=p.v;p.t+=.02;p.x+=p.d+Math.sin(p.t)*.25;
      if(p.y<-10)Object.assign(p,mk(false));
      const al=p.a*Math.min(1,p.y/(H*.35));
      x.beginPath();x.fillStyle='rgba('+p.h+','+Math.max(0,al)+')';x.shadowColor='rgba('+p.h+',.9)';x.shadowBlur=8;
      x.arc(p.x,p.y,p.r,0,6.283);x.fill();
    }
    requestAnimationFrame(loop);
  })();
})();
</script>
</body>
</html>
"""


def _make_session_token(role: str = "admin") -> str:
    exp = str(int(time.time()) + SESSION_DAYS * 86400)
    sig = _hmac.new(_SESSION_SECRET, f"{role}|{exp}".encode(), _hashlib.sha256).hexdigest()
    return f"{role}.{exp}.{sig}"


def _token_role(token: Optional[str]) -> Optional[str]:
    """সঠিক টোকেন হলে role ('admin' / 'user') ফেরত দেয়, নইলে None"""
    if not token:
        return None
    parts = token.split(".")
    if len(parts) != 3:
        return None
    role, exp, sig = parts
    if role not in ("admin", "user") or not exp.isdigit() or int(exp) < time.time():
        return None
    good = _hmac.new(_SESSION_SECRET, f"{role}|{exp}".encode(), _hashlib.sha256).hexdigest()
    return role if _hmac.compare_digest(sig, good) else None


def _client_ip(request: web.Request) -> str:
    fwd = request.headers.get("X-Forwarded-For", "")
    if fwd:
        return fwd.split(",")[0].strip()
    return request.remote or "?"


def _is_https(request: web.Request) -> bool:
    return request.secure or request.headers.get("X-Forwarded-Proto", "").lower() == "https"


def _session_role(request: web.Request) -> Optional[str]:
    return _token_role(request.cookies.get(SESSION_COOKIE))


def _is_authed(request: web.Request) -> bool:
    return _session_role(request) is not None


# ✅ OWNER ID: প্রতিটি User ব্রাউজারের আলাদা পরিচয় (লগআউট করলেও থাকে) — নিজের যোগ করা আইডি চিনতে লাগে
import secrets as _secrets
OWNER_COOKIE = "afx_owner"


def _sign_owner(oid: str) -> str:
    return _hmac.new(_SESSION_SECRET, ("owner|" + oid).encode(), _hashlib.sha256).hexdigest()[:24]


def _owner_id(request: web.Request) -> Optional[str]:
    raw = request.cookies.get(OWNER_COOKIE, "")
    oid, _, sig = raw.partition(".")
    if oid and sig and _hmac.compare_digest(sig, _sign_owner(oid)):
        return oid
    return None


def _owner_cookie_value(oid: str) -> str:
    return f"{oid}.{_sign_owner(oid)}"


@web.middleware
async def auth_middleware(request: web.Request, handler):
    path = request.path
    if path in ("/login", "/api/login", "/logo.jpg", "/favicon.ico"):
        return await handler(request)
    role = _session_role(request)
    if role:
        request["role"] = role
        # User শুধু দেখতে ও Add Account করতে পারবে — বাকি সব API সার্ভারেই আটকানো
        if role == "user" and path not in USER_ALLOWED_PATHS:
            if path.startswith("/api/"):
                return web.json_response({"status": "error", "error": "Admin access only"}, status=403)
            raise web.HTTPFound("/")
        return await handler(request)
    if path.startswith("/api/"):
        return web.json_response({"status": "error", "error": "unauthorized"}, status=401)
    raise web.HTTPFound("/login")


async def handle_login_page(request: web.Request) -> web.Response:
    if _is_authed(request):
        raise web.HTTPFound("/")
    return web.Response(text=LOGIN_HTML, content_type="text/html", charset="utf-8",
                        headers={"Cache-Control": "no-store"})


async def handle_logo(request: web.Request) -> web.Response:
    return web.Response(body=LOGO_JPG, content_type="image/jpeg",
                        headers={"Cache-Control": "public, max-age=86400"})


async def handle_login(request: web.Request) -> web.Response:
    ip = _client_ip(request)
    now = time.time()
    rec = _LOGIN_FAILS.get(ip, {"n": 0, "until": 0})
    if rec["until"] > now:
        return web.json_response(
            {"status": "error", "error": "Too many attempts", "retry_after": int(rec["until"] - now) + 1},
            status=429)
    try:
        data = await request.json()
    except Exception:
        data = {}
    supplied = str(data.get("key", "")).strip()
    # case-insensitive, constant-time compare
    sup = supplied.upper().encode("utf-8")
    role = None
    if _hmac.compare_digest(sup, DASHBOARD_KEY.upper().encode("utf-8")):
        role = "admin"
    elif _hmac.compare_digest(sup, USER_KEY.upper().encode("utf-8")):
        role = "user"
    if role is None:
        rec["n"] = rec.get("n", 0) + 1
        if rec["n"] >= _MAX_FAILS:
            rec = {"n": 0, "until": now + _LOCK_SECONDS}
            _LOGIN_FAILS[ip] = rec
            return web.json_response(
                {"status": "error", "error": "Too many attempts", "retry_after": _LOCK_SECONDS}, status=429)
        _LOGIN_FAILS[ip] = rec
        left = _MAX_FAILS - rec["n"]
        return web.json_response(
            {"status": "error", "error": f"Wrong access key. {left} attempt(s) left."}, status=401)
    _LOGIN_FAILS.pop(ip, None)
    resp = web.json_response({"status": "ok", "role": role})
    if role == "user" and not _owner_id(request):
        resp.set_cookie(OWNER_COOKIE, _owner_cookie_value(_secrets.token_hex(6)), max_age=365 * 86400,
                        httponly=True, samesite="Lax", secure=_is_https(request), path="/")
    resp.set_cookie(SESSION_COOKIE, _make_session_token(role), max_age=SESSION_DAYS * 86400,
                    httponly=True, samesite="Lax", secure=_is_https(request), path="/")
    return resp


async def handle_logout(request: web.Request) -> web.Response:
    resp = web.json_response({"status": "ok"})
    resp.del_cookie(SESSION_COOKIE, path="/")
    return resp


# Global bot state shared between app.py and Web Dashboard
class BotState:
    def __init__(self):
        self.accounts: Dict[str, Dict[str, Any]] = {}
        self.logs: List[Dict[str, Any]] = []
        self.max_logs = 200
        self.total_matches = 0
        self.total_gained_exp = 0
        self.start_time = time.time()
        self.account_workers: Dict[str, asyncio.Task] = {}
        self.refresh_callbacks: Dict[str, Any] = {}
        self.account_credentials: Dict[str, Dict[str, Any]] = {}
        # ✅ DELETE করা UID গুলো ব্ল্যাকলিস্টে রাখা হয়
        # যাতে চলমান worker পুনরায় register করতে না পারে
        # ✅ FIX: এখন ডিস্কে সেভ হয় — redeploy-এর পরেও টিকে থাকে
        self.deleted_uids_file = os.path.join(BASE_DIR, "deleted_uids.json")
        self.deleted_uids: set = set()
        self._load_deleted_uids()
        # ✅ প্রতিটি UID-এর জন্য আলাদা match type — "BR" বা "LONE_WOLF"
        self.match_types: Dict[str, str] = {}
        # ✅ Global ON/OFF — False হলে কোনো আইডি match search করবে না
        self.global_running: bool = True
        # ✅ AUTO-DELETE: gained_exp এই লিমিট পার হলে আইডি অটো ডিলিট হবে
        self.exp_limit: int = 45000
        # ✅ AUTO-DELETE queue: async cleanup-এর জন্য
        self.auto_delete_queue: set = set()
        # ✅ LEVEL LIMIT: আইডির level এই সংখ্যায় পৌঁছালে dashboard থেকে সরে যাবে (0 = বন্ধ)
        # EXP লিমিটের মতোই accounts.json থেকেও স্থায়ীভাবে মুছে যাবে
        self.level_limit: int = 0
        self.level_remove_queue: set = set()
        # ✅ config-এর guest UID → login-এর পর real account id (app.py সেট করে)
        self.guest_alias: Dict[str, str] = {}
        # ✅ OWNERS: config key (guest UID বা tok_xxxx) → যে User যোগ করেছে তার owner id
        self.owners_file = os.path.join(BASE_DIR, "account_owners.json")
        self.account_owner: Dict[str, str] = {}
        self._load_owners()
        # ✅ USER ADD LIMIT: Admin ঠিক করে প্রতিটি User সর্বোচ্চ কয়টি আইডি রাখতে পারবে (0 = সীমাহীন)
        self.settings_file = os.path.join(BASE_DIR, "dashboard_settings.json")
        self.user_add_limit: int = 0
        self._load_settings()

    def set_match_type(self, uid: str, match_type: str):
        """Dashboard থেকে UID-এর match type সেট করা: 'BR' অথবা 'LONE_WOLF'"""
        uid_str = str(uid)
        allowed = {"BR", "LONE_WOLF"}
        if match_type not in allowed:
            match_type = "LONE_WOLF"
        self.match_types[uid_str] = match_type
        if uid_str in self.accounts:
            self.accounts[uid_str]["match_type"] = match_type
            self.accounts[uid_str]["last_updated"] = time.strftime("%H:%M:%S")

    def get_match_type(self, uid: str) -> str:
        """UID-এর বর্তমান match type পড়া — default LONE_WOLF.
        Level == 2 → auto BR. AUTO_LW_LEVEL (default 3) বা বেশি → auto LONE_WOLF."""
        uid_str = str(uid)
        lvl = self.get_account_level(uid_str)

        # ✅ Level 2 → Auto Battle Royale
        if lvl == 2:
            if self.match_types.get(uid_str) != "BR":
                self.match_types[uid_str] = "BR"
                if uid_str in self.accounts:
                    self.accounts[uid_str]["match_type"] = "BR"
                try:
                    self.log(f"[AUTO] UID {uid_str} Level {lvl} → Battle Royale (BR)", "success", uid_str)
                except Exception:
                    pass
            return "BR"

        # ✅ Level >= AUTO_LW_LEVEL (3) → Auto Lone Wolf
        mt = self.match_types.get(uid_str, "LONE_WOLF")
        if mt == "BR" and AUTO_LW_LEVEL > 0 and lvl >= AUTO_LW_LEVEL:
            self.set_match_type(uid_str, "LONE_WOLF")
            try:
                self.log(f"[AUTO] UID {uid_str} Level {lvl} >= {AUTO_LW_LEVEL} → Lone Wolf (LW)", "success", uid_str)
            except Exception:
                pass
            return "LONE_WOLF"
        return mt

    async def _async_auto_delete(self, uid_str: str):
        """45000 EXP পূর্ণ হওয়া আইডির async cleanup: worker cancel + JSON ফাইল থেকে মুছে ফেলা"""
        try:
            short_key = uid_str.replace("tok_", "")[:10]

            # ✅ STEP 1: bot_state থেকে সরাও
            self.accounts.pop(uid_str, None)
            self.recalc_totals()

            # ✅ STEP 2: accounts*.json ফাইল থেকে atomic delete
            for accounts_file in get_all_account_files_dashboard():
                if not os.path.exists(accounts_file):
                    continue
                try:
                    with open(accounts_file, "r", encoding="utf-8") as f:
                        existing = json.load(f)
                    if not isinstance(existing, list):
                        continue
                    new_list = [
                        acc for acc in existing
                        if str(acc.get("uid", "")).strip() not in self._json_ids(uid_str)
                        and str(acc.get("token", ""))[:10] != short_key
                    ]
                    if len(new_list) < len(existing):
                        tmp_file = accounts_file + ".tmp"
                        with open(tmp_file, "w", encoding="utf-8") as f:
                            json.dump(new_list, f, indent=2, ensure_ascii=False)
                        os.replace(tmp_file, accounts_file)
                except Exception:
                    pass

            # ✅ STEP 3: Worker task বাতিল করো
            for worker_key in [uid_str, short_key]:
                if worker_key in self.account_workers:
                    task = self.account_workers.pop(worker_key)
                    task.cancel()
                    try:
                        await asyncio.wait_for(asyncio.shield(task), timeout=3.0)
                    except (asyncio.CancelledError, asyncio.TimeoutError, Exception):
                        pass

            self.auto_delete_queue.discard(uid_str)
            self.log(f"[AUTO-DELETE] UID {uid_str} → 45000 EXP লিমিট পূর্ণ। আইডি সম্পূর্ণরূপে মুছে ফেলা হয়েছে।", "warning", uid_str)
        except Exception as e:
            self.log(f"[AUTO-DELETE ERROR] UID {uid_str}: {e}", "error", uid_str)

    def _load_deleted_uids(self):
        """redeploy-এর পরেও deleted/level-limit আইডি blacklist-এ থাকবে"""
        try:
            if os.path.exists(self.deleted_uids_file):
                with open(self.deleted_uids_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, list):
                    self.deleted_uids = set(str(u) for u in data)
        except Exception:
            self.deleted_uids = set()

    def _save_deleted_uids(self):
        """deleted_uids ডিস্কে সেভ — atomic write"""
        try:
            tmp = self.deleted_uids_file + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(list(self.deleted_uids), f, ensure_ascii=False)
            os.replace(tmp, self.deleted_uids_file)
        except Exception:
            pass

    def _load_settings(self):
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    d = json.load(f)
                if isinstance(d, dict):
                    self.user_add_limit = max(0, int(d.get("user_add_limit", 0) or 0))
                    # ✅ FIX: রিডিপ্লয়ের পরেও exp_limit ও level_limit টিকে থাকবে
                    saved_exp = d.get("exp_limit", None)
                    if saved_exp is not None:
                        self.exp_limit = max(0, int(saved_exp or 0))
                    saved_lv = d.get("level_limit", None)
                    if saved_lv is not None:
                        self.level_limit = max(0, int(saved_lv or 0))
        except Exception:
            self.user_add_limit = 0

    def _save_settings(self):
        try:
            tmp = self.settings_file + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump({
                    "user_add_limit": self.user_add_limit,
                    "exp_limit": self.exp_limit,       # ✅ FIX: persist
                    "level_limit": self.level_limit,   # ✅ FIX: persist
                }, f, indent=2)
            os.replace(tmp, self.settings_file)
        except Exception:
            pass

    def count_user_ids(self, owner: str, existing: list) -> int:
        """এই User-এর যোগ করা আইডি, যেগুলো এখনো accounts.json-এ আছে (অটো-ডিলিট/ডিলিট হলে সংখ্যা কমে)"""
        present = set()
        for acc in existing:
            if not isinstance(acc, dict):
                continue
            if acc.get("uid") is not None:
                present.add(str(acc.get("uid")))
            if acc.get("token"):
                present.add("tok_" + str(acc["token"])[:10])
        return sum(1 for k, v in self.account_owner.items() if v == owner and k in present)

    def _load_owners(self):
        try:
            if os.path.exists(self.owners_file):
                with open(self.owners_file, "r", encoding="utf-8") as f:
                    d = json.load(f)
                if isinstance(d, dict):
                    self.account_owner = {str(k): str(v) for k, v in d.items()}
        except Exception:
            self.account_owner = {}

    def _save_owners(self):
        try:
            tmp = self.owners_file + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(self.account_owner, f, indent=2, ensure_ascii=False)
            os.replace(tmp, self.owners_file)
        except Exception:
            pass

    def owner_of(self, key: str) -> Optional[str]:
        """ড্যাশবোর্ড key (guest হলে login-এর পর real id) থেকে মালিক খোঁজে"""
        key = str(key)
        o = self.account_owner.get(key)
        if o:
            return o
        for guest, real in self.guest_alias.items():
            if real == key and guest in self.account_owner:
                return self.account_owner[guest]
        return None

    def _json_ids(self, uid_str: str) -> set:
        """accounts.json-এ এই আইডি যে নামে আছে (guest UID হলে login-এর আগের UID-ও)"""
        ids = {uid_str}
        for guest, real in self.guest_alias.items():
            if real == uid_str:
                ids.add(guest)
        return ids

    def _remove_from_json(self, uid_str: str):
        """accounts*.json থেকে আইডি স্থায়ীভাবে মুছে ফেলে (atomic write)"""
        short_key = uid_str.replace("tok_", "")[:10]
        ids = self._json_ids(uid_str)
        for accounts_file in get_all_account_files_dashboard():
            if not os.path.exists(accounts_file):
                continue
            try:
                with open(accounts_file, "r", encoding="utf-8") as f:
                    existing = json.load(f)
                if not isinstance(existing, list):
                    continue
                new_list = [
                    acc for acc in existing
                    if str(acc.get("uid", "")).strip() not in ids
                    and str(acc.get("token", ""))[:10] != short_key
                ]
                if len(new_list) < len(existing):
                    tmp_file = accounts_file + ".tmp"
                    with open(tmp_file, "w", encoding="utf-8") as f:
                        json.dump(new_list, f, indent=2, ensure_ascii=False)
                    os.replace(tmp_file, accounts_file)
            except Exception:
                pass

    async def _async_level_remove(self, uid_str: str):
        """Level লিমিট পূর্ণ হলে: শুধু worker বন্ধ করা।
        accounts ও JSON check_level_limit()-এই synchronously মুছে ফেলা হয়েছে।"""
        try:
            short_key = uid_str.replace("tok_", "")[:10]
            # ✅ accounts & JSON ইতিমধ্যে check_level_limit()-এ মুছে ফেলা হয়েছে
            # শুধু worker task cancel করতে হবে
            for worker_key in [uid_str, short_key]:
                if worker_key in self.account_workers:
                    task = self.account_workers.pop(worker_key)
                    task.cancel()
                    try:
                        await asyncio.wait_for(asyncio.shield(task), timeout=3.0)
                    except (asyncio.CancelledError, asyncio.TimeoutError, Exception):
                        pass
            self.log(f"[LEVEL-LIMIT] UID {uid_str} → worker বন্ধ করা হয়েছে।", "warning", uid_str)
        except Exception as e:
            self.log(f"[LEVEL-LIMIT ERROR] UID {uid_str}: {e}", "error", uid_str)
        finally:
            self.level_remove_queue.discard(uid_str)

    def check_level_limit(self, uid_str: str):
        """আইডির level লিমিটে পৌঁছালে সাথে সাথে blacklist করে সরিয়ে দেয়"""
        if self.level_limit <= 0 or uid_str in self.level_remove_queue or uid_str in self.deleted_uids:
            return
        acc = self.accounts.get(uid_str)
        if not acc:
            return
        try:
            lv = int(acc.get("level", 1) or 1)
        except (ValueError, TypeError):
            return
        if lv >= self.level_limit:
            self.level_remove_queue.add(uid_str)
            self.deleted_uids.add(uid_str)      # reload না চাপা পর্যন্ত আর register/start হবে না
            self._save_deleted_uids()           # ✅ FIX: redeploy-এর পরেও blacklist টিকে থাকবে
            self.match_types.pop(uid_str, None)

            # ✅ FIX: Dashboard থেকে সাথে সাথে (synchronously) মুছে ফেলো।
            # আগে শুধু async task-এর উপর নির্ভর করত — task fail হলে account
            # "Offline" হয়ে dashboard-এ রয়ে যেত। এখন এখানেই মুছে যাবে।
            self.accounts.pop(uid_str, None)
            self.recalc_totals()
            self._remove_from_json(uid_str)     # accounts.json থেকেও এখনই মুছে ফেলো
            self.log(
                f"[LEVEL-LIMIT] UID {uid_str} → Lv{lv} (লিমিট: Lv{self.level_limit})। "
                f"আইডি dashboard ও accounts.json থেকে মুছে ফেলা হয়েছে।",
                "warning", uid_str
            )
            # Worker cancel async-এ করা হবে
            try:
                asyncio.get_event_loop().create_task(self._async_level_remove(uid_str))
            except RuntimeError:
                # Event loop না থাকলেও কোনো সমস্যা নেই — account ইতিমধ্যে মুছে গেছে
                self.level_remove_queue.discard(uid_str)

    def enforce_level_limit(self):
        """লিমিট সেট/পরিবর্তনের সময় চলমান সব আইডি যাচাই"""
        for uid_str in list(self.accounts.keys()):
            self.check_level_limit(uid_str)

    def get_account_level(self, uid: str) -> int:
        """UID-এর current level পড়া — default 1"""
        uid_str = str(uid)
        if uid_str in self.accounts:
            return int(self.accounts[uid_str].get("level", 1) or 1)
        return 1

    def log(self, message: str, level: str = "info", uid: Optional[str] = None):
        entry = {
            "time": time.strftime("%H:%M:%S"),
            "level": level,
            "message": message,
            "uid": uid
        }
        self.logs.append(entry)
        if len(self.logs) > self.max_logs:
            self.logs.pop(0)

    def register_account(self, uid: str, nickname: str, region: str, level: int, exp: int, likes: int = 0):
        uid_str = str(uid)
        # ✅ ব্ল্যাকলিস্টে থাকলে re-register করবে না — এটাই মূল সমস্যা ছিল
        if uid_str in self.deleted_uids:
            return
        if uid_str not in self.accounts:
            self.accounts[uid_str] = {
                "uid": uid_str,
                "nickname": nickname or f"Player_{uid_str[:6]}",
                "region": region or "BD",
                "level": level or 1,
                "initial_exp": exp,
                "current_exp": exp,
                "gained_exp": 0,
                "likes": likes or 0,
                "status": "ONLINE",
                "matches_played": 0,
                "active_matches": 0,
                "last_match_time": None,
                "last_updated": time.strftime("%H:%M:%S"),
                "match_type": self.match_types.get(uid_str, "LONE_WOLF")
            }
        else:
            acc = self.accounts[uid_str]
            if nickname:
                acc["nickname"] = nickname
            if region:
                acc["region"] = region
            if level:
                acc["level"] = level
                self.get_match_type(uid_str)   # level barhle BR -> LW auto switch
            acc["current_exp"] = exp
            acc["gained_exp"] = max(0, exp - acc["initial_exp"])
            acc["likes"] = likes
            acc["status"] = "ONLINE"
            acc["last_updated"] = time.strftime("%H:%M:%S")
        self.recalc_totals()
        self.check_level_limit(uid_str)

    def update_exp(self, uid: str, current_exp: int, level: Optional[int] = None):
        uid_str = str(uid)
        # ✅ ডিলিট করা আইডি আপডেট হবে না
        if uid_str in self.deleted_uids:
            return
        if uid_str in self.accounts:
            acc = self.accounts[uid_str]
            old_exp = acc["current_exp"]
            acc["current_exp"] = current_exp
            if level is not None and level > 0:
                acc["level"] = level
                self.get_match_type(uid_str)   # level barhle BR -> LW auto switch
            acc["gained_exp"] = max(0, current_exp - acc["initial_exp"])
            acc["last_updated"] = time.strftime("%H:%M:%S")
            diff = current_exp - old_exp
            if diff > 0:
                self.log(f"Account {acc['nickname']} ({uid_str}) gained +{diff} EXP! Total: +{acc['gained_exp']}", "success", uid_str)
            self.recalc_totals()
            self.check_level_limit(uid_str)

            # ✅ AUTO-DELETE: gained_exp ≥ exp_limit হলে আইডি অটোমেটিক মুছে যাবে
            if self.exp_limit > 0 and acc["gained_exp"] >= self.exp_limit and uid_str not in self.auto_delete_queue:
                self.auto_delete_queue.add(uid_str)
                nickname = acc.get("nickname", uid_str)
                # তৎক্ষণাৎ blacklist করো — worker আর কোনো match খেলবে না
                self.deleted_uids.add(uid_str)
                self._save_deleted_uids()       # ✅ FIX: redeploy-এর পরেও blacklist টিকে থাকবে
                self.match_types.pop(uid_str, None)
                # ✅ FIX: Dashboard ও JSON থেকে সাথে সাথে (synchronously) মুছে ফেলো।
                # আগে শুধু async task-এর উপর নির্ভর করত — task fail হলে account
                # "Offline" হয়ে dashboard-এ রয়ে যেত। এখন level_limit-এর মতোই
                # synchronous removal করা হচ্ছে।
                self.accounts.pop(uid_str, None)
                self.recalc_totals()
                self._remove_from_json(uid_str)
                self.log(
                    f"[AUTO-DELETE] {nickname} ({uid_str}) → {acc['gained_exp']} EXP অর্জন করেছে "
                    f"(লিমিট: {self.exp_limit})। আইডি dashboard ও accounts.json থেকে মুছে ফেলা হয়েছে।",
                    "warning", uid_str
                )
                # Async cleanup: এখন শুধু worker task cancel করতে হবে
                try:
                    asyncio.get_event_loop().create_task(
                        self._async_auto_delete(uid_str)
                    )
                except RuntimeError:
                    self.auto_delete_queue.discard(uid_str)

    def update_status(self, uid: str, status: str, active_matches: Optional[int] = None):
        uid_str = str(uid)
        # ✅ ডিলিট করা আইডি status update হবে না
        if uid_str in self.deleted_uids:
            return
        if uid_str in self.accounts:
            self.accounts[uid_str]["status"] = status
            if status in ("ONLINE", "IN_MATCH", "SEARCHING"):
                self.accounts[uid_str].pop("last_error", None)
            if active_matches is not None:
                self.accounts[uid_str]["active_matches"] = active_matches
            self.accounts[uid_str]["last_updated"] = time.strftime("%H:%M:%S")

    def set_error(self, uid: str, message: str):
        uid_str = str(uid)
        if uid_str in self.deleted_uids:
            return
        if uid_str in self.accounts:
            self.accounts[uid_str]["last_error"] = f"{time.strftime('%H:%M:%S')} - {message}"[:300]

    def set_info(self, uid: str, message: str):
        uid_str = str(uid)
        if uid_str in self.deleted_uids:
            return
        if uid_str in self.accounts:
            self.accounts[uid_str]["last_info"] = f"{time.strftime('%H:%M:%S')} - {message}"[:300]

    def increment_match(self, uid: str):
        uid_str = str(uid)
        self.total_matches += 1
        if uid_str in self.accounts:
            self.accounts[uid_str]["matches_played"] += 1
            self.accounts[uid_str]["last_match_time"] = time.strftime("%H:%M:%S")
            self.accounts[uid_str]["last_updated"] = time.strftime("%H:%M:%S")
            self.log(f"Account {self.accounts[uid_str]['nickname']} finished Match #{self.accounts[uid_str]['matches_played']}", "info", uid_str)

    def recalc_totals(self):
        self.total_gained_exp = sum(acc.get("gained_exp", 0) for acc in self.accounts.values())


bot_state = BotState()


# ==================== HTTP HANDLERS ====================

async def handle_index(request: web.Request) -> web.Response:
    # HTML is embedded — always works regardless of file system state
    return web.Response(text=DASHBOARD_HTML, content_type="text/html", charset="utf-8")


async def handle_get_stats(request: web.Request) -> web.Response:
    role = request.get("role", "admin")
    accounts_data = list(bot_state.accounts.values())
    logs = bot_state.logs[-60:]
    total_matches = bot_state.total_matches
    total_exp = bot_state.total_gained_exp
    if role == "user":
        # ✅ User শুধু নিজের যোগ করা আইডি ও সেগুলোর লগ দেখবে
        me = _owner_id(request)
        accounts_data = [a for a in accounts_data if me and bot_state.owner_of(str(a.get("uid"))) == me]
        logs = [l for l in bot_state.logs if l.get("uid") and me and bot_state.owner_of(str(l["uid"])) == me][-60:]
        total_matches = sum(int(a.get("matches_played", 0) or 0) for a in accounts_data)
        total_exp = sum(int(a.get("gained_exp", 0) or 0) for a in accounts_data)
    # ✅ বেশি লেভেল উপরে (descending); একই লেভেল হলে বেশি gained EXP আগে
    accounts_data.sort(key=lambda x: (int(x.get("level", 0) or 0), x.get("gained_exp", 0)), reverse=True)
    return web.json_response({
        "total_accounts": len(accounts_data),
        "total_matches": total_matches,
        "total_gained_exp": total_exp,
        "accounts": accounts_data,
        "logs": logs,
        "uptime": int(time.time() - bot_state.start_time),
        "global_running": bot_state.global_running,
        "exp_limit": bot_state.exp_limit,
        "level_limit": bot_state.level_limit,
        "user_add_limit": bot_state.user_add_limit,
        "role": role
    })


def _check_user_limit(role: str, owner: Optional[str], owner_key: str, existing: list) -> Optional[str]:
    """User-এর আইডি লিমিট পূর্ণ হলে error মেসেজ ফেরত দেয়। Admin-এর কোনো লিমিট নেই।"""
    lim = bot_state.user_add_limit
    if role != "user" or lim <= 0 or not owner:
        return None
    # নিজের আগে যোগ করা আইডি আবার যোগ করলে নতুন স্লট লাগে না
    if bot_state.account_owner.get(owner_key) == owner:
        return None
    if bot_state.count_user_ids(owner, existing) >= lim:
        return f"ID limit reached. You can add up to {lim} ID(s) only."
    return None


async def handle_add_account(request: web.Request) -> web.Response:
    try:
        data = await request.json()
        role = request.get("role", "admin")
        new_owner_cookie = None
        owner = None
        if role == "user":
            owner = _owner_id(request)
            if not owner:
                owner = _secrets.token_hex(6)
                new_owner_cookie = _owner_cookie_value(owner)
        accounts_file = ACCOUNTS_FILE_PATH
        existing = []
        if os.path.exists(accounts_file):
            try:
                with open(accounts_file, "r", encoding="utf-8") as f:
                    existing = json.load(f)
            except Exception:
                existing = []

        if "uid" in data and "password" in data:
            uid = str(data["uid"]).strip()
            pwd = str(data["password"]).strip()
            if not uid or not pwd:
                return web.json_response({"status": "error", "error": "UID and Password are required"})
            owner_key = uid
            if role == "user" and (any(str(acc.get("uid")) == uid for acc in existing) or uid in bot_state.accounts) \
                    and bot_state.account_owner.get(uid) != owner:
                return web.json_response({"status": "error", "error": "This account already exists"})
            lim_err = _check_user_limit(role, owner, owner_key, existing)
            if lim_err:
                return web.json_response({"status": "error", "error": lim_err})
            existing = [acc for acc in existing if str(acc.get("uid")) != uid]
            existing.append({"uid": uid, "password": pwd})
            # ✅ Re-add করলে blacklist থেকে সরাও — না হলে আর চালু হবে না
            bot_state.deleted_uids.discard(uid)
            bot_state._save_deleted_uids()  # ✅ FIX: ফাইল থেকেও সরাও
        elif "token" in data:
            token = str(data["token"]).strip()
            if not token:
                return web.json_response({"status": "error", "error": "Token is required"})
            owner_key = f"tok_{token[:10]}"
            if role == "user" and (any(acc.get("token") == token for acc in existing) or owner_key in bot_state.accounts) \
                    and bot_state.account_owner.get(owner_key) != owner:
                return web.json_response({"status": "error", "error": "This account already exists"})
            lim_err = _check_user_limit(role, owner, owner_key, existing)
            if lim_err:
                return web.json_response({"status": "error", "error": lim_err})
            existing = [acc for acc in existing if acc.get("token") != token]
            existing.append({"token": token})
            # ✅ Token re-add করলে blacklist থেকে সরাও
            bot_state.deleted_uids.discard(token[:10])
            bot_state.deleted_uids.discard(f"tok_{token[:10]}")
            bot_state._save_deleted_uids()  # ✅ FIX: ফাইল থেকেও সরাও
        else:
            return web.json_response({"status": "error", "error": "Invalid payload"})

        with open(accounts_file, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2)

        # মালিক নথিভুক্ত করো (User হলে) — Admin যোগ করলে মালিক থাকে না, শুধু Admin দেখবে
        if role == "user" and owner:
            bot_state.account_owner[owner_key] = owner
            bot_state._save_owners()
        elif role == "admin":
            if bot_state.account_owner.pop(owner_key, None) is not None:
                bot_state._save_owners()

        bot_state.log(f"New account added: {data.get('uid') or 'Token'}", "success", owner_key)

        # Trigger dynamic worker launch
        if "on_account_added" in bot_state.refresh_callbacks:
            asyncio.create_task(bot_state.refresh_callbacks["on_account_added"](data))

        resp = web.json_response({"status": "ok"})
        if new_owner_cookie:
            resp.set_cookie(OWNER_COOKIE, new_owner_cookie, max_age=365 * 86400,
                            httponly=True, samesite="Lax", secure=_is_https(request), path="/")
        return resp
    except Exception as e:
        return web.json_response({"status": "error", "error": str(e)})


async def handle_delete_account(request: web.Request) -> web.Response:
    try:
        data = await request.json()
        uid = str(data.get("uid", "")).strip()
        if not uid:
            return web.json_response({"status": "error", "error": "uid missing"})

        # token-based worker key: "tok_abcdefghij" → "abcdefghij"
        short_key = uid.replace("tok_", "")[:10]

        # ✅ সব accounts*.json ফাইলে খুঁজে atomic write দিয়ে delete করে
        for accounts_file in get_all_account_files_dashboard():
            if not os.path.exists(accounts_file):
                continue
            try:
                with open(accounts_file, "r", encoding="utf-8") as f:
                    existing = json.load(f)
                if not isinstance(existing, list):
                    continue

                new_list = [
                    acc for acc in existing
                    if str(acc.get("uid", "")).strip() != uid
                    and str(acc.get("token", ""))[:10] != short_key
                ]

                if len(new_list) < len(existing):
                    # ✅ Atomic write — crash হলে ফাইল নষ্ট হবে না
                    tmp_file = accounts_file + ".tmp"
                    with open(tmp_file, "w", encoding="utf-8") as f:
                        json.dump(new_list, f, indent=2, ensure_ascii=False)
                    os.replace(tmp_file, accounts_file)
            except Exception:
                pass

        # ✅ STEP 1: আগেই ব্ল্যাকলিস্টে যোগ করো
        # এর ফলে চলমান worker আর re-register করতে পারবে না
        bot_state.deleted_uids.add(uid)
        bot_state.deleted_uids.add(short_key)
        bot_state._save_deleted_uids()  # ✅ FIX: redeploy-এর পরেও blacklist টিকে থাকবে

        # ✅ STEP 2: bot_state থেকে সরাও এবং totals আপডেট করো
        if uid in bot_state.accounts:
            del bot_state.accounts[uid]
            bot_state.recalc_totals()

        # ✅ STEP 3: Worker বাতিল করো এবং সম্পূর্ণভাবে await করো
        # break ছিল আগে — এর ফলে দুটো key-এর একটাই cancel হতো
        # এখন দুটোই cancel করা হবে এবং properly await করা হবে
        for worker_key in [uid, short_key]:
            if worker_key in bot_state.account_workers:
                task = bot_state.account_workers.pop(worker_key)
                task.cancel()
                try:
                    await asyncio.wait_for(asyncio.shield(task), timeout=3.0)
                except (asyncio.CancelledError, asyncio.TimeoutError, Exception):
                    pass  # cancel হয়েছে — এটাই স্বাভাবিক

        bot_state.log(f"Account {uid} deleted from dashboard and accounts.json.", "warning", uid)
        return web.json_response({"status": "ok"})
    except Exception as e:
        return web.json_response({"status": "error", "error": str(e)})


async def handle_refresh_account(request: web.Request) -> web.Response:
    try:
        data = await request.json()
        uid = str(data.get("uid")).strip()
        if "on_refresh_account" in bot_state.refresh_callbacks:
            asyncio.create_task(bot_state.refresh_callbacks["on_refresh_account"](uid))
        return web.json_response({"status": "ok"})
    except Exception as e:
        return web.json_response({"status": "error", "error": str(e)})


async def handle_reload_accounts(request: web.Request) -> web.Response:
    """
    accounts*.json ফাইল থেকে নতুন করে সব account load করে।
    - deleted_uids blacklist পুরোপুরি clear হয়
    - যে accounts এখন চলছে না কিন্তু JSON এ আছে সেগুলো স্বয়ংক্রিয়ভাবে চালু হয়
    - ইতিমধ্যে চলমান accounts অপরিবর্তিত থাকে
    """
    try:
        # ✅ STEP 1: পুরো blacklist clear করো
        cleared = len(bot_state.deleted_uids)
        bot_state.deleted_uids.clear()
        bot_state.level_remove_queue.clear()
        bot_state._save_deleted_uids()  # ✅ FIX: ফাইলও clear করো

        # ✅ STEP 2: app.py-এর reload callback ডাকো
        added = 0
        if "on_reload_accounts" in bot_state.refresh_callbacks:
            added = await bot_state.refresh_callbacks["on_reload_accounts"]()

        msg = f"Reload complete: {cleared} blacklisted UIDs cleared, {added} new account(s) started."
        bot_state.log(msg, "success")
        return web.json_response({"status": "ok", "message": msg, "cleared": cleared, "started": added})
    except Exception as e:
        return web.json_response({"status": "error", "error": str(e)})


async def handle_set_match_type(request: web.Request) -> web.Response:
    """Dashboard থেকে UID-এর match type পরিবর্তন করা: BR অথবা LONE_WOLF"""
    try:
        data = await request.json()
        uid = str(data.get("uid", "")).strip()
        match_type = str(data.get("match_type", "LONE_WOLF")).strip().upper()
        if not uid:
            return web.json_response({"status": "error", "error": "UID required"}, status=400)
        if match_type not in ("BR", "LONE_WOLF"):
            return web.json_response({"status": "error", "error": "Invalid match_type. Use BR or LONE_WOLF"}, status=400)
        bot_state.set_match_type(uid, match_type)
        label = "⚔ Battle Royale" if match_type == "BR" else "🐺 Lone Wolf"
        bot_state.log(f"[MATCH TYPE] UID {uid} → {label}", "info", uid)
        return web.json_response({"status": "ok", "uid": uid, "match_type": match_type})
    except Exception as e:
        return web.json_response({"status": "error", "error": str(e)}, status=500)


async def handle_toggle_global(request: web.Request) -> web.Response:
    """সব আইডি ON/OFF করা — running=true হলে ম্যাচ শুরু, false হলে বন্ধ"""
    try:
        data = await request.json()
        running = bool(data.get("running", True))
        bot_state.global_running = running
        state_str = "চালু (ON)" if running else "বন্ধ (OFF)"
        bot_state.log(f"[GLOBAL] সব বট {state_str} করা হয়েছে", "success" if running else "warning")

        # If turning OFF, update all account statuses to PAUSED
        if not running:
            for uid_str in list(bot_state.accounts.keys()):
                if uid_str not in bot_state.deleted_uids:
                    status = bot_state.accounts[uid_str].get("status", "ONLINE")
                    if status not in ("OFFLINE", "ERROR", "CONNECTING"):
                        bot_state.accounts[uid_str]["status"] = "PAUSED"
        else:
            # Turning ON — reset PAUSED statuses to ONLINE
            for uid_str in list(bot_state.accounts.keys()):
                if uid_str not in bot_state.deleted_uids:
                    if bot_state.accounts[uid_str].get("status") == "PAUSED":
                        bot_state.accounts[uid_str]["status"] = "ONLINE"

        return web.json_response({"status": "ok", "running": running})
    except Exception as e:
        return web.json_response({"status": "error", "error": str(e)}, status=500)


async def handle_set_all_mode(request: web.Request) -> web.Response:
    """ড্যাশবোর্ডের সব আইডির match type একসাথে পরিবর্তন করা"""
    try:
        data = await request.json()
        mode = str(data.get("mode", "LONE_WOLF")).strip().upper()
        if mode not in ("BR", "LONE_WOLF", "AUTO"):
            return web.json_response({"status": "error", "error": "Invalid mode. Use BR, LONE_WOLF or AUTO"}, status=400)

        changed = 0
        if mode == "AUTO":
            # ✅ AUTO: সব আইডির manually-forced match_type সরিয়ে দেওয়া
            # get_match_type() এর Level-based auto-logic আবার কাজ করবে
            for uid_str in list(bot_state.accounts.keys()):
                if uid_str not in bot_state.deleted_uids:
                    # match_types থেকে সরালে get_match_type() নিজেই level দেখে সিদ্ধান্ত নেবে
                    bot_state.match_types.pop(uid_str, None)
                    if uid_str in bot_state.accounts:
                        lvl = bot_state.get_account_level(uid_str)
                        auto_mt = "BR" if lvl == 2 else "LONE_WOLF"
                        bot_state.accounts[uid_str]["match_type"] = auto_mt
                    changed += 1
            label = "🔄 Auto Level Mode"
        else:
            for uid_str in list(bot_state.accounts.keys()):
                if uid_str not in bot_state.deleted_uids:
                    bot_state.set_match_type(uid_str, mode)
                    changed += 1
            label = "⚔ Battle Royale" if mode == "BR" else "🐺 Lone Wolf"

        bot_state.log(f"[GLOBAL MODE] সব {changed}টি আইডি → {label}", "success")
        return web.json_response({"status": "ok", "mode": mode, "changed": changed})
    except Exception as e:
        return web.json_response({"status": "error", "error": str(e)}, status=500)


async def handle_set_exp_limit(request: web.Request) -> web.Response:
    """EXP লিমিট আপডেট করা — এই সীমা পার হলে আইডি অটো ডিলিট হবে"""
    try:
        data = await request.json()
        raw = data.get("exp_limit", None)
        if raw is None:
            return web.json_response({"status": "error", "error": "exp_limit missing"}, status=400)
        try:
            limit = int(str(raw).strip().replace(",", ""))
        except (ValueError, TypeError):
            return web.json_response({"status": "error", "error": "exp_limit must be a number"}, status=400)
        if limit < 0:
            return web.json_response({"status": "error", "error": "exp_limit cannot be negative"}, status=400)
        bot_state.exp_limit = limit
        bot_state._save_settings()  # ✅ FIX: redeploy-এর পরেও টিকে থাকবে
        msg = f"EXP লিমিট সেট: {limit:,}" if limit > 0 else "EXP লিমিট বন্ধ (0 = কোনো লিমিট নেই)"
        bot_state.log(f"[EXP LIMIT] {msg}", "success")
        return web.json_response({"status": "ok", "exp_limit": limit})
    except Exception as e:
        return web.json_response({"status": "error", "error": str(e)}, status=500)


async def handle_set_level_limit(request: web.Request) -> web.Response:
    """Level লিমিট সেট — আইডি এই level-এ পৌঁছালে dashboard থেকে সরে যাবে (0 = বন্ধ)"""
    try:
        data = await request.json()
        raw = data.get("level_limit", None)
        if raw is None:
            return web.json_response({"status": "error", "error": "level_limit missing"}, status=400)
        try:
            limit = int(str(raw).strip())
        except (ValueError, TypeError):
            return web.json_response({"status": "error", "error": "level_limit must be a number"}, status=400)
        if limit == 1 or limit < 0 or limit > 200:
            return web.json_response({"status": "error", "error": "Level লিমিট 0 (বন্ধ) অথবা 2 থেকে 200 এর মধ্যে দিন"}, status=400)
        bot_state.level_limit = limit
        bot_state._save_settings()  # ✅ FIX: redeploy-এর পরেও টিকে থাকবে
        msg = f"Level লিমিট সেট: Lv{limit}" if limit > 0 else "Level লিমিট বন্ধ (0 = কোনো লিমিট নেই)"
        bot_state.log(f"[LEVEL LIMIT] {msg}", "success")
        bot_state.enforce_level_limit()
        return web.json_response({"status": "ok", "level_limit": limit})
    except Exception as e:
        return web.json_response({"status": "error", "error": str(e)}, status=500)


async def handle_set_user_limit(request: web.Request) -> web.Response:
    """প্রতিটি User সর্বোচ্চ কয়টি আইডি যোগ করতে পারবে — শুধু Admin ঠিক করে (0 = সীমাহীন)"""
    try:
        data = await request.json()
        raw = data.get("user_add_limit", None)
        if raw is None:
            return web.json_response({"status": "error", "error": "user_add_limit missing"}, status=400)
        try:
            limit = int(str(raw).strip())
        except (ValueError, TypeError):
            return web.json_response({"status": "error", "error": "user_add_limit must be a number"}, status=400)
        if limit < 0 or limit > 100000:
            return web.json_response({"status": "error", "error": "user_add_limit must be 0 to 100000"}, status=400)
        bot_state.user_add_limit = limit
        bot_state._save_settings()
        msg = f"প্রতি User সর্বোচ্চ {limit}টি আইডি" if limit > 0 else "User ID লিমিট বন্ধ (0 = সীমাহীন)"
        bot_state.log(f"[USER LIMIT] {msg}", "success")
        return web.json_response({"status": "ok", "user_add_limit": limit})
    except Exception as e:
        return web.json_response({"status": "error", "error": str(e)}, status=500)


async def handle_clear_logs(request: web.Request) -> web.Response:
    """Activity Log পরিষ্কার করা"""
    bot_state.logs.clear()
    return web.json_response({"status": "ok"})


async def start_web_dashboard(host: str = "0.0.0.0", port: int = 5000):
    app = web.Application(middlewares=[auth_middleware])
    app.router.add_get("/login", handle_login_page)
    app.router.add_post("/api/login", handle_login)
    app.router.add_post("/api/logout", handle_logout)
    app.router.add_get("/logo.jpg", handle_logo)
    app.router.add_get("/", handle_index)
    app.router.add_get("/api/stats", handle_get_stats)
    app.router.add_post("/api/account/add", handle_add_account)
    app.router.add_post("/api/account/delete", handle_delete_account)
    app.router.add_post("/api/account/refresh", handle_refresh_account)
    app.router.add_post("/api/accounts/reload", handle_reload_accounts)
    app.router.add_post("/api/account/match-type", handle_set_match_type)
    app.router.add_post("/api/bot/toggle", handle_toggle_global)
    app.router.add_post("/api/accounts/set-all-mode", handle_set_all_mode)
    app.router.add_post("/api/settings/exp-limit", handle_set_exp_limit)
    app.router.add_post("/api/settings/level-limit", handle_set_level_limit)
    app.router.add_post("/api/settings/user-limit", handle_set_user_limit)
    app.router.add_post("/api/logs/clear", handle_clear_logs)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()
    print(f"\033[92m[+] Web Dashboard running on http://localhost:{port}\033[0m")
