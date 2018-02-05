# !/usr/bin/env python
# Google example
import pprint
import simplejson as json
from googleapiclient.discovery import build


def snippets(str):
    service = build("customsearch", "v1",
                    developerKey="AIzaSyAeOp7L_cXV_VGjXuXkj_in8I1-pccZEEU")

    res = service.cse().list(q=str,
                             cx='004635228232604600486:dehcqnd7kkq', num=9).execute()
    items = json.loads(json.dumps(res)).get('items')
    snippet = []
    count = 0
    for i in items:
        j = items.pop(count)
        snippet.append(j.get('snippet'))
        count = count + 1
    return snippet


if __name__ == '__main__':
    main()
