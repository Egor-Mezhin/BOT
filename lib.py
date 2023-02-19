from config import connection 



# from config import connection 
class sQl_bot:
    def check_users(user_id, colum): # Проверка на создание персонажа

        with connection.cursor() as cursor: # Проверка на создание аккаунта
            select =( f"""SELECT {colum} FROM users WHERE `user_id` = '{user_id}';""")
            select = cursor.execute(select)
            select = cursor.fetchone()
        return select
    

def check_index(one, too):
    index = 0
    for i in one:
        if list(i) == [too]:
            break
        index += 1
    return index