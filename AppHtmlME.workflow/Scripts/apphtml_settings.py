# vim: fileencoding=utf-8
"""
AppHtml settings
@author Toshiya NISHIO(http://www.toshiya240.com)
"""

defaultTemplate = {
    '1) 小さいボタン': '${badgeS}',
    '2) 大きいボタン': '${badgeL}',
    '3) テキストのみ': '${textonly}'
}

settings = {
    'aff': "",
    'cnt': 8,
    'scs': {
        'iphone': 320,
        'ipad': 320,
        'mac': 480
    },
    'template': {
        'software': defaultTemplate,
        'iPadSoftware': defaultTemplate,
        'macSoftware': defaultTemplate,
        'song': defaultTemplate,
        'album': defaultTemplate,
        'movie': defaultTemplate,
        'ebook': defaultTemplate
    }
}
