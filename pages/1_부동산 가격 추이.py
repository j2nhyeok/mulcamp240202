import streamlit as st
import pandas as pd
import plotly.express as px

def seoul_sale(house_gbn_nm):
    df_seoul = pd.read_csv('서울전체/df_서울.csv')
    df_seoul = df_seoul.loc[df_seoul['주택유형'] == f'{house_gbn_nm}', :]
    df_seoul['계약년월'] = df_seoul['계약년월'].astype(str)

    st.subheader(f'서울 월별 {house_gbn_nm} 매매 평균 가격')

    fig = px.line(
        x=df_seoul['계약년월'].unique(),
        y=df_seoul.groupby('계약년월')['물건금액(만원)'].mean(),
        labels={'x': '월', 'y': f'평균 {house_gbn_nm} 가격(만원)'},
        template='plotly_dark',
        line_shape='linear',
        width=800,
        height=400,
        markers=True, )

    fig.update_yaxes(tickformat=",d")
    st.plotly_chart(fig)
def gimpo_sale(house_gbn_nm):
    df_gimpo = pd.read_csv('김포데이터/df_김포.csv')
    df_gimpo = df_gimpo.loc[df_gimpo['주택유형'] == f'{house_gbn_nm}', :]
    df_gimpo['계약년월'] = df_gimpo['계약년월'].astype(str)

    st.subheader(f'김포 월별  {house_gbn_nm} 매매 평균 가격')
    
    fig = px.line(
        x=df_gimpo['계약년월'].unique(),
        y=df_gimpo.groupby('계약년월')['거래금액(만원)'].mean(),
        labels={'x': '월', 'y': f'평균 {house_gbn_nm} 가격(만원)'},
        template='plotly_dark',
        line_shape='linear',
        width=800,
        height=400,
        markers=True, )
    fig.update_yaxes(tickformat=",d")
    st.plotly_chart(fig)
def seoul_rent(rent_gbn, house_gbn_nm):
    df = pd.read_csv('서울전체/seoul_all.csv', encoding='euc_kr')
    df = df[(df['RENT_GBN'] == rent_gbn) & (df['HOUSE_GBN_NM'] == house_gbn_nm)]

    df = df[['RENT_GTN', 'CNTRCT_DE']]

    # 'RENT_GTN'을 월 별로 그룹화하여 평균값 계산
    monthly_data = df.groupby(df['CNTRCT_DE'].astype(str).str[:-2])['RENT_GTN'].mean().reset_index()

    # Streamlit 앱 시작
    st.subheader(f'서울 월별 {house_gbn_nm} {rent_gbn} 평균가격')

    # 선 그래프 그리기
    fig = px.line(
        monthly_data,
        x='CNTRCT_DE',
        y='RENT_GTN',
        labels={'CNTRCT_DE': '월', 'RENT_GTN': f'평균 {rent_gbn} 가격(만원)'},
        template='plotly_dark',  # Dark mode template
        line_shape='linear',  # Linear interpolation between points
        markers=True,  # Show markers on data points
        width=800,  # Width of the plot
        height=400,  # Height of the plot
    )

    # y-axis tick 포맷 변경 (5억 단위로)
    fig.update_yaxes(tickformat=",d")

    # Plotly 그래프를 Streamlit에 표시
    st.plotly_chart(fig)

def gimpo_rent(rent_gbn, house_gbn_nm):
    df = pd.read_csv(f'김포데이터/gimpo_all2.csv')

    st.subheader(f'김포 월별 {house_gbn_nm} {rent_gbn} 평균가격')

    # '전월세구분'이 '전세'이고 '주택유형'이 'temp2'인 행들만 필터링
    df = df[(df['전월세구분'] == rent_gbn) & (df['주택유형'] == house_gbn_nm)]

    # '계약년월'을 문자열로 변환 후 월 정보 추출
    df['year_month'] = df['계약년월'].astype(str)

    # '보증금(만원)' 열의 쉼표 제거하고 숫자로 변환
    df['보증금(만원)'] = df['보증금(만원)'].str.replace(',', '').astype(float)

    # 'year_month'를 월별로 그룹화하여 평균값 계산
    monthly_data = df.groupby('year_month')['보증금(만원)'].mean().reset_index()

    # 선 그래프 그리기
    fig = px.line(
        monthly_data,
        x='year_month',
        y='보증금(만원)',
        labels={'year_month': '월', '보증금(만원)': '보증금(만원)'},
        template='plotly_dark',
        line_shape='linear',
        markers=True,
        width=800,
        height=400,
    )

    # y-axis tick 포맷 변경 (5억 단위로)
    fig.update_yaxes(tickformat=",d")

    # Plotly 그래프를 Streamlit에 표시
    st.plotly_chart(fig)

def main():
    # Using object notation
    add_selectbox = st.sidebar.selectbox(
        "How would you like to be contacted?",
        ("아파트", "오피스텔", "연립다세대")
    )

    # Using "with" notation
    with st.sidebar:
        add_radio = st.radio(
            "구분",
            ("매매", "전세", "월세")
        )

    if add_selectbox == "아파트":
        if add_radio == "매매":
            seoul_sale("아파트")
            st.write('고금리로 인한 대출 이자금 부담의 영향으로 급매 사례 발생 -> 매매가 하락')
            st.write("-" * 50)
            gimpo_sale("아파트")
            st.write('고금리로 인한 대출 이자금 부담의 영향으로 급매 사례 발생 -> 매매가 하락')

        elif add_radio == "전세":
            seoul_rent("전세", "아파트")
            st.write('매매가 부담의 영향으로 상대적으로 전세 수요 증가 -> 전세가 상승')
            st.write("-" * 50)
            gimpo_rent("전세", "아파트")
            st.write('매매가 부담의 영향으로 상대적으로 전세 수요 증가 -> 전세가 상승')
            
        else:
            seoul_rent("월세", "아파트")
            st.write('매매가 부담의 영향으로 상대적으로 전세 수요 증가 -> 전세가 상승')
            st.write("-" * 50)
            gimpo_rent("월세", "아파트")
            st.write('큰 변화가 없음')

    elif add_selectbox == '오피스텔':
        if add_radio == "매매":
            seoul_sale("오피스텔")
            st.write('큰 변화가 없음')
            st.write("-" * 50)
            gimpo_sale("오피스텔")
            st.write('큰 변화가 없음')

        elif add_radio == "전세":
            seoul_rent("전세", "오피스텔")
            st.write('서울 포화현상으로 인한 전세 보증금 지속적 상승')
            st.write("-" * 50)
            gimpo_rent("전세", "오피스텔")
            st.write('큰 변화가 없음')
        else:
            seoul_rent("월세", "오피스텔")
            st.write('매매가 부담의 영향으로 상대적으로 월세 수요 증가 -> 월세가 상승')
            st.write("-" * 50)
            gimpo_rent("월세", "오피스텔")
            st.write('큰 변화가 없음')
    else:
        if add_radio == "매매":
            seoul_sale("연립다세대")
            st.write('고금리로 인한 대출 이자금 부담의 영향으로 급매 사례 발생 -> 매매가 지속적으로 하락')
            st.write("-" * 50)
            gimpo_sale("연립다세대")
            st.write('비교적 큰 변화가 없으며, 일부소폭상승')

        elif add_radio == "전세":
            seoul_rent("전세", "연립다세대")
            st.write('서울 포화현상으로 인한 전세 수요로 전세가 증가 이후 소폭 감소하며 그래프 횡보 지속 예상')
            st.write("-" * 50)
            gimpo_rent("전세", "연립다세대")
            st.write('지속적인 수요와 공급 존재 -> 큰 변화가 없음')

        else:
            seoul_rent("월세", "연립다세대")
            st.write('서울 포화현상으로 인한 월세 수요 증가 -> 월세 보증금 소폭 증가')
            st.write("-" * 50)
            gimpo_rent("월세", "연립다세대")
            st.write('6월경 강서구 전세 대규모 사기의 영향으로 인접지역 김포에서 보증금 불안 존재 -> 월세 보증금 하락')
            st.write('8월   이후   지속적인   수요와   공급으로 완만하게 횡보')

if __name__ == '__main__':
    main()
