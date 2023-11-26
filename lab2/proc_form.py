import cgi

print("Content-type: text/html\n")

form = cgi.FieldStorage()

brand = form.getvalue("brand")
model = form.getvalue("model")
body_types = form.getlist("body_type")
year = form.getvalue("year")
engine_type = form.getvalue("engine_type")

print("<html>")
print("<head><title>Результат обробки форми</title></head>")
print("<body>")
print("<h2>Результат обробки форми:</h2>")
print("<p>Марка: {}</p>".format(brand))
print("<p>Модель: {}</p>".format(model))
print("<p>Тип кузова: {}</p>".format(", ".join(body_types)))
print("<p>Рік випуску: {}</p>".format(year))
print("<p>Тип двигуна: {}</p>".format(engine_type))
print("</body>")
print("</html>")
