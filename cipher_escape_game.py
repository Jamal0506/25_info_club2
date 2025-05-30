import streamlit as st
import random
import string

def caesar_decrypt(ciphertext, shift):
    plaintext = ""
    for char in ciphertext:
        if char.isalpha():
            start = ord('a') if char.islower() else ord('A')
            shifted_char = chr((ord(char) - start - shift) % 26 + start)
        elif char.isdigit():
            shifted_char = str((int(char) - shift) % 10)
        else:
            shifted_char = char
        plaintext += shifted_char
    return plaintext

def simple_substitution_decrypt(ciphertext, mapping):
    plaintext = ""
    reverse_mapping = {v: k for k, v in mapping.items()}
    for char in ciphertext:
        plaintext += reverse_mapping.get(char, char)
    return plaintext

def prime_factorization_challenge(n):
    factors = []
    d = 2
    temp_n = n
    while d * d <= temp_n:
        while temp_n % d == 0:
            factors.append(d)
            temp_n //= d
        d += 1
    if temp_n > 1:
        factors.append(temp_n)
    if len(factors) == 2:
        return factors[0], factors[1]
    else:
        return None, None

st.title("고전 암호 방탈출")
st.sidebar.title("메뉴")
page = st.sidebar.radio("이동", ["시저 암호", "단순 치환 암호", "RSA 인수분해 (보너스)"])

if page == "시저 암호":
    st.header("시저 암호 해독")
    ciphertext = st.text_area("암호문을 입력하세요:", "")
    shift = st.slider("이동 거리:", 1, 25, 3)
    if st.button("해독"):
        plaintext = caesar_decrypt(ciphertext, shift)
        st.success(f"해독된 평문: {plaintext}")

elif page == "단순 치환 암호":
    st.header("단순 치환 암호 해독")
    ciphertext = st.text_area("암호문을 입력하세요:", "")
    hint = st.text_area("치환 힌트 (예: a=x, b=y, ...):", "")
    mapping = {}
    if hint:
        pairs = hint.split(',')
        for pair in pairs:
            if '=' in pair:
                key, value = pair.strip().split('=')
                if len(key) == 1 and len(value) == 1:
                    mapping[key.strip()] = value.strip()

    if st.button("해독"):
        plaintext = simple_substitution_decrypt(ciphertext, mapping)
        st.success(f"해독된 평문: {plaintext}")

elif page == "RSA 인수분해 (보너스)":
    st.header("RSA 키 복구 챌린지")
    n = st.number_input("주어진 N 값:", min_value=1, value=91)
    st.write("N은 두 소수 p와 q의 곱입니다. p와 q를 찾아보세요.")
    col1, col2 = st.columns(2)
    p_guess = col1.number_input("예상되는 p 값:", min_value=1, step=1)
    q_guess = col2.number_input("예상되는 q 값:", min_value=1, step=1)

    if st.button("소수 확인"):
        if p_guess > 1 and q_guess > 1 and p_guess * q_guess == n:
            st.success(f"정답입니다! p = {p_guess}, q = {q_guess}")
        else:
            st.error("다시 시도해보세요.")
