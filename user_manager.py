import os
import json
import hashlib
from datetime import datetime

# 사용자 데이터 파일
USERS_FILE = 'users_data.json'

def hash_password(password):
    """비밀번호를 해시화"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """저장된 사용자 정보 불러오기"""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_users(users):
    """사용자 정보 저장"""
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def register_user(username, password):
    """회원가입"""
    users = load_users()

    # 중복 확인
    if username in users:
        return False, "이미 존재하는 사용자명입니다."

    # 최소 요구사항 확인
    if len(username) < 3:
        return False, "사용자명은 3글자 이상이어야 합니다."

    if len(password) < 4:
        return False, "비밀번호는 4글자 이상이어야 합니다."

    # 새 사용자 추가
    users[username] = {
        'password': hash_password(password),
        'created_at': datetime.now().isoformat(),
        'travels_file': f'{username}_travels.json'
    }

    save_users(users)
    return True, "회원가입이 완료되었습니다!"

def login_user(username, password):
    """로그인"""
    users = load_users()

    if username not in users:
        return False, "사용자명이 존재하지 않습니다."

    if users[username]['password'] != hash_password(password):
        return False, "비밀번호가 틀렸습니다."

    return True, "로그인 성공!"

def change_password(username, old_password, new_password):
    """비밀번호 변경"""
    users = load_users()

    if username not in users:
        return False, "사용자명이 존재하지 않습니다."

    # 기존 비밀번호 확인
    if users[username]['password'] != hash_password(old_password):
        return False, "기존 비밀번호가 틀렸습니다."

    if len(new_password) < 4:
        return False, "새 비밀번호는 4글자 이상이어야 합니다."

    # 비밀번호 변경
    users[username]['password'] = hash_password(new_password)
    save_users(users)

    return True, "비밀번호가 변경되었습니다!"

def get_user_travels_file(username):
    """사용자의 여행 기록 파일 경로 반환"""
    return f'{username}_travels.json'
