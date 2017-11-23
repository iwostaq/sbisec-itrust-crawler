# vim:set fileencoding=utf-8, fileformat=unix
#

import json
from urllib.parse import parse_qs, quote, urlparse

import scrapy
from sbisec_itrust_crawler.items import (InvestmentTrust,
                                         InvestmentTrustItemLoader)


class SbisecITrustSpider(scrapy.Spider):
    """
    SBI証券で検索可能な投資信託商品情報を解析するためのスパイダークラスです。
    """
    name = "sbisec_itrust"

    SBI_BASE0_URL = 'https://site0.sbisec.co.jp'
    url_trust_detail = SBI_BASE0_URL +\
        '/marble/fund/detail/achievement.do?' +\
        's_rflg=1&Param6=2{}&int_fd=fund:psearch:search_result'

    def __init__(self, search_words=None):
        self.jita_code = None
        if search_words is None:
            self.search_words = []
        else:
            self.search_words = search_words.split()
        self.logger.info('search words: {}'.
                         format("/".join(self.search_words)))

    def start_requests(self):
        if self.jita_code is not None:
            self.logger.info('jita_code: {}'.format(self.jita_code))

        if self.jita_code:
            req = scrapy.Request(url=InvestmentTrustSpider.url_trust_detail.format(self.jita_code),
                                 method='GET',
                                 callback=self._parse_investmenttrust)
        else:
            url_search = SbisecITrustSpider.SBI_BASE0_URL +\
                '/marble/fund/powersearch/fundpsearch/search.do'

            search_param = SearchParameter(search_words=self.search_words)
            req = scrapy.FormRequest(url=url_search, method='GET',
                                     encoding='cp932',
                                     formdata=search_param.to_request_params(),
                                     callback=self._parse_search_result)
        yield req

    def _parse_search_result(self, response):
        """
        検索結果一覧ページ(正確には、その情報を持ったJSON)を解析します。
        """
        search_response = json.loads(response.text)

        pager_total_pages = search_response['pager']['totalPage']
        pager_page_index = search_response['pager']['pageInfo']['page']
        self.logger.info('search result (index/total): {0}/{1}'.\
            format(pager_page_index, pager_total_pages + 1))

        for r in search_response['records']:
            sreq = scrapy.Request(SbisecITrustSpider.url_trust_detail.format(r['fundCode']),
                                  method='GET', callback=self._parse_investmenttrust)
            yield sreq

        if pager_total_pages <= pager_page_index:
            return None

        url_search = SbisecITrustSpider.SBI_BASE0_URL +\
            '/marble/fund/powersearch/fundpsearch/search.do'
        search_param = SearchParameter.create(search_response)
        search_param.add_page_index()
        req = scrapy.FormRequest(url=url_search, method='POST',
                                 formdata=search_param.to_request_params(),
                                 callback=self._parse_search_result)
        yield req

    def _parse_investmenttrust(self, response):
        """
        投資信託の詳細ページを解析します。
        """
        jita_code = self._extract_jita_code(response.url)

        loader = InvestmentTrustItemLoader(
            InvestmentTrust(), response=response)
        loader = loader.nested_xpath(
            '/html/body/table/tr/td[@id="MAINAREA02_780"]')

        self._parse_商品ヘッダ情報(loader)

        loader.context['didx'] = 4
        div_お知らせ = loader.get_xpath('div[4]/h2/text()')
        if 0 < len(div_お知らせ) and div_お知らせ[0].count(u'お知らせ') > 0:
            loader.context['didx'] += 1

        self._parse_商品情報1(loader)
        self._parse_買付手数料(loader)
        self._parse_商品情報2(loader)
        self._parse_基準価額推移(loader)
        self._parse_分配金実績(loader)
        self._parse_基準価額騰落率(loader)
        self._parse_ランキング(loader)
        loader.context['didx'] += 2
        self._parse_純資産推移(loader)

        url_fragment = '/marble/fund/detail/achievement/totalreturn-data.do?fundCode={}'
        req = self._create_request_for_nextdata(
            loader, url_fragment, self._parse_トータルリターン情報)
        return req

    def _parse_トータルリターン情報(self, response):
        """
        投資信託のトータルリターン情報のJSONを解析します。
        """
        loader = response.meta['loader']
        トータルリターン情報 = json.loads(response.text)

        for period, avr, val in zip(トータルリターン情報['period'],
                                    トータルリターン情報['totalReturnCategory'],
                                    トータルリターン情報['totalReturnTarget']):
            if val is not None:
                loader.add_value('トータルリターン_' + period, str(val))
            if avr is not None:
                loader.add_value('トータルリターン_平均_' + period, str(avr))

        url_fragment = '/marble/fund/detail/achievement/rating-data.do?fundCode={}'
        return self._create_request_for_nextdata(loader, url_fragment, self._parse_レーティング情報)

    def _parse_レーティング情報(self, response):
        """
        投資信託のレーティング情報のJSONを解析します。
        """
        loader = response.meta['loader']
        レーティング情報 = json.loads(response.text)

        for val in レーティング情報['rating']:
            if val['msRating'] is not None:
                loader.add_value('レーティング_MSレーティング_' + val['period'],
                                 str(val['msRating']))

        jita_code = loader.get_collected_values('協会コード')[0]

        url_fragment = '/marble/fund/detail/achievement/riskMajor-data.do?fundCode={}'
        return self._create_request_for_nextdata(loader, url_fragment, self._parse_リスクメジャー情報)

    def _parse_リスクメジャー情報(self, response):
        """
        投資信託のリスクメジャー情報のJSONを解析します。
        """
        loader = response.meta['loader']
        リスクメジャー情報 = json.loads(response.text)

        for val in リスクメジャー情報['riskMajor']:
            if val[0] is None:
                continue
            loader.add_value('リスクメジャー_' + val[0], str(val[1:].count(1)))

        url_fragment = '/marble/fund/detail/achievement/sharpRatio-data.do?fundCode={}'
        return self._create_request_for_nextdata(loader, url_fragment, self._parse_シャープレシオ情報)

    def _parse_シャープレシオ情報(self, response):
        """
        投資信託のシャープレシオ情報のJSONを解析します。
        """
        loader = response.meta['loader']
        シャープレシオ情報 = json.loads(response.text)

        for period, avr, val in zip(シャープレシオ情報['period'],
                                    シャープレシオ情報['sharpRatioCategory'],
                                    シャープレシオ情報['sharpRatioTarget']):
            if val is not None:
                loader.add_value('シャープレシオ_' + period, str(val))
            if avr is not None:
                loader.add_value('シャープレシオ_平均_' + period, str(avr))

        url_fragment = '/marble/fund/detail/achievement/sigma-data.do?fundCode={}'
        return self._create_request_for_nextdata(loader, url_fragment, self._parse_標準偏差情報)

    def _parse_標準偏差情報(self, response):
        """
        投資信託の標準偏差(シグマ)情報のJSONを解析します。
        """
        loader = response.meta['loader']
        標準偏差情報 = json.loads(response.text)

        for period, avr, val in zip(標準偏差情報['period'],
                                    標準偏差情報['sigmaCategory'],
                                    標準偏差情報['sigmaTarget']):
            if val is not None:
                loader.add_value('標準偏差_' + period, str(val))
            if avr is not None:
                loader.add_value('標準偏差_平均_' + period, str(avr))

        return loader.load_item()

    def _parse_商品ヘッダ情報(self, loader):
        """
        投資信託商品画面上部のヘッダ情報を解析します。
        """
        loader.add_xpath('投資信託名', 'div[1]/div/div/h3[1]/text()')
        loader.add_xpath(
            '愛称', 'div[2]/div/div/h3[2]/text()', re='\s*（愛称：(\S+)）\s*$')
        loader.add_xpath('純資産', 'div[2]/div[2]/table/tbody/tr[1]/td[1]/text()')
        loader.add_xpath(
            '設定来高値', 'div[2]/div[2]/table/tbody/tr[2]/td[1]/text()')
        loader.add_xpath(
            '設定来安値', 'div[2]/div[2]/table/tbody/tr[3]/td[1]/text()')

    def _parse_商品情報1(self, loader):
        """
        投資信託商品画面左の基本情報(上半分)を解析します。
        """
        didx = loader.context['didx']
        loader.add_xpath('委託会社', 'div[{}]/div/p[2]/text()'.format(didx))
        loader.add_xpath(
            'モーニングスターカテゴリ', 'div[{}]/div/p[4]/text()'.format(didx))

        loader = loader.nested_xpath('div[{}]/div/table[1]/tbody'.format(didx))
        loader.add_xpath('運用方針', 'tr[2]/td/text()')
        loader.add_xpath('ベンチマーク', 'tr[4]/td/text()')
        loader.add_xpath('商品分類', 'tr[6]/td/text()')
        loader.add_xpath('協会コード', 'tr[8]/td/text()')

    def _parse_買付手数料(self, item_loader):
        """
        買付手数料を解析します。
        """
        base_xpath = 'div[{}]/div/table[1]/tbody/tr[10]/td/div'.format(
            item_loader.context['didx'])
        loader = item_loader.nested_xpath(base_xpath)
        loader.add_xpath('買付手数料_ネット_金額指定', 'div[2]/text()[2]')
        loader.add_xpath('買付手数料_ネット_NISA預かり', 'div[2]/text()[4]')
        loader.add_xpath('買付手数料_ネット_口数指定', 'div[2]/text()[6]')
        loader.add_xpath('買付手数料_対面_金額指定', 'div[3]/text()[2]')
        loader.add_xpath('買付手数料_対面_NISA預かり', 'div[3]/text()[4]')
        loader.add_xpath('買付手数料_対面_口数指定', 'div[3]/text()[6]')

    def _parse_商品情報2(self, item_loader):
        """
        投資信託商品の基本情報(下半分)を解析します。
        """
        loader = item_loader.nested_xpath(
            'div[{}]/div[1]/table[1]/tbody'.format(item_loader.context['didx']))

        loader.add_xpath('信託報酬年率', 'tr[12]/td/text()')
        loader.add_xpath('信託財産留保額', 'tr[14]/td/text()')
        loader.add_xpath('解約手数料', 'tr[16]/td/text()')
        loader.add_xpath('約定日', 'tr[18]/td/text()')
        loader.add_xpath('受渡日', 'tr[20]/td/text()')
        loader.add_xpath('決算日', 'tr[22]/td/text()')
        loader.add_xpath('決算頻度', 'tr[24]/td/text()')
        loader.add_xpath('注文申込締切時間', 'tr[26]/td/text()')
        loader.add_xpath('休場日', 'tr[28]/td/text()')
        for 買付単位 in loader.get_xpath('tr[30]/td/text()'):
            if 0 < 買付単位.find('金額'):
                loader.add_value('買付単位_金額', 買付単位)
            if 0 < 買付単位.find('口数'):
                loader.add_value('買付単位_口数', 買付単位)
            if 0 < 買付単位.find('積立'):
                loader.add_value('買付単位_積立', 買付単位)
        for 売却単位 in loader.get_xpath('tr[32]/td/text()'):
            if 0 < 売却単位.find('金額'):
                loader.add_value('売却単位_金額', 売却単位)
            if 0 < 売却単位.find('口数'):
                loader.add_value('売却単位_口数', 売却単位)
            loader.add_xpath('当初一口当たり元本', 'tr[34]/td/text()')
        for 分配金受取方法 in loader.get_xpath('tr[36]/td/text()'):
            if 0 < 分配金受取方法.find('金額'):
                loader.add_value('分配金受取方法_金額', 分配金受取方法)
            if 0 < 分配金受取方法.find('口数'):
                loader.add_value('分配金受取方法_口数', 分配金受取方法)
        loader.add_xpath('償還優遇の適用', 'tr[38]/td/text()')
        loader.add_xpath('設定日', 'tr[40]/td/text()')
        loader.add_xpath('償還日', 'tr[42]/td/text()')

    def _parse_基準価額推移(self, item_loader):
        """
        基準価額推移の表を解析します。
        """
        xpath = 'div[{}]/div[2]/div[2]/div[1]/table/tbody/tr'.format(
            item_loader.context['didx'])
        loader = item_loader.nested_xpath(xpath)

        idx = 1
        for date, amount in zip(loader.get_xpath('th/text()'), loader.get_xpath('td[1]/text()')):
            loader.add_value('基準価額推移_{}_日付'.format(idx), date)
            loader.add_value('基準価額推移_{}_価額'.format(idx), amount)
            idx += 1

    def _parse_分配金実績(self, item_loader):
        """
        分配金実績の表を解析します。
        """
        xpath = 'div[{}]/div[2]/div[2]/div[2]/table/tbody/tr'.format(
            item_loader.context['didx'])
        loader = item_loader.nested_xpath(xpath)

        idx = 1
        for sdate, amount in \
                zip(loader.get_xpath('th/text()'), loader.get_xpath('td[1]/text()')):
            loader.add_value('分配金実績_{}_決算日'.format(idx), sdate)
            if amount == '-':
                loader.add_value('分配金実績_{}_分配金'.format(idx), None)
            else:
                loader.add_value('分配金実績_{}_分配金'.format(idx), amount)
            idx += 1

    def _parse_基準価額騰落率(self, item_loader):
        """
        基準価額騰落率の表を解析します。
        """
        xpath = 'div[{}]/div[2]/div[3]/div[1]/table/tbody/tr'.format(
            item_loader.context['didx'])
        loader = item_loader.nested_xpath(xpath)

        for period, rate in \
                zip(loader.get_xpath('th/text()'), loader.get_xpath('td[1]/text()')):
            loader.add_value('基準価額騰落率_{}'.format(period), rate)

    def _parse_ランキング(self, item_loader):
        """
        ランキングの表を解析します。
        """
        xpath = 'div[{}]/div[2]/div[5]/table/tbody'.format(
            item_loader.context['didx'])
        loader = item_loader.nested_xpath(xpath)

        self._read_rank_data(loader, 'ランキング_週間販売金額', 'tr[1]/td[1]')
        self._read_rank_data(loader, 'ランキング_トータルリターン', 'tr[1]/td[2]')
        self._read_rank_data(loader, 'ランキング_週間販売件数', 'tr[2]/td[1]')
        self._read_rank_data(loader, 'ランキング_分配金利回り', 'tr[2]/td[2]')
        self._read_rank_data(loader, 'ランキング_積立設定金額', 'tr[3]/td[1]')
        self._read_rank_data(loader, 'ランキング_騰落率上位', 'tr[3]/td[2]')
        self._read_rank_data(loader, 'ランキング_積立設定件数', 'tr[4]/td[1]')
        self._read_rank_data(loader, 'ランキング_純資産増加率', 'tr[4]/td[2]')
        self._read_rank_data(loader, 'ランキング_NISA販売金額', 'tr[5]/td[1]')
        self._read_rank_data(loader, 'ランキング_資金連続流入', 'tr[5]/td[2]')
        self._read_rank_data(loader, 'ランキング_銘柄注目度', 'tr[6]/td[1]')

    def _parse_純資産推移(self, item_loader):
        """
        純資産推移の表を解析します。
        """
        xpath = 'div[{}]/div[2]/div[1]/div[1]/table/tbody/tr'.format(
            item_loader.context['didx'])
        loader = item_loader.nested_xpath(xpath)
        for period, amount in zip(loader.get_xpath('th/text()'), loader.get_xpath('td/text()')):
            if amount == '-':
                loader.add_value('純資産推移_{}'.format(period), None)
            else:
                loader.add_value('純資産推移_{}'.format(period), amount)

    def _read_rank_data(self, loader, name, xpath):
        """
        ランキング情報を解析します。
        """
        if len(loader.get_xpath(xpath + '/span[1]/text()')) == 0:
            loader.add_value(name, None)
        else:
            loader.add_xpath(name, xpath + '/span[1]/text()', re='(.*)位')

    def _extract_jita_code(self, url_string):
        """
        指定されたURLから、投信コードを抽出します。
        """
        url = urlparse(url_string)
        param6 = parse_qs(url.query)['Param6']
        if param6 is not '' and 0 < len(param6):
            return param6[0]
        else:
            return ''

    def _create_request_for_nextdata(self, loader, url_path_format, callback):
        """
        一つの商品に対する関連情報を取得するためのHTTPリクエストを作成します。
        """
        jita_code = loader.get_collected_values('協会コード')[0]
        req = scrapy.Request(SbisecITrustSpider.SBI_BASE0_URL +
                             url_path_format.format(jita_code),
                             method='GET', callback=callback)
        req.meta['loader'] = loader
        return req


class SearchParameter(object):
    """
    信託商品を検索するときのパラメタを表すクラスです。
    """
    DEFAULT_ROWS_PER_PAGE = 20

    @staticmethod
    def create(response_json):
        search_words = response_json['selects']['fundName']
        page_index = response_json['pager']['pageInfo']['page']
        rows_per_page = response_json['pager']['pageInfo']['rows']
        return SearchParameter(search_words=search_words, first_page_index=page_index)

    def __init__(self, search_words=[], first_page_index=0):
        self.search_words = search_words
        self.page_index = first_page_index
        self.rows_per_page = SearchParameter.DEFAULT_ROWS_PER_PAGE

    def add_page_index(self, increment=1):
        """
        検索結果のページインデックスを指定分増加させます。
        """
        self.page_index += increment

    def to_request_params(self):
        """
        scrapy.Requestに渡せる形に変換します。必須パラメタは、以下の四つです。
        - pageNo: ページ番号
        - pageRows: 0ページあたりの行数
        - budget: 不明('1')
        - company: 不明('--')
        """
        param = {
            'pageNo': str(self.page_index),
            'pageRows': str(self.rows_per_page),
            #'tabName': 'base',
            #'sortColumn': '89',
            #'sortOrder': '0',
            #'unyouColumnName': 'totalReturnColumns',
            'searchWordMode': '1',
            #'commission': 'X',
            #'trustCharge': 'X',
            #'yield': 'X',
            #'sharpRatio': 'X',
            #'sigma': 'X',
            #'flow': 'X',
            #'asset': 'X',
            #'standardPrice': 'X',
            #'redemption': 'X',
            #'period': 'X',
            'budget': '1',
            'company': '--',
        }

        if self.search_words:
            param['fundName'] = ' '.join(self.search_words)
        return param
