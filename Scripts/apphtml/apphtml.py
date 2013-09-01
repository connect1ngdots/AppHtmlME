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

# テンプレートの予約語(41個)
# ['appname', 'version', 'price', 'title', 'category', 'appsize', 'pubdate',
#  'seller', 'sellersite', 'selleritunes', 'linkshareurl', 'url',
#  'icon175url', 'icon100url', 'icon75url', 'icon53url',
#  'moveos', 'os', 'gamecenter', 'univ', 'lang', 'rating', 'curverrating',
#  'curverstar', 'curreviewcnt', 'allverrating', 'allverstar', 'allreviewcnt',
#  'desc', 'descnew',
#  'image1', 'image2', 'image3', 'image4', 'image5',
#  'univimage1', 'univimage2', 'univimage3', 'univimage4', 'univimage5',
#  'storeButton'];

locale.setlocale(locale.LC_ALL, "ja_JP")

kinds = ['1) iPhone App', '2) iPad App', '3) Mac App']
kindsDict = dict(zip(kinds, ['software', 'iPadSoftware', 'macSoftware']))

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
        appname = result['trackCensoredName'].encode('utf-8')
        version = result['version'].encode('utf-8')
        if result['price'] == 0:
            price = "無料"
        else:
            price = "￥" + locale.currency(int(result['price']),
                    symbol=False, grouping=True)
        title = "%d) %s %s (%s)" % (i, appname, version, price)
        titles.append(title)
        i = i + 1
    dic = dict(zip(titles, searchResult))
    return dic

def affiliateUrl(url, affid):
    # url には既にパラメータが付いている状態と想定
    return url + '&' + urllib.urlencode({'at': affid})

def getStar(val):
    star = u"<img alt='' src='http://s.mzstatic.com/htmlResources/E6C6/web-storefront/images/rating_star.png' />"
    half = u"<img alt='' src='http://s.mzstatic.com/htmlResources/E6C6/web-storefront/images/rating_star_half.png' />"
    if val is None:
        ret = u"無し"
    else:
        v = str(val).split(".")
        ret = star * int(v[0])
        if 1 < len(v):
            ret = ret + half
    return ret

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
    app['seller'] = "%s - %s" % (getValue(jsonData, 'artistName'), getValue(jsonData, 'sellerName'))
    app['sellersite'] = getValue(jsonData, 'sellerUrl')
    if aff == "":
        app['selleritunes'] = getValue(jsonData, 'artistViewUrl')
        app['linkshareurl'] = getValue(jsonData, 'trackViewUrl')
    else:
        app['selleritunes'] = affiliateUrl(getValue(jsonData, 'artistViewUrl'), aff)
        app['linkshareurl'] = affiliateUrl(getValue(jsonData, 'trackViewUrl'), aff)
    app['url'] = getValue(jsonData, 'trackViewUrl')

    (iconUrlBase, nil, nil) = getValue(jsonData, 'artworkUrl100').replace("512x512-75.", "").rpartition(".")
    app['icon175url'] = iconUrlBase + ".175x175-75.png"
    app['icon100url'] = iconUrlBase + ".100x100-75.png"
    app['icon75url'] = iconUrlBase + ".75x75-65.png"
    app['icon53url'] = iconUrlBase + ".53x53075.png"

    # Store Button
    if knd == "macSoftware":
        app['storeButton'] = 'http://r.mzstatic.com/images/web/linkmaker/badge_macappstore-sm.gif'
    else:
        app['storeButton'] = 'http://r.mzstatic.com/images/web/linkmaker/badge_appstore-sm.gif'

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
            app['gamecenter'] = u"<img width='100' alt='GameCenter対応' src='http://s.mzstatic.com/htmlResources/E6C6/web-storefront/images/gc_badge.png'>"
        if features and 'iosUniversal' in features:
            app['univ'] = u"<img alt='+' src='http://s.mzstatic.com/htmlResources/E6C6/web-storefront/images/fat-binary-badge-web.png' />iPhone/iPadの両方に対応"

    app['lang'] = ", ".join(getValue(jsonData, 'languageCodesISO2A'))
    app['rating'] = getValue(jsonData, 'trackContentRating')

    if hasValue(jsonData, 'averageUserRatingForCurrentVersion'):
        app['curverrating'] = jsonData['averageUserRatingForCurrentVersion']
        app['curverstar'] = getStar(jsonData['averageUserRatingForCurrentVersion'])
    else:
        app['curverrating'] = u"無し"
        app['curverstar'] = u"無し"

    if hasValue(jsonData, 'userRatingCountForCurrentVersion'):
        app['curreviewcnt'] = locale.currency(
                jsonData['userRatingCountForCurrentVersion'],
                symbol=False, grouping=True)
    else:
        app['curreviewcnt'] = u"0"
    app['curreviewcnt'] = app['curreviewcnt'] + u"件の評価"

    if hasValue(jsonData, 'averageUserRating'):
        app['allverrating'] = jsonData['averageUserRating']
        app['allverstar'] = getStar(jsonData['averageUserRating'])
    else:
        app['allverrating'] = u"無し"
        app['allverstar'] = u"無し"

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
    return app
