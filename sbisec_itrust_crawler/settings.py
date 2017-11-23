# vim:set fileencoding=utf-8, fileformat=unix
#
# Scrapy settings for sbisec_itrust_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'sbisec_itrust_crawler'

SPIDER_MODULES = ['sbisec_itrust_crawler.spiders']
NEWSPIDER_MODULE = 'sbisec_itrust_crawler.spiders'


# Crawl responsibly by identifying yourself (and your website) on the
# user-agent

USER_AGENT = 'sbisec_itrust_crawler (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
DOWNLOAD_DELAY = 5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'sbisec_itrust_crawler.middlewares.SbisecITrustCrawlerSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'sbisec_itrust_crawler.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'sbisec_itrust_crawler.pipelines.SbisecTrustCrawlerPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See
# http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = True
#HTTPCACHE_ENABLED = False
#HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Enable and configure CSV Feed exporter

FEED_URI = 'file:///tmp/output.csv'
FEED_FORMAT = 'csv'
FEED_EXPORT_ENCODING = 'cp932'
FEED_EXPORT_FIELDS = [
    '協会コード',
    '投資信託名',
    '愛称',
    '純資産',
    '設定来高値',
    '設定来安値',
    '委託会社',
    'モーニングスターカテゴリ',
    '運用方針',
    'ベンチマーク',
    '商品分類',
    '買付手数料_ネット_金額指定',
    '買付手数料_ネット_NISA預かり',
    '買付手数料_ネット_口数指定',
    '買付手数料_対面_金額指定',
    '買付手数料_対面_NISA預かり',
    '買付手数料_対面_口数指定',
    '信託報酬年率',
    '信託財産留保額',
    '解約手数料',
    '約定日',
    '受渡日',
    '決算日',
    '決算頻度',
    '注文申込締切時間',
    '休場日',
    '買付単位_金額',
    '買付単位_口数',
    '買付単位_積立',
    '売却単位_金額',
    '売却単位_口数',
    '当初一口当たり元本',
    '分配金受取方法_金額',
    '分配金受取方法_口数',
    '償還優遇の適用',
    '設定日',
    '償還日',
    '基準価額推移_1_日付',
    '基準価額推移_1_価額',
    '基準価額推移_2_日付',
    '基準価額推移_2_価額',
    '基準価額推移_3_日付',
    '基準価額推移_3_価額',
    '基準価額推移_4_日付',
    '基準価額推移_4_価額',
    '基準価額推移_5_日付',
    '基準価額推移_5_価額',
    '分配金実績_1_決算日',
    '分配金実績_1_分配金',
    '分配金実績_2_決算日',
    '分配金実績_2_分配金',
    '分配金実績_3_決算日',
    '分配金実績_3_分配金',
    '分配金実績_4_決算日',
    '分配金実績_4_分配金',
    '分配金実績_5_決算日',
    '分配金実績_5_分配金',
    '基準価額騰落率_前日比',
    '基準価額騰落率_1週間',
    '基準価額騰落率_1カ月',
    '基準価額騰落率_3カ月',
    '基準価額騰落率_6カ月',
    '基準価額騰落率_1年',
    '基準価額騰落率_3年',
    '基準価額騰落率_5年',
    '基準価額騰落率_10年',
    '基準価額騰落率_設定来',
    'トータルリターン_1ヵ月',
    'トータルリターン_6ヵ月',
    'トータルリターン_1年',
    'トータルリターン_3年',
    'トータルリターン_5年',
    'トータルリターン_設定来',
    'トータルリターン_平均_1ヵ月',
    'トータルリターン_平均_6ヵ月',
    'トータルリターン_平均_1年',
    'トータルリターン_平均_3年',
    'トータルリターン_平均_5年',
    'トータルリターン_平均_設定来',
    'ランキング_週間販売金額',
    'ランキング_週間販売件数',
    'ランキング_積立設定金額',
    'ランキング_積立設定件数',
    'ランキング_NISA販売金額',
    'ランキング_銘柄注目度',
    'ランキング_トータルリターン',
    'ランキング_分配金利回り',
    'ランキング_騰落率上位',
    'ランキング_純資産増加率',
    'ランキング_資金連続流入',
    '純資産推移_前日比',
    '純資産推移_1週間',
    '純資産推移_1カ月',
    '純資産推移_3カ月',
    '純資産推移_6カ月',
    '純資産推移_1年',
    '純資産推移_3年',
    '純資産推移_5年',
    '純資産推移_10年',
    '純資産推移_設定来',
    'レーティング_MSレーティング_総合',
    'レーティング_MSレーティング_3年',
    'レーティング_MSレーティング_5年',
    'レーティング_MSレーティング_10年',
    'リスクメジャー_3年',
    'リスクメジャー_5年',
    'リスクメジャー_10年',
    'リスクメジャー_総合'
    'シャープレシオ_1年',
    'シャープレシオ_3年',
    'シャープレシオ_5年',
    'シャープレシオ_10年',
    'シャープレシオ_平均_1年',
    'シャープレシオ_平均_3年',
    'シャープレシオ_平均_5年',
    'シャープレシオ_平均_10年',
    '標準偏差_1年',
    '標準偏差_3年',
    '標準偏差_5年',
    '標準偏差_10年',
    '標準偏差_平均_1年',
    '標準偏差_平均_3年',
    '標準偏差_平均_5年',
    '標準偏差_平均_10年',
]
