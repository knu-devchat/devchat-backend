## devchat backend

### 🚀 빠르게 시작하기
1. `.env.example`을 복사해 `.env`를 만들고 필수 값을 채웁니다.
   - `DJANGO_SECRET_KEY`: Django 시크릿 키
   - `CLIENT_ID` / `CLIENT_SECRET`: GitHub OAuth 설정 값
   - `MASTER_KEY_B64`: 16/24/32바이트 마스터 키를 Base64로 인코딩한 문자열 (AES-GCM 암복호화에 사용)
2. 필요한 패키지를 설치합니다.
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install django channels channels-redis cryptography pyotp python-dotenv
   ```
3. 데이터베이스와 마이그레이션을 적용합니다.
   ```bash
   python server/manage.py migrate
   ```
4. 개발 서버를 실행합니다.
   ```bash
   python server/manage.py runserver
   ```

### 🔌 API & WebSocket
- **채팅방 생성**: `POST /chat/create-chat-room/` (JSON 본문 `{"room_name": "..."}`)
- **TOTP 코드 발급**: `GET /chat/rooms/<room_id>/generate-totp/`
- **메시지 목록 조회**: `GET /chat/rooms/<room_name>/messages/`
- **WebSocket 채팅**: `ws://<host>/ws/chat/<room_name>/`
  - 클라이언트 -> 서버: `{ "message": "내용", "username": "닉네임" }`
  - 서버 -> 클라이언트: 저장된 메시지 ID와 생성 시각을 포함해 브로드캐스트

### 📌 todo-list
- [x] 로그인 로직
- [x] TOTP 알고리즘 구현
- [x] 채팅 메시지 송수신 코드 구현
- [ ] LLM 구현
