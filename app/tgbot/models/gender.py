class Gender:
    values = {"male": "Чоловік", "female": "Жінка", None: "Не вказано"}
    values_reversed = {value: key for key, value in values.items()}

    @staticmethod
    def get_value(data: dict, key: str) -> str:
        value = data.get(key)

        if value is None:
            raise ValueError(f"{key} is not a valid")

        return value

    @staticmethod
    def get_label(key: str):
        return Gender.get_value(Gender.values, key)

    @staticmethod
    def get_key(key: str):
        return Gender.get_value(Gender.values_reversed, key)
