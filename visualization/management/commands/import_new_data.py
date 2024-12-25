import os
import json
from django.core.management.base import BaseCommand
from django.conf import settings
from visualization.models import RichPerson

class Command(BaseCommand):
    help = 'Imports data from people_info.json into the RichPerson model'

    def handle(self, *args, **options):
        # 指定 JSON 文件路径
        json_file_path = os.path.join(settings.BASE_DIR, 'visualization/people_info.json')

        # 加载 JSON 数据
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                people_info = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"文件未找到: {json_file_path}"))
            return
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f"JSON 解码错误: {e}"))
            return

        # 统计更新情况
        updated = 0
        created = 0
        skipped = 0

        for name, info in people_info.items():
            try:
                # 根据 name 查找对应的 RichPerson 实例
                person, created_flag = RichPerson.objects.get_or_create(name=name)

                # 更新字段
                person.extract = info.get('extract', person.extract)
                person.image_url = info.get('image_url', person.image_url)
                person.titles = info.get('titles', person.titles)
                person.save()

                if created_flag:
                    created += 1
                    self.stdout.write(self.style.SUCCESS(f"创建新记录: {name}"))
                else:
                    updated += 1
                    self.stdout.write(self.style.SUCCESS(f"更新记录: {name}"))

            except Exception as e:
                skipped += 1
                self.stdout.write(self.style.ERROR(f"处理 {name} 时出错: {e}"))

        self.stdout.write(self.style.SUCCESS(f"导入完成: 创建 {created} 条，更新 {updated} 条，跳过 {skipped} 条。"))