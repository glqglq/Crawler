import ghost
import time
def test_ghost():
    gh = ghost.Ghost()
    se = ghost.Session(gh, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
                       wait_timeout=30,display=False,viewport_size=(5000,1000),ignore_ssl_errors=True,
                       plugins_enabled=True,java_enabled=True,download_images=False)
    print time.localtime()
    se.open("https://jd.com",
            timeout=30,user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36")
    se.wait_for_page_loaded(30)
    """
    try:
        se.wait_for_alert(30)
    except:
        pass

def func():
    return True
    """
    print se.content
    print time.localtime()
test_ghost()
