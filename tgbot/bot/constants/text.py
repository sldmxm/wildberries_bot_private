START_MESSAGE = '''
Привет! Чтобы воспользоваться ботом, нужно подписаться на наш
<a href="https://t.me/mpexperts">telegram канал</a>.
'''
STOP_MESSAGE = 'Работа приложения остановлена.'
CANCEL_MESSAGE = 'Действие отменено'
HELP_MESSAGE = '''
Добро пожаловать!
Узнайте на каких позициях находится ваш товар в поиске Wildberries,
отправив запрос с указанием артикула и запросом.
'''
PARSING_START_MESSAGE = (
    'Для определения позиции артикула отправьте сообщение '
    'в формате "Артикул Поисковая фраза"\n\n'
    'Например:\n'
    '36704403 футболка женская'
)
PARSING_WAIT_MESSAGE = '''
Запрос создан! В ближайшие время вам будет отправлен результат.
'''
MEMBER_STATUSES = ('administrator', 'member', 'creator',)
PARSER_MESSAGE = '''
Результат:

Артикул: {article}
Запрос: {query}

{result}
'''
PRODUCT_POSITION_MESSAGE = '{city} - Место: {position} (стр. {page})\n'
PRODUCT_POSITION_SCHEDULE_MESSAGE = (
    '{city} - Место: {position}/{prev_position} '
    '({position_arrow} {position_difference}) (стр. {page}/{prev_page} '
    '({page_arrow} {page_difference}))'
)
PRODUCT_POSITION_NOT_FOUND_MESSAGE = '{city} - нет на первых 60 страниц\n'
RESIDUE_PARSER_START_MESSAGE = '''
Отправьте артикул для вывода остатков:

Например:
36704403
'''
ACCEPTANCE_RATE_START_MESSAGE = '''
Выберите склад:

Например:

'''
SUBSCRIPTIONS_MESSAGE = '''
Ваши подписки:

{results}
'''
SUBSCRIBE_MESSAGE = 'Вы подписались'
UNSUBSCRIBE_MESSAGE = 'Вы отписались'
NO_SUBSCRIPTIONS_MESSAGE = 'У вас нет подписок'
