try:
    from PySide.QtGui import *
    from PySide.QtCore import *
    from PySide.QtWebKit import *

except ImportError:
    pass
import lxml.html as HTML
def test_webkit(url):
    app = QApplication([])
    webview =  QWebView()
    loop = QEventLoop()
    webview.loadFinished.connect(loop.quit)
    webview.load(QUrl(url))
    loop.exec_()
    webview.show()
    frame = webview.page().mainFrame()
    frame.findFirstElement('#search_term').setAttribute('value','.')
    frame.findFirstElement('#page_size option:checked').setPlainText('1000')
    frame.findFirstElement('#search').evaluateJavaScript('this.click()')
    app.exec_()
    elements = None
    while not elements:
        app.processEvents()
        elements = frame.findAllElements('#results a')
    countries = [e.toPlainText().strip() for e in elements]
    return countries
    #html = webview.page().mainFrame().toHtml()
    #tree = HTML.fromstring(html)
    #return tree.cssselect('#result')[0].text_content()

if __name__ == '__main__':
    print test_webkit('http://example.webscraping.com/search')