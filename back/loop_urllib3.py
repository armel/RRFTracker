import urllib3
import datetime
import time
import sys
import json

url = 'http://rrf.f5nlg.ovh/api/svxlink/technique'

http = urllib3.PoolManager(timeout=1.0)
http = urllib3.PoolManager(
    timeout=urllib3.Timeout(connect=.5, read=.5)
)

def main(argv):
    # Boucle principale
    while(True):
        chrono_start = time.time()
        tmp = datetime.datetime.now()
        now = tmp.strftime('%Y-%m-%d %H:%M:%S')

        # Request HTTP datas
        try:
            r = http.request('GET', url, timeout=1, retries=Retry(10))
            data = json.loads(r.data.decode('utf-8'))

            print('Trace 1', now, 'Success')
        except:
            print('Trace 0', now, 'Failure')
            data = ''

        chrono_stop = time.time()
        chrono_time = chrono_stop - chrono_start
        if chrono_time < 1:
            sleep = 1 - chrono_time
        else:
            tmp = datetime.datetime.now()
            now = tmp.strftime('%Y-%m-%d %H:%M:%S')
            print('Trace 2', now, '>>>>>>>>>> Freeze')
            sleep = 0
        time.sleep(sleep)

        if count['Success'] == 500:
            print(count)
            exit()

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        pass