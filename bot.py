import requests
import os
from slack_sdk import WebClient
from datetime import datetime, timedelta, timezone

# 미국 태평양 표준시(PDT) 설정 (UTC-7)
OFFSET = timezone(timedelta(hours=-7))

def get_today_menu():
    try:
        res = requests.get(API_URL)
        data = res.json()
        
        # 서버 시간이 아닌 미국 현지 시간 기준으로 날짜 생성
        today_str = datetime.now(OFFSET).strftime("%Y-%m-%d")


# GitHub Secrets에서 설정한 값들을 가져옵니다.
SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
API_URL = "https://cafemanager-api.cafebonappetit.com/api/2/menus?cafe=641"

def get_today_menu():
    try:
        res = requests.get(API_URL)
        data = res.json()
        
        # 오늘 날짜 확인
        today_str = datetime.now().strftime("%Y-%m-%d")
        
        # API 구조에서 메뉴 이름들만 추출
        items = data.get('items', {})
        menu_list = []
        
        for item_id in items:
            item = items[item_id]
            # 메뉴 이름(label)만 리스트에 추가
            menu_list.append(f"• {item.get('label')}")
            
        return "\n".join(menu_list) if menu_list else "오늘 등록된 메뉴가 없습니다."
    except Exception as e:
        return f"메뉴를 가져오는 중 오류 발생: {e}"

def send_to_slack():
    if not SLACK_TOKEN or not CHANNEL_ID:
        print("에러: SLACK_TOKEN 또는 CHANNEL_ID 설정이 없습니다.")
        return

    client = WebClient(token=SLACK_TOKEN)
    menu_text = f"🍴 *오늘의 SRA 런치 메뉴 ({datetime.now().strftime('%m/%d')})*\n\n{get_today_menu()}"
    
    try:
        client.chat_postMessage(channel=CHANNEL_ID, text=menu_text)
        print("슬랙 메시지 전송 성공!")
    except Exception as e:
        print(f"슬랙 전송 실패: {e}")

if __name__ == "__main__":
    send_to_slack()
