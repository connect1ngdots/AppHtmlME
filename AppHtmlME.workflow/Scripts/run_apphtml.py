#!/usr/bin/env python
# vim: fileencoding=utf-8
import sys
import os
import imp
import string

import apphtml
import apphtml_settings
import marsedit


settings = apphtml_settings.settings

# try to load user's settings
user_settings = None
fp = None
try:
    fp, path, desc = imp.find_module('apphtml_settings', [os.path.expanduser('~')])
    module = imp.load_module('apphtml_settings', fp, path, desc)
    user_settings = module.settings
except:
    pass
finally:
    if fp: fp.close()
if user_settings:
    settings = user_settings

# validation-1
if not ('cnt' in settings
        and 'aff' in settings
        and 'scs' in settings
        and 'iphone' in settings['scs']
        and 'ipad' in settings['scs']
        and 'mac' in settings['scs']
        and 'template' in settings
        and 'software' in settings['template']
        and len(settings['template']['software']) > 0
        and 'iPadSoftware' in settings['template']
        and len(settings['template']['iPadSoftware']) > 0
        and 'macSoftware' in settings['template']
        and len(settings['template']['macSoftware']) > 0
        and 'song' in settings['template']
        and len(settings['template']['song']) > 0
        and 'album' in settings['template']
        and len(settings['template']['album']) > 0
        and 'movie' in settings['template']
        and len(settings['template']['movie']) > 0
        and 'ebook' in settings['template']
        and len(settings['template']['ebook']) > 0
        ):
    marsedit.displayError("設定に定義が不足しています。")
    sys.exit(1)

cnt = settings['cnt'] # 検索の最大件数
aff = settings['aff'] # PHG Affiliate ID
scs = settings['scs']['iphone'] # スクショの長辺px
ipd = settings['scs']['ipad'] # iPadスクショの長辺px
mac = settings['scs']['mac'] # Macスクショの長辺px

# validation-2
def templateIsValid(templateDict):
    return len([k for k in templateDict
            if not isinstance(k, basestring)
                or not isinstance(templateDict[k], basestring)
            ]) == 0

if not (isinstance(cnt, int)
        and isinstance(aff, str)
        and isinstance(scs, int)
        and isinstance(ipd, int)
        and isinstance(mac, int)
        and templateIsValid(settings['template']['software'])
        and templateIsValid(settings['template']['iPadSoftware'])
        and templateIsValid(settings['template']['macSoftware'])
        and templateIsValid(settings['template']['song'])
        and templateIsValid(settings['template']['album'])
        and templateIsValid(settings['template']['movie'])
        and templateIsValid(settings['template']['ebook'])
        ):
    marsedit.displayError("設定値の型に誤りがあります。")
    sys.exit(2)

# main

knd = marsedit.choose("検索対象を選択してください", apphtml.kindsDict)
if knd is None:
    sys.exit(0)

kwd = marsedit.inputText("検索キーワードを入力してください")
if kwd is None:
    sys.exit(0)

searchResult = apphtml.search(kwd, knd, cnt)
if searchResult is None:
    marsedit.displayError("見つかりませんでした")
    sys.exit(0)

app = marsedit.choose("選択してください", apphtml.appDict(searchResult, knd))
if app is None:
    sys.exit(0)

fmt = marsedit.choose("書式テンプレートを選択してください", settings['template'][knd])
if fmt is None:
    sys.exit(0)

app = apphtml.getApp(app, knd, scs, ipd, mac, aff, fmt)

result = string.Template(fmt).safe_substitute(app)
marsedit.write(result)
