from urllib.parse import urlencode

SCRAPEOPS_API_KEY = 'YOUR_API_KEY'


def get_scrapeops_url(url):
    payload = {
        'api_key': SCRAPEOPS_API_KEY,
        'url': url,
        # 'render_js': True,
        'country': 'us',
        # 'premium': True,
        # 'residential': True,
        # 'bypass': 'cloudflare_level_1',
        # 'bypass': 'cloudflare_level_2',
        'bypass': 'cloudflare_level_3',
        # 'bypass': 'generic_level_1',
        # 'bypass': 'generic_level_2',
        # 'bypass': 'generic_level_3',
        # 'bypass': 'generic_level_4',
        # 'bypass': 'incapsula',
        # 'bypass': 'perimeterx',
        # 'bypass': 'datadome',
        'keep_headers': True,
        # 'wait': 3000,
        # 'wait_for': '.loading-done',
    }

    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url
