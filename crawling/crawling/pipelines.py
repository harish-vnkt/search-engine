# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from os import POSIX_FADV_WILLNEED
from itemadapter import ItemAdapter
from scrapy.exporters import JsonLinesItemExporter


class CrawlingPipeline:

    def __init__(self, file_name) -> None:
        self.file_name = file_name
        self.file_handle = None

    def open_spider(self, spider):
        print("Export started")
        self.file_handle = open(self.file_name, 'wb')
        self.exporter = JsonLinesItemExporter(self.file_handle)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        print("Export stopped")
        self.exporter.finish_exporting()
        self.file_handle.close()

    @classmethod
    def from_crawler(cls, crawler):
        output_file_name = crawler.settings.get('FILE_NAME')
        return cls(output_file_name)

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
