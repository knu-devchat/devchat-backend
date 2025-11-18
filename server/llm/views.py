from django.shortcuts import render
# llm/views.py
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .services import get_chatbot_response

@csrf_exempt 
@require_http_methods(["POST"])
def chat_message(request):
    try:
        data = json.loads(request.body)
        user_prompt = data.get("prompt")
        
        if not user_prompt:
            return JsonResponse({"error": "Prompt field is required"}, status=400)

        # 서비스 로직 호출
        chatbot_response_text = get_chatbot_response(user_prompt)

        # 응답 반환
        return JsonResponse({
            "response": chatbot_response_text,
            "success": True
        },
        json_dumps_params={'ensure_ascii': False} # 한글 깨짐 방지
        )

        #예외 처리
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"Internal Server Error: {str(e)}"}, status=500)

# Create your views here.
