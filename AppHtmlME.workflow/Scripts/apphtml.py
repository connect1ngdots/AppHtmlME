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
#  'appname', 'version', 'price', 'title', 'category', 'appsize', 'pubdate',
#  'affurl', 'url',
#  'artistname', 'sellername', 'seller', 'sellersite', 'selleritunes', 
#  'icon100url', 'icon60url',
#  'moveos', 'os', 'gamecenter', 'univ', 'lang',
#  'rating', 'curverrating', 'curreviewcnt', 'allverrating', 'allreviewcnt',
#  'desc', 'descnew',
#  'image1', 'image2', 'image3', 'image4', 'image5',
#  'univimage1', 'univimage2', 'univimage3', 'univimage4', 'univimage5']

locale.setlocale(locale.LC_ALL, "ja_JP")

kindsDict = {
    '1) iPhone App': 'software',
    '2) iPad App': 'iPadSoftware',
    '3) Mac App': 'macSoftware'
}

# proxy
proxies = None

def searchApp(kwd, knd, cnt):
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

def appDict(searchResult):
    titles = []
    i = 1
    for result in searchResult:
        appname = getValue(result, 'trackCensoredName').encode('utf-8')
        version = getValue(result, 'version').encode('utf-8')
        price = getValue(result, 'price')
        if price == "":
            continue
        elif price == 0:
            price = "無料"
        else:
            price = "￥" + locale.currency(int(price),
                    symbol=False, grouping=True)
        title = "%d) %s %s (%s)" % (i, appname, version, price)
        titles.append(title)
        i = i + 1
    dic = dict(zip(titles, searchResult))
    return dic

def affiliateUrl(url, affid):
    # url には既にパラメータが付いている状態と想定
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

    app['appname'] = getValue(jsonData, 'trackCensoredName')
    app['version'] = getValue(jsonData, 'version')
    if not hasValue(jsonData, 'price'):
        app['price'] = u"?"
    elif jsonData['price'] == 0:
        app['price'] = u"無料"
    else:
        app['price'] = u"￥" + locale.currency(int(jsonData['price']),
                symbol=False, grouping=True)
    app['title'] = "%s %s (%s)" % (app['appname'], app['version'], app['price'])
    app['category'] = ", ".join(getValue(jsonData, 'genres'))
    if not hasValue(jsonData, 'fileSizeBytes'):
        app['appsize'] = u"?"
    else:
        app['appsize'] = str(round(int(jsonData['fileSizeBytes'])/1000000.0 * 10) / 10) + u" MB"
    app['pubdate'] = getValue(jsonData, 'releaseDate').replace("-", "/").split("T")[0]
    app['artistname'] = getValue(jsonData, 'artistName')
    app['sellername'] = getValue(jsonData, 'sellerName')
    app['seller'] = "%s - %s" % (app['artistname'], app['sellername'])
    app['sellersite'] = getValue(jsonData, 'sellerUrl')
    if aff == "":
        app['selleritunes'] = getValue(jsonData, 'artistViewUrl')
        app['affurl'] = getValue(jsonData, 'trackViewUrl')
    else:
        app['selleritunes'] = affiliateUrl(getValue(jsonData, 'artistViewUrl'), aff)
        app['affurl'] = affiliateUrl(getValue(jsonData, 'trackViewUrl'), aff)
    app['url'] = getValue(jsonData, 'trackViewUrl')

    app['icon100url'] = getValue(jsonData, 'artworkUrl100')
    app['icon60url'] = getValue(jsonData, 'artworkUrl60')

    # Mac の場合はない(moveos, os, gamecenter, univ)
    app['moveos'] = u""
    app['os'] = u""
    app['gamecenter'] = u""
    app['univ'] = u""
    if knd != "macSoftware":
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

    app['lang'] = ", ".join(getValue(jsonData, 'languageCodesISO2A'))
    app['rating'] = getValue(jsonData, 'trackContentRating')

    if hasValue(jsonData, 'averageUserRatingForCurrentVersion'):
        app['curverrating'] = jsonData['averageUserRatingForCurrentVersion']
    else:
        app['curverrating'] = u"無し"

    if hasValue(jsonData, 'userRatingCountForCurrentVersion'):
        app['curreviewcnt'] = locale.currency(
                jsonData['userRatingCountForCurrentVersion'],
                symbol=False, grouping=True)
    else:
        app['curreviewcnt'] = u"0"
    app['curreviewcnt'] = app['curreviewcnt'] + u"件の評価"

    if hasValue(jsonData, 'averageUserRating'):
        app['allverrating'] = jsonData['averageUserRating']
    else:
        app['allverrating'] = u"無し"

    if hasValue(jsonData, 'userRatingCount'):
        app['allreviewcnt'] = locale.currency(
                jsonData['userRatingCount'],
                symbol=False, grouping=True)
    else:
        app['allreviewcnt'] = u"0"
    app['allreviewcnt'] = app['allreviewcnt'] + u"件の評価"

    app['desc'] = getValue(jsonData, 'description').replace('\n', '<br />')
    app['descnew'] = getValue(jsonData, 'releaseNotes').replace('\n', '<br />')

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

    # Badge
    if aff == "":
        url = app['url']
    else:
        url = app['affurl']
    if knd == "macSoftware":
        app['badgeS'] = '<a href="%s" target="itunes_store" style="display:inline-block;overflow:hidden;background:url(http://linkmaker.itunes.apple.com/htmlResources/assets//images/web/linkmaker/badge_macappstore-sm.png) no-repeat;width:81px;height:15px;@media only screen{background-image:url(http://linkmaker.itunes.apple.com/htmlResources/assets//images/web/linkmaker/badge_macappstore-sm.svg);}"></a>' % url
        app['badgeL'] = '<a href="%s" target="itunes_store" style="display:inline-block;overflow:hidden;background:url(http://linkmaker.itunes.apple.com/htmlResources/assets/ja_jp//images/web/linkmaker/badge_macappstore-lrg.png) no-repeat;width:165px;height:40px;@media only screen{background-image:url(http://linkmaker.itunes.apple.com/htmlResources/assets/ja_jp//images/web/linkmaker/badge_macappstore-lrg.svg);}"></a>' % url
    else:
        app['badgeS'] = "<a href='%s' target='itunes_store' style='display:inline-block;overflow:hidden;background:url(http://linkmaker.itunes.apple.com/htmlResources/assets//images/web/linkmaker/badge_appstore-sm.png) no-repeat;width:61px;height:15px;@media only screen{background-image:url(http://linkmaker.itunes.apple.com/htmlResources/assets//images/web/linkmaker/badge_appstore-sm.svg);}'></a>" % url
        app['badgeL'] = "<a href='%s' target='itunes_store' style='display:inline-block;overflow:hidden;background:url(http://linkmaker.itunes.apple.com/htmlResources/assets/ja_jp//images/web/linkmaker/badge_appstore-lrg.png) no-repeat;width:135px;height:40px;@media only screen{background-image:url(http://linkmaker.itunes.apple.com/htmlResources/assets/ja_jp//images/web/linkmaker/badge_appstore-lrg.svg);}'></a>" % url
    app['textonly'] = "<a href='%s' target='itunes_store'>%s - %s</a>" % (url, app['appname'], app['artistname'])

    return app
