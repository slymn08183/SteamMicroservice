import threading
from datetime import datetime
from json.decoder import JSONDecodeError
from time import sleep
from app.data_access.game_dao import GameDAO
from bs4 import BeautifulSoup
from core.models import Game as GameCore
from app.models.game import Game

import requests
import re

from app.constants import *
from app.models.custom_errors import *
global counter_games


def get_all_game_data_steam(_locale, _country, is_update):
    offline = False
    written_game_ids_steam = open(WRITTEN_GAME_IDS.
                                  format(_locale, _country), 'r', encoding='utf-8')
    written_game_ids_steam_ = written_game_ids_steam.readlines()
    written_game_ids_steam.close()

    page_data_failed_ids_steam = open(PAGE_DATA_FAILED_IDS.
                                      format(_locale, _country), 'r', encoding='utf-8')
    page_data_failed_ids_steam_ = page_data_failed_ids_steam.readlines()
    page_data_failed_ids_steam.close()

    non_game_ids_steam = open(NON_GAME_IDS.
                              format(_locale, _country), 'r', encoding='utf-8')
    non_game_ids_steam_ = non_game_ids_steam.readlines()
    non_game_ids_steam.close()

    if offline is False:
        all_game_ids_steam_ = [json_['appid'] for json_ in requests.get(GET_GAME_IDS).json()['applist']['apps']]

        print(len(all_game_ids_steam_))
        all_game_ids_steam_ = [x for x in all_game_ids_steam_ if x not in non_game_ids_steam_]
        print(len(all_game_ids_steam_))
        all_game_ids_steam_ = [x for x in all_game_ids_steam_ if x not in written_game_ids_steam_]
        print(len(all_game_ids_steam_))
        all_game_ids_steam_ = [x for x in all_game_ids_steam_ if x not in page_data_failed_ids_steam_]
        print(len(all_game_ids_steam_))

    else:
        data = open('html.txt', 'r')
        all_game_ids_steam_ = [x.replace("\n", "") for x in data.readlines()]
        data.close()

    global counter_games
    counter_games = len(page_data_failed_ids_steam_) + len(non_game_ids_steam_) + len(written_game_ids_steam_)

    # split_processing(all_game_ids_steam_, get_game_steam_loop, 10)
    # print(str(all_game_ids_steam_))
    get_game_steam_loop(all_game_ids_steam_, 0, -1, _locale, _country, is_update)

    written_game_ids_xbox = open(WRITTEN_GAME_IDS.format(_locale, _country), 'w', encoding='utf-8')
    written_game_ids_xbox.close()


def split_processing(items, func, num_splits=2):
    split_size = len(items) // num_splits
    threads = []
    for i in range(num_splits):
        # time.sleep(i)
        # determine the indices of the list this thread will handle
        start = i * split_size
        # special case on the last chunk to account for uneven splits
        end = None if i+1 == num_splits else (i+1) * split_size
        # create the thread
        threads.append(
            threading.Thread(target=func, args=(items, start, end)))
        threads[-1].start()  # start the thread we just created

    # wait for all threads to finish
    for t in threads:
        t.join()


def get_game_steam_loop(all_game_ids_steam_, start, end, _locale, _country, is_update):
    dao = GameDAO()
    if end == -1:
        end = len(all_game_ids_steam_)
    for id_ in all_game_ids_steam_[start: end]:

        page_data_failed_ids_steam = open(PAGE_DATA_FAILED_IDS.
                                          format(_locale, _country), 'a', encoding='utf-8')
        written_game_ids_steam = open(WRITTEN_GAME_IDS.
                                      format(_locale, _country), 'a', encoding='utf-8')
        non_game_ids_steam = open(NON_GAME_IDS.
                                  format(_locale, _country), 'a', encoding='utf-8')

        global counter_games
        print('Getting game : {}'.format(counter_games))
        counter_games += 1
        is_once = True
        while True:
            try:
                if is_update:
                    _game = get_game_data_steam(_locale, _country, str(id_))
                    query = dao.get_by_name(_game.get('name'))
                    dao.update(query, _game)
                else:
                    dao.create(get_game_data_steam(_locale, _country, str(id_)))
                # time.sleep(1)
                written_game_ids_steam.write('{}\n'.format(id_))
                print('\t\tOk:' + str(id_))
            except PageDataIsNotJson as err:
                non_game_ids_steam.write('{}\n'.format(id_))
                print('\t\t' + err.game_id)
                # print("To continue type 1")
                # num1 = int(input())
                # if num1 == 1:
                #     pass
                # else:
                #     sys.exit()
            except GetPageDataFailed as err:
                # counter = 0
                # while True:
                #     sleep(1)
                #     print("Waiting 2 min cause of steam ban: {}s".format(counter))
                #     counter += 1
                #     if counter == 120:
                #         break
                # if not is_once:
                #     is_once = False
                #     continue
                page_data_failed_ids_steam.write('{}\n'.format(id_))
                print('\t\t' + err.game_id)
            except GetNameFailed as err:
                page_data_failed_ids_steam.write('{}\n'.format(id_))
                print('\t\t' + err.game_id)
            except ErrorWhileLoadingStoreUrl as err:
                non_game_ids_steam.write('{}\n'.format(id_))
                print('\t\t' + err.game_id)
            except NotGameError as err:
                non_game_ids_steam.write('{}\n'.format(id_))
                print('\t\t' + err.game_id)
            except GameCore.DoesNotExist:
                dao.create(get_game_data_steam(_locale, _country, str(id_)))
            except Exception as e:
                print(e)
                raise e
            print('\n')
            is_once = True
            break

        page_data_failed_ids_steam.close()
        written_game_ids_steam.close()
        non_game_ids_steam.close()


def __get_price_data_steam(_locale, _country, steam_id, variable=None):

    if variable is None:

        try:
            variable = requests.get("https://store.steampowered.com/api/appdetails?appids={}&cc={}&l={}".
                                    format(steam_id, _country, _locale)).json()
        except JSONDecodeError:
            raise PageDataIsNotJson(steam_id)
        # print('\t\t' + 'PAGE -----> '+str(result))

        try:
            if variable[steam_id]['success'] is False:
                raise NotGameError(steam_id)
        except KeyError:
            raise GetPageDataFailed(steam_id)
        except TypeError:
            raise GetPageDataFailed(steam_id)

        if variable[steam_id]['data']['type'] != 'game':
            raise NotGameError(steam_id)

    try:
        price = [variable[steam_id]['data']['price_overview']['final'],
                 variable[steam_id]['data']['price_overview']['initial'],
                 variable[steam_id]['data']['price_overview']['final_formatted'],
                 variable[steam_id]['data']['price_overview']['initial_formatted']]
    except TypeError:
        price = None
        GetPriceDataFailed(steam_id)
    except KeyError:
        price = None
        GetPriceDataFailed(steam_id)

    return price  # TODO: should give an output maybe txt.


def get_game_data_steam(_locale, _country, steam_id):

    # steam_key = "57690"
    # steam_key = "233450"
    # tr_ = "cc=tr&l=turkish"
    # de_ = "cc=DE&l=german"
    en_ = "cc=US&l=en"

    try:
        result = requests.get(GET_GAME_DETAIL.
                              format(steam_id, _locale, _country)).json()
    except JSONDecodeError:
        raise PageDataIsNotJson(steam_id)
    # print('\t\t' + 'PAGE -----> '+str(result))

    try:
        if result[steam_id]['success'] is False:

            raise GetPageDataFailed(steam_id)
    except ErrorWhileLoadingStoreUrl:
        raise GetPageDataFailed(steam_id)
    except TypeError:
        raise GetPageDataFailed(steam_id)

    if result[steam_id]['data']['type'] != 'game':
        raise NotGameError(steam_id)

    # game.store = _type.steam
    identifier = steam_id

    try:
        name = result[steam_id]['data']['name']
    except KeyError:
        raise GetNameFailed(steam_id)
    except TypeError:
        raise GetNameFailed(steam_id)
    thumbnail = result[steam_id]['data']['header_image']
    # should be get ridden of html tags

    text = []
    store_url = 'https://store.steampowered.com/app/{}/'.format(steam_id)

    try:
        for i in BeautifulSoup(requests.get(store_url).text,
                               'html.parser').find('div', {'id': 'game_area_description'}):
            text.append(str(i).replace('<br/>', '').replace('<h2>', '').
                        replace('</h2>', '').replace('\t', '').replace('\r', ''))
    except TypeError:
        raise ErrorWhileLoadingStoreUrl(steam_id)
    except KeyError:
        raise ErrorWhileLoadingStoreUrl(steam_id)

    while '' in text:
        text.remove('')

    long_desc = ""
    for i in text:
        long_desc += i + '\n'

    # get url/urls and clean tags
    try:
        tmp = re.search('<(.*?)url=(.*?)"(.*?)a>', long_desc).group(2)
        long_desc = re.sub('<(.*?)url=(.*?)"(.*?)a>', tmp, long_desc)
    except AttributeError:
        print('\t\t' + 'No link found in description.')

    # clean all tags
    try:
        long_desc = re.sub('<.*?>', '', long_desc)
    except KeyError:
        print('\t\t' + 'No tags left in description.')
    except TypeError:
        print('\t\t' + 'No tags left in description.')

    long_desc = long_desc[0:5000]
    short_desc = result[steam_id]['data']['short_description'][0:2000]

    try:
        developers = result[steam_id]['data']['developers']
    except KeyError:
        developers = None
        GetDevelopersDataFailed(steam_id)
    except TypeError:
        developers = None
        GetDevelopersDataFailed(steam_id)

    try:
        publishers = result[steam_id]['data']['publishers']
    except TypeError:
        publishers = None
    except KeyError:
        publishers = None

    price = __get_price_data_steam(_locale, _country, steam_id, result)

    genres = []

    if _locale != 'en':
        result_en = requests.get("https://store.steampowered.com/api/appdetails?appids={}&{}".
                                 format(steam_id, en_)).json()
    else:
        result_en = result

    try:
        for word in [json_['description'] for json_ in result_en[steam_id]['data']['genres']]:
            genres.append(str(word).replace(' ', '').upper())
    except TypeError:
        genres = None
        GetGenreFailed(steam_id)
    except KeyError:
        genres = None
        GetGenreFailed(steam_id)

    try:
        release_date = result_en[steam_id]['data']['release_date']['date']
    except TypeError:
        release_date = None
        GetReleaseDateFailed(steam_id)
    except KeyError:
        release_date = None
        GetReleaseDateFailed(steam_id)

    try:
        vid_urls = [urls['webm']['max'] for urls in result_en[steam_id]['data']['movies']]
    except TypeError:
        vid_urls = None
        GetVideoDataFailed(steam_id)
    except KeyError:
        vid_urls = None
        GetVideoDataFailed(steam_id)

    try:
        pic_urls = [urls['path_full'] for urls in result_en[steam_id]['data']['screenshots']]
    except KeyError:
        pic_urls = None
        GetPictureDataFailed(steam_id)
    except TypeError:
        pic_urls = None
        GetPictureDataFailed(steam_id)

    title_specs = []
    min_specs = []
    rec_specs = []

    try:
        for i in BeautifulSoup(result[steam_id]['data']['pc_requirements']['recommended'], "html.parser").find():
            tmp = str(BeautifulSoup(str(i), "html.parser").text).split(":")
            rec_specs.append(tmp[1])
    except TypeError:
        rec_specs = None
    except KeyError:
        rec_specs = None
    except IndexError:
        rec_specs = None

    # FIXME: bura ne amk index err falan iyi ayarla burayı

    try:
        min_str = result[steam_id]['data']['pc_requirements']['minimum']
        if rec_specs[0] == "null":
            min_str = min_str.replace("<strong>Minimum:</strong><br>", "")

        for i in BeautifulSoup(min_str, "html.parser").find():
            tmp = str(BeautifulSoup(str(i), "html.parser").text).split(":")
            title_specs.append(tmp[0])
            min_specs.append(tmp[1])
    except TypeError:
        min_specs = None
        rec_specs = None
        title_specs = None
    except KeyError:
        min_specs = None
        rec_specs = None
        title_specs = None
    except IndexError:
        min_specs = None
        rec_specs = None
        title_specs = None

    return Game(
        locale=_locale,
        country=_country,
        name=name,
        thumbnail=thumbnail,
        short_desc=short_desc,
        long_desc=long_desc,
        title_specs=title_specs,
        min_specs=min_specs,
        rec_specs=rec_specs,
        store_url=store_url,
        release_date=release_date,
        developers=developers,
        publishers=publishers,
        genres=genres,
        pic_urls=pic_urls,
        vid_urls=vid_urls,
        price=price,
    ).get()


# def get_all_price_data_steam(_locale, _country):
#
#     get_price_ids_steam = open('outputs/steam/{}-{}/price/set_price_ids_steam.txt'.
#                                format(_locale, _country), 'r', encoding='utf-8')
#     get_price_ids_steam_ = get_price_ids_steam.readlines()
#     get_price_ids_steam.close()
#
#     written_game_ids_steam_price = open('outputs/steam/{}-{}/price/written_game_ids_steam_price.txt'.
#                                         format(_locale, _country), 'r', encoding='utf-8')
#     written_game_ids_steam_price_ = written_game_ids_steam_price.readlines()
#     written_game_ids_steam_price.close()
#
#     global counter_games
#     counter_games = 0
#     counter_games += len(written_game_ids_steam_price_)
#
#     get_price_ids_steam_ = [x.replace("\n", "") for x in get_price_ids_steam_ if
#                             x.replace("\n", "") not in [a.replace("\n", "")
#                                                         for a in written_game_ids_steam_price_]]
#
#     game = Game()
#
#
#     __get_price_steam_loop(get_price_ids_steam_, game, _type, _locale, _country)  # func call
#
#     output_json_steam_price = open('outputs/steam/{}-{}/price/output_json_steam_price.txt'.
#                                    format(_locale, _country), "r", encoding='utf-8')
#     output_json_steam_price_ = output_json_steam_price.read()
#     output_json_steam_price.close()
#
#     output_json_steam_price = open('outputs/steam/{}-{}/price/output_json_steam_price.txt'.
#                                    format(_locale, _country), "w", encoding='utf-8')
#     output_json_steam_price.write('[')
#     output_json_steam_price.write(output_json_steam_price_[:-1])
#     output_json_steam_price.write(']')
#     output_json_steam_price.close()
#
#
# def __get_price_steam_loop(all_game_ids_steam_, game, _type, _locale, _country):
#     for id_ in all_game_ids_steam_:
#
#         output_json_steam_price = open('outputs/steam/{}-{}/price/output_json_steam_price.txt'.
#                                        format(_locale, _country), 'a', encoding='utf-8')
#         page_data_failed_ids_steam_price = open('outputs/steam/{}-{}/price/page_data_failed_ids_steam_price.txt'.
#                                                 format(_locale, _country), 'a', encoding='utf-8')
#         written_game_ids_steam_price = open('outputs/steam/{}-{}/price/written_game_ids_steam_price.txt'.
#                                             format(_locale, _country), 'a', encoding='utf-8')
#
#         global counter_games
#         print('Getting game : {}'.format(counter_games))
#         counter_games += 1
#
#         try:
#             game.price = __get_price_data_steam(_locale, _country, str(id_))
#             game.store = _type.steam
#             game.identifier = id_
#             game.store_url = 'https://store.steampowered.com/app/{}/'.format(id_)
#
#             output_json_steam_price.write('{},'.format((game, _type)))
#             written_game_ids_steam_price.write('{}\n'.format(id_))
#             print('\t\tOk:' + str(id_))
#         except GetPageDataFailed as err:
#             page_data_failed_ids_steam_price.write('{}\n'.format(id_))
#             print('\t\t' + err.game_id)
#         except NotGameError as err:
#             page_data_failed_ids_steam_price.write('{}\n'.format(id_))  # FIXME: not game aç
#             print('\t\t' + err.game_id)
#
#         # FIXME: except really does nothing should be configured (except not game err)
#
#         page_data_failed_ids_steam_price.close()
#         written_game_ids_steam_price.close()
#         output_json_steam_price.close()
