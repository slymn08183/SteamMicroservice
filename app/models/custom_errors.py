class GetPageDataFailed(Exception):
    def __init__(self, *args):
        self.game_id = "Couldn't Get Any Data For -> ({})".format(args[0])


class PageDataIsNotJson(Exception):
    def __init__(self, *args):
        self.game_id = "Page Data Is Not Json -> ({})".format(args[0])


class GetPriceDataFailed(Exception):
    def __init__(self, *args):
        print("Couldn't Get Price Data For -> ({})".format(args[0]))


class GetVideoDataFailed(Exception):
    def __init__(self, *args):
        print("Couldn't Find Any Video For -> ({})".format(args[0]))


class GetDevelopersDataFailed(Exception):
    def __init__(self, *args):
        print("Couldn't Find Any Developer For -> ({})".format(args[0]))


class GetPublishersDataFailed(Exception):
    def __init__(self, *args):
        print("Couldn't Find Any Publisher For -> ({})".format(args[0]))


class ErrorWhileLoadingStoreUrl(Exception):
    def __init__(self, *args):
        self.game_id = "There Is No Store For -> ({})".format(args[0])


class NotGameError(Exception):
    def __init__(self, *args):
        self.game_id = "This Is Not A Game -> ({})".format(args[0])


class GetReleaseDateFailed(Exception):
    def __init__(self, *args):
        print("Release Date Not Found -> ({})".format(args[0]))


class GetPictureDataFailed(Exception):
    def __init__(self, *args):
        print("Couldn't Find Any Picture For -> ({})".format(args[0]))


class GetNameFailed(Exception):
    def __init__(self, *args):
        self.game_id = "Couldn't Get Name For -> ({})".format(args[0])


class GetGenreFailed(Exception):
    def __init__(self, *args):
        print("Couldn't Get Any Genre For -> ({})".format(args[0]))
