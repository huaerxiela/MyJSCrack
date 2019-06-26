import re
import requests


headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
}


def get_goods(goods_name):
    """
    根据商品名称返回商品列表页
    :param goods_name: 商品名称
    :return: 商品列表页
    """
    url = 'http://yangkeduo.com/search_result.html?search_key=' + goods_name
    print(url)

    res = requests.get(url, headers=headers, timeout=5)
    res_text = res.text
    list_id = re.search(r'"listID":"([^"]+)"', res_text).group(1)
    flip = re.search(r'"flip":"([^"]+)"', res_text).group(1)
    print([list_id, flip])

    res = requests.get('http://localhost:8085/pdd_search', timeout=5)
    anti_content = res.json().get('anti_result')
    print(anti_content)

    goods_params = {
        'page': 1,
        'list_id': list_id,
        'key_name': goods_name,
        'flip': flip,
        'anti_content': anti_content,
    }
    goods_url = 'http://apiv3.yangkeduo.com/search?page={page}&size=20&sort=default&requery=0&list_id={list_id}&q={key_name}&flip={flip}&anti_content={anti_content}&pdduid=0'
    res = requests.get(goods_url.format(**goods_params), headers=headers, timeout=5)
    return res.json()


if __name__ == '__main__':
    goods_list = get_goods('手机')
    print(goods_list)
