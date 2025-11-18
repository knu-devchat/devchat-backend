# llm/services.py

import os
from openai import OpenAI

# 1. 클라이언트 초기화: 환경 변수에서 키를 가져와 사용합니다.
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def get_chatbot_response(prompt: str, conversation_history: list = None) -> str:
    """
    사용자의 프롬프트를 받아 OpenAI API를 호출하고 응답을 반환합니다.
    """
    messages = [{"role": "system", "content": "You are a helpful and friendly assistant."}] # 시스템 메시지 설정
    
    # 대화 기록 추가 (있는 내용 경우 이전에 초기화한 messages에 추가)
    if conversation_history:
        messages.extend(conversation_history)
    
    
    messages.append({"role": "user", "content": prompt})

    #api 호출 로직
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"OpenAI API 호출 오류: {e}")
        return "죄송합니다. 서비스 처리 중 오류가 발생했습니다."