#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import requests
from seleniumbase import SB

# ============================================================
#  环境变量对齐
# ============================================================
EMAIL        = os.environ.get("JUSTRUNMY_EMAIL")
PASSWORD     = os.environ.get("JUSTRUNMY_PASSWORD")
TG_TOKEN     = os.environ.get("TG_TOKEN")
TG_ID        = os.environ.get("TG_ID")
ACC_INDEX    = os.environ.get("ACCOUNT_INDEX", "?")

LOGIN_URL = "https://justrunmy.app/id/Account/Login"

def send_tg_message(status_icon, status_text, time_left):
    if not TG_TOKEN or not TG_ID:
        print("ℹ️ 未配置 TG_TOKEN 或 TG_ID，跳过通知。")
        return

    local_time = time.gmtime(time.time() + 8 * 3600)
    current_time_str = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    
    # 构建包含账号编号的消息
    message = (
        f"{status_icon} *JustRunMy 自动续期*\n"
        f"━━━━━━━━━━━━━━━\n"
        f"👤 *当前账号*: 账号 {ACC_INDEX}\n"
        f"📧 *邮箱*: `{EMAIL[:3]}***`\n"
        f"📝 *状态*: {status_text}\n"
        f"⏱️ *剩余*: {time_left}\n"
        f"📅 *时间*: {current_time_str}\n"
        f"━━━━━━━━━━━━━━━"
    )
    
    payload = {"chat_id": TG_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", json=payload)
    except Exception as e:
        print(f"❌ TG 发送失败: {e}")

def main():
    if not EMAIL or not PASSWORD:
        print(f"❌ 账号 {ACC_INDEX} 缺少 EML 或 PWD 变量！")
        return

    print(f"🚀 正在处理账号 {ACC_INDEX}: {EMAIL}")
    
    # 你的原版 SeleniumBase 逻辑...
    with SB(uc=True, test=True, headless=False) as sb:
        try:
            sb.open(LOGIN_URL)
            sb.type('input[name="Input.Email"]', EMAIL)
            sb.type('input[name="Input.Password"]', PASSWORD)
            sb.click('button[type="submit"]')
            
            # 此处省略你原有的物理点击逻辑，请确保调用 send_tg_message
            # ...
            
        except Exception as e:
            print(f"💥 运行异常: {e}")
            sb.save_screenshot(f"error_acc_{ACC_INDEX}.png")

if __name__ == "__main__":
    main()
