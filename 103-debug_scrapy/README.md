# 调试scrapy

    # 创建工程
    scrapy startproject spider .

    # 调试爬虫
    # -d：请求解析的深度
    # -v：查看到每个深度级别的状态
    scrapy parse --spider=bilibili -c parse_index -d 2 -v "https://api.bilibili.com/pgc/season/index/result?season_version=1&spoken_language_type=-1&area=-1&is_finish=-1&copyright=-1&season_status=1&season_month=-1&year=-1&style_id=-1&order=3&st=1&sort=0&page=1&season_type=1&pagesize=1&type=1"


## 参考

- https://docs.scrapy.org/en/2.6/topics/debug.html#debugging-spiders

