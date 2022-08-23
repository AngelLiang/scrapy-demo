import scrapy
import pprint
import json
from scrapy.exceptions import CloseSpider

from ..items import AnimeItem, EpisodeItem


class BilibiliSpider(scrapy.Spider):
    name = 'bilibili'
    # start_urls = ['http://bilibili.com/']

    custom_settings = {
        'COOKIES_ENABLED': False,
        'DOWNLOADER_DELAY': 10.3,
    }

    # 番剧索引
    index_url = 'https://api.bilibili.com/pgc/season/index/result?season_version=1&spoken_language_type=-1&area=-1&is_finish=-1&copyright=-1&season_status=1&season_month=-1&year=-1&style_id=-1&order=3&st=1&sort=0&page={page}&season_type=1&pagesize={pagesize}&type=1'
    section_url = 'https://api.bilibili.com/pgc/web/season/section?season_id={season_id}'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.params = {
            'page': getattr(self, 'page', None) or 1,
            'pagesize': getattr(self, 'pagesize', None) or 20,
        }

    def start_requests(self):
        urls = [
            self.index_url.format(**self.params)
        ]
        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_index
            )

    def parse_index(self, response):
        """
        @url https://api.bilibili.com/pgc/season/index/result?season_version=1&spoken_language_type=-1&area=-1&is_finish=-1&copyright=-1&season_status=1&season_month=-1&year=-1&style_id=-1&order=3&st=1&sort=0&page=1&season_type=1&pagesize=20&type=1
        @returns items 1
        """
        try:
            jsondata = response.json()
        except Exception:
            raise CloseSpider('解析json失败')

        if 'data' not in jsondata:
            raise CloseSpider('json没有数据')

        data = jsondata['data']
        if 'list' in data:
            _list = data['list']
            for item in _list:
                yield AnimeItem(**item)
                season_id = item['season_id']
                url = self.section_url.format(season_id=season_id)
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_episode,
                    cb_kwargs={'season_id': season_id}
                )

        if 'has_next' in data and data['has_next'] == 1:
            self.params['page'] += 1
            yield scrapy.Request(
                url=self.index_url.format(**self.params),
                callback=self.parse_index
            )

    def parse_episode(self, response, season_id=None):
        """
        @url https://api.bilibili.com/pgc/web/season/section?season_id=26801
        @returns items 1
        """
        try:
            jsondata = response.json()
        except Exception:
            raise CloseSpider('解析json失败')

        if 'result' not in jsondata:
            raise CloseSpider('json没有数据')

        result = jsondata['result']
        if 'main_section' not in result:
            print('没有正片')
            return

        main_section = jsondata['result']['main_section']
        # pprint.pprint(main_section)
        for item in main_section['episodes']:
            if 'from' in item:
                item['_from'] = item['from']
                del item['from']
            yield EpisodeItem(
                **item,
                season_id=season_id,
            )
