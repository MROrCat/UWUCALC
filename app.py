import math
from flask import Flask, render_template, request

app = Flask(__name__)


def calculate_fractions(n1, d1, n2, d2, op):
    """Выполняет вычисления и возвращает (res_n, res_d, error_message)"""
    # Проверка на заполненность полей
    if None in (n1, d1, n2, d2):
        return None, None, "Заполни все квадратики!"

    # Проверка деления на ноль в исходных данных
    if d1 == 0 or d2 == 0:
        return None, None, "В знаменателе не может быть 0!"

    # Вычисление в зависимости от операции
    if op == "+":
        res_n = n1 * d2 + n2 * d1
        res_d = d1 * d2
    elif op == "-":
        res_n = n1 * d2 - n2 * d1
        res_d = d1 * d2
    elif op == "x":
        res_n = n1 * n2
        res_d = d1 * d2
    elif op == "/":
        res_n = n1 * d2
        res_d = d1 * n2
    else:
        return None, None, "Неверная операция!"

    # Проверка деления на ноль в результате
    if res_d == 0:
        return None, None, "Ошибка: деление на ноль!"

    # Сокращение дроби (НОД)
    common = math.gcd(res_n, res_d)

    # В Python math.gcd возвращает всегда положительное число.
    # Если знаменатель получился отрицательным, переносим минус наверх.
    final_n = int(res_n / common)
    final_d = int(res_d / common)
    if final_d < 0:
        final_n = -final_n
        final_d = -final_d

    return final_n, final_d, None


@app.route("/", methods=["GET", "POST"])
def index():
    # Значения по умолчанию для первой загрузки страницы
    context = {
        "n1": "",
        "d1": "",
        "n2": "",
        "d2": "",
        "op": "+",
        "res_n": "",
        "res_d": "",
        "error": None,
    }

    if request.method == "POST":
        # Получаем данные из HTML-формы
        try:
            n1 = (
                int(request.form.get("n1")) if request.form.get("n1") else None
            )
            d1 = (
                int(request.form.get("d1")) if request.form.get("d1") else None
            )
            n2 = (
                int(request.form.get("n2")) if request.form.get("n2") else None
            )
            d2 = (
                int(request.form.get("d2")) if request.form.get("d2") else None
            )
        except ValueError:
            context["error"] = "Вводи только целые числа!"
            return render_template("index.html", **context)

        op = request.form.get("op", "+")

        # Сохраняем введенные пользователем данные, чтобы они не стирались
        context.update({"n1": n1, "d1": d1, "n2": n2, "d2": d2, "op": op})

        # Считаем
        res_n, res_d, error = calculate_fractions(n1, d1, n2, d2, op)

        if error:
            context["error"] = error
        else:
            context["res_n"] = res_n
            context["res_d"] = res_d

    return render_template("index.html", **context)


if __name__ == "__main__":
    app.run(debug=True)
