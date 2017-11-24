# sbisec-itrust-crawler
Scrapy を使って、SBI証券の投資信託商品の情報を読み込むサンプルプログラムです。

実行する際、何も指定しないと全商品を対象とすることになりますが、2,500商品以上あって、各サブページも含めた全リクエストが 5 秒間隔なので長大な時間がかかります。

以下のようにして `-a` オプションで適当な検索ワードを指定することをお勧めします。事前に SBI証券のサイトで何件くらい返されるか確認してからのほうがよいです。

```
$ scrapy list
sbisec_itrust
$ scrapy crawl sbisec_itrust -a search_words="アフリカ 毎月"
 :
 :
 2017-11-24 22:58:45 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://site0.sbisec.co.jp/marble/fund/detail/achievement.do?s_rflg=1&Param6=26431311C&int_fd=fund:psearch:search_result> (referer: https://site0.sbisec.co.jp/marble/fund/powersearch/fundpsearch/search.do?budget=1&pageNo=0&company=--&searchWordMode=1&fundName=%83A%83t%83%8A%83J+%96%88%8C%8E&pageRows=20)
 2017-11-24 22:58:46 [scrapy.core.scraper] ERROR: Spider error processing <GET https://site0.sbisec.co.jp/marble/fund/detail/achievement.do?s_rflg=1&Param6=26431311C&int_fd=fund:psearch:search_result> (referer: https://site0.sbisec.co.jp/marble/fund/powersearch/fundpsearch/search.do?budget=1&pageNo=0&company=--&searchWordMode=1&fundName=%83A%83t%83%8A%83J+%96%88%8C%8E&pageRows=20)
Traceback (most recent call last):
  File "/usr/lib64/python3.4/site-packages/twisted/internet/defer.py", line 653, in _runCallbacks
    current.result = callback(current.result, *args, **kw)
  File "/home/tatsuya/devel/github/sbisec-itrust-crawler/sbisec_itrust_crawler/spiders/SbisecITrustSpider.py", line 109, in _parse_investmenttrust
    loader, url_fragment, self._parse_トータルリターン情報)
  File "/home/tatsuya/devel/github/sbisec-itrust-crawler/sbisec_itrust_crawler/spiders/SbisecITrustSpider.py", line 378, in _create_request_for_nextdata
    jita_code = loader.get_collected_values('協会コード')[0]
IndexError: list index out of range
(↑ 例の追加のお知らせが挟み込まれる商品で発生するエラーです。そのうち直します。)
 :
 :
$ wc -l /tmp/output.csv 
5 /tmp/output.csv
```

