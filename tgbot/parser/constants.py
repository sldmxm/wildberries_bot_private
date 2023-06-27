TOTAL_PRODUCTS_LINK = (
        'https://search.wb.ru/exactmatch/ru/common/v4/search?'
        'dest=-{destination}&'
        'query={query}&'
        'resultset=filters'
)
PAGE_PARSING_LINK = (
        'https://search.wb.ru/exactmatch/ru/common/v4/search?'
        'dest=-{destination}&'
        'page={page}&'
        'query={query}&'
        'resultset=catalog'
)
ACCEPTANCE_LINK = 'https://wbcon.ru/wp-admin/admin-ajax.php?action=get_limit_store&id={index}'  # noqa
PACKAGE = {
    'mono_pallet': 'Монопаллет',
    'super_safe': 'Суперсейф',
    'koroba': 'Короб',
}
ACCEPTANCE_HEADERS = {
    'Cookie': 'beget=begetok'
}
