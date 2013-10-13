# vim: fileencoding=utf-8
"""
AppHtml settings
@author Toshiya NISHIO(http://www.toshiya240.com)
"""

defaultTemplate = {
    '1) 小さいボタン': '${badgeS}',
    '2) 大きいボタン': '${badgeL}',
    '3) テキストのみ': '${textonly}',
    "4) アイコン付き(小)": u"""<span class="appIcon"><img class="appIconImg" height="60" src="${icon60url}" style="float:left;margin: 0px 15px 15px 5px;"></span>
<span class="appName"><strong><a href="${url}" target="itunes_store">${name}</a></strong></span><br>
<span class="appCategory">カテゴリ: ${category}</span><br>
<span class="badgeS" style="display:inline-block; margin:6px">${badgeS}</span><br style="clear:both;">
""",
    "5) アイコン付き(大)": u"""<span class="appIcon"><img class="appIconImg" height="100" src="${icon100url}" style="float:left;;margin: 0px 15px 15px 5px;"></span>
<span class="appName"><strong><a href="${url}" target="itunes_store">${name}</a></strong></span><br>
<span class="appCategory">カテゴリ: ${category}</span><br>
<span class="badgeL" style="display:inline-block; margin:4px">${badgeL}</span><br style="clear:both;">
"""
}

settings = {
    'phg': "",
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
