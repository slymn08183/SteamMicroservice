from app.bussines.steam_mini_main import get_all_game_data_steam


class GameManager:
    def __init__(self, is_update):
        get_all_game_data_steam('tr', 'TR', is_update)
