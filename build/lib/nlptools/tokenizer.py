from systemtools.basics import *
from nltk.tokenize import word_tokenize


def tokenize(obj):
    if obj is None:
        return None
    elif isinstance(obj, str):
        return word_tokenize(obj)
    elif isinstance(obj, list):
        return [tokenize(i) for i in obj]
    else:
        return obj # Or throw an exception, or parse a dict, a set...



if __name__ == "__main__":
    data = \
    [
        "jhg bfdguyjgfd fd gjd",
        [
            [
                ["ugtuyf", "vuhgvds"],
                None
            ],
            [
                [None],
                ["a", "b bdsf! id"]
            ],
        ],
        [
            [
                "jhsdg fjhdsg fgvsdk fksd ", None
            ],
            [
                "jhgsv defhgv sdufg uksdf jsd"
            ],
            "hjubvkujhv refgh. bvuljg ug udsfg li d. isdgf v . usdgf? sdvf ?"
        ],
    ]

    data = [["Lorem ipsum dolor. Sit amet?", "Hello World!", None], ["a"], "Hi!", None, ""]
    print(tokenize(data))