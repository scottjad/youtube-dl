# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor


class EspnfcIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?espnfc\.us/*/video/(?P<id>[0-9]+)'
    _TEST = {
        'url': 'http://www.espnfc.us/french-ligue-1/9/video/2296888',
        'md5': 'TODO: md5 sum of the first 10241 bytes of the video file (use --test)',
        'info_dict': {
            'id': '2296888',
            'ext': 'mp4',
            'title': 'Zlatan immortalized in wax',
            'thumbnail': 're:^https?://.*\.jpg$',
            # TODO more properties, either as:
            # * A value
            # * MD5 checksum; start the string with md5:
            # * A regular expression; start the string with re:
            # * Any Python type (for example int or float)
        }
    }

    def _real_extract(self, url):
        video_num = self._match_id(url)
        webpage = self._download_webpage(url, video_num)

        video_title = self._html_search_regex(r'<title>(.*?) - ESPN FC</title>', webpage, 'title')
        video_description = self._html_search_meta('description', webpage, 'description')

        # The server URL is hardcoded
        video_url = 'rtmp://svod.espn.go.com/motion/ESPNi/'

        # Extract video URL
        # "2015/0212/int_150212_INET_Zlatan_immortalized_in_wax/int_150212_INET_Zlatan_immortalized_in_wax"
        video_slug = self._search_regex(
            # TODO not sure about this *, maybe needs to be non-greedy
            r"/media/motion/ESPNi/(*)\.jpg", webpage, 'slug')
        video_slug_split = video_slug.split("/")
        # "int_150212_INET_Zlatan_immortalized_in_wax"
        video_ref = "/".join(video_slug_split[-2])
        # "2015/0212/int_150212_INET_Zlatan_immortalized_in_wax"
        video_ref_with_date = "/".join(video_slug_split[:-1])

        playpath = 'mp4:' + video_ref + "_720p30_2896k.mp4"

        video_filename = playpath.split(':')[-1]
        video_id, extension = video_filename.split('.')

        http_base = self._search_regex(
            r'EXPRESSINSTALL_SWF\s*=\s*"(https?://[^/"]+/)', webpage,
            'HTTP base URL')

        formats = [{
            'format_id': 'rtmp',
            'url': video_url,
            'ext': extension,
            'play_path': playpath,
        }, {
            'format_id': 'http',
            'url': http_base + real_id,
        }]
        self._sort_formats(formats)

        return {
            'id': video_id,
            'title': video_title,
            'description': video_description,
            'formats': formats,
        }
