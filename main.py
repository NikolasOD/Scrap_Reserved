import requests
import json
from math import ceil

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image'
              '/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}


def collect_data(url_id):
    url_woman = 'https://arch.reserved.com/api/1007/category/27931/products?filters%5BsortBy%5D=3'
    url_man = 'https://arch.reserved.com/api/1007/category/27933/products?filters%5BsortBy%5D=3'
    url = ''
    if url_id == 1:
        url = url_woman
    elif url_id == 2:
        url = url_man
    s = requests.Session()
    response = s.get(
        url=f'{url}&filters%5Bsizes%5D'
            '%5B%5D=xs-s-i-ua-44-48&filters%5Bsizes%5D%5B%5D=xs&filters%5Bsizes%5D%5B%5D=xs-s&filters%5Bsizes%5D'
            '%5B%5D=xs-i-ua-42&filters%5Bsizes%5D%5B%5D=xs-s-i-ua-40-42&filters%5Bsizes%5D%5B%5D=xs-i-ua-44-46'
            '&filters%5Bsizes%5D%5B%5D=s-i-ua-46-48&filters%5Bsizes%5D%5B%5D=s&filters%5Bsizes%5D%5B%5D=s-i-ua'
            '-44&offset=200&pageSize=200',
        headers=headers
    )

    data = response.json()
    pagination_count = ceil(data.get('productsTotalAmount')/200)

    result_data = []

    for page in range(pagination_count):
        product_count = page * 200
        url = f'{url}&filters%5Bsizes%5D' \
              f'%5B%5D=xs-s-i-ua-44-48&filters%5Bsizes%5D%5B%5D=xs&filters%5Bsizes%5D%5B%5D=xs-s&filters%5Bsizes%5D' \
              f'%5B%5D=xs-i-ua-42&filters%5Bsizes%5D%5B%5D=xs-s-i-ua-40-42&filters%5Bsizes%5D%5B%5D=xs-i-ua-44-46' \
              f'&filters%5Bsizes%5D%5B%5D=s-i-ua-46-48&filters%5Bsizes%5D%5B%5D=s&filters%5Bsizes%5D%5B%5D=s-i-ua-44' \
              f'&offset={product_count}&pageSize=200'
        r = s.get(url=url, headers=headers)

        data = r.json()
        products = data.get('products')

        for product in products:
            colors = product.get('colorOptions')

            for color in colors:
                if color.get('hasDiscount') and color.get('isInStock'):
                    old_price = color.get('prices').get('minQtyRegularPrice')
                    new_price = color.get('prices').get('minQtyFinalPrice')
                    discount_percent = 100 - (new_price / old_price) * 100
                    if discount_percent >= 75:
                        result_data.append(
                            {
                                'title': color.get('name'),
                                'url': color.get('url'),
                                'old_price': old_price,
                                'new_price': new_price,
                                'discount_percent': ceil(discount_percent)
                            }
                        )
        print(f'{page + 1}/{pagination_count}')
    with open('result_data.json', 'w', encoding='utf-8') as file:
        json.dump(result_data, file, indent=4, ensure_ascii=False)


def main():
    collect_data(url_id=1)


if __name__ == '__main__':
    main()
