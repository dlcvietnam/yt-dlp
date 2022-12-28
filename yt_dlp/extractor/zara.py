from .common import InfoExtractor
from ..utils import (
    ExtractorError,
    int_or_none,
    js_to_json,
)


class ZaraItemIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?zara\.(?:[a-z]{2,3})(?:\.[a-z]{2})?/(?:[^/]+/)?(?:[^/]+/)?(?:[^/&#$?]+\-p)(?P<id>[^-/&#$?]+)\.html'

    _TESTS = [{
        'url': 'https://www.zara.com/us/en/combination-fleece-vest-p02969256.html?v1=236019850&v2=2113441',
        'info_dict': {
            'id': 'p02969256',
            'title': 'md5:dae240564cbb2642170c02f7f0d7e472',
        },
        'playlist_mincount': 1,
        'playlist': [{
            'info_dict': {
                'id': 'A1F83G8C2ARO7P',
                'ext': 'mp4',
                'title': 'mcdodo usb c cable 100W 5a',
                'thumbnail': r're:^https?://.*\.jpg$',
                'duration': 34,
            },
        }],
        'expected_warnings': ['Unable to extract data'],
    }]

    def _real_extract(self, url):
        id = self._match_id(url)
        for retry in self.RetryManager():
            webpage = self._download_webpage(url, id)
            try:
                data_json = self._search_json(
                    r'\<script type\=\"application\/ld\+json\"\>', webpage, 'data', id,
                    transform_source=js_to_json)
            except ExtractorError as e:
                retry.error = e
        print(data_json)
        title = data_json.get('title') or ""
        vid = data_json.get('mediaAsin') or ""
        videolst = []
        for video in (data_json.get('videos') or []):
            if video.get('isVideo') and video.get('url'):
                vid = video['marketPlaceID']
                videolst.append({
                    'id': video['marketPlaceID'],
                    'url': video['url'],
                    'title': video.get('title'),
                    'thumbnail': video.get('thumbUrl') or video.get('thumb'),
                    'duration': video.get('durationSeconds'),
                    'height': int_or_none(video.get('videoHeight')),
                    'width': int_or_none(video.get('videoWidth')),
                })
        # print(videolst)
        imagelst = []
        jsonImage = data_json.get('colorImages')
        for i in (jsonImage or {}):
            for colorimg in jsonImage[i]:
                if colorimg.get('hiRes'):
                    # print(colorimg['hiRes'])
                    imagelst.append({
                        'url': colorimg['hiRes'],
                    })
        formats = []
        if not videolst:
            formats.append({
                'url': 'http://bo.vutn.net/no-video.mp4',
                'ext': 'mp4',
                'format_id': 'http-mp4',
            })
        else:
            formats.append({
                'url': videolst[0]['url'],
                'ext': 'mp4',
                'format_id': 'http-mp4',
            })
        # print(imagelst)
        if not formats:
            self.raise_no_formats('No video found for this customer review', expected=True)
        return {
            'id': vid,
            'title': title,
            'thumbnails': imagelst,
            'formats': formats,
        }
