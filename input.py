import json

from geometry import Circle


# TODO сделать структуру для хранения Circle и оптимизировать для поиска ближайщих пересеченных соседей \
#  и конечно переделать саму функцию поиска
# TODO тесты производительности

class InputBuilderFromJson:
    @staticmethod
    def build(_json: str):
        parsed_json = json.loads(_json)
        circles = []
        for circle in parsed_json["circles"]:
            circles.append(Circle(circle["X"], circle["Y"], circle["R"]))
        return parsed_json["name"], circles, parsed_json["dt"], parsed_json["Fmax"]
