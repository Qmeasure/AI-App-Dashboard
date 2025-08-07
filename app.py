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

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .track-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #667eea;
        border-bottom: 2px solid #667eea;
        padding-bottom: 0.5rem;
        margin: 1rem 0;
    }
    
    .stDataFrame {
        border: 1px solid #e1e5e9;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_summary_data():
    """加载总表数据"""
    return pd.read_excel('toolify_processed_2025_summary.xlsx')

@st.cache_data
def load_track_data():
    """加载各赛道数据"""
    track_files = {}
    data_dir = Path('data/2025H1')
    
    for file_path in data_dir.glob('2025H1*.xlsx'):
        track_name = file_path.stem.replace('2025H1', '')
        try:
            df = pd.read_excel(file_path)
            track_files[track_name] = df
        except Exception as e:
            st.warning(f"无法读取文件 {file_path}: {e}")
    
    return track_files

def format_number(num):
    """格式化数字显示"""
    if pd.isna(num):
        return "N/A"
    if num >= 1e9:
        return f"{num/1e9:.1f}B"
    elif num >= 1e6:
        return f"{num/1e6:.1f}M"
    elif num >= 1e3:
        return f"{num/1e3:.1f}K"
    else:
        return f"{num:,.0f}"

def create_overview_metrics(df):
    """创建概览指标"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 总工具数</h3>
            <h2>{:,}</h2>
        </div>
        """.format(len(df)), unsafe_allow_html=True)
    
    with col2:
        total_visits_june = df['2025年6月访问量'].sum()
        st.markdown("""
        <div class="metric-card">
            <h3>🚀 6月总访问量</h3>
            <h2>{}</h2>
        </div>
        """.format(format_number(total_visits_june)), unsafe_allow_html=True)
    
    with col3:
        total_growth = df['半年访问增量'].sum()
        st.markdown("""
        <div class="metric-card">
            <h3>📈 半年总增量</h3>
            <h2>{}</h2>
        </div>
        """.format(format_number(total_growth)), unsafe_allow_html=True)
    
    with col4:
        track_count = df['赛道分类'].nunique()
        st.markdown("""
        <div class="metric-card">
            <h3>🎯 赛道数量</h3>
            <h2>{}</h2>
        </div>
        """.format(track_count), unsafe_allow_html=True)

def create_track_distribution_chart(df):
    """创建赛道分布图表"""
    track_counts = df['赛道分类'].value_counts()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 饼图
        fig_pie = px.pie(
            values=track_counts.values, 
            names=track_counts.index,
            title="🎯 AI工具赛道分布",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_layout(height=500)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # 条形图
        fig_bar = px.bar(
            x=track_counts.values,
            y=track_counts.index,
            orientation='h',
            title="📊 各赛道工具数量排行",
            color=track_counts.values,
            color_continuous_scale="viridis"
        )
        fig_bar.update_layout(height=500, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_bar, use_container_width=True)

def create_growth_analysis(df):
    """创建增长分析图表"""
    # 获取有效增长率数据
    df_growth = df[df['2025H1访问量增速'] != 'N/A'].copy()
    df_growth['增长率'] = df_growth['2025H1访问量增速'].str.rstrip('%').astype(float)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 增长率分布直方图
        fig_hist = px.histogram(
            df_growth, 
            x='增长率',
            title="📈 工具增长率分布",
            nbins=50,
            color_discrete_sequence=['#667eea']
        )
        fig_hist.update_layout(height=400)
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        # 各赛道平均增长率
        track_growth = df_growth.groupby('赛道分类')['增长率'].mean().sort_values(ascending=True)
        fig_track_growth = px.bar(
            x=track_growth.values,
            y=track_growth.index,
            orientation='h',
            title="🚀 各赛道平均增长率",
            color=track_growth.values,
            color_continuous_scale="Reds"
        )
        fig_track_growth.update_layout(height=400, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_track_growth, use_container_width=True)

def create_top_tools_analysis(df):
    """创建顶级工具分析"""
    st.markdown('<div class="track-header">🏆 顶级工具分析</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 访问量TOP 10")
        top_visits = df.nlargest(10, '2025年6月访问量')[['Tools名称', '2025年6月访问量', '赛道分类']]
        top_visits['2025年6月访问量'] = top_visits['2025年6月访问量'].apply(format_number)
        st.dataframe(top_visits, use_container_width=True, hide_index=True)
    
    with col2:
        st.subheader("🚀 增长量TOP 10")
        top_growth = df.nlargest(10, '半年访问增量')[['Tools名称', '半年访问增量', '2025H1访问量增速', '赛道分类']]
        top_growth['半年访问增量'] = top_growth['半年访问增量'].apply(format_number)
        st.dataframe(top_growth, use_container_width=True, hide_index=True)

def display_track_details(track_files):
    """显示赛道详细信息"""
    st.markdown('<div class="track-header">🎯 赛道详细分析</div>', unsafe_allow_html=True)
    
    # 选择赛道
    selected_track = st.selectbox(
        "选择要查看的赛道：",
        options=list(track_files.keys()),
        key="track_selector"
    )
    
    if selected_track and selected_track in track_files:
        df_track = track_files[selected_track]
        
        # 赛道概览
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("工具数量", len(df_track) - 1)  # 减去总和行
        
        with col2:
            if len(df_track) > 1:
                total_visits = df_track.iloc[0]['2025年6月访问量']
                st.metric("6月总访问量", format_number(total_visits))
        
        with col3:
            if len(df_track) > 1:
                total_growth = df_track.iloc[0]['半年访问增量']
                st.metric("半年总增量", format_number(total_growth))
        
        # 显示表格
        st.subheader(f"📋 {selected_track} 详细数据")
        
        # 格式化数据显示
        df_display = df_track.copy()
        for col in ['2025年6月访问量', '2025年5月访问量', '2025年4月访问量', 
                   '2025年3月访问量', '2025年2月访问量', '2025年1月访问量', '半年访问增量']:
            if col in df_display.columns:
                df_display[col] = df_display[col].apply(lambda x: format_number(x) if pd.notna(x) else 'N/A')
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        # 赛道内工具对比图表
        if len(df_track) > 2:  # 除了总和行，至少有2个工具
            track_tools = df_track.iloc[1:].copy()  # 排除总和行
            
            if len(track_tools) > 0:
                col1, col2 = st.columns(2)
                
                with col1:
                    # 访问量对比
                    fig_visits = px.bar(
                        track_tools.head(10),
                        x='Tools名称',
                        y='2025年6月访问量',
                        title=f"{selected_track} - 工具访问量对比",
                        color='2025年6月访问量',
                        color_continuous_scale="Blues"
                    )
                    fig_visits.update_xaxes(tickangle=45)
                    st.plotly_chart(fig_visits, use_container_width=True)
                
                with col2:
                    # 增长率对比（如果有增长率数据）
                    if '2025H1访问量增速' in track_tools.columns:
                        valid_growth = track_tools[track_tools['2025H1访问量增速'] != 'N/A'].copy()
                        if len(valid_growth) > 0:
                            valid_growth['增长率'] = valid_growth['2025H1访问量增速'].str.rstrip('%').astype(float)
                            fig_growth = px.bar(
                                valid_growth.head(10),
                                x='Tools名称',
                                y='增长率',
                                title=f"{selected_track} - 工具增长率对比",
                                color='增长率',
                                color_continuous_scale="Reds"
                            )
                            fig_growth.update_xaxes(tickangle=45)
                            st.plotly_chart(fig_growth, use_container_width=True)

def main():
    """主函数"""
    # 标题
    st.markdown('<div class="main-header">🤖 Toolify AI工具数据分析仪表板</div>', unsafe_allow_html=True)
    
    # 加载数据
    try:
        df_summary = load_summary_data()
        track_files = load_track_data()
        
        # 侧边栏
        st.sidebar.title("📊 导航菜单")
        view_option = st.sidebar.selectbox(
            "选择视图：",
            ["🏠 总览", "📈 数据分析", "🎯 赛道详情", "📋 原始数据"]
        )
        
        if view_option == "🏠 总览":
            st.markdown("### 📊 数据概览")
            create_overview_metrics(df_summary)
            
            st.markdown("---")
            create_track_distribution_chart(df_summary)
            
        elif view_option == "📈 数据分析":
            st.markdown("### 📈 深度数据分析")
            create_growth_analysis(df_summary)
            
            st.markdown("---")
            create_top_tools_analysis(df_summary)
            
        elif view_option == "🎯 赛道详情":
            display_track_details(track_files)
            
        elif view_option == "📋 原始数据":
            st.markdown("### 📋 原始数据查看")
            st.subheader("🗂️ 总表数据")
            st.dataframe(df_summary, use_container_width=True)
            
            st.markdown("---")
            st.subheader("📁 数据下载")
            st.download_button(
                label="📥 下载总表数据 (Excel)",
                data=open('toolify_processed_2025_summary.xlsx', 'rb').read(),
                file_name='toolify_processed_2025_summary.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        
        # 页脚
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666; padding: 20px;">
            📊 Toolify AI工具数据分析仪表板 | 数据更新时间: 2025年1月-6月 | 
            💡 总工具数: {:,} | 🎯 覆盖赛道: {} 个
        </div>
        """.format(len(df_summary), df_summary['赛道分类'].nunique()), unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"数据加载失败: {e}")
        st.info("请确保数据文件存在于正确的路径中。")

if __name__ == "__main__":
    main()