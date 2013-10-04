AppHtmlME
=========

AppHtml for MarsEdit

はじめに
--------

AppHtml for MarsEdit は入力したキーワードにマッチするものを iTunes ストアから検索して、指定したフォーマットに整形して MarsEdit のエディタに挿入するものである。

ストアから以下のものを検索することができる。

1. iPhone アプリ
2. iPad アプリ
3. Mac アプリ
4. 曲
5. アルバム
6. 映画
7. 電子書籍


インストール
------------

1. AppHtmlME.worflow をダブルクリックして \[インストール\] をクリックする。
   (`~/Library/Services` に AppHtmlME.workflow を配置しても OK)

起動
----

MarsEdit の `Services` メニューから `AppHtmlME` を選択する。
\[システム環境設定\] > \[キーボード\] > \[キーボードショートカット\]
でキーボードショートカットを設定するとキーボードで起動できる。

カスタマイズ
------------

`~/Library/Services/AppHtmlMe.workflow/Scripts/apphtml_settings.py`
を `~/` にコピーして書き換えるとこちらの設定が使用される。

`template` のキー('中アイコン表示'など)が画面に表示される。
キーの辞書順に表示されるため、先頭に数字をつけることを推奨する。

### 予約語

名称                      | 予約語              | 使用可能な検索対象
--------------------------|---------------------|--------------------
小さいボタン              | ${badgeS}           | すべて
大きいボタン              | ${badgeL}           | すべて
テキストのみ              | ${textonly}         | すべて
名前                      | ${name}             | すべて
ストアへのリンク          | ${url}              | すべて
プレビューURL             | ${preview}          | Song/Movie
価格                      | ${price}            | すべて
カテゴリ                  | ${category}         | すべて
再生時間                  | ${playtime}         | Movie
トラック数                | ${trackcnt}         | Song/Album
リリース日                | ${pubdate}          | すべて
アイコン100               | ${icon100url}       | すべて
アイコン60                | ${icon60url}        | すべて
アーティスト名            | ${artist}           | すべて
アーティストURL           | ${artisturl}        | すべて
販売元                    | ${seller}           | アプリ(iPhone/iPad/Mac)
販売元サイトURL           | ${sellerurl}        | アプリ(iPhone/iPad/Mac)
コピーライト              | ${copyr}            | Album
説明                      | ${desc}             | アプリ(iPhone/iPad/Mac)/Book
What's New                | ${descnew}          | アプリ(iPhone/iPad/Mac)
短い説明                  | ${shortdesc}        | Movie
バージョン                | ${version}          | アプリ(iPhone/iPad/Mac)
レーティング              | ${rating}           | アプリ(iPhone/iPad/Mac)
評価★                    | ${userrating}       | アプリ(iPhone/iPad/Mac)/Book
レビュー件数              | ${userratingcnt}    | アプリ(iPhone/iPad/Mac)/Book
評価★(現)                | ${curuserrating}    | アプリ(iPhone/iPad/Mac)
レビュー件数(現)          | ${curuserratingcnt} | アプリ(iPhone/iPad/Mac)
サイズ                    | ${appsize}          | アプリ(iPhone/iPad/Mac)
サポートデバイス          | ${moveos}           | iPhone/iPadアプリ
言語                      | ${lang}             | アプリ(iPhone/iPad/Mac)
GameCenter対応            | ${gamecenter}       | iPhone/iPadアプリ
ユニバーサル対応          | ${univ}             | iPhone/iPadアプリ
スクリーンショット1       | ${image1}           | アプリ(iPhone/iPad/Mac)
スクリーンショット2       | ${image2}           | アプリ(iPhone/iPad/Mac)
スクリーンショット3       | ${image3}           | アプリ(iPhone/iPad/Mac)
スクリーンショット4       | ${image4}           | アプリ(iPhone/iPad/Mac)
スクリーンショット5       | ${image5}           | アプリ(iPhone/iPad/Mac)
スクリーンショット(univ)1 | ${univimage1}       | iPhone/iPadアプリ
スクリーンショット(univ)2 | ${univimage2}       | iPhone/iPadアプリ
スクリーンショット(univ)3 | ${univimage3}       | iPhone/iPadアプリ
スクリーンショット(univ)4 | ${univimage4}       | iPhone/iPadアプリ
スクリーンショット(univ)5 | ${univimage5}       | iPhone/iPadアプリ

