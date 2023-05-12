from config import connection 



# from config import connection 
class sQl_bot:
    def check_table(user_id, table, colum):

        with connection.cursor() as cursor: 
            select =( f"""
                        SELECT {colum} 
                        FROM {table}
                        WHERE `user_id` = '{user_id}';
            """)
            select = cursor.execute(select)
            select = cursor.fetchone()
        return select
    
    def update_table(user_id, table, SET): 

        with connection.cursor() as cursor: 
            select = ( f"""
                        UPDATE {table} 
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