from config import connection 
import cogs.create.create as create


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
    
class checks:
    def check_index(one, too):
        index = 0
        for i in one:
            if list(i) == [too]:
                break
            index += 1
        return index

    def check_author(My_id, id):
        if My_id != id:
            interaction = interaction.response.send_message("Ты не автор сообщения", ephemeral = True)
            return True, interaction
        else:
            return False, False
        
    def check_ogr(My_id):
        with connection.cursor() as cursor: 
            org =( f"""
                        SELECT `organization`
                        FROM `users`
                        WHERE `user_id` = '{My_id}';
            """)
            org = cursor.execute(org)
            org = cursor.fetchone()
        if org == 'Безработный':
            interaction = interaction.response.send_message("Ты не состоишь в организации", ephemeral = True)
            return True, interaction
        else:
            return False, False
        

        
    def check_create(My_id, ctx):
        with connection.cursor() as cursor: 
            select =( f"""
                        SELECT `id`
                        FROM `users`
                        WHERE `user_id` = '{My_id}';
            """)
            select = cursor.execute(select)
            select = cursor.fetchone()

        if select == None:
            ctxx = ctx.respond("Ты еще не создал персонажа. Нажми на заветную кнопку и начни покорять этот мир!!!", view = create.createView(), ephemeral=True)
            return True, ctxx
        else:
            return False, None
    
