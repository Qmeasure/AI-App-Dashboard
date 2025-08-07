import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os
from pathlib import Path

# 页面配置
st.set_page_config(
    page_title="Toolify AI工具数据分析仪表板",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 现代化CSS样式
st.markdown("""
<style>
    /* 主题色彩 */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --accent-color: #06b6d4;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
        --dark-bg: #1e293b;
        --light-bg: #f8fafc;
    }
    
    /* 隐藏默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 主标题样式 */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* 现代化指标卡片 */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        margin: 0.5rem 0;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px -3px rgba(0, 0, 0, 0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #64748b;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* 侧边栏样式 */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
    }
    
    .css-1d391kg .css-1avcm0n {
        color: white;
    }
    
    /* 选择框样式 */
    .stSelectbox > div > div {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    /* 表格样式 */
    .dataframe {
        border: none !important;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .dataframe th {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)) !important;
        color: white !important;
        font-weight: 600 !important;
        text-align: center !important;
        padding: 12px !important;
    }
    
    .dataframe td {
        padding: 10px !important;
        border-bottom: 1px solid #f1f5f9 !important;
    }
    
    /* 分段控制器样式 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f1f5f9;
        border-radius: 12px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        padding: 0 24px;
        background: transparent;
        border-radius: 8px;
        color: #64748b;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: white;
        color: var(--primary-color);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* 图表容器 */
    .chart-container {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    /* 响应式设计 */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        
        .metric-card {
            padding: 1rem;
        }
        
        .metric-value {
            font-size: 1.5rem;
        }
    }
    
    /* 加载动画 */
    .stSpinner > div {
        border-color: var(--primary-color) transparent transparent transparent;
    }
    
    /* 成功/警告色彩 */
    .success { color: var(--success-color); }
    .warning { color: var(--warning-color); }
    .danger { color: var(--danger-color); }
    
    /* 渐变背景 */
    .gradient-bg {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """加载和预处理数据"""
    try:
        # 读取主数据文件
        df = pd.read_excel('toolify_processed_2025_summary.xlsx')
        
        # 确保数据类型正确
        month_columns = ['2025年1月访问量', '2025年2月访问量', '2025年3月访问量', 
                        '2025年4月访问量', '2025年5月访问量', '2025年6月访问量']
        
        for col in month_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # 计算MoM增长率
        df = calculate_mom_growth(df)
        
        return df
    except Exception as e:
        st.error(f"数据加载失败: {str(e)}")
        return pd.DataFrame()

def calculate_mom_growth(df):
    """计算月度环比增长率"""
    month_columns = ['2025年1月访问量', '2025年2月访问量', '2025年3月访问量', 
                    '2025年4月访问量', '2025年5月访问量', '2025年6月访问量']
    
    # 计算每月的MoM增长率
    for i in range(1, len(month_columns)):
        current_month = month_columns[i]
        previous_month = month_columns[i-1]
        
        # 计算增长率，避免除零错误
        growth_rate = ((df[current_month] - df[previous_month]) / 
                      (df[previous_month] + 1)) * 100  # +1避免除零
        
        month_name = current_month.replace('访问量', 'MoM%')
        df[month_name] = growth_rate.round(1)
    
    return df

def format_large_number(num):
    """格式化大数字显示"""
    if pd.isna(num):
        return "0"
    if num >= 1e9:
        return f"{num/1e9:.1f}B"
    elif num >= 1e6:
        return f"{num/1e6:.1f}M"
    elif num >= 1e3:
        return f"{num/1e3:.1f}K"
    else:
        return f"{num:.0f}"

def create_mom_heatmap(df):
    """创建MoM增长率热力图"""
    # 准备热力图数据
    mom_columns = [col for col in df.columns if 'MoM%' in col]
    
    if not mom_columns:
        return None
    
    # 按赛道聚合数据
    track_mom = df.groupby('赛道分类')[mom_columns].mean().round(1)
    
    # 创建热力图
    fig = go.Figure(data=go.Heatmap(
        z=track_mom.values,
        x=[col.replace('2025年', '').replace('MoM%', '') for col in mom_columns],
        y=track_mom.index,
        colorscale='RdYlGn',
        zmid=0,
        text=track_mom.values,
        texttemplate="%{text}%",
        textfont={"size": 10},
        hoverongaps=False,
        hovertemplate='<b>%{y}</b><br>%{x}: %{z}%<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': '各赛道月度环比增长率热力图 (MoM%)',
            'x': 0.5,
            'font': {'size': 20, 'family': 'Arial Black'}
        },
        xaxis_title="月份",
        yaxis_title="AI赛道",
        height=600,
        font=dict(size=12),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

def create_track_overview_table(df):
    """创建赛道概览表格"""
    # 按赛道聚合数据
    track_summary = df.groupby('赛道分类').agg({
        'Tools名称': 'count',
        '2025年6月访问量': 'sum',
        '半年访问增量': 'sum',
        '2025H1访问量增速': lambda x: pd.to_numeric(x.str.replace('%', '').str.replace('N/A', '0'), errors='coerce').mean()
    }).round(2)
    
    track_summary.columns = ['工具数量', '6月总访问量', '半年总增量', '平均增速(%)']
    
    # 按6月访问量排序
    track_summary = track_summary.sort_values('6月总访问量', ascending=False)
    
    # 格式化数字
    track_summary['6月总访问量'] = track_summary['6月总访问量'].apply(format_large_number)
    track_summary['半年总增量'] = track_summary['半年总增量'].apply(format_large_number)
    track_summary['平均增速(%)'] = track_summary['平均增速(%)'].apply(lambda x: f"{x:.1f}%" if not pd.isna(x) else "N/A")
    
    return track_summary

def create_growth_distribution_chart(df):
    """创建增长率分布图表"""
    # 处理增速数据
    growth_data = df['2025H1访问量增速'].str.replace('%', '').str.replace('N/A', '0')
    growth_numeric = pd.to_numeric(growth_data, errors='coerce').fillna(0)
    
    # 分段显示分布
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('整体分布', '正增长分布 (0-100%)', '高增长分布 (100%+)', '负增长分布'),
        specs=[[{"type": "histogram"}, {"type": "histogram"}],
               [{"type": "histogram"}, {"type": "histogram"}]]
    )
    
    # 整体分布
    fig.add_trace(
        go.Histogram(x=growth_numeric, nbinsx=50, name="整体", 
                    marker_color='rgba(99, 102, 241, 0.7)'),
        row=1, col=1
    )
    
    # 正增长分布 (0-100%)
    positive_growth = growth_numeric[(growth_numeric >= 0) & (growth_numeric <= 100)]
    fig.add_trace(
        go.Histogram(x=positive_growth, nbinsx=20, name="正增长 (0-100%)",
                    marker_color='rgba(16, 185, 129, 0.7)'),
        row=1, col=2
    )
    
    # 高增长分布 (100%+)
    high_growth = growth_numeric[growth_numeric > 100]
    fig.add_trace(
        go.Histogram(x=high_growth, nbinsx=20, name="高增长 (100%+)",
                    marker_color='rgba(245, 158, 11, 0.7)'),
        row=2, col=1
    )
    
    # 负增长分布
    negative_growth = growth_numeric[growth_numeric < 0]
    fig.add_trace(
        go.Histogram(x=negative_growth, nbinsx=20, name="负增长",
                    marker_color='rgba(239, 68, 68, 0.7)'),
        row=2, col=2
    )
    
    fig.update_layout(
        title={
            'text': '2025H1访问量增速分布分析',
            'x': 0.5,
            'font': {'size': 20}
        },
        height=600,
        showlegend=False
    )
    
    return fig

def create_track_detail_page(df, track_name):
    """创建赛道详情页面"""
    track_data = df[df['赛道分类'] == track_name].copy()
    
    if track_data.empty:
        st.warning(f"未找到 {track_name} 的数据")
        return
    
    # 赛道概览指标
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(track_data)}</div>
            <div class="metric-label">工具总数</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_visits = track_data['2025年6月访问量'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{format_large_number(total_visits)}</div>
            <div class="metric-label">6月总访问量</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_growth = track_data['半年访问增量'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{format_large_number(total_growth)}</div>
            <div class="metric-label">半年总增量</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_growth = track_data['2025H1访问量增速'].str.replace('%', '').str.replace('N/A', '0')
        avg_growth_num = pd.to_numeric(avg_growth, errors='coerce').mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{avg_growth_num:.1f}%</div>
            <div class="metric-label">平均增速</div>
        </div>
        """, unsafe_allow_html=True)
    
    # TOP 10工具排行
    st.markdown(f"### 🏆 {track_name} TOP 10 工具")
    
    # 按6月访问量排序
    top_tools = track_data.nlargest(10, '2025年6月访问量')[
        ['Tools名称', '2025年6月访问量', '半年访问增量', '2025H1访问量增速']
    ].copy()
    
    # 重置索引并添加排名
    top_tools.reset_index(drop=True, inplace=True)
    top_tools.index = top_tools.index + 1
    
    # 使用color-coding显示表格
    def highlight_growth(val):
        if isinstance(val, str) and '%' in val:
            try:
                num = float(val.replace('%', ''))
                if num > 50:
                    return 'background-color: #dcfce7; color: #166534'
                elif num > 0:
                    return 'background-color: #fef3c7; color: #92400e'
                else:
                    return 'background-color: #fee2e2; color: #991b1b'
            except:
                return ''
        return ''
    
    styled_table = top_tools.style.applymap(highlight_growth, subset=['2025H1访问量增速'])
    st.dataframe(styled_table, use_container_width=True)
    
    # 月度趋势图
    st.markdown(f"### 📈 {track_name} 月度访问量趋势")
    
    month_columns = ['2025年1月访问量', '2025年2月访问量', '2025年3月访问量', 
                    '2025年4月访问量', '2025年5月访问量', '2025年6月访问量']
    
    # 选择显示前5名工具的趋势
    top_5_tools = track_data.nlargest(5, '2025年6月访问量')
    
    fig = go.Figure()
    
    for idx, (_, tool) in enumerate(top_5_tools.iterrows()):
        visits = [tool[col] for col in month_columns]
        months = ['1月', '2月', '3月', '4月', '5月', '6月']
        
        fig.add_trace(go.Scatter(
            x=months,
            y=visits,
            mode='lines+markers',
            name=tool['Tools名称'][:20] + ('...' if len(tool['Tools名称']) > 20 else ''),
            line=dict(width=3),
            marker=dict(size=8)
        ))
    
    fig.update_layout(
        title=f"{track_name} TOP 5 工具月度访问量趋势",
        xaxis_title="月份",
        yaxis_title="访问量",
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 增长率分析
    st.markdown(f"### 📊 {track_name} 增长率分析")
    
    growth_data = track_data['2025H1访问量增速'].str.replace('%', '').str.replace('N/A', '0')
    growth_numeric = pd.to_numeric(growth_data, errors='coerce').fillna(0)
    
    fig = px.histogram(
        x=growth_numeric,
        nbins=20,
        title=f"{track_name} 增长率分布",
        labels={'x': '增长率 (%)', 'y': '工具数量'},
        color_discrete_sequence=['#6366f1']
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

def main():
    """主函数"""
    # 页面标题
    st.markdown('<h1 class="main-title">🤖 Toolify AI工具数据分析仪表板</h1>', unsafe_allow_html=True)
    
    # 加载数据
    df = load_data()
    
    if df.empty:
        st.error("无法加载数据，请检查数据文件")
        return
    
    # 侧边栏导航
    st.sidebar.markdown("## 📊 导航菜单")
    
    # 定义重点赛道
    key_tracks = ["AI Chatbot", "AI虚拟陪伴", "AI编程", "AI音频", "AI视频"]
    other_tracks = [track for track in df['赛道分类'].unique() 
                   if track not in key_tracks and track != "其他"]
    
    page_options = ["总览"] + key_tracks + ["其他赛道"]
    selected_page = st.sidebar.selectbox("选择页面", page_options)
    
    if selected_page == "总览":
        # 总览页面
        st.markdown("## 📈 数据总览")
        
        # 核心指标
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_tools = len(df)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_tools:,}</div>
                <div class="metric-label">AI工具总数</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_visits = df['2025年6月访问量'].sum()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{format_large_number(total_visits)}</div>
                <div class="metric-label">6月总访问量</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            total_growth = df['半年访问增量'].sum()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{format_large_number(total_growth)}</div>
                <div class="metric-label">半年总增量</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            avg_growth = df['2025H1访问量增速'].str.replace('%', '').str.replace('N/A', '0')
            avg_growth_num = pd.to_numeric(avg_growth, errors='coerce').mean()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{avg_growth_num:.1f}%</div>
                <div class="metric-label">平均增速</div>
            </div>
            """, unsafe_allow_html=True)
        
        # 赛道概览表
        st.markdown("## 🎯 赛道概览")
        track_overview = create_track_overview_table(df)
        st.dataframe(track_overview, use_container_width=True)
        
        # MoM热力图
        st.markdown("## 🌡️ 月度环比增长率分析")
        mom_heatmap = create_mom_heatmap(df)
        if mom_heatmap:
            st.plotly_chart(mom_heatmap, use_container_width=True)
        
        # 增长率分布
        st.markdown("## 📊 增长率分布分析")
        growth_chart = create_growth_distribution_chart(df)
        st.plotly_chart(growth_chart, use_container_width=True)
        
    elif selected_page in key_tracks:
        # 重点赛道详情页
        st.markdown(f"## 🎯 {selected_page} 详细分析")
        create_track_detail_page(df, selected_page)
        
    elif selected_page == "其他赛道":
        # 其他赛道页面
        st.markdown("## 🔍 其他赛道")
        
        selected_other_track = st.selectbox("选择要查看的赛道", other_tracks)
        
        if selected_other_track:
            create_track_detail_page(df, selected_other_track)

if __name__ == "__main__":
    main()