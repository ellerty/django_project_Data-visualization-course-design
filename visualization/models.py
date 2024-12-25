from django.db import models

class RichPerson(models.Model):
    rank = models.IntegerField()
    name = models.CharField(max_length=255)
    total_net_worth = models.CharField(max_length=50)
    last_change = models.CharField(max_length=50)
    ytd_change = models.CharField(max_length=50)
    country_region = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)

    # 新增字段
    extract = models.TextField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    titles = models.JSONField(null=True, blank=True)  # 使用 JSONField 存储列表
    def __str__(self):
        return f"{self.rank}. {self.name}"
