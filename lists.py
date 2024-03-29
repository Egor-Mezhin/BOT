import discord
bot = discord.Bot()

resources = { # Список всех ресурсов
    'gems': "<:gems:990318941819768892>",
    'iron': "<:iron:987380754810040370>",
    'wood': "<:wood1:987380748807966751>",
    'organic': "<:organic:987380756445794354>",
    'details': "<:details:987380753266520194>",
    'batteries': "<:batteries:987380746589208676>",
    'shards': "<:shards:987380760212291644>"
} 

Ogr_info = {
    'Безработный': None,
    'Шахта': {
                "Должность" : {
                    "Шахтер": 100,
                    "Старший шахтер": 200,
                    "Прораб": 300,
                    "Руководитель шахтерской отрасли": 400,
                    "Директор рудников (Железные горы)": None,
                },

                "Инструменты": {
                    "Старая кирка": {
                        "Стоймость": 500, 
                        "Буст": 1.5, 
                        "Прочность": 10},

                    "Улучшенная кирка": {
                        "Стоймость": 1500, 
                        "Буст": 2, 
                        "Прочность": 15},
                }
    },
    'Лесопилка': {
                "Должность" : {
                    "Топоруб": 100,
                    "Дровосек": 200,
                    "Смотрящий лесопилки": 300,
                    "Руководитель Лесоповалом": 500,
                    "Древесный магнат": None,
                },

                "Инструменты": {
                    "Старый топор": {
                        "Стоймость": 500, 
                        "Буст": 1.5, 
                        "Прочность": 10},
                        
                    "Улучшенный топор": {
                        "Стоймость": 1500, 
                        "Буст": 2, 
                        "Прочность": 15},
                }
    },    
    'Органический сад': {
                "Должность" : {
                    "Поливатель": 100,
                    "Фермер": 200,
                    "Считающий растительность": 300,
                    "Следящий за фермой": 500,
                    "Хозяин долины": None,
                },

                "Инструменты": {
                    "Старая лейка": {
                        "Стоймость": 500, 
                        "Буст": 1.5, 
                        "Прочность": 10},

                    "Улучшенная лейка": {
                        "Стоймость": 1500, 
                        "Буст": 2, 
                        "Прочность": 15},
                }
    },
    'Завод': {
                "Должность" : {
                    "Жестянщик": 100,
                    "Слесарь": 200,
                    "Мастер кузнецов": 300,
                    "Начальник цеха": 500,
                    "Распорядитель завода": None,
                },

                "Инструменты": {
                    "Старая кувалда": {
                        "Стоймость": 500, 
                        "Буст": 1.5, 
                        "Прочность": 10},

                    "Улучшенная кувалда": {
                        "Стоймость": 1500, 
                        "Буст": 2, 
                        "Прочность": 15},
                }
    },  
    'Электростанция': {
                "Должность" : {
                    "Изготовитель батарей": 100,
                    "Оператор станции": 200,
                    "Инженер": 300,
                    "Управляющий Энерго станцией": 500,
                    "Председатель электростанции": None,
                },

                "Инструменты": {
                    "Старые перчатки": {
                        "Стоймость": 500, 
                        "Буст": 1.5, 
                        "Прочность": 10},

                    "Улучшенные перчатки": {
                        "Стоймость": 1500, 
                        "Буст": 2, 
                        "Прочность": 15},
                }
    },
    'Лаборатрия 903': {
                "Должность" : {
                    "Стажер": 100,
                    "Ученый": 200,
                    "Сотрудник отдела 901-А": 300,
                    "Директор Лаборатории": 500,
                    "Объект A901JT": None,
                },

                "Инструменты": {
                    "Старый картонный планшет": {
                        "Стоймость": 500, 
                        "Буст": 1.5, 
                        "Прочность": 10},

                    "Улучшенный картонный планшет": {
                        "Стоймость": 1500, 
                        "Буст": 2, 
                        "Прочность": 15},
                }
    },          
}

