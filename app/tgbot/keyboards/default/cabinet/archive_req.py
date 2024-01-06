from keyboards.default.consts import DefaultConstructor

later_text = "Пізніше"

rate_request_kb = DefaultConstructor.create_kb(
    actions=['⭐', '⭐⭐', '⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐', later_text],
    schema=[2, 2, 2]
)
