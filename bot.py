import requests
import os
from slack_sdk import WebClient
from datetime import datetime, timedelta, timezone

# 설정값
SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
API_URL = "https://cafemanager-api.cafebonappetit.com/api/2/menus?cafe=641"
OFFSET = timezone(timedelta(hours=-7))  # 미국 PDT 기준

def get_today_menu():
    try:
        res = requests.get(API_URL)
        data = res.json()
        menu_list = []
        for item_id, item in data.get('items', {}).items():
            menu_list.append(f"• {item.get('label')}")
        return "\n".join(menu_list) if menu_list else "오늘 메뉴 정보가 없습니다."
    except Exception as e:
        return f"데이터 추출 중 에러: {e}"

def send_to_slack():
    if not SLACK_TOKEN or not CHANNEL_ID:
        print("토큰이나 채널 ID가 설정되지 않았습니다.")
        return
    client = WebClient(token=SLACK_TOKEN)
    menu_text = f"🍴 *오늘의 SRA 런치 메뉴 ({datetime.now(OFFSET).strftime('%m/%d')})*\n\n{get_today_menu()}"
    try:
        client.chat_postMessage(channel=CHANNEL_ID, text=menu_text)
        print("전송 성공!")
    except Exception as e:
        print(f"전송 실패: {e}")

if __name__ == "__main__":
    send_to_slack()
