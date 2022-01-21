import json

import requests

def post_pic(data):
    resp = requests.post(url, headers=headers, data=data).json()
    next_max_id = resp.get('next_max_id')   # 获取下一页id
    if next_max_id:
        print(next_max_id)
    else:
        print('None')
    # next_media_ids = resp.get('next_media_ids') # 不用
    items = resp.get('sections')
    for item in items:
        medias = item.get('layout_content').get('medias')
        for m in medias:
            i = m.get('media')
            image_versions2 = i.get('image_versions2')
            if image_versions2 is not None:
                candidates = image_versions2.get('candidates')
                img_url = candidates[0].get('url')
                img_url_list.append(img_url)
    return next_max_id  # 返回下一页id

def get_pic(data):
    resp = requests.get(url2, headers=headers, params=data).json()
    end_cursor = resp.get('data').get('user').get('edge_owner_to_timeline_media').get('page_info').get('end_cursor')
    item = resp.get('data').get('user').get('edge_owner_to_timeline_media').get('edges')
    for i in item:
        img_url = i.get('node').get('display_url')
        img_url_list.append(img_url)
        print(img_url)
    # print(resp.url)
    return end_cursor

def saveImg(img_url_list):
    '''保存图'''
    i = 1
    for url in img_url_list:
        img = requests.get(url)
        with open('./qiandaolake/' + str(i) +'.jpg', 'wb') as f:
            f.write(img.content)
            print(f'正在保存{i}')
            i += 1

if __name__ == '__main__':
    img_url_list = []
    url = 'https://i.instagram.com/api/v1/tags/qiandaolake/sections/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'cookie': 'mid=YeZ94wAEAAGyx8Q1bFaT6iUzGJIT; ig_did=5C86459E-9A38-46CB-8E3F-6BC890EA4EA4; ig_nrcb=1; csrftoken=2IsYCKW07NIT03XteGaBzgRZ6GWUQTXo; ds_user_id=51266732797; sessionid=51266732797%3AqRNizHF5wi9eJL%3A0; rur="PRN\05451266732797\0541674111542:01f76de254d45da04b619cd1507dded1a7d02e32bff1d9dae3af076ef862f3ad6bd19f6c"',
        'x-asbd-id': '198387',
        'x-csrftoken': '2IsYCKW07NIT03XteGaBzgRZ6GWUQTXo',
        'x-ig-app-id': '936619743392459',
        'x-ig-www-claim': 'hmac.AR1QvbEv8aIrMpj789ZZ0ffgzBFv5vmKqkXzOMY7FI5mc-Z-',
        'x-instagram-ajax': 'bc3569920aaf',
        'x-requested-with': 'XMLHttpRequest',
        'referer':'https://www.instagram.com/visitqiandaolake/',
    }
    max_id = 'QVFCU2d1ZjM4Y1RHTGs5X3dEY2VhUVFxY29RUXlHajdMQW1qM05wRVdac1BaYnV5MHZlYmtCY0pjeUdXQjNqYnc0enJSQ2tEb0ZxMGwtdlRRdmNqNlJYMA=='
    # next_media_ids = '2742095404914821000'
    for i in range(71):
        # print(len(img_url_list))
        data = {
            'include_persistent': 0,
            'max_id': max_id,
            # 'next_media_ids[]': next_media_ids,
            'page': i + 1,
            'surface': 'grid',
            'tab': 'recent',
        }
        # next_max_id = post_pic(data)
        # max_id = next_max_id
        # next_media_ids = next_media_ids

    after = 'QVFCa2ZBVVdfV0FtY043aDRSQ0ItdEROZ0RfMHJNR3NPam9MalJOdkVrMXgzc3I5QzJHVkNDWlR3VE1GVXVjM1dQNVE5Z1VNOWVaMEFYMW9JMDA1aTRkUQ=='
    for i in range(10):
        url2 = 'https://www.instagram.com/graphql/query/'
        data = {
            'query_hash': '8c2a529969ee035a5063f2fc8602a0fd',
            'variables': '{"id":"5883068459","first":50,"after": "%s"}' % (after),
        }
        print(after)
        print(len(img_url_list))
        end_cursor = get_pic(data)
        after = end_cursor
        # break
    print(len(img_url_list))
    saveImg(img_url_list)

