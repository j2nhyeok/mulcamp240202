import streamlit as st
import pandas as pd
import plotly.express as px


def get_increase(df,temp):
    sentence = ""
    if temp == "매매":
        sentence ="거래금액(만원)"
    else:
        sentence = "보증금(만원)"

    df['계약년월'] = pd.to_datetime(df['계약년월'], format='%Y%m')

    # '보증금(만원)' 열의 쉼표 제거하고 숫자로 변환
    df[f'{sentence}'] = df[f'{sentence}'].replace({',': ''}, regex=True).astype(float)

    if temp == "매매":
        before_megaseoul = df[(df['계약년월'] <= '2023-09') & (df['계약년월'] >= '2023-06')]
        after_megaseoul = df[(df['계약년월'] <= '2024-01') & (df['계약년월'] >= '2023-10')]
    else:
    # 조건에 따라 데이터 필터링
        before_megaseoul = df[(df['전월세구분'] == f'{temp}') & (df['계약년월'] <= '2023-09') & (df['계약년월'] >= '2023-06')]
        after_megaseoul = df[(df['전월세구분'] == f'{temp}') & (df['계약년월'] <= '2024-01') & (df['계약년월'] >= '2023-10')]

    before_mean = before_megaseoul[f'{sentence}'].mean()
    after_mean = after_megaseoul[f'{sentence}'].mean()

    # 증가율 계산
    increase_rate = ((after_mean - before_mean) / before_mean) * 100

    return increase_rate

def gimpo(temp):
    increase_rate = []

    if temp == "매매":
        df = pd.read_csv('김포데이터/df_김포.csv')
        gimpo_apart = df[df['주택유형'] == '아파트']
        gimpo_officetels = df[df['주택유형'] == '오피스텔']
        gimpo_multi_complex = df[df['주택유형'] == '연립다세대']

    else:
    # CSV 파일을 읽어와 데이터프레임으로 저장
        gimpo_all2 = pd.read_csv('김포데이터/gimpo_all2.csv')
        gimpo_apart = gimpo_all2[gimpo_all2['주택유형'] == '아파트']
        gimpo_multi_complex = gimpo_all2[gimpo_all2['주택유형'] == '연립다세대']
        gimpo_officetels = gimpo_all2[gimpo_all2['주택유형'] == '오피스텔']

    # '계약년월'을 datetime 형식으로 변환

    increase_rate.append(get_increase(gimpo_apart, temp))
    increase_rate.append(get_increase(gimpo_officetels, temp))
    increase_rate.append(get_increase(gimpo_multi_complex, temp))

    print(increase_rate)

    # 그래프를 그리기 위한 데이터프레임 생성
    data = {'Category': ['아파트', '오피스텔', '연립다세대'],
            'increase_rate': [increase_rate[0], increase_rate[1], increase_rate[2]]}

    df_bar = pd.DataFrame(data)

    # 막대 그래프 그리기
    fig = px.bar(
        df_bar,
        x='Category',
        y='increase_rate',
        title=f'메가서울 발표 이후 김포시 평균 {temp} 가격 증가/감소율',
        labels={'Category': '구분', 'increase_rate': '증가율'},
        template='plotly_dark',  # Dark mode template
        width=800,  # Width of the plot
        height=400,  # Height of the plot
    )

    fig.update_yaxes(tickformat=',d')
    # Show the plot
    st.plotly_chart(fig)
def main():
    with st.sidebar:
        add_radio = st.radio(
            "구분",
            ("매매", "전세", "월세")
        )

    if add_radio == "매매":
        gimpo("매매")
        st.write("1인 가구 증가 및 부동산 완화 정책 확대 -> 오피스텔 매매가 증가")
    elif add_radio == "전세":
        gimpo("전세")
        st.write("비아파트 대비 아파트 실거래가 대폭 상승 -> 아파트 전세 수요 증가")
    else:
        gimpo("월세")
        st.write("아파트 대비 비아파트 실거래가 대폭 감소 -> 비아파트 월세 수요 감소")

if __name__ == '__main__':
    main()