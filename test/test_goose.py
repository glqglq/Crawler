# -*- coding: utf-8 -*-

from test.goose import Goose
from test.goose.text import StopWordsChinese
url  = 'http://www.ict.cas.cn/xwzx/jssxw/201705/t20170520_4794655.html'
g = Goose({'stopwords_class': StopWordsChinese})
article = g.extract(url=url)
print article.cleaned_text