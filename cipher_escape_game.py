import streamlit as st
import pandas as pd # 알파벳 표를 만들기 위해 추가

# --- 암호화/복호화 함수 정의 ---

# 1. 시저 암호
def encrypt_caesar(plaintext, shift):
    """시저 암호화 함수"""
    ciphertext = ""
    for char in plaintext:
        if 'a' <= char <= 'z':
            ciphertext += chr(((ord(char) - ord('a') + shift) % 26) + ord('a'))
        elif 'A' <= char <= 'Z':
            ciphertext += chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
        else:
            ciphertext += char
    return ciphertext

def decrypt_caesar(ciphertext, shift):
    """시저 복호화 함수 (암호화의 역방향)"""
    return encrypt_caesar(ciphertext, -shift)

# 2. 비즈네르 암호
def encrypt_vigenere(plaintext, keyword):
    """비즈네르 암호화 함수"""
    ciphertext = ""
    keyword = keyword.upper()
    keyword_idx = 0
    for char in plaintext:
        if 'A' <= char <= 'Z':
            shift = ord(keyword[keyword_idx % len(keyword)]) - ord('A')
            ciphertext += chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
            keyword_idx += 1
        elif 'a' <= char <= 'z':
            shift = ord(keyword[keyword_idx % len(keyword)]) - ord('A')
            ciphertext += chr(((ord(char) - ord('a') + shift) % 26) + ord('a'))
            keyword_idx += 1
        else:
            ciphertext += char
    return ciphertext

def decrypt_vigenere(ciphertext, keyword):
    """비즈네르 복호화 함수"""
    plaintext = ""
    keyword = keyword.upper()
    keyword_idx = 0
    for char in ciphertext:
        if 'A' <= char <= 'Z':
            shift = ord(keyword[keyword_idx % len(keyword)]) - ord('A')
            plaintext += chr(((ord(char) - ord('A') - shift) % 26) + ord('A'))
            keyword_idx += 1
        elif 'a' <= char <= 'z':
            shift = ord(keyword[keyword_idx % len(keyword)]) - ord('A')
            plaintext += chr(((ord(char) - ord('a') - shift) % 26) + ord('a'))
            keyword_idx += 1
        else:
            plaintext += char
    return plaintext

# 3. 아핀 암호
def mod_inverse(a, m):
    """a * x = 1 (mod m) 에서 x (모듈러 역원)를 찾음"""
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None # 역원이 존재하지 않음

def encrypt_affine(plaintext, a, b):
    """아핀 암호화 함수"""
    ciphertext = ""
    for char in plaintext:
        if 'a' <= char <= 'z':
            val = (ord(char) - ord('a'))
            ciphertext += chr(((a * val + b) % 26) + ord('a'))
        elif 'A' <= char <= 'Z':
            val = (ord(char) - ord('A'))
            ciphertext += chr(((a * val + b) % 26) + ord('A'))
        else:
            ciphertext += char
    return ciphertext

def decrypt_affine(ciphertext, a, b):
    """아핀 복호화 함수"""
    plaintext = ""
    a_inv = mod_inverse(a, 26)
    if a_inv is None:
        return "ERROR: Invalid 'a' value" # 오류 메시지를 반환하여 상위 함수에서 처리
    
    for char in ciphertext:
        if 'a' <= char <= 'z':
            val = (ord(char) - ord('a'))
            plaintext += chr(((a_inv * (val - b + 26)) % 26) + ord('a')) # +26은 음수 방지
        elif 'A' <= char <= 'Z':
            val = (ord(char) - ord('A'))
            plaintext += chr(((a_inv * (val - b + 26)) % 26) + ord('A'))
        else:
            plaintext += char
    return plaintext

# --- 알파벳 표 생성 함수 ---
def create_alphabet_table():
    """알파벳 표를 생성하여 데이터프레임으로 반환"""
    alphabet = [chr(ord('A') + i) for i in range(26)]
    shifted_alphabet = [f"Shift {i}" for i in range(26)]
    data = {
        "Original": alphabet
    }
    for i in range(26):
        shifted_list = [chr(((ord(char) - ord('A') + i) % 26) + ord('A')) for char in alphabet]
        data[f"Shift +{i}"] = shifted_list
    
    # 0부터 25까지의 인덱스 추가
    index_values = [str(i) for i in range(26)]
    return pd.DataFrame(data, index=index_values)


# --- 게임 데이터 및 설정 ---

GAME_TITLE = "암호 방탈출: 미스터리 랩"

# 스테이지 정보
stages = {
    "intro": {
        "title": "시작",
        "text": (
            "당신은 알 수 없는 실험실에 갇혔습니다. 문은 굳게 잠겨있고, 탈출할 방법은 오직 "
            "방 곳곳에 숨겨진 암호화된 메시지를 해독하는 것뿐입니다. 행운을 빕니다!"
        ),
        "button_text": "첫 번째 단서 찾기"
    },
    "stage1_caesar": {
        "title": "스테이지 1: 낡은 책상",
        "text": (
            "낡은 책상 위에는 빛바랜 노트가 놓여 있습니다. 거기에 다음과 같은 메시지가 적혀 있습니다:\n\n"
            "`KHOOR`\n\n"
            "**힌트:** 이 메시지는 '세 칸 뒤로' 밀려있다고 합니다. (알파벳 표를 참고하세요.)"
        ),
        "cipher_type": "caesar",
        "cipher_text": "KHOOR",
        "correct_answer": "HELLO", # 더 쉬운 답으로 변경
        "key_hint": 3, # 시저 암호의 shift 값 (힌트용)
        "input_label": "복호화된 메시지 (대문자로):",
        "key_input_label": "쉬프트 값 (숫자, 예: 3):", # 힌트 구체화
        "next_stage": "stage2_vigenere",
        "correct_message": "첫 번째 암호가 해독되었습니다! 다음 단서는 벽에 걸린 그림 뒤에 있습니다."
    },
    "stage2_vigenere": {
        "title": "스테이지 2: 벽의 그림",
        "text": (
            "그림 뒤에서 종이 한 장을 발견했습니다. 이번에는 더 복잡해 보이는 암호입니다:\n\n"
            "`LXVW HQRXJK WR JHW WR WKH JHG.`\n\n"
            "**힌트:** 어둠 속에서 속삭이는 '숲'의 목소리에 귀 기울여라. (키워드는 모두 대문자로 입력하세요.)"
        ),
        "cipher_type": "vigenere",
        "cipher_text": "LXVW HQRXJK WR JHW TO THE JHG.", # 비즈네르 암호는 대소문자를 유지하는 경우가 많아서, 예시 메시지도 대문자 유지
        "correct_answer": "JUST ENOUGH TO GET TO THE END.",
        "key_hint": "FOREST", # 비즈네르 암호의 키워드
        "input_label": "복호화된 메시지 (대문자로):",
        "key_input_label": "키워드 (대문자로):",
        "next_stage": "stage3_affine",
        "correct_message": "두 번째 암호도 풀었습니다! 다음 단서는 바닥의 작은 상자 안에 있습니다."
    },
    "stage3_affine": {
        "title": "스테이지 3: 비밀 상자",
        "text": (
            "상자를 열자, 마지막 단서가 나타납니다. 하지만 이번에도 암호화되어 있습니다:\n\n"
            "`YVSF`\n\n"
            "**힌트:** 첫 번째 키는 26과 서로소인 숫자 7, 두 번째 키는 숫자 11입니다. (A=0, B=1, ... Z=25 로 계산)"
        ),
        "cipher_type": "affine",
        "cipher_text": "YVSF",
        "correct_answer": "CODE", # 최종 탈출 코드
        "key_hint": (7, 11), # 아핀 암호의 a, b 값
        "input_label": "복호화된 메시지 (대문자로):",
        "key_input_label": "키 'a' (숫자):",
        "key2_input_label": "키 'b' (숫자):",
        "next_stage": "end_game_success",
        "correct_message": "세 번째 암호까지 풀었습니다! 마지막 단서인 탈출 코드를 얻었습니다: `CODE`\n\n이 코드를 입력하여 탈출하세요!"
    },
    "end_game_success": {
        "title": "탈출 성공!",
        "text": "축하합니다! 모든 암호를 해독하고 실험실을 탈출했습니다! 당신은 진정한 암호 마스터입니다!",
        "type": "win"
    },
    "end_game_fail": {
        "title": "게임 오버",
        "text": "아쉽게도 암호를 해독하지 못했습니다. 다시 시도하여 실험실을 탈출해 보세요!",
        "type": "lose"
    }
}

# --- 스트림릿 앱 로직 ---

st.set_page_config(page_title=GAME_TITLE, layout="centered")

st.title(GAME_TITLE)
st.markdown("암호를 해독하여 미스터리 랩을 탈출하세요!")

# 세션 상태 초기화 함수
def initialize_game():
    st.session_state.current_stage = "intro"
    st.session_state.game_over = False
    st.session_state.attempts = {} # 스테이지별 시도 횟수 또는 상태 추적 (확장용)

# 세션 상태가 초기화되지 않았다면 초기화
if 'current_stage' not in st.session_state:
    initialize_game()

current_stage_id = st.session_state.current_stage
current_stage = stages[current_stage_id]

# --- UI 렌더링 ---

# 게임 오버 상태일 경우
if st.session_state.game_over:
    if current_stage['type'] == "win":
        st.balloons()
        st.success(current_stage['text'])
    else: # type == "lose"
        st.error(current_stage['text'])
    
    if st.button("새 게임 시작", key="restart_game_button"):
        initialize_game() # 게임 상태 초기화
        st.rerun() # 앱 새로고침
    st.stop() # 더 이상 코드 실행 방지

# 게임 진행 중인 경우
st.subheader(current_stage["title"])
st.markdown(current_stage["text"])

# 인트로 스테이지 처리
if current_stage_id == "intro":
    if st.button(current_stage["button_text"], key="start_game_button"):
        st.session_state.current_stage = "stage1_caesar"
        st.rerun()

# 암호 풀이 스테이지 처리
elif current_stage_id in ["stage1_caesar", "stage2_vigenere", "stage3_affine"]:
    st.code(current_stage["cipher_text"]) # 암호화된 메시지 코드 블록으로 표시

    # 시저 암호 스테이지에서 알파벳 표 표시
    if current_stage_id == "stage1_caesar":
        st.markdown("---")
        st.subheader("💡 시저 암호 알파벳 표")
        st.markdown("암호화된 글자에서 쉬프트 값만큼 왼쪽으로 이동하면 원래 글자를 찾을 수 있습니다.")
        st.dataframe(create_alphabet_table().T) # 전치하여 가로로 길게 표시
        st.markdown("---")

    user_input = st.text_input(current_stage["input_label"], key=f"user_input_{current_stage_id}").strip().upper()
    
    if current_stage["cipher_type"] == "caesar":
        user_shift = st.number_input(current_stage["key_input_label"], min_value=1, max_value=25, value=3, key=f"user_shift_{current_stage_id}")
        if st.button("복호화 시도", key=f"decrypt_button_{current_stage_id}"):
            decrypted_message = decrypt_caesar(current_stage["cipher_text"], user_shift).upper()
            if decrypted_message == current_stage["correct_answer"].upper():
                st.success(current_stage["correct_message"])
                st.session_state.current_stage = current_stage["next_stage"]
                st.rerun()
            else:
                st.error("오답입니다. 다시 시도해 보세요!")
                st.info(f"당신의 복호화: {decrypted_message}") # 디버깅을 위해 추가
    
    elif current_stage["cipher_type"] == "vigenere":
        user_keyword = st.text_input(current_stage["key_input_label"], key=f"user_keyword_{current_stage_id}").strip().upper()
        if st.button("복호화 시도", key=f"decrypt_button_{current_stage_id}"):
            decrypted_message = decrypt_vigenere(current_stage["cipher_text"], user_keyword).upper()
            if decrypted_message == current_stage["correct_answer"].upper():
                st.success(current_stage["correct_message"])
                st.session_state.current_stage = current_stage["next_stage"]
                st.rerun()
            else:
                st.error("오답입니다. 다시 시도해 보세요!")
                st.info(f"당신의 복호화: {decrypted_message}") # 디버깅을 위해 추가

    elif current_stage["cipher_type"] == "affine":
        user_a = st.number_input(current_stage["key_input_label"], min_value=1, max_value=25, value=7, key=f"user_a_{current_stage_id}")
        user_b = st.number_input(current_stage["key2_input_label"], min_value=0, max_value=25, value=11, key=f"user_b_{current_stage_id}")
        
        # 'a' 값이 26과 서로소인지 확인 (아핀 암호의 조건)
        coprime_a_values = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
        if user_a not in coprime_a_values:
            st.warning(f"경고: 키 'a' ({user_a})는 26과 서로소가 아닙니다. 올바른 복호화를 위해 26과 서로소인 숫자를 사용하세요.")
            st.info("가능한 'a' 값: " + ", ".join(map(str, coprime_a_values)))

        if st.button("복호화 시도", key=f"decrypt_button_{current_stage_id}"):
            decrypted_message = decrypt_affine(current_stage["cipher_text"], user_a, user_b).upper()
            if decrypted_message == "ERROR: INVALID 'A' VALUE": # mod_inverse에서 에러 발생 시
                 st.error("입력된 'a' 값으로는 복호화할 수 없습니다. 26과 서로소인 'a' 값을 사용해주세요.")
            elif decrypted_message == current_stage["correct_answer"].upper():
                st.success(current_stage["correct_message"])
                st.session_state.current_stage = current_stage["next_stage"]
                st.rerun()
            else:
                st.error("오답입니다. 다시 시도해 보세요!")
                st.info(f"당신의 복호화: {decrypted_message}") # 디버깅을 위해 추가
                
    # 사용자의 입력이 정답인지 최종 확인 (복호화된 메시지 확인)
    if current_stage_id == "stage3_affine" and current_stage["next_stage"] == "end_game_success":
        st.markdown("\n---")
        final_code_input = st.text_input("최종 탈출 코드 입력:", key="final_code_input").strip().upper()
        if st.button("탈출 시도", key="escape_button"):
            if final_code_input == current_stage["correct_answer"].upper():
                st.session_state.current_stage = "end_game_success"
                st.session_state.game_over = True
                st.rerun()
            else:
                st.error("틀린 코드입니다. 다시 확인해 보세요!")
                
else: # 알 수 없는 스테이지 (예기치 않은 오류 방지)
    st.error("알 수 없는 게임 상태입니다. 게임을 다시 시작합니다.")
    initialize_game()
    st.rerun()
