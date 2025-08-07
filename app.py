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
    
    /* 侧边栏样式 */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
        padding: 1rem 0;
    }
    
    /* 导航按钮样式 */
    .nav-button {
        display: block;
        width: 100%;
        padding: 12px 20px;
        margin: 4px 0;
        background: rgba(255, 255, 255, 0.1);
        color: white;
        text-decoration: none;
        border-radius: 8px;
        border: none;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: left;
    }
    
    .nav-button:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateX(4px);
    }
    
    .nav-button.active {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    
    .nav-section {
        margin: 20px 0;
        padding: 0 16px;
    }
    
    .nav-section-title {
        color: #94a3b8;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 8px;
        padding: 0 4px;
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
        text-align: center;
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
        text-align: center !important;
    }
    
    /* 特殊处理工具名称列 - 左对齐 */
    .dataframe td:first-child {
        text-align: left !important;
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
    
    /* 隐藏Streamlit默认的单选按钮样式 */
    .stRadio > div {
        display: none;
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
        
        # 确保增量列也是数值型
        df['半年访问增量'] = pd.to_numeric(df['半年访问增量'], errors='coerce').fillna(0)
        
        return df
    except Exception as e:
        st.error(f"数据加载失败: {str(e)}")
        return pd.DataFrame()



def format_number(num, is_percentage=False):
    """统一的数字格式化函数"""
    if pd.isna(num) or num == 0:
        return "0" if not is_percentage else "0.0%"
    
    if is_percentage:
        return f"{num:.1f}%"
    else:
        # 访问量和增量使用千分位，不保留小数，统一使用B、M、K格式
        # 处理负数
        is_negative = num < 0
        abs_num = abs(num)
        
        if abs_num >= 1e9:
            formatted = f"{abs_num/1e9:.1f}B"
        elif abs_num >= 1e6:
            formatted = f"{abs_num/1e6:.1f}M"
        elif abs_num >= 1e3:
            formatted = f"{abs_num/1e3:.0f}K"
        else:
            # 小于1000的数字显示完整数字
            formatted = f"{abs_num:.0f}"
        
        # 添加负号
        return f"-{formatted}" if is_negative else formatted

def format_growth_rate(rate_str):
    """格式化增长率字符串"""
    if pd.isna(rate_str) or rate_str == 'N/A':
        return "0.0%"
    
    if isinstance(rate_str, str):
        # 移除百分号并转换为数字
        clean_rate = rate_str.replace('%', '').strip()
        try:
            rate_num = float(clean_rate)
            return f"{rate_num:.1f}%"
        except:
            return "0.0%"
    else:
        try:
            return f"{float(rate_str):.1f}%"
        except:
            return "0.0%"

def create_sidebar_navigation():
    """创建侧边栏导航"""
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h2 style="color: #60a5fa; margin: 0; font-family: 'Arial Black'; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">🚀 AI Analysis</h2>
        <p style="color: #94a3b8; margin: 5px 0 0 0; font-size: 12px;">数据驱动的洞察</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 初始化会话状态
    if 'current_page' not in st.session_state:
        st.session_state.current_page = '总览'
    
    # 定义页面结构
    pages = {
        '总览': '📊',
        'AI Chatbot': '💬',
        'AI虚拟陪伴': '🤗',
        'AI编程': '💻',
        'AI音频': '🎵',
        'AI视频': '🎬',
        '其他赛道': '🔍'
    }
    
    st.sidebar.markdown('<div class="nav-section-title">核心页面</div>', unsafe_allow_html=True)
    
    # 创建导航按钮
    for page_name, icon in pages.items():
        button_class = "nav-button active" if st.session_state.current_page == page_name else "nav-button"
        
        if st.sidebar.button(f"{icon} {page_name}", key=f"nav_{page_name}", use_container_width=True):
            st.session_state.current_page = page_name
            st.rerun()
    
    # 添加其他功能区域
    st.sidebar.markdown('<div class="nav-section-title" style="margin-top: 30px;">数据信息</div>', unsafe_allow_html=True)
    
    # 数据概要信息
    st.sidebar.markdown("""
    <div style="background: rgba(255,255,255,0.1); padding: 12px; border-radius: 8px; margin: 8px 0;">
        <div style="color: #94a3b8; font-size: 11px; margin-bottom: 4px;">数据更新</div>
        <div style="color: white; font-size: 13px;">2025年6月</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("""
    <div style="background: rgba(255,255,255,0.1); padding: 12px; border-radius: 8px; margin: 8px 0;">
        <div style="color: #94a3b8; font-size: 11px; margin-bottom: 4px;">工具总数</div>
        <div style="color: white; font-size: 13px;">1,418个</div>
    </div>
    """, unsafe_allow_html=True)
    
    return st.session_state.current_page

def load_track_summary_data():
    """从各赛道Excel文件读取第一行总和数据"""
    track_data_dir = "data/2025H1"
    track_summary_data = []
    
    if not os.path.exists(track_data_dir):
        return pd.DataFrame()
    
    # 遍历所有Excel文件
    for filename in os.listdir(track_data_dir):
        if filename.startswith("2025H1") and filename.endswith(".xlsx") and "processed" not in filename:
            try:
                file_path = os.path.join(track_data_dir, filename)
                # 读取Excel文件
                track_df = pd.read_excel(file_path)
                
                if len(track_df) > 0:
                    # 获取第一行（总和行）数据
                    summary_row = track_df.iloc[0].copy()
                    track_summary_data.append(summary_row)
                    
            except Exception as e:
                print(f"读取文件 {filename} 时出错: {e}")
                continue
    
    if track_summary_data:
        return pd.DataFrame(track_summary_data)
    else:
        return pd.DataFrame()

def calculate_track_mom_growth(track_summary_df):
    """基于赛道总和数据计算MoM增长率"""
    if track_summary_df.empty:
        return pd.DataFrame()
    
    month_columns = ['2025年1月访问量', '2025年2月访问量', '2025年3月访问量', 
                    '2025年4月访问量', '2025年5月访问量', '2025年6月访问量']
    
    # 确保所有月份列都是数值类型
    for col in month_columns:
        if col in track_summary_df.columns:
            track_summary_df[col] = pd.to_numeric(track_summary_df[col], errors='coerce').fillna(0)
    
    # 计算每月的MoM增长率（5个月环比）
    mom_data = []
    
    for _, row in track_summary_df.iterrows():
        track_name = row.get('赛道分类', '未知赛道')
        mom_row = {'赛道分类': track_name}
        
        # 计算5个月的环比增长率
        for i in range(1, len(month_columns)):
            current_month = month_columns[i]
            previous_month = month_columns[i-1]
            
            current_value = row.get(current_month, 0)
            previous_value = row.get(previous_month, 0)
            
            # 计算MoM增长率
            if previous_value > 0:
                growth_rate = ((current_value - previous_value) / previous_value) * 100
            else:
                growth_rate = 0 if current_value == 0 else 100
            
            # 月份名称（如：2月MoM、3月MoM等）
            month_num = i + 1
            mom_col_name = f"{month_num}月MoM"
            mom_row[mom_col_name] = round(growth_rate, 1)
        
        mom_data.append(mom_row)
    
    return pd.DataFrame(mom_data)

def create_mom_heatmap(df):
    """创建MoM增长率热力图"""
    # 从赛道文件获取总和数据
    track_summary_df = load_track_summary_data()
    
    if track_summary_df.empty:
        return None
    
    # 计算各赛道的总访问量（6个月总和）
    month_columns = ['2025年1月访问量', '2025年2月访问量', '2025年3月访问量', 
                    '2025年4月访问量', '2025年5月访问量', '2025年6月访问量']
    
    # 确保月份列为数值型
    for col in month_columns:
        if col in track_summary_df.columns:
            track_summary_df[col] = pd.to_numeric(track_summary_df[col], errors='coerce').fillna(0)
    
    # 计算总访问量
    track_summary_df['总访问量'] = track_summary_df[month_columns].sum(axis=1)
    
    # 计算MoM增长率
    mom_df = calculate_track_mom_growth(track_summary_df)
    
    if mom_df.empty:
        return None
    
    # 将总访问量信息添加到MoM数据中
    track_summary_df_indexed = track_summary_df.set_index('赛道分类')
    mom_df = mom_df.set_index('赛道分类')
    mom_df['总访问量'] = track_summary_df_indexed['总访问量']
    
    # 按总访问量降序排序（访问量高的在上面）
    # 注意：由于Plotly热力图从下往上显示，所以要用ascending=True让高访问量显示在顶部
    mom_df = mom_df.sort_values('总访问量', ascending=True)
    
    # 准备热力图数据
    mom_columns = [col for col in mom_df.columns if 'MoM' in col]
    
    if not mom_columns:
        return None
    
    # 创建热力图
    fig = go.Figure(data=go.Heatmap(
        z=mom_df[mom_columns].values,
        x=[col.replace('MoM', '') for col in mom_columns],
        y=mom_df.index,
        colorscale='RdYlGn',
        zmid=0,
        text=[[f"{val:.1f}%" for val in row] for row in mom_df[mom_columns].values],
        texttemplate="%{text}",
        textfont={"size": 14, "color": "black", "family": "Arial Black"},
        hoverongaps=False,
        hovertemplate='<b>%{y}</b><br>%{x}环比: %{z:.1f}%<br>总访问量: %{customdata}<extra></extra>',
        customdata=[[format_number(total_visits)] for total_visits in mom_df['总访问量']]
    ))
    
    fig.update_layout(
        title={
            'text': '各赛道月度环比增长率热力图 (MoM%) - 按总访问量排序',
            'x': 0.5,
            'font': {'size': 20, 'family': 'Arial Black'}
        },
        xaxis_title="月份环比",
        yaxis_title="AI赛道 (按总访问量排序)",
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
    }).round(1)
    
    track_summary.columns = ['工具数量', '6月总访问量', '半年总增量', '平均增速']
    
    # 按6月访问量排序
    track_summary = track_summary.sort_values('6月总访问量', ascending=False)
    
    # 保存原始数值用于排序和计算
    track_summary['6月总访问量_原始'] = track_summary['6月总访问量']
    track_summary['半年总增量_原始'] = track_summary['半年总增量']
    
    # 格式化显示
    track_summary['工具数量'] = track_summary['工具数量'].apply(lambda x: f"{x:,}")
    track_summary['6月总访问量'] = track_summary['6月总访问量'].apply(lambda x: format_number(x))
    track_summary['半年总增量'] = track_summary['半年总增量'].apply(lambda x: format_number(x))
    track_summary['平均增速'] = track_summary['平均增速'].apply(lambda x: format_number(x, is_percentage=True))
    
    return track_summary

def create_growth_distribution_chart(df):
    """创建增长率分布图表"""
    # 处理增速数据
    growth_data = df['2025H1访问量增速'].str.replace('%', '').str.replace('N/A', '0')
    growth_numeric = pd.to_numeric(growth_data, errors='coerce').fillna(0)
    
    # 分段显示分布，使用更合理的区间
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('主要分布 (-50% ~ 200%)', '稳定增长 (0% ~ 50%)', '高速增长 (50% ~ 200%)', '下降趋势 (-50% ~ 0%)'),
        specs=[[{"type": "histogram"}, {"type": "histogram"}],
               [{"type": "histogram"}, {"type": "histogram"}]]
    )
    
    # 主要分布 (-50% ~ 200%)
    main_growth = growth_numeric[(growth_numeric >= -50) & (growth_numeric <= 200)]
    fig.add_trace(
        go.Histogram(
            x=main_growth, 
            nbinsx=25, 
            name="主要分布", 
            marker_color='rgba(99, 102, 241, 0.8)',
            hovertemplate='增长率: %{x:.1f}%<br>工具数: %{y}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # 稳定增长 (0% ~ 50%)
    stable_growth = growth_numeric[(growth_numeric >= 0) & (growth_numeric <= 50)]
    fig.add_trace(
        go.Histogram(
            x=stable_growth, 
            nbinsx=15, 
            name="稳定增长",
            marker_color='rgba(16, 185, 129, 0.8)',
            hovertemplate='增长率: %{x:.1f}%<br>工具数: %{y}<extra></extra>'
        ),
        row=1, col=2
    )
    
    # 高速增长 (50% ~ 200%)
    high_growth = growth_numeric[(growth_numeric > 50) & (growth_numeric <= 200)]
    fig.add_trace(
        go.Histogram(
            x=high_growth, 
            nbinsx=15, 
            name="高速增长",
            marker_color='rgba(245, 158, 11, 0.8)',
            hovertemplate='增长率: %{x:.1f}%<br>工具数: %{y}<extra></extra>'
        ),
        row=2, col=1
    )
    
    # 下降趋势 (-50% ~ 0%)
    negative_growth = growth_numeric[(growth_numeric >= -50) & (growth_numeric < 0)]
    fig.add_trace(
        go.Histogram(
            x=negative_growth, 
            nbinsx=15, 
            name="下降趋势",
            marker_color='rgba(239, 68, 68, 0.8)',
            hovertemplate='增长率: %{x:.1f}%<br>工具数: %{y}<extra></extra>'
        ),
        row=2, col=2
    )
    
    # 更新坐标轴标签
    fig.update_xaxes(title_text="增长率 (%)", row=1, col=1)
    fig.update_xaxes(title_text="增长率 (%)", row=1, col=2)
    fig.update_xaxes(title_text="增长率 (%)", row=2, col=1)
    fig.update_xaxes(title_text="增长率 (%)", row=2, col=2)
    
    fig.update_yaxes(title_text="工具数量", row=1, col=1)
    fig.update_yaxes(title_text="工具数量", row=1, col=2)
    fig.update_yaxes(title_text="工具数量", row=2, col=1)
    fig.update_yaxes(title_text="工具数量", row=2, col=2)
    
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
        tool_count = len(track_data)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{tool_count:,}</div>
            <div class="metric-label">工具总数</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_visits = track_data['2025年6月访问量'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{format_number(total_visits)}</div>
            <div class="metric-label">6月总访问量</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_growth = track_data['半年访问增量'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{format_number(total_growth)}</div>
            <div class="metric-label">半年总增量</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_growth = track_data['2025H1访问量增速'].str.replace('%', '').str.replace('N/A', '0')
        avg_growth_num = pd.to_numeric(avg_growth, errors='coerce').mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{format_number(avg_growth_num, is_percentage=True)}</div>
            <div class="metric-label">平均增速</div>
        </div>
        """, unsafe_allow_html=True)
    
    # TOP 10工具排行
    st.markdown(f"### 🏆 {track_name} TOP 10 工具")
    
    # 按6月访问量排序
    top_tools = track_data.nlargest(10, '2025年6月访问量')[
        ['Tools名称', '2025年6月访问量', '半年访问增量', '2025H1访问量增速']
    ].copy()
    
    # 格式化数据显示
    top_tools['6月访问量'] = top_tools['2025年6月访问量'].apply(lambda x: format_number(x))
    top_tools['半年增量'] = top_tools['半年访问增量'].apply(lambda x: format_number(x))
    top_tools['增长率'] = top_tools['2025H1访问量增速'].apply(lambda x: format_growth_rate(x))
    
    # 重置索引并添加排名
    display_df = top_tools[['Tools名称', '6月访问量', '半年增量', '增长率']].copy()
    display_df.reset_index(drop=True, inplace=True)
    display_df.index = display_df.index + 1
    
    # 设置表格样式，数字居中对齐
    st.markdown("""
    <style>
    .track-table table {
        margin: 0 auto;
    }
    .track-table td:nth-child(2),
    .track-table td:nth-child(3),
    .track-table td:nth-child(4) {
        text-align: center !important;
    }
    .track-table th:nth-child(2),
    .track-table th:nth-child(3),
    .track-table th:nth-child(4) {
        text-align: center !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 使用HTML表格以确保样式生效
    st.markdown('<div class="track-table">', unsafe_allow_html=True)
    st.dataframe(display_df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 月度趋势图
    st.markdown(f"### 📈 {track_name} 月度访问量趋势")
    
    month_columns = ['2025年1月访问量', '2025年2月访问量', '2025年3月访问量', 
                    '2025年4月访问量', '2025年5月访问量', '2025年6月访问量']
    
    # 选择显示前5名工具的趋势
    top_5_tools = track_data.nlargest(5, '2025年6月访问量')
    
    fig = go.Figure()
    
    colors = ['#6366f1', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b']
    
    for idx, (_, tool) in enumerate(top_5_tools.iterrows()):
        visits = [tool[col] for col in month_columns]
        months = ['1月', '2月', '3月', '4月', '5月', '6月']
        
        # 格式化hover text
        hover_text = [f"{month}: {format_number(visit)}" for month, visit in zip(months, visits)]
        
        fig.add_trace(go.Scatter(
            x=months,
            y=visits,
            mode='lines+markers',
            name=tool['Tools名称'][:20] + ('...' if len(tool['Tools名称']) > 20 else ''),
            line=dict(width=3, color=colors[idx % len(colors)]),
            marker=dict(size=8),
            hovertemplate='<b>%{fullData.name}</b><br>%{text}<extra></extra>',
            text=hover_text
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
    
    # 格式化Y轴
    fig.update_yaxes(tickformat=",.0f")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 月度环比增速分析
    st.markdown(f"### 📈 {track_name} 月度环比增速分析")
    
    # 计算各月环比增速
    month_columns = ['2025年1月访问量', '2025年2月访问量', '2025年3月访问量', 
                    '2025年4月访问量', '2025年5月访问量', '2025年6月访问量']
    
    # 计算赛道总体的月度访问量
    track_monthly_totals = []
    for col in month_columns:
        total = track_data[col].sum()
        track_monthly_totals.append(total)
    
    # 计算环比增速
    mom_rates = []
    for i in range(1, len(track_monthly_totals)):
        if track_monthly_totals[i-1] > 0:
            mom_rate = ((track_monthly_totals[i] - track_monthly_totals[i-1]) / track_monthly_totals[i-1]) * 100
        else:
            mom_rate = 0
        mom_rates.append(mom_rate)
    
    # 创建环比增速图
    fig_mom = go.Figure()
    
    months = ['2月', '3月', '4月', '5月', '6月']
    colors = ['#ef4444' if rate < 0 else '#10b981' if rate < 20 else '#f59e0b' for rate in mom_rates]
    
    fig_mom.add_trace(go.Bar(
        x=months,
        y=mom_rates,
        name='月度环比增速',
        marker_color=colors,
        text=[f'{rate:.1f}%' for rate in mom_rates],
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>环比增速: %{y:.1f}%<extra></extra>'
    ))
    
    fig_mom.update_layout(
        title=f'{track_name} 月度环比增速走势',
        xaxis_title='月份',
        yaxis_title='环比增速 (%)',
        height=400,
        showlegend=False
    )
    
    # 添加零线
    fig_mom.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="零增长线")
    
    st.plotly_chart(fig_mom, use_container_width=True)
    
    # 访问量与增量双轴图
    st.markdown(f"### 💹 {track_name} 访问量vs增量分析")
    
    # 按访问量排序的TOP 15工具
    top_15_tools = track_data.nlargest(15, '2025年6月访问量')
    
    fig_dual = go.Figure()
    
    # 6月访问量（柱状图）
    fig_dual.add_trace(go.Bar(
        x=top_15_tools['Tools名称'],
        y=top_15_tools['2025年6月访问量'],
        name='6月访问量',
        marker_color='rgba(99, 102, 241, 0.7)',
        yaxis='y',
        hovertemplate='<b>%{x}</b><br>6月访问量: %{y:,.0f}<extra></extra>'
    ))
    
    # 半年增量（线图）
    fig_dual.add_trace(go.Scatter(
        x=top_15_tools['Tools名称'],
        y=top_15_tools['半年访问增量'],
        mode='lines+markers',
        name='半年增量',
        line=dict(color='rgba(239, 68, 68, 1)', width=3),
        marker=dict(size=8, color='rgba(239, 68, 68, 1)'),
        yaxis='y2',
        hovertemplate='<b>%{x}</b><br>半年增量: %{y:,.0f}<extra></extra>'
    ))
    
    # 设置双Y轴
    fig_dual.update_layout(
        title=f'{track_name} TOP 15工具访问量与增量对比',
        xaxis_title='工具名称',
        height=500,
        yaxis=dict(
            title='6月访问量',
            side='left',
            showgrid=True
        ),
        yaxis2=dict(
            title='半年增量',
            side='right',
            overlaying='y',
            showgrid=False
        ),
        legend=dict(x=0.01, y=0.99),
        hovermode='x unified'
    )
    
    # 旋转X轴标签避免重叠
    fig_dual.update_xaxes(tickangle=45)
    
    st.plotly_chart(fig_dual, use_container_width=True)
    
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
    
    fig.update_traces(
        hovertemplate='增长率: %{x:.1f}%<br>工具数: %{y}<extra></extra>'
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

def create_other_tracks_page(df):
    """创建其他赛道页面"""
    key_tracks = ["AI Chatbot", "AI虚拟陪伴", "AI编程", "AI音频", "AI视频"]
    other_tracks = [track for track in df['赛道分类'].unique() 
                   if track not in key_tracks and track != "其他"]
    
    st.markdown("## 🔍 其他赛道选择")
    
    # 创建选择框
    selected_track = st.selectbox(
        "选择要查看的赛道",
        other_tracks,
        key="other_track_select"
    )
    
    if selected_track:
        st.markdown(f"## 📊 {selected_track} 详细分析")
        create_track_detail_page(df, selected_track)

def main():
    """主函数"""
    # 加载数据
    df = load_data()
    
    if df.empty:
        st.error("无法加载数据，请检查数据文件")
        return
    
    # 创建侧边栏导航并获取当前页面
    current_page = create_sidebar_navigation()
    
    # 主内容区域
    if current_page == "总览":
        # 页面标题
        st.markdown('<h1 class="main-title">📊 AI工具数据总览</h1>', unsafe_allow_html=True)
        
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
                <div class="metric-value">{format_number(total_visits)}</div>
                <div class="metric-label">6月总访问量</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            total_growth = df['半年访问增量'].sum()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{format_number(total_growth)}</div>
                <div class="metric-label">半年总增量</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            avg_growth = df['2025H1访问量增速'].str.replace('%', '').str.replace('N/A', '0')
            avg_growth_num = pd.to_numeric(avg_growth, errors='coerce').mean()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{format_number(avg_growth_num, is_percentage=True)}</div>
                <div class="metric-label">平均增速</div>
            </div>
            """, unsafe_allow_html=True)
        
        # 赛道概览表
        st.markdown("## 🎯 赛道概览")
        track_overview = create_track_overview_table(df)
        
        # 显示表格（不包含原始数据列）
        display_cols = ['工具数量', '6月总访问量', '半年总增量', '平均增速']
        st.dataframe(track_overview[display_cols], use_container_width=True)
        
        # MoM热力图
        st.markdown("## 🌡️ 月度环比增长率分析")
        mom_heatmap = create_mom_heatmap(df)
        if mom_heatmap:
            st.plotly_chart(mom_heatmap, use_container_width=True)
        
        # 增长率分布
        st.markdown("## 📊 增长率分布分析")
        growth_chart = create_growth_distribution_chart(df)
        st.plotly_chart(growth_chart, use_container_width=True)
        
    elif current_page in ["AI Chatbot", "AI虚拟陪伴", "AI编程", "AI音频", "AI视频"]:
        # 重点赛道详情页
        icon_map = {
            "AI Chatbot": "💬",
            "AI虚拟陪伴": "🤗", 
            "AI编程": "💻",
            "AI音频": "🎵",
            "AI视频": "🎬"
        }
        st.markdown(f'<h1 class="main-title">{icon_map[current_page]} {current_page} 详细分析</h1>', unsafe_allow_html=True)
        create_track_detail_page(df, current_page)
        
    elif current_page == "其他赛道":
        # 其他赛道页面
        st.markdown('<h1 class="main-title">🔍 其他赛道</h1>', unsafe_allow_html=True)
        create_other_tracks_page(df)

if __name__ == "__main__":
    main()