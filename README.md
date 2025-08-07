# 🤖 Toolify AI工具数据分析仪表板

一个基于Streamlit构建的交互式数据分析仪表板，用于展示和分析Toolify AI工具的访问量、增长率和赛道分布数据。

## ✨ 功能特性

- 📊 **数据概览**: 总体统计指标和赛道分布可视化
- 📈 **深度分析**: 增长率分析、顶级工具排行
- 🎯 **赛道详情**: 各AI赛道的详细数据展示和对比
- 📋 **原始数据**: 完整数据表格查看和下载功能

## 🚀 快速开始

### 本地运行

1. 克隆仓库
```bash
git clone <your-repo-url>
cd toolify_dashboard
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行应用
```bash
streamlit run app.py
```

4. 在浏览器中打开 `http://localhost:8501`

### 在线访问

访问部署的应用: [Streamlit Cloud链接]

## 📊 数据说明

### 数据来源
- **数据范围**: 2025年1月-6月
- **工具数量**: 1,418个AI工具
- **覆盖赛道**: 18个AI细分领域

### 主要指标
- **半年访问增量**: 2025年6月与1月访问量的差值
- **2025H1访问量增速**: (最晚月份-最早月份)/最早月份 × 100%
- **赛道分类**: 基于工具功能和应用场景的智能分类

### 赛道分类
- 🤖 AI Chatbot
- 🖼️ AI图像  
- 🎥 AI视频
- ✍️ AI写作
- 👥 AI虚拟陪伴
- 💻 AI编程
- 🎵 AI音乐
- 🔊 AI音频
- 📚 AI教育
- 📈 AI市场营销
- 🤖 AI Agent
- 📊 AI数据分析
- 🏢 AI Office
- ⚖️ AI法律金融
- 🏥 AI健康
- 🔒 AI安全
- 🎨 AI艺术创作
- 📂 其他

## 🛠️ 技术栈

- **前端框架**: Streamlit
- **数据处理**: Pandas, NumPy
- **可视化**: Plotly
- **数据格式**: Excel (XLSX)

## 📁 项目结构

```
toolify_dashboard/
├── app.py                              # 主应用文件
├── requirements.txt                     # Python依赖
├── README.md                           # 项目说明
├── toolify_processed_2025_summary.xlsx # 总表数据
└── data/
    └── 2025H1/                         # 分赛道数据文件
        ├── 2025H1AI Chatbot.xlsx
        ├── 2025H1AI图像.xlsx
        ├── 2025H1AI视频.xlsx
        └── ...
```

## 📈 主要可视化图表

1. **赛道分布饼图**: 各AI赛道工具数量占比
2. **工具数量条形图**: 各赛道工具数量排行
3. **增长率分布直方图**: 工具增长率分布情况
4. **赛道平均增长率**: 各赛道增长表现对比
5. **TOP工具排行**: 访问量和增长量排行榜
6. **赛道内对比**: 单个赛道内工具详细对比

## 🔧 自定义配置

### 样式调整
应用使用自定义CSS样式，可在`app.py`中的`st.markdown`部分修改样式配置。

### 数据更新
替换数据文件即可更新展示内容：
- 总表: `toolify_processed_2025_summary.xlsx`
- 分赛道: `data/2025H1/` 目录下的Excel文件

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📞 联系方式

如有问题或建议，请通过GitHub Issues联系。