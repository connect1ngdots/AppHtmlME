# vim: fileencoding=utf-8
"""
AppHtml
@author Toshiya NISHIO(http://www.toshiya240.com)
"""
import locale
import urllib
import json
import imghdr
import struct

# テンプレートの予約語
# ['badgeS', 'badgeL', 'textonly',
#  'name', 'url', 'price', 'category', 'pubdate',
#  'icon100url', 'icon60url',
#  'artist', 'artisturl',
#  'desc', 'descnew', 'shortdesc'
#  'rating',
#  'userrating', 'userratingcnt',
#  'curuserrating', 'curuserratingcnt',
#  'version',
#  'seller', 'sellerurl',
#  'appsize', 'moveos', 'os', 'gamecenter', 'univ', 'lang',
#  'image1', 'image2', 'image3', 'image4', 'image5',
#  'univimage1', 'univimage2', 'univimage3', 'univimage4', 'univimage5',
#  'trackcnt', 'copyr', 'playtime', 'preview']

locale.setlocale(locale.LC_ALL, "ja_JP")

kindsDict = {
    '1) iPhone App': 'software',
    '2) iPad App': 'iPadSoftware',
    '3) Mac App': 'macSoftware',
    '4) Song': 'song',
    '5) Album': 'album',
    '6) Movie': 'movie',
    '7) Book': 'ebook'
}

proxies = None

def search(kwd, knd, cnt):
    url_base = "https://itunes.apple.com/jp/search?"

    url = url_base + urllib.urlencode({'term': kwd,
            'country': 'JP',
            'entity': knd,
            'limit': cnt});

    result = json.load(urllib.urlopen(url, proxies=proxies))
    if result['resultCount'] == 0:
        return None
    else:
        return result['results']

def appDict(searchResult, knd):
    titles = []
    noises = []
    i = 1
    for result in searchResult:
        if knd == "album":
            name = getValue(result, 'collectionCensoredName').encode('utf-8')
        else:
            name = getValue(result, 'trackCensoredName').encode('utf-8')
        artist = getValue(result, 'artistName').encode('utf-8')
        version = getValue(result, 'version').encode('utf-8')
        if knd in ["software", "iPadSoftware", "macSoftware", "ebook"]:
            price = getValue(result, 'price')
        elif knd in ["album"]:
            price = getValue(result, 'collectionPrice')
        elif knd in ["song", "movie"]:
            price = getValue(result, 'trackPrice')
        if price == "":
            noises.append(result)
            continue
        elif price == 0:
            price = "無料"
        else:
            price = "￥" + locale.currency(int(price),
                    symbol=False, grouping=True)
        title = "%d) %s %s - %s (%s)" % (i, name, version, artist, price)
        titles.append(title)
        i = i + 1
    for noise in noises:
        searchResult.remove(noise)
    dic = dict(zip(titles, searchResult))
    return dic

def affiliateUrl(url, affid):
    # url には既にパラメータが付いている状態と想定
    if url == "":
        return ""
    return url + '&' + urllib.urlencode({'at': affid})

def getImgSize(url):
    width = 0
    height = 0
    data = urllib.urlopen(url, proxies=proxies).read()
    kind = imghdr.what(None, h=data)
    if kind == 'jpeg':
        start = data.find('\xff\xc0')
        if start != -1:
            start += 5
            (height, width) = struct.unpack('>HH', data[start:start+4])
        # else: SOF0 is not found!
    elif kind == 'png':
        (width, height) = struct.unpack('>II', data[16:24])
    return (width, height)

def getWidth(url, scs):
    result = 0
    (width, height) = getImgSize(url)
    if height < width:
        result = int(scs)
    else:
        result = round(int(scs) * ((float(width) / height)))
    return result

def hasValue(jsonData, key):
    return key in jsonData and jsonData[key] is not None

def getValue(jsonData, key):
    if hasValue(jsonData, key):
        return jsonData[key]
    else:
        return ""

def getApp(jsonData, knd, scs, ipd, mac, aff, fmt):
    app = {}

    if knd == "album":
        app['name'] = getValue(jsonData, 'collectionCensoredName')
    else:
        app['name'] = getValue(jsonData, 'trackCensoredName')

    if knd in ["ebook", "software", "iPadSoftware", "macSoftware"]:
        price = getValue(jsonData, 'price')
    elif knd in ["album"]:
        price = getValue(jsonData, 'collectionPrice')
    elif knd in ["song", "movie"]:
        price = getValue(jsonData, 'trackPrice')
    else:
        price = ""
    if price == "":
        app['price'] = u"？"
    elif price == 0:
        app['price'] = u"無料"
    else:
        app['price'] = u"￥" + locale.currency(int(price),
                symbol=False, grouping=True)

    if knd in ["ebook", "software", "iPadSoftware", "macSoftware"]:
        app['category'] = ", ".join(getValue(jsonData, 'genres'))
    else:
        app['category'] = getValue(jsonData, 'primaryGenreName')

    app['pubdate'] = getValue(jsonData, 'releaseDate').replace("-", "/").split("T")[0]
    app['artist'] = getValue(jsonData, 'artistName')
    app['artisturl'] = getValue(jsonData, 'artistViewUrl')

    if knd in ["album"]:
        app['url'] = getValue(jsonData, 'collectionViewUrl')
    else:
        app['url'] = getValue(jsonData, 'trackViewUrl')
    if aff != "":
        app['artisturl'] = affiliateUrl(app['artisturl'], aff)
        app['url'] = affiliateUrl(app['url'], aff)

    app['icon100url'] = getValue(jsonData, 'artworkUrl100')
    app['icon60url'] = getValue(jsonData, 'artworkUrl60')

    app['rating'] = getValue(jsonData, 'trackContentRating')

    if hasValue(jsonData, 'averageUserRatingForCurrentVersion'):
        app['curuserrating'] = jsonData['averageUserRatingForCurrentVersion']
    else:
        app['curuserrating'] = u"無し"

    if hasValue(jsonData, 'userRatingCountForCurrentVersion'):
        app['curuserratingcnt'] = locale.currency(
                jsonData['userRatingCountForCurrentVersion'],
                symbol=False, grouping=True)
    else:
        app['curuserratingcnt'] = u"0"
    app['curuserratingcnt'] = app['curuserratingcnt'] + u"件の評価"

    if hasValue(jsonData, 'averageUserRating'):
        app['userrating'] = jsonData['averageUserRating']
    else:
        app['userrating'] = u"無し"

    if hasValue(jsonData, 'userRatingCount'):
        app['userratingcnt'] = locale.currency(
                jsonData['userRatingCount'],
                symbol=False, grouping=True)
    else:
        app['userratingcnt'] = u"0"
    app['userratingcnt'] = app['userratingcnt'] + u"件の評価"

    app['desc'] = u""
    app['descnew'] = u""
    app['shortdesc'] = u""
    if knd in ["ebook", "software", "iPadSoftware", "macSoftware"]:
        app['desc'] = getValue(jsonData, 'description').replace('\n', '<br>')
    elif knd in ["movie"]:
        app['desc'] = getValue(jsonData, 'longDescription').replace('\n', '<br>')
        app['shortdesc'] = getValue(jsonData, 'shortDescription').replace('\n', '<br>')
    if knd in ["software", "iPadSoftware", "macSoftware"]:
        app['descnew'] = getValue(jsonData, 'releaseNotes').replace('\n', '<br>')

    # iOS アプリの場合のみ(moveos, os, gamecenter, univ)
    app['moveos'] = u""
    app['os'] = u""
    app['gamecenter'] = u""
    app['univ'] = u""
    if knd in ["software", "iPadSoftware"]:
        app['moveos'] = ", ".join(getValue(jsonData, 'supportedDevices'))
        if app['moveos'].find("all") != -1:
            app['os'] = u"iPhone"
        elif app['moveos'].find("iPhone") != -1:
            app['os'] = u"iPhone"
        elif app['moveos'].find("iPad") != -1:
            app['os'] = u"iPad"
        features = getValue(jsonData, 'features')
        if features and 'gameCenter' in features:
            app['gamecenter'] = u"GameCenter対応"
        if features and 'iosUniversal' in features:
            app['univ'] = u"iPhone/iPadの両方に対応"

    # version, seller, sellerurl はアプリのみ(アプリ以外の場合は "" になる)
    app['version'] = getValue(jsonData, 'version')
    app['seller'] = getValue(jsonData, 'sellerName')
    app['sellerurl'] = getValue(jsonData, 'sellerUrl')

    # ファイルサイズはアプリのみ
    if knd in ["software", "iPadSoftware", "macSoftware"]:
        if not hasValue(jsonData, 'fileSizeBytes'):
            app['appsize'] = u"？"
        else:
            app['appsize'] = str(round(int(jsonData['fileSizeBytes'])/1000000.0 * 10) / 10) + u" MB"
    else:
        app['appsize'] = u""

    # lang はアプリのみ
    if knd in ["software", "iPadSoftware", "macSoftware"]:
        app['lang'] = ", ".join(getValue(jsonData, 'languageCodesISO2A'))
    else:
        app['lang'] = u""

    # スクショはアプリのみ
    if knd in ["software", "iPadSoftware", "macSoftware"]:
        for i in range(1, 6):
            app['image' + str(i)] = u""
            app['univimage' + str(i)] = u""
        # テンプレート文字列をチェックして必要な場合だけセットする
        # iPhone の場合は、Univスクショに iPad 画像をセット
        if knd == 'software':
            i = 1
            for ss in getValue(jsonData, 'screenshotUrls'):
                if fmt.find('image' + str(i)) != -1:
                    app['image' + str(i)] = u"<img alt='ss%d' src='%s' width='%dpx'>" % (i, ss, getWidth(ss, scs))
                i += 1
            i = 1
            for ss in getValue(jsonData, 'ipadScreenshotUrls'):
                if fmt.find('univimage' + str(i)) != -1:
                    app['univimage' + str(i)] = u"<img alt='univss%d' src='%s' width='%dpx'>" % (i, ss, round(getWidth(ss, ipd)))
                i += 1
        # iPad の場合は、Univスクショに iPhone 画像をセット(image, univimage)
        elif knd == 'iPadSoftware':
            i = 1
            for ss in getValue(jsonData, 'ipadScreenshotUrls'):
                if fmt.find('image' + str(i)) != -1:
                    app['image' + str(i)] = u"<img alt='ss%d' src='%s' width='%dpx'>" % (i, ss, round(getWidth(ss, ipd)))
                i += 1
            i = 1
            for ss in getValue(jsonData, 'screenshotUrls'):
                if fmt.find('univimage' + str(i)) != -1:
                    app['univimage' + str(i)] = u"<img alt='univss%d' src='%s' width='%dpx'>" % (i, ss, getWidth(ss, scs))
                i += 1
        # Mac の場合は、スクショのみで Univスクショは無し(image)
        elif knd == 'macSoftware':
            i = 1
            for ss in getValue(jsonData, 'screenshotUrls'):
                if fmt.find('image' + str(i)) != -1:
                    app['image' + str(i)] = u"<img alt='ss%d' src='%s' width='%dpx'>" % (i, ss, round(getWidth(ss, mac)))
                i += 1

    # 音楽のみ
    if knd in ["song", "album"]:
        app['trackcnt'] = getValue(jsonData, 'trackCount')

    # album のみ(album 以外の場合は "" になる)
    app['copyr'] = getValue(jsonData, 'copyright')

    # 映画のみ
    if knd in ['movie']:
        app['playtime'] = locale.currency(
                round(int(getValue(jsonData, 'trackTimeMillis'))/60000.0 * 10) / 10,
                symbol=False, grouping=True) + u" 分"

    # song と movie のみ
    if knd in ["song", "movie"]:
        app['preview'] = getValue(jsonData, 'previewUrl')

    # Badge
    if knd in ["macSoftware"]:
        app['badgeS'] = '<a href="%s" target="itunes_store" style="display:inline-block;overflow:hidden;background:url(http://linkmaker.itunes.apple.com/htmlResources/assets//images/web/linkmaker/badge_macappstore-sm.png) no-repeat;width:81px;height:15px;@media only screen{background-image:url(http://linkmaker.itunes.apple.com/htmlResources/assets//images/web/linkmaker/badge_macappstore-sm.svg);}"></a>' % app['url']
        app['badgeL'] = '<a href="%s" target="itunes_store" style="display:inline-block;overflow:hidden;background:url(http://linkmaker.itunes.apple.com/htmlResources/assets/ja_jp//images/web/linkmaker/badge_macappstore-lrg.png) no-repeat;width:165px;height:40px;@media only screen{background-image:url(http://linkmaker.itunes.apple.com/htmlResources/assets/ja_jp//images/web/linkmaker/badge_macappstore-lrg.svg);}"></a>' % app['url']
    elif knd in ["software", "iPadSoftware"]:
        app['badgeS'] = '<a href="%s" target="itunes_store" style="display:inline-block;overflow:hidden;background:url(http://linkmaker.itunes.apple.com/htmlResources/assets//images/web/linkmaker/badge_appstore-sm.png) no-repeat;width:61px;height:15px;@media only screen{background-image:url(http://linkmaker.itunes.apple.com/htmlResources/assets//images/web/linkmaker/badge_appstore-sm.svg);}"></a>' % app['url']
        app['badgeL'] = '<a href="%s" target="itunes_store" style="display:inline-block;overflow:hidden;background:url(http://linkmaker.itunes.apple.com/htmlResources/assets/ja_jp//images/web/linkmaker/badge_appstore-lrg.png) no-repeat;width:135px;height:40px;@media only screen{background-image:url(http://linkmaker.itunes.apple.com/htmlResources/assets/ja_jp//images/web/linkmaker/badge_appstore-lrg.svg);}"></a>' % app['url']
    elif knd in ["ebook"]:
        app['badgeS'] = '<a href="%s" target="itunes_store" style="display:inline-block;overflow:hidden;background:url(http://linkmaker.itunes.apple.com/htmlResources/assets//images/web/linkmaker/badge_bookstore-sm.png) no-repeat;width:65px;height:15px;@media only screen{background-image:url(http://linkmaker.itunes.apple.com/htmlResources/assets//images/web/linkmaker/badge_bookstore-sm.svg);}"></a>' % app['url']
        app['badgeL'] = '<a href="%s" target="itunes_store" style="display:inline-block;overflow:hidden;background:url(http://linkmaker.itunes.apple.com/htmlResources/assets/ja_jp//images/web/linkmaker/badge_bookstore-lrg.png) no-repeat;width:146px;height:40px;@media only screen{background-image:url(http://linkmaker.itunes.apple.com/htmlResources/assets/ja_jp//images/web/linkmaker/badge_bookstore-lrg.svg);}"></a>' % app['url']
    elif knd in ["song", "album", "movie"]:
        app['badgeS'] = '<a href="%s" target="itunes_store" style="display:inline-block;overflow:hidden;background:url(http://linkmaker.itunes.apple.com/htmlResources/assets//images/web/linkmaker/badge_itunes-sm.png) no-repeat;width:45px;height:15px;@media only screen{background-image:url(http://linkmaker.itunes.apple.com/htmlResources/assets//images/web/linkmaker/badge_itunes-sm.svg);}"></a>' % app['url']
        app['badgeL'] = '<a href="%s" target="itunes_store" style="display:inline-block;overflow:hidden;background:url(http://linkmaker.itunes.apple.com/htmlResources/assets/ja_jp//images/web/linkmaker/badge_itunes-lrg.png) no-repeat;width:110px;height:40px;@media only screen{background-image:url(http://linkmaker.itunes.apple.com/htmlResources/assets/ja_jp//images/web/linkmaker/badge_itunes-lrg.svg);}"></a>' % app['url']
    app['textonly'] = "<a href='%s' target='itunes_store'>%s - %s</a>" % (app['url'], app['name'], app['artist'])

    return app
