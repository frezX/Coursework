from src.env import app_env

CONFIG: dict = {
    'web/static/js/admin_panel.js': {
        'data': {
            'ws_url': app_env.websockets_url,
            'token': True
        },
        'content_type': 'application/javascript'
    },
    'web/static/js/logger.js': {
        'data': {
            'ws_url': app_env.websockets_url,
            'token': True
        },
        'content_type': 'application/javascript'
    },
    # 'web/static/css/forms.css': {
    #     'data': {
    #         'url': app_env.url
    #     },
    #     'content_type': 'text/css'
    # }
}
