STOP_MESSAGE = 'Работа приложения остановлена.'
HELP_MESSAGE = '''
Добро пожаловать!
Узнайте на каких позициях находится ваш товар в поиске Wildberries,
отправив запрос с указанием артикула и запросом.
'''
START_MESSAGE = '''
Привет! Чтобы воспользоваться ботом, нужно подписаться на наш
<a href="https://t.me/mpexperts">telegram канал</a>.
'''
PRODUCT_POSITION_MESSAGE = '{city} - Место: {position} (стр. {page})\n'
PRODUCT_POSITION_SCHEDULE_MESSAGE = (
    '{city} - Место: {position}/{prev_position} '
    '({position_arrow} {position_difference}) (стр. {page}/{prev_page} '
    '({page_arrow} {page_difference}))'
)
PRODUCT_POSITION_NOT_FOUND_MESSAGE = '{city} - нет на первых 60 страниц\n'
