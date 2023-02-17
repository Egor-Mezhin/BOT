import pymysql

try:
    connection = pymysql.connect(
        host = "127.0.0.1",
        port = 3306,
        user = "root",
        password = "123890321098qaz",
        database = "discord",
        cursorclass = pymysql.cursors.DictCursor
    )
    print("БД подключена")
    print("#" * 20)
except Exception as ex:
    print('Неполучилось подключить бд...')
    print(ex)