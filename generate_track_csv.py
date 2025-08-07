#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
根据赛道分类生成分组Excel文件
"""

import pandas as pd
import os

def generate_track_excel_files():
    """根据赛道分类生成Excel文件"""
    
    # 读取处理后的Excel文件
    print("读取Excel文件...")
    df = pd.read_excel('toolify_processed_2025_summary.xlsx')
    
    print(f"总共读取了 {len(df)} 条记录")
    
    # 按赛道分类分组
    print("\n按赛道分类分组...")
    track_groups = df.groupby('赛道分类')
    
    print(f"共有 {len(track_groups)} 个赛道分类:")
    for track_name, group in track_groups:
        print(f"  {track_name}: {len(group)} 个工具")
    
    # 创建输出目录（如果不存在）
    output_dir = "/Users/blackfischer/Downloads/Toolify/toolify_dashboard/data/2025H1"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n开始生成Excel文件到 {output_dir} 目录...")
    
    # 为每个赛道生成Excel文件
    for track_name, group_data in track_groups:
        try:
            # 准备数据
            track_data = group_data.copy()
            
            # 计算总和行，包括2025H1访问量增速
            # 计算半年访问增量总和
            total_increment = track_data['半年访问增量'].sum()
            
            # 计算各月访问量总和
            total_jan = track_data['2025年1月访问量'].sum()
            total_feb = track_data['2025年2月访问量'].sum()
            total_mar = track_data['2025年3月访问量'].sum()
            total_apr = track_data['2025年4月访问量'].sum()
            total_may = track_data['2025年5月访问量'].sum()
            total_jun = track_data['2025年6月访问量'].sum()
            
            # 计算该赛道的2025H1访问量增速
            # 找到最早有访问量的月份和最晚有访问量的月份
            monthly_totals = [total_jan, total_feb, total_mar, total_apr, total_may, total_jun]
            monthly_names = ['1月', '2月', '3月', '4月', '5月', '6月']
            
            # 找到第一个和最后一个非零月份
            earliest_visit = 0
            latest_visit = 0
            
            for i, total in enumerate(monthly_totals):
                if total > 0:
                    if earliest_visit == 0:
                        earliest_visit = total
                    latest_visit = total
            
            # 计算增速
            if earliest_visit > 0 and latest_visit != earliest_visit:
                growth_rate = ((latest_visit - earliest_visit) / earliest_visit) * 100
                h1_growth_rate = f"{growth_rate:.1f}%"
            else:
                h1_growth_rate = "N/A"
            
            summary_row = {
                'Tools名称': f'{track_name}赛道总和',
                '半年访问增量': total_increment,
                '2025H1访问量增速': h1_growth_rate,
                '2025年6月访问量': total_jun,
                '2025年5月访问量': total_may,
                '2025年4月访问量': total_apr,
                '2025年3月访问量': total_mar,
                '2025年2月访问量': total_feb,
                '2025年1月访问量': total_jan,
                'Introduction': '',
                'Tags': '',
                '赛道分类': track_name
            }
            
            # 将总和行添加到数据框的第一行
            summary_df = pd.DataFrame([summary_row])
            final_data = pd.concat([summary_df, track_data], ignore_index=True)
            
            # 生成Excel文件名
            excel_filename = f"2025H1{track_name}.xlsx"
            excel_path = os.path.join(output_dir, excel_filename)
            
            # 保存Excel文件
            final_data.to_excel(excel_path, index=False, engine='openpyxl')
            
            print(f"✅ 已生成: {excel_filename} ({len(track_data)} 个工具 + 1 个总和行)")
            
        except Exception as e:
            print(f"❌ 生成 {track_name} 的Excel文件时出错: {e}")
    
    print(f"\n🎉 所有Excel文件已生成完成！")
    print(f"文件位置: {os.path.abspath(output_dir)}")
    
    # 列出生成的文件
    print("\n生成的文件列表:")
    for filename in sorted(os.listdir(output_dir)):
        if filename.endswith('.xlsx'):
            file_path = os.path.join(output_dir, filename)
            file_size = os.path.getsize(file_path)
            print(f"  {filename} ({file_size:,} bytes)")

if __name__ == "__main__":
    generate_track_excel_files()