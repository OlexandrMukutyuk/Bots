from app.tgbot.keyboards.default.consts import DefaultConstructor

hello_text = "Привіт! 👋"
yes_text = "Так ✅"
no_text = "Ні ❌"
other_mail_text = "Інша пошта 🔁"
start_again_text = "Почати спочатку 🔁"

auth_types = {
    'subscription': "Підписка",
    'advanced': "Розширена",
}

hello_kb = DefaultConstructor.create_kb(
    actions=[hello_text],
    schema=[1]
)

auth_types_kb = DefaultConstructor.create_kb(
    actions=[auth_types['subscription'], auth_types['advanced']],
    schema=[2]
)

is_register_on_site = DefaultConstructor.create_kb(
    actions=[yes_text, no_text, other_mail_text],
    schema=[2, 1]
)

start_again_kb = DefaultConstructor.create_kb(
    actions=[start_again_text],
    schema=[1]
)
