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

cnt = settings['cnt'] # 検索の最大件数
aff = settings['aff'] # PHG Affiliate ID
scs = settings['scs']['iphone'] # スクショの長辺px
ipd = settings['scs']['ipad'] # iPadスクショの長辺px
mac = settings['scs']['mac'] # Macスクショの長辺px

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
