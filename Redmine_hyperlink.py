import requests # requests 모듈 - HTTP 요청을 보내는데 사용
import json # json 모듈 - JSON 데이터를 다루는데 사용

with open("info.json") as f:
    info = json.load(f)
"""
레드마인에 이슈를 번호 검색 시 슬랙으로 보내주는 코드 - kevin

Redmine API의 엔드포인트 URL을 저장할 변수 / Redmine의 주소가 들어감
Redmine API에 인증에 사용될 API 토큰을 저장할 변수 / Redmine의 토큰 값이 들어감
Slack 웹훅 URL을 저장할 변수 / Slack 웹훅 URL이 들어감 / redmine_hyperlink URL이 들어가있음
"""

def get_redmine_issue(issue_numbers):
    redmine_api_endpoint = info.get("redmine_api_endpoint")
    api_token = info.get("api_token")
    slack_webhook_url = info.get("slack_webhook_url")

    attachments = []  # Slack으로 전송할 여러 개의 메시지를 담을 리스트 변수

    # issue_numbers 리스트에 있는 이슈 번호 반복 확인
    for number in issue_numbers:
        # Redmine API에서 이슈 정보를 가져오기 위한 요청 URL을 생성
        api_url = f"{redmine_api_endpoint}/issues/{number}.json"
        # API 요청에 필요한 헤더를 생성
        headers = {"X-Redmine-API-Key": api_token}
        # 생성한 URL과 헤더를 사용하여 GET 요청
        response = requests.get(api_url, headers=headers)

        # 응답 상태 코드가 200인지 확인 / 200은 HTTP에서 OK를 나타내는 상태 코드
        if response.status_code == 200:
            # 응답 데이터를 JSON 형식으로 변환하여 변수에 저장
            issue_data = json.loads(response.text)
            # 이슈 제목 가져오기
            issue_title = issue_data["issue"]["subject"]

            #Slack 메시지에 추가할 attachment 정보를 생성 / attachment에는 이슈 번호, 제목, URL이 들어감
            attachment = {
                "text": "<http://192.168.0.35:30002//issues/{}|#{} {}>".format(number,number,issue_title.replace(">", "&gt;"))
            }
            # 생성한 attachment를 attachments 리스트에 추가
            attachments.append(attachment)

        # 응답 상태 코드가 200이 아닌 경우 이슈를 가져오는데 실패를 출력
        else:
            print(f"이슈 - #{number}를 가져오는데 실패")

    # Slack으로 전송할 payload를 생성
    payload = {
        "attachments": attachments
    }
    # 생성한 payload를 Slack 웹훅 URL로 POST 요청
    requests.post(slack_webhook_url, json=payload)

# 이슈 번호를 입력받고 쉼표로 구분하여 리스트로 저장
issue_numbers = input("이슈 번호를 입력 (쉼표로 구분): ").split(",")

# 함수를 호출하여 이슈 정보를 가져오고 Slack으로 메시지를 전송
get_redmine_issue(issue_numbers)