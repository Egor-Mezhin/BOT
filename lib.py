from config import connection 



# from config import connection 
class sQl_bot:
    def check_users(user_id: int, colum: str): # Проверка на создание персонажа

        with connection.cursor() as cursor: # Проверка на создание аккаунта
            select =( f"""SELECT {colum} FROM users WHERE `user_id` = '{user_id}';""")
            select = cursor.execute(select)
            select = cursor.fetchone()
        return select