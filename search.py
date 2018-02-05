# !/usr/bin/env python
# Google example
import pprint
import simplejson as json
from googleapiclient.discovery import build



def main():
    service = build("customsearch", "v1",
                    developerKey="AIzaSyAeOp7L_cXV_VGjXuXkj_in8I1-pccZEEU")

    res = service.cse().list(q='lectures',
                             cx='004635228232604600486:dehcqnd7kkq', num=10).execute()
    dct = json.loads(json.dumps(res)).get('items').get('snippet')
    print dct




def snippet(dct):
    if "items" in dct:
        return dct['items']


if __name__ == '__main__':
    main()
