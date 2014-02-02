AppHtmlME
=========

AppHtml for MarsEdit

はじめに
--------

AppHtml for MarsEdit は入力したキーワードから iTunes ストアを検索し、
以下のコンテンツを指定フォーマットに整形して MarsEdit のエディタに挿入するものです。
コンテンツの紹介記事やレビュー記事を投稿したいブロガーに最適なツールです。

1. iPhone アプリ
2. iPad アプリ
3. Mac アプリ
4. 曲
5. アルバム
6. 映画
7. 電子書籍


インストール
------------

1. AppHtmlME.worflow をダブルクリックして \[インストール\] をクリックします。
   (`~/Library/Services` に AppHtmlME.workflow を配置しても OK)

起動
----

MarsEdit の `Services` メニューから `AppHtmlME` を選択します。
\[システム環境設定\] > \[キーボード\] > \[キーボードショートカット\]
でキーボードショートカットを設定するとキーボードで起動できます。

カスタマイズ
------------

`~/Library/Services/AppHtmlMe.workflow/Scripts/apphtml_settings.py`
を `~/` にコピーして書き換えるとこちらの設定が使用されます。

`template` のキー('大きいボタン'など)が画面に表示されます。
キーの辞書順に表示されるため、先頭に数字をつけることを推奨します。

### 予約語

書式テンプレートは HTML および以下の予約語を用いて記述してください。

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
説明                      | ${desc}             | アプリ(iPhone/iPad/Mac)/Movie/Book
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
実行日                    | ${today}            | すべて

既知の問題
----------

 1. 映画コンテンツのうちレンタルのみの場合 iTunes Search API から price の値が返されないため「レンタルのみ」を表示するようにしています。
 2. ボタンのバッジアイコンは、公式Link MakerにあわせてHTMLを返していましたが、style属性内のMedia Queriesの指定方法（@media only screen以降）では機能しないことを確認し、またブログ内で表示崩れが発生する可能性があることから、公式ツールの修正まで当該記述部分を削除します。
 3. その他に既知の問題がある場合はIssuesに記載しています。

免責事項
--------

本プロジェクトは、これらのツールが所定のデザイン・ガイドラインやアフィリエイト規約等へ準拠していることを保証するものではありません。
これらのツールを利用して生じたいかなる損害に対しても一切責任を負いません。

LICENSE
-------

This software is released under the MIT License, see LICENSE.
