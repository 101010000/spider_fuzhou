# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd

class ScrapyFuzhouPipeline:
    def __init__(self):
        self.data = []  # 创建一个空列表用于保存数据

    def process_item(self, item, spider):
        self.data.append({
            'title': item['title'],
            'date': item['date'],
            'email': item['email'],
            'tel': item['tel']
        })
        return item

    def close_spider(self, spider):
        df = pd.DataFrame(self.data)  # 创建DataFrame
        df.to_excel('fuzhou.xlsx', index=False)  # 导出到Excel文件