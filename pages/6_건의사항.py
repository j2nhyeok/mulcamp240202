import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# SQLite 데이터베이스 연결
conn = sqlite3.connect('게시판.db')
cursor = conn.cursor()

# 테이블 생성
cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        author TEXT,
        content TEXT,
        timestamp TEXT
    )
''')
conn.commit()

# Streamlit 애플리케이션 시작
st.title('건의사항')

# 글 작성 폼
author = st.text_input('작성자:', key="author", value='')  # 초기값을 빈 문자열로 설정
content = st.text_area('내용:', key="content", value='')  # 초기값을 빈 문자열로 설정
submit_button = st.button('글 작성')

# 글 작성 버튼이 눌렸을 때
if submit_button:
    if not author or not content:
        st.warning("작성자나 내용을 모두 입력해주세요.")
    else:
        # 현재 시간을 기록
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 작성된 글을 데이터베이스에 추가
        cursor.execute('INSERT INTO posts (author, content, timestamp) VALUES (?, ?, ?)', (author, content, timestamp))
        conn.commit()

        if author == "관리자" and content == "글삭제":
            conn.execute('Delete from posts ')
            conn.commit()

        # 작성자와 내용 초기화
        author = ""
        content = ""

# 작성된 글 목록 표시
st.subheader('작성된 글 목록')
# 데이터베이스에서 글 목록 불러오기
posts = pd.read_sql('SELECT * FROM posts', conn, index_col='id')  # index_col을 'id'로 설정하여 인덱스를 해당 칼럼으로 지정
st.dataframe(posts)

# SQLite 연결 종료
conn.close()
