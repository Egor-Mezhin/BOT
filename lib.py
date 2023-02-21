from config import connection 



# from config import connection 
class sQl_bot:
    def check_users(user_id, colum):

        with connection.cursor() as cursor: 
            select =( f"""
                        SELECT {colum} 
                        FROM users 
                        WHERE `user_id` = '{user_id}';
            """)
            select = cursor.execute(select)
            select = cursor.fetchone()
        return select
    
    def update_users(user_id, SET): 

        with connection.cursor() as cursor: 
            select = ( f"""
                        UPDATE users 
                        SET {SET} 
                        WHERE `user_id` = {user_id};""")
            cursor.execute(select)
            connection.commit()
    

def check_index(one, too):
    index = 0
    for i in one:
        if list(i) == [too]:
            break
        index += 1
    return index