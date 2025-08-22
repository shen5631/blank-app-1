import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# --- 한글 폰트 설정 ---
# Streamlit 앱 실행 환경에 맞는 한글 폰트를 설정합니다.
# 로컬 PC에 '맑은 고딕'이 설치되어 있다면 자동으로 사용됩니다.
try:
    plt.rc('font', family='Malgun Gothic')
except:
    st.warning("맑은고딕 폰트를 찾을 수 없습니다. 차트의 한글이 깨질 수 있습니다.")
    pass

# --- 1. 확장된 데이터 생성 (수정된 버전) ---
def get_dummy_data():
    """사용자가 요청한 팀 목록과 특정 경기 결과를 반영한 가상 데이터를 생성합니다."""
    # 팀 데이터: 리그, 능력치, 대표 색상 등
    teams_data = {
        'Team': [
            # K리그 1
            '울산 HD', '전북 현대 모터스', 'FC 서울', '포항 스틸러스', '수원 삼성 블루윙즈',
            # EPL
            '맨체스터 시티', '리버풀', '토트넘 홋스퍼', '아스널', '첼시', '맨체스터 유나이티드',
            # 라리가
            '레알 마드리드', 'FC 바르셀로나', '아틀레티코 마드리드', '세비야 FC', '레알 소시에다드',
            # 분데스리가
            '바이에른 뮌헨', '보루시아 도르트문트', 'RB 라이프치히', '바이어 04 레버쿠젠', '아인트라흐트 프랑크푸르트',
            # 세리에 A
            '인터 밀란', 'AC 밀란'
        ],
        'League': [
            'K리그 1', 'K리그 1', 'K리그 1', 'K리그 1', 'K리그 1',
            '프리미어리그', '프리미어리그', '프리미어리그', '프리미어리그', '프리미어리그', '프리미어리그',
            '라리가', '라리가', '라리가', '라리가', '라리가',
            '분데스리가', '분데스리가', '분데스리가', '분데스리가', '분데스리가',
            '세리에 A', '세리에 A'
        ],
        'Attack': [
            85, 84, 82, 83, 79,  # K리그
            94, 90, 95, 80, 85, 84,  # EPL (맨시티>맨유, 토트넘>>아스널)
            93, 88, 86, 82, 84,  # 라리가
            92, 89, 87, 91, 85,  # 분데스리가
            92, 86  # 세리에 A (인터>밀란)
        ],
        'Defense': [
            84, 82, 80, 83, 78,  # K리그
            92, 88, 92, 78, 83, 82,  # EPL (맨시티>맨유, 토트넘>>아스널)
            90, 85, 87, 80, 83,  # 라리가
            88, 85, 84, 86, 82,  # 분데스리가
            89, 83  # 세리에 A (인터>밀란)
        ],
        'Color': [
            '#003472', '#008B4E', '#BE0028', '#DD1F26', '#1D2E68', # K리그
            '#6CABDD', '#D00027', '#132257', '#EF0107', '#034694', '#DA291C', # EPL
            '#FEBE10', '#A50044', '#CE3524', '#D40026', '#0067B1', # 라리가
            '#DC052D', '#FDE100', '#001A5C', '#E32221', '#E1000F', # 분데스리가
            '#0068C8', '#FB090B' # 세리에 A
        ]
    }
    teams_df = pd.DataFrame(teams_data)
    teams_df['Overall'] = ((teams_df['Attack'] + teams_df['Defense']) / 2).astype(int)

    # 선수 데이터 (주요 선수 일부 추가)
    players_data = {
        'Player': ['주민규', '홍명보', '기성용', '이동국', '염기훈', '엘링 홀란', '케빈 더 브라위너', '손흥민', '데클란 라이스', '콜 팔머', '브루노 페르난데스', '주드 벨링엄', '비니시우스 주니오르', '앙투안 그리즈만', '세르히오 라모스', '해리 케인', '마르코 로이스', '플로리안 비르츠', '라우타로 마르티네스', '테오 에르난데스'],
        'Team': ['울산 HD', '포항 스틸러스', 'FC 서울', '전북 현대 모터스', '수원 삼성 블루윙즈', '맨체스터 시티', '맨체스터 시티', '토트넘 홋스퍼', '아스널', '첼시', '맨체스터 유나이티드', '레알 마드리드', '레알 마드리드', '아틀레티코 마드리드', '세비야 FC', '바이에른 뮌헨', '보루시아 도르트문트', '바이어 04 레버쿠젠', '인터 밀란', 'AC 밀란'],
        'Position': ['FW', 'DF', 'MF', 'FW', 'MF', 'FW', 'MF', 'FW', 'MF', 'MF', 'MF', 'MF', 'FW', 'FW', 'DF', 'FW', 'MF', 'MF', 'FW', 'DF'],
        'OVR': [85, 90, 86, 88, 84, 94, 93, 92, 88, 87, 89, 94, 92, 89, 88, 93, 88, 91, 91, 89]
    }
    players_df = pd.DataFrame(players_data)
    
    # 최근 경기 결과 (가상) - 23개로 수정
    teams_df['Recent Form'] = [
        '승-승-무-승-패', '승-패-승-승-무', '무-승-패-승-승', '패-무-승-패-승', '승-승-패-무-승',
        '승-승-승-무-승', '승-무-패-승-승', '무-패-승-승-패', '패-승-무-승-승', '승-무-승-패-무',
        '승-패-무-승-패', '승-승-무-승-무', '무-패-패-승-승', '패-무-승-승-승', '승-승-패-패-무',
        '승-무-승-패-승', '무-승-승-패-승', '승-승-무-무-패', '패-승-승-승-승', '무-무-승-패-승',
        '승-패-승-무-승', '승-승-승-패-무',
        '무-승-패-승-승'  # <-- 누락되었던 마지막 팀의 데이터 추가
    ]

    return teams_df, players_df

teams_df, players_df = get_dummy_data()

# --- Streamlit UI ---
st.set_page_config(page_title="축구 AI 승부 예측", layout="wide")

st.title('⚽ AI 승부 예측 및 선수 OVR 뷰어')
st.markdown("K리그를 포함한 5대 리그 확장 데이터와 **사용자 요청 규칙**이 반영된 최종 버전입니다.")
st.divider()

# --- 팀 선택 ---
col1, col2 = st.columns(2)
with col1:
    selected_league = st.selectbox('**1. 리그를 선택하세요**', teams_df['League'].unique())
    available_teams = teams_df[teams_df['League'] == selected_league]['Team'].tolist()
    home_team = st.selectbox('**2. 홈 팀을 선택하세요**', available_teams, index=0)

with col2:
    away_teams = [team for team in available_teams if team != home_team]
    if not away_teams: away_teams = available_teams
    away_team_index = 1 if len(away_teams) > 1 else 0
    away_team = st.selectbox('**3. 원정 팀을 선택하세요**', away_teams, index=away_team_index)

# --- 팀 정보 및 전력 분석 ---
home_stats = teams_df[teams_df['Team'] == home_team].iloc[0]
away_stats = teams_df[teams_df['Team'] == away_team].iloc[0]

home_color = home_stats['Color']
away_color = away_stats['Color']

st.subheader(f'📈 {home_team} vs {away_team} 전력 분석')

col1, col2 = st.columns(2)
with col1:
    st.markdown(f'<h4 style="color:white; background-color:{home_color}; padding: 10px; border-radius: 5px; text-align: center;">{home_team} (홈)</h4>', unsafe_allow_html=True)
    st.metric(label="팀 OVR", value=home_stats['Overall'])
    st.write(f"**최근 경기 결과:** {home_stats['Recent Form']}")
    st.progress(home_stats['Attack'] / 100, text=f"공격력: {home_stats['Attack']}")
    st.progress(home_stats['Defense'] / 100, text=f"수비력: {home_stats['Defense']}")
    
with col2:
    st.markdown(f'<h4 style="color:white; background-color:{away_color}; padding: 10px; border-radius: 5px; text-align: center;">{away_team} (원정)</h4>', unsafe_allow_html=True)
    st.metric(label="팀 OVR", value=away_stats['Overall'])
    st.write(f"**최근 경기 결과:** {away_stats['Recent Form']}")
    st.progress(away_stats['Attack'] / 100, text=f"공격력: {away_stats['Attack']}")
    st.progress(away_stats['Defense'] / 100, text=f"수비력: {away_stats['Defense']}")

st.divider()

# --- AI 승부 예측 및 커스텀 시각화 ---
def predict_match_winner(home_stats, away_stats):
    """간단한 승부 예측 로직"""
    home_score = (home_stats['Attack'] * 1.05) - away_stats['Defense']
    away_score = away_stats['Attack'] - home_stats['Defense']
    diff = home_score - away_score
    
    if diff > 15: win_prob, draw_prob = 80 + (diff - 15) * 0.5, 15 # 압도적일 경우
    elif diff > 5: win_prob, draw_prob = 60 + (diff - 5), 25
    elif diff > 0: win_prob, draw_prob = 50 + diff, 30
    elif diff == 0: win_prob, draw_prob = 40, 20
    else: win_prob, draw_prob = 35 + diff, 30
        
    win_prob = min(max(win_prob, 5), 95)
    draw_prob = min(max(draw_prob, 5), 40)
    lose_prob = 100 - win_prob - draw_prob
    
    total = win_prob + draw_prob + lose_prob
    return {'win': round((win_prob / total) * 100), 'draw': round((draw_prob / total) * 100), 'lose': round((lose_prob / total) * 100)}

def create_prediction_bar(probs, home_color, away_color):
    """커스텀 예측 결과 막대 차트 생성"""
    win_prob, draw_prob = probs['win'], probs['draw']
    lose_prob = 100 - win_prob - draw_prob

    fig, ax = plt.subplots(figsize=(10, 1.5))
    ax.barh([0], [win_prob], color=home_color, edgecolor='white')
    ax.barh([0], [draw_prob], left=[win_prob], color='grey', edgecolor='white')
    ax.barh([0], [lose_prob], left=[win_prob + draw_prob], color=away_color, edgecolor='white')

    ax.text(win_prob/2, 0, f'{win_prob}%', ha='center', va='center', color='white', fontsize=14, weight='bold')
    ax.text(win_prob + draw_prob/2, 0, f'{draw_prob}%', ha='center', va='center', color='white', fontsize=14, weight='bold')
    ax.text(win_prob + draw_prob + lose_prob/2, 0, f'{lose_prob}%', ha='center', va='center', color='white', fontsize=14, weight='bold')

    ax.set_xlim(0, 100)
    ax.axis('off')
    return fig

if st.button('**🤖 AI 승부 예측 실행하기**'):
    with st.spinner('AI가 경기 결과를 분석하고 있습니다...'):
        prediction = predict_match_winner(home_stats, away_stats)

        st.subheader('🔮 AI 예측 결과')
        st.markdown(f"""<div style="display: flex; justify-content: center; gap: 20px; margin-bottom: 10px;">
            <span style="font-weight: bold;"><span style="color:{home_color};">■</span> {home_team} 승</span>
            <span style="font-weight: bold;"><span style="color:grey;">■</span> 무승부</span>
            <span style="font-weight: bold;"><span style="color:{away_color};">■</span> {away_team} 승</span>
        </div>""", unsafe_allow_html=True)

        prediction_fig = create_prediction_bar(prediction, home_color, away_color)
        st.pyplot(prediction_fig, use_container_width=True)

        winner = max(prediction, key=prediction.get)
        if winner == 'win': st.success(f"**결론:** AI는 **{home_team}**의 승리를 더 높게 예측합니다!")
        elif winner == 'draw': st.info("**결론:** AI는 팽팽한 **무승부**를 예측합니다.")
        else: st.error(f"**결론:** AI는 **{away_team}**의 승리를 더 높게 예측합니다!")

st.divider()

# --- 선수 OVR 정보 ---
st.subheader('⭐ 주요 선수 OVR (Overall Rating)')
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**{home_team} 선수단**")
    home_players = players_df[players_df['Team'] == home_team]
    st.dataframe(home_players[['Player', 'Position', 'OVR']].sort_values('OVR', ascending=False).reset_index(drop=True), use_container_width=True, hide_index=True)
with col2:
    st.markdown(f"**{away_team} 선수단**")
    away_players = players_df[players_df['Team'] == away_team]
    st.dataframe(away_players[['Player', 'Position', 'OVR']].sort_values('OVR', ascending=False).reset_index(drop=True), use_container_width=True, hide_index=True)