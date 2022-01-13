class Game:
    def __init__(self, name: str, price: list, thumbnail: str, short_desc: str,
                 long_desc: str, publishers: list, developers: list, release_date, genres: list,
                 min_specs: list, rec_specs: list, title_specs: list, vid_urls: list,
                 pic_urls: list, store_url: str, locale, country: str):

        if title_specs is not None:
            _specification = {
                'min': None if min_specs is None else
                ";".join('{}: {}'.format(y, x) for y, x in zip(title_specs[0:], min_specs[0:])),
                'max': None if rec_specs is None else
                ";".join('{}: {}'.format(y, x) for y, x in zip(title_specs[0:], rec_specs[0:]))
            }
        else:
            _specification = {
                'min': None,
                'max': None
            }

        _price = {
            'discount': None,
            'original': None,
            'discount_fmt': None,
            'original_fmt': None,
        } if not price or len(price) is not 4 else {
            'discount': price[0],
            'original': price[1],
            'discount_fmt': price[2],
            'original_fmt': price[3],
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
            'videos': [] if vid_urls is None else [{'url': item} for item in vid_urls],
            'pictures': [] if pic_urls is None else [{'url': item} for item in pic_urls],
            'developers': [] if developers is None else [{'name': item} for item in developers],
            'features': [],
            'genres': [] if genres is None else [{'title': item} for item in genres],
            'prices': [_price],
            'publishers': [] if publishers is None else [{'name': item} for item in publishers]
        }

    def get(self):
        return self.game
