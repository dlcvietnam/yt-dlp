# coding: utf-8
from .common import InfoExtractor
import json
import re
import ast
from ..utils import (
    # int_or_none,
    # js_to_json,
    # mimetype2ext,
    ExtractorError,
)


class TmallIE(InfoExtractor):
    IE_NAME = 'tmall:product'
    _VALID_URL = r'https?:\/\/(?:(?:www|[a-z]{2})\.)?detail\.tmall\.com\/.*?id\=(?P<id>\d+)'

    _TESTS = [{
        'url': 'https://detail.tmall.com/item.htm?id=656308694954',
        'info_dict': {
            'id': '656308694954',
            'ext': 'mp4',
            'title': 'Video title goes here',
            'thumbnail': r're:^https?://.*\.jpg$',
            # TODO more properties, either as:
            # * A value
            # * MD5 checksum; start the string with md5:
            # * A regular expression; start the string with re:
            # * Any Python type (for example int or float)
        }
    }]

    def _real_extract(self, url):
        pid = self._match_id(url)
        webpage, urlh = self._download_webpage_handle(url, pid)
        visitor_url = urlh.geturl()
        if 'detail.tmall.com' in visitor_url:
            vid = self._search_regex(
                r'"imgVedioID"\s*:\s*"?(\d+)"?',
                webpage, 'video id')
            uid = self._search_regex(
                r'"userId"\s*:\s*"?(?P<uid>\d+)"?',
                webpage, 'video uid')

            title = self._search_regex(r'<title>([^<]+)<', webpage, 'title')
        elif 'item.taobao.com' in visitor_url:
            vid = self._search_regex(
                r'"videoId"\s*:\s*"?(\d+)"?',
                webpage, 'video id')
            uid = self._search_regex(
                r'"videoOwnerId"\s*:\s*"?(?P<uid>\d+)"?',
                webpage, 'video uid')
            title = self._search_regex(r'<title>([^<]+)<', webpage, 'title')
        return {
            # I have no idea what these params mean but it at least seems to work
            'url': 'https://cloud.video.taobao.com/play/u/%s/p/1/e/6/t/1/%s.mp4' % (uid, vid),
            'id': vid,
            'title': title,
        }


class TaobaoIE(InfoExtractor):
    IE_NAME = 'taobao:product'
    _VALID_URL = r'https?:\/\/(?:(?:www|[a-z]{2})\.)?item\.taobao\.com\/.*?id\=(?P<id>\d+)'

    _LOGIN_URL = 'https://login.taobao.com/member/login.jhtml'
    _TESTS = [{
        'url': 'https://item.taobao.com/item.htm?id=656308694954',
        'info_dict': {
            'id': '656308694954',
            'ext': 'mp4',
            'title': 'Video title goes here',
            'thumbnail': r're:^https?://.*\.jpg$',
            # TODO more properties, either as:
            # * A value
            # * MD5 checksum; start the string with md5:
            # * A regular expression; start the string with re:
            # * Any Python type (for example int or float)
        }
    }]

    def _real_extract(self, url):
        pid = self._match_id(url)
        webpage, urlh = self._download_webpage_handle(url, pid)
        visitor_url = urlh.geturl()
        thumb = []
        if 'login.jhtml' in visitor_url:
            raise ExtractorError(
                'Lỗi đăng nhập Taobao - Cookies Error - Vui lòng báo lỗi cho hỗ trợ @cpanel10x',
                expected=True)
        if 'detail.tmall.com' in visitor_url:
            vid = self._search_regex(
                r'"imgVedioID"\s*:\s*"?(\d+)"?',
                webpage, 'video id')
            uid = self._search_regex(
                r'"userId"\s*:\s*"?(?P<uid>\d+)"?',
                webpage, 'video uid')
            shop = self._search_regex(
                r'TShop.Setup\(\s*(.*)\s*\)\;',
                webpage, 'shop setup')
            y = json.loads(shop)
            imgsku = y["propertyPics"]
            for key, value in imgsku.items():
                if key in "default":
                    for i in range(len(value)):
                        thumb.append({
                            'url': value[i],
                        })
                else:
                    thumb.append({
                        'url': value[0],
                    })
            title = self._search_regex(r'<title>([^<]+)<', webpage, 'title')
        elif 'item.taobao.com' in visitor_url:
            vid = self._search_regex(
                r'"videoId"\s*:\s*"?(\d+)"?',
                webpage, 'video id')
            uid = self._search_regex(
                r'"videoOwnerId"\s*:\s*"?(?P<uid>\d+)"?',
                webpage, 'video uid')
            title = self._search_regex(r'<title>([^<]+)<', webpage, 'title')
        return {
            # I have no idea what these params mean but it at least seems to work
            'url': 'https://cloud.video.taobao.com/play/u/%s/p/1/e/6/t/1/%s.mp4' % (uid, vid),
            'id': vid,
            'title': title,
            'thumbnails': thumb,
        }


class TaobaoWorldIE(InfoExtractor):
    IE_NAME = 'taobaoworld:product'
    _VALID_URL = r'https?:\/\/(?:(?:www|[a-z]{2})\.)?world\.taobao\.com\/item\/(?P<id>\d+)\.htm'

    _LOGIN_URL = 'https://login.taobao.com/member/login.jhtml'
    _TESTS = [{
        'url': 'https://world.taobao.com/item/643681750378.htm',
        'info_dict': {
            'id': '643681750378',
            'ext': 'mp4',
            'title': 'Video title goes here',
            'thumbnail': r're:^https?://.*\.jpg$',
            # TODO more properties, either as:
            # * A value
            # * MD5 checksum; start the string with md5:
            # * A regular expression; start the string with re:
            # * Any Python type (for example int or float)
        }
    }]

    def _real_extract(self, url):
        pid = self._match_id(url)
        webpage, urlh = self._download_webpage_handle(url, pid)
        visitor_url = urlh.geturl()
        if 'login.jhtml' in visitor_url:
            raise ExtractorError(
                'Lỗi đăng nhập Taobao - Cookies Error - Vui lòng báo lỗi cho hỗ trợ @cpanel10x',
                expected=True)
        videoURL = self._search_regex(
            r'"videoUrl"\s*:\s*"?(\S+)"}',
            webpage, 'video url', default=None)
        if not videoURL:
            videoURL = 'http://bo.vutn.net/no-video.mp4'
        uid = self._search_regex(
            r'"userId"\s*:\s*"?(?P<uid>\d+)"?',
            webpage, 'user id', default=None)
        if not uid:
            raise ExtractorError(
                'Không thể lấy video/ảnh, vui lòng kiểm tra lại liên kết hoặc liên hệ hỗ trợ',
                expected=True)
        urlthumb = self._search_regex(
            r'"images"\s*:\s*(?P<urlthumb>"?\S+\"\])',
            webpage, 'imglist', default=None)
        title = self._search_regex(r'<title>([^<]+)<', webpage, 'title')
        thumb = []
        listthumb = json.loads(urlthumb)
        for i in range(len(listthumb)):
            thumb.append({
                'url': listthumb[i],
            })
        shopjs = self._search_regex(
            r'window\.\_\_INITIAL\_DATA\_\_\=(.*}}})',
            webpage, 'shop JS', default=None)
        y = json.loads(shopjs)
        price = y["pageInitialProps"]["httpData"]["normalItemResponse"]["itemPrice"]["promotionPrice"]
        fulltitle = f"{title} - Giá bán: {price} tệ"
        htmldesc = y["pageInitialProps"]["httpData"]["normalItemResponse"]["itemDesc"]
        imgdesc = re.findall(r'((img|cbu01)\.alicdn\.com.*?\.(jpg|png))', htmldesc)
        imgdesc.sort()
        for image in imgdesc:
            thumb.append({
                'url': 'https://' + image[0],
            })
        probimg = str(y["pageInitialProps"]["httpData"]["normalItemResponse"]["itemSkuDO"]["skuPropertyList"])
        if probimg is not None:
            probimglst = re.findall(r'((img|cbu01)\.alicdn\.com.*?\.(jpg|png))', probimg)
            probimglst.sort()
            for image in probimglst:
                thumb.append({
                    'url': 'https://' + image[0],
                })
        # pageInitialProps►httpData►normalItemResponse►itemSkuDO►skuPropertyList►1►propertyValues►
        # print(thumb)
        seen = set()
        new_finalthumb = []
        for d in thumb:
            t = tuple(d.items())
            if t not in seen:
                seen.add(t)
                new_finalthumb.append(d)
        return {
            # I have no idea what these params mean but it at least seems to work
            'url': videoURL,
            'id': uid,
            'title': fulltitle,
            'thumbnails': new_finalthumb,
        }


class Ali1688IE(InfoExtractor):
    IE_NAME = 'ali1688:product'
    _VALID_URL = r'https?:\/\/(?:(?:www|[a-z]{2})\.)?(?:detail|m)\.1688\.com\/offer\/(?P<id>\d+)\.html'

    _LOGIN_URL = 'https://login.taobao.com/member/login.jhtml'
    _TESTS = [{
        'url': 'https://m.1688.com/offer/594689528709.html',
        'info_dict': {
            'id': '594689528709',
            'ext': 'mp4',
            'title': 'Video title goes here',
            'thumbnail': r're:^https?://.*\.jpg$',
            # TODO more properties, either as:
            # * A value
            # * MD5 checksum; start the string with md5:
            # * A regular expression; start the string with re:
            # * Any Python type (for example int or float)
        }
    }]

    def _real_extract(self, url):
        pid = self._match_id(url)
        webpage, urlh = self._download_webpage_handle(url, pid)
        # visitor_url = urlh.geturl()
        # debug print('visitor url %s' % visitor_url)
        uid = self._search_regex(
            r'"videoId":(?P<uid>\d+)',
            webpage, 'video id')
        videoURL = ''
        # debug print('uid is %s' % uid)
        if uid == '0':
            videoURL = 'http://bo.vutn.net/no-video.mp4'
        else:
            videoURL = self._search_regex(
                r'"videoUrl":"(?P<videoUrl>.+?)"',
                webpage, 'video url', default=None)
        shopjs = self._search_regex(
            r'window\.\_\_INIT\_DATA\=(.*}]})',
            webpage, 'shop JS', default=None)
        # print(shopjs)
        y = json.loads(shopjs)
        # urlthumb = y["data"]["5908930030501"]["data"]["offerImgList"]
        urlthumb = []
        detailurl = []
        for key, value in y["data"].items():
            if 'componentType' not in value:
                continue
            if value.get('data', {}).get('offerImgList'):
                urlthumb = value['data']['offerImgList']
            if value.get('data', {}).get('detailUrl'):
                detailurl = value['data']['detailUrl']
        # print('offerImgList', offerImgList)
        # urlthumb = self._search_regex(
        #    r'"offerImgList"\s*:\s*(?P<urlthumb>\["?\S+\"\])',
        #    webpage, 'imglist')
        # print(urlthumb)
        # print(detailurl)
        thumb = []
        # listthumb = json.loads(urlthumb)
        for i in range(len(urlthumb)):
            thumb.append({
                'url': urlthumb[i],
            })
        title = self._search_regex(r'<title>([^<]+)<', webpage, 'title')
        if "skuProps" in y["globalData"]["skuModel"]:
            imgprob = str(y["globalData"]["skuModel"]["skuProps"])
            imgproblst = re.findall(r'((img|cbu01)\.alicdn\.com.*?\.(jpg|png))', imgprob)
            imgproblst.sort()
            # print("sku")
            # print(imgproblst)
            for image in imgproblst:
                thumb.append({
                    'url': 'https://' + image[0],
                })
        # detailurl = (str(y["data"]["590893002100"]["data"]["detailUrl"]))
        # print(detailurl)
        if detailurl is not None:
            # print(detailurl)
            webpage2 = str(self._download_webpage_handle(detailurl, pid))
            detailimglst = re.findall(r'((cbu01|img)\.alicdn\.com\/img.*?\.(jpg|png))', webpage2)
            # print(detailimglst)
            detailimglst.sort()
            # detailimglst1 = list(dict.fromkeys(detailimglst))
            # print(detailimglst1)
            for image in detailimglst:
                thumb.append({
                    'url': 'https://' + image[0],
                })
            # print(detailimglst)
        thumblstnew = str(thumb)
        # print(thumblstnew)
        prethumb = re.sub(r'(\.(?:[-_]?\d{2,4}x\d{2,4})+\.)|(.summ.)|(.search.)', '.', thumblstnew)
        finalthumb = ast.literal_eval(prethumb)
        # print(finalthumb)
        seen = set()
        new_finalthumb = []
        for d in finalthumb:
            t = tuple(d.items())
            if t not in seen:
                seen.add(t)
                new_finalthumb.append(d)
        # print(new_finalthumb)
        # thumb = [w.replace('(?:[-_]?[0-9]+x[0-9]+)+', '') for w in thumb]
        return {
            # I have no idea what these params mean but it at least seems to work
            'url': videoURL,
            'id': uid,
            'title': title,
            'thumbnails': new_finalthumb,
        }
