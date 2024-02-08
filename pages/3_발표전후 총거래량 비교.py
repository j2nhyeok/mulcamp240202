import streamlit as st
import pandas as pd
import plotly.express as px

def seoul_sale():
    df_seoul = pd.read_csv("서울전체/df_서울.csv")

    before_seoul = df_seoul.loc[df_seoul['발표'] == '발표전', :]
    after_seoul = df_seoul.loc[df_seoul['발표'] == '발표후', :]

    before_avg = before_seoul.groupby('자치구명')['물건금액(만원)'].count().reset_index()
    after_avg = after_seoul.groupby('자치구명')['물건금액(만원)'].count().reset_index()

    merge_df = pd.concat([before_avg.assign(dataset='Before Mega Seoul'), after_avg.assign(dataset='After Mega Seoul')])

    fig = px.bar(merge_df,
                 x='자치구명',
                 y='물건금액(만원)',
                 color='dataset',
                 barmode='group',
                 title='발표 전 후 서울 매매 총거래  비교',
                 labels={'자치구명': '구분', '물건금액(만원)': '거래량(건)'},
                 template='plotly_dark',  # Dark mode template
                 width=1000,  # Width of the plot
                 height=600,  # Height of the plo
                 )

    for sgg in merge_df['자치구명'].unique():
        before_count = before_avg[before_avg['자치구명'] == sgg]['물건금액(만원)'].values[0]
        after_count = after_avg[after_avg['자치구명'] == sgg]['물건금액(만원)'].values[0]
        percent_increase = ((after_count - before_count) / before_count) * 100
        fig.add_annotation(
            x=sgg,
            y=max(before_count, after_count),
            text=f'{percent_increase:.2f}%',
            showarrow=True,
            arrowcolor='red',
            arrowhead=4,
            ax=0,
            ay=-40
        )
    st.plotly_chart(fig)
def gimpo_sale():
    df_gimpo = pd.read_csv("김포데이터/df_김포.csv")

    before_gimpo = df_gimpo.loc[df_gimpo['발표'] == '발표전', :]
    after_gimpo = df_gimpo.loc[df_gimpo['발표'] == '발표후', :]

    before_avg = before_gimpo.groupby('시군구')['거래금액(만원)'].count().reset_index()
    after_avg = after_gimpo.groupby('시군구')['거래금액(만원)'].count().reset_index()

    merge_df = pd.concat([before_avg.assign(dataset='Before Mega Seoul'), after_avg.assign(dataset='After Mega Seoul')])

    fig = px.bar(merge_df,
                 x='시군구',
                 y='거래금액(만원)',
                 color='dataset',
                 barmode='group',
                 title='발표 전 후 김포 매매 총거래  비교',
                 labels={'시군구': '구분', '거래금액(만원)': '거래량(건)'},
                 template='plotly_dark',  # Dark mode template
                 width=1000,  # Width of the plot
                 height=600,  # Height of the plo
    )

    for sgg in merge_df['시군구'].unique():
        before_count = before_avg[before_avg['시군구'] == sgg]['거래금액(만원)'].values[0]
        after_count = after_avg[after_avg['시군구'] == sgg]['거래금액(만원)'].values[0]
        percent_increase = ((after_count - before_count) / before_count) * 100
        fig.add_annotation(
            x=sgg,
            y=max(before_count, after_count),
            text=f'{percent_increase:.2f}%',
            showarrow=True,
            arrowcolor='red',
            arrowhead=4,
            ax=0,
            ay=-40
        )

    st.plotly_chart(fig)

def seoul_rent():
    # CSV 파일을 읽어와 데이터프레임으로 저장
    df = pd.read_csv('서울전체/seoul_all.csv', encoding='euc_kr')
    before_mega = df[df['MEGASEOUL'] == 'Before']
    after_mega = df[df['MEGASEOUL'] == 'After']

    # 각 데이터프레임에서 아파트 전세 보증금 평균 계산
    before_mega_avg = before_mega.groupby('SGG_NM')['RENT_GTN'].count().reset_index()
    after_mega_avg = after_mega.groupby('SGG_NM')['RENT_GTN'].count().reset_index()

    # 두 데이터프레임을 합치기 (for plotting)
    merged_data = pd.concat([before_mega_avg.assign(dataset='Before Mega Seoul'),
                             after_mega_avg.assign(dataset='After Mega Seoul')])

    # 막대 차트 그리기
    fig = px.bar(
        merged_data,
        x='SGG_NM',
        y='RENT_GTN',
        color='dataset',
        barmode='group',
        title='서울특별시 구별 전월세 총 거래량 비교',
        labels={'SGG_NM': '구', 'RENT_GTN': '거래량(건)'},
        template='plotly_dark',  # Dark mode template
        width=1000,  # Width of the plot
        height=600,  # Height of the plo
    )

    # After Mega Seoul 대비 거래량 증가 비율 계산 및 텍스트로 추가
    for sgg in merged_data['SGG_NM'].unique():
        before_count = before_mega_avg[before_mega_avg['SGG_NM'] == sgg]['RENT_GTN'].values[0]
        after_count = after_mega_avg[after_mega_avg['SGG_NM'] == sgg]['RENT_GTN'].values[0]
        percent_increase = ((after_count - before_count) / before_count) * 100

        fig.add_annotation(
            x=sgg,
            y=max(before_count, after_count),
            text=f'{percent_increase:.2f}%',
            showarrow=True,
            arrowcolor='red',
            arrowhead=4,
            ax=0,
            ay=-40
        )

    fig.update_yaxes(tickformat=",d")
    # Show the plot
    st.plotly_chart(fig)


def gimpo_rent():
    df = pd.read_csv('김포데이터/gimpo_all2.csv')
    # '계약년월'을 문자열로 변환 후
    df['year_month'] = df['계약년월'].astype(str)
    df['시군구'] = df['시군구'].str[8:11]

    before_mega = df[(df['year_month'] <= '202309')]
    after_mega = df[(df['year_month'] >= '202310')]

    before_mega_cnt = before_mega.groupby('시군구')['계약일'].count().reset_index()
    after_mega_cnt = after_mega.groupby('시군구')['계약일'].count().reset_index()

    # 두 데이터프레임을 합치기 (for plotting)
    merged_data = pd.concat([before_mega_cnt.assign(dataset='Before Mega Seoul'),
                             after_mega_cnt.assign(dataset='After Mega Seoul')])

    # 막대 차트 그리기
    fig = px.bar(
        merged_data,
        x='시군구',
        y='계약일',
        color='dataset',
        barmode='group',
        title='김포시 행정구역별 전월세 총 거래량 비교',
        labels={'시군구': '행정구역', '계약일': '거래량(건)'},
        template='plotly_dark',  # Dark mode template
        width=1000,  # Width of the plot
        height=600,  # Height of the plo
    )

    # After Mega Seoul 대비 거래량 증가 비율 계산 및 텍스트로 추가
    for sgg in merged_data['시군구'].unique():
        before_count = before_mega_cnt[before_mega_cnt['시군구'] == sgg]['계약일'].values[0]
        after_count = after_mega_cnt[after_mega_cnt['시군구'] == sgg]['계약일'].values[0]
        percent_increase = ((after_count - before_count) / before_count) * 100

        fig.add_annotation(
            x=sgg,
            y=max(before_count, after_count),
            text=f'{percent_increase:.2f}%',
            showarrow=True,
            arrowcolor='red',
            arrowhead=4,
            ax=0,
            ay=-40
        )

    fig.update_yaxes(tickformat=",d")
    st.plotly_chart(fig)
def main():
    with st.sidebar:
        add_radio = st.radio(
            "구분",
            ("매매", "전월세")
        )

    if add_radio == "매매":
        seoul_sale()
        st.write("-" * 50)
        gimpo_sale()
    elif add_radio == "전월세":
        seoul_rent()
        st.write("-" * 50)
        gimpo_rent()
        st.write('5ㅎ')

if __name__ == '__main__':
    main()