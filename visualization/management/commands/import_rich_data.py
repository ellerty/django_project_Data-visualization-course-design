import pandas as pd
from django.core.management.base import BaseCommand
from visualization.models import RichPerson
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Import rich person data from CSV to the database'

    def handle(self, *args, **kwargs):
        # 构建 CSV 文件路径
        csv_file_path = os.path.join(settings.BASE_DIR, 'top rich2024.csv')
        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR(f"CSV file not found at {csv_file_path}"))
            return

        # 使用 pandas 读取 CSV 文件
        try:
            data = pd.read_csv(csv_file_path, encoding='utf-8-sig')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error reading CSV file: {e}"))
            return

        # 预处理数据（去掉多余的空格，处理 NaN 值等）
        data = data.rename(columns=lambda x: x.strip())  # 去掉列名中的空格
        data = data.applymap(lambda x: x.strip() if isinstance(x, str) else x)  # 去掉单元格中的空格

        # 遍历数据并写入数据库
        for _, row in data.iterrows():
            try:
                # 转换数据类型
                rank = int(row['Rank']) if pd.notna(row['Rank']) and str(row['Rank']).isdigit() else None
                total_net_worth = row['Total net worth'] if pd.notna(row['Total net worth']) else ''
                last_change = row['$ Last change'] if pd.notna(row['$ Last change']) else ''
                ytd_change = row['$ YTD change'] if pd.notna(row['$ YTD change']) else ''
                country_region = row['Country / Region'] if pd.notna(row['Country / Region']) else ''
                industry = row['Industry'] if pd.notna(row['Industry']) else ''

                # 确保关键字段非空
                if rank is not None and country_region:
                    RichPerson.objects.update_or_create(
                        rank=rank,
                        defaults={
                            'name': row['Name'] if pd.notna(row['Name']) else '',
                            'total_net_worth': total_net_worth,
                            'last_change': last_change,
                            'ytd_change': ytd_change,
                            'country_region': country_region,
                            'industry': industry,
                        }
                    )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing row {row.to_dict()}: {e}"))

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
