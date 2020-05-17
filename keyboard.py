import json


def getKeyboard():
    keyboard = {
        "one_time": False,
        "buttons": [
            [{
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"1\"}",
                    "label": "Добавить получателя"
                },
                "color": "negative"
            },
                {
                    "action": {
                        "type": "text",
                        "payload": "{\"button\": \"1\"}",
                        "label": "Удалить получателя"
                    },
                    "color": "negative"
                },
                {
                    "action": {
                        "type": "text",
                        "payload": "{\"button\": \"1\"}",
                        "label": "Мой id"
                    },
                    "color": "negative"
                },
            ]
        ]
    }

    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    return str(keyboard.decode('utf-8'))