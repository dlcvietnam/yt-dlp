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


class EbayItemIE(InfoExtractor):
    IE_NAME = 'ebay:product'
    _VALID_URL = r'https?://(?:www\.)?ebay\.(?:[a-z]{2,3})(?:\.[a-z]{2})?/(?:itm)(?:[/\S])*/(?P<id>[0-9]{9,12})'

    _LOGIN_URL = 'https://login.taobao.com/member/login.jhtml'
    _TESTS = [{
        'url': 'https://www.ebay.com/itm/adidas-Originals-Ultraboost-DNA-XXII-Shoes-Men-039-s-/155249878436?&_trksid=p2056016.m2516.l5255',
        'info_dict': {
            'id': '155249878436',
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
        initial_state = self._search_json(r'\[\[\"PICTURE0\-0\"\,0\,\{\"model\"\:', webpage, 'initial state', pid)
        #print(initial_state)
        #print(type(initial_state))
        thumb = []
        videoURL = ''
        newjson = json.loads(json.dumps(initial_state))
        for i in range(len(newjson['mediaList'])):
            for key, value in newjson['mediaList'][i].items():
                if key in "video":
                    videoURL = value["playlistMap"]["HLS"]
                if key in "image":
                    thumb.append({
                        'url': value["originalImg"]["URL"],
                    })
        if not pid:
            raise ExtractorError(
                'Không thể lấy video/ảnh, vui lòng kiểm tra lại liên kết hoặc liên hệ hỗ trợ',
                expected=True)
        title = self._search_regex(r'<title>([^<]+)<', webpage, 'title')
        if videoURL is None:
            videoURL = "http://bo.vutn.net/no-video.mp4"
            return {
            # I have no idea what these params mean but it at least seems to work
            'url': videoURL,
            'id': pid,
            'title': title,
            'thumbnails': thumb,
            }
        else:
            formats = self._extract_m3u8_formats(
                videoURL, pid, 'mp4')
            return {
                # I have no idea what these params mean but it at least seems to work
                'formats': formats,
                'id': pid,
                'title': title,
                'thumbnails': thumb,
            }
