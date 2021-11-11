class Game:
    def __init__(self, name: str, price: list, thumbnail: str, short_desc: str,
                 long_desc: str, publishers: list, developers: list, release_date, genres: list,
                 min_specs: list, rec_specs: list, title_specs: list, vid_urls: list,
                 pic_urls: list, store_url: str, locale, country: str):

        _description = {
                'short': short_desc,
                'long': long_desc
                }

        _specification = {
            'min': ";".join('{}: {}'.format(y, x) for y, x in zip(title_specs[0:], min_specs[0:])),
            'max': ";".join('{}: {}'.format(y, x) for y, x in zip(title_specs[0:], rec_specs[0:]))
        }

        _price = {
            'discount': price[0],
            'original': price[1],
            'discount_fmt': price[2],
            'original_fmt': price[3],
        }

        _description = {
            'short': short_desc,
            'long': long_desc
        }

        _description = {
            'short': short_desc,
            'long': long_desc
        }

        self.game = {
            'name': name,
            'thumbnail': thumbnail,
            'release_date': release_date,
            'store_url': store_url,
            'locale_code': locale,
            'country_code': country,
            'description': _description,
            'specification': _specification,
            'videos': [{'url': item} for item in vid_urls],
            'pictures': [{'url': item} for item in pic_urls],
            'developers': [{'name': item} for item in developers],
            'features': [],
            'genres': [{'title': item} for item in genres],
            'prices': [_price],
            'publishers': [{'name': item} for item in publishers]
        }

    def get(self):
        return self.game
