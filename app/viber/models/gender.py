class Gender:
    values = {"male": "Чоловік", "female": "Жінка", None: "Не вказано", "": "Не вказано", "0": "Не вказано"}
    values_reversed = {"Чоловік": "male", "Жінка": "female", "Не хочу вказувати": None}

    @staticmethod
    def _get_value(data: dict, key: str) -> str:
        value = data.get(key)

        if value is None and key not in data:
            raise ValueError(f"{key} is not a valid")

        return value

    @staticmethod
    def get_label(key: str):
        return Gender._get_value(Gender.values, key)

    @staticmethod
    def get_key(key: str):
        return Gender._get_value(Gender.values_reversed, key)
