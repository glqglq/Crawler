import mechanize


def test_mechanize():
    br = mechanize.Browser()
    br.open("https://tmall.com")
    print br