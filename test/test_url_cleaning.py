urls = ['asdsadsadas','.asdasdsadsa','.feewfwefewf']
url_now = 'http://www.ict.ac.cn'

for i in range(len(urls)):
    if urls[i][0] == '.':
        urls[i] = url_now + r'/' + urls[i][1:]
print urls