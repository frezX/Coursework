class ValueFromCookies:
    ...


class ValueFromHeaders:
    ...


CONFIG: dict = {
    'web/static/css/index.css': {
        'data': {
            'role': ValueFromCookies
        },
        'content_type': 'text/css'
    }
}
