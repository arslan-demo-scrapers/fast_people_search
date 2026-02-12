import base64
import logging
import os
import re
import time
from csv import DictReader
from html import unescape
from random import choice

from nameparser import HumanName


def get_name_parts(name):
    name_parts = HumanName(name)
    punctuation_re = re.compile(r'[^\w-]')

    return {
        'full name': name.strip(),
        # 'prefix': re.sub(punctuation_re, '', name_parts.title),
        'first name': re.sub(punctuation_re, '', name_parts.first),
        # 'middle name': re.sub(punctuation_re, '', name_parts.middle),
        'last name': re.sub(punctuation_re, '', name_parts.last),
        # 'suffix': re.sub(punctuation_re, '', name_parts.suffix)
    }


def clean(text):
    if isinstance(text, (int, float)):
        return text

    text = unescape(text or '')
    for c in ['\r\n', '\n\r', u'\n', u'\r', u'\t', u'\xa0', '...']:
        text = text.replace(c, ' ')
    return re.sub(' +', ' ', text).strip()


def clean_all(seq):
    return [clean(e) for e in seq if clean(e)]


def get_phone_cols(start=1, stop=15):
    return [f"phone number {i}" for i in range(start, stop + 1)]


def log_info(message):
    logging.info(f"{message}")
    # print(message)


def retry_invalid_response(callback):
    def wrapper(spider, response):
        if response.status >= 400:
            if response.status == 404:
                log_info('Person not found.')
                return

            retry_times = response.meta.get('retry_times', 0)
            if retry_times < 3:
                time.sleep(7)
                response.meta['retry_times'] = retry_times + 1
                return response.request.replace(dont_filter=True, meta=response.meta)

            log_info("Dropped after 3 retries. url: {}".format(response.url))
            response.meta.pop('retry_times', None)

            person = response.meta['person']

            if 'addresses' in person:
                records = []
                for address in person['addresses']:
                    person.update(address)
                    records.append(person)

                # return [{**person, **address} for address in person['addresses']]
                return records
            else:
                return response.meta['person']
        return callback(spider, response)

    return wrapper


def get_base64_encoded_str(text):
    return str(base64.b64encode(text.encode("utf-8")))[2:-1]


def del_file(path):
    if os.path.exists(path):
        os.remove(path)


def get_csv_rows(file_name):
    persons = [dict(r) for r in DictReader(open(f'../input/{file_name}', encoding='utf-8')) if r]
    if not persons:
        log_info(f"{file_name} FILE EMPTY!")
    return persons


def get_actual_url(response):
    return response.url.split('url=')[-1].split('&')[0]


def update_request_user_agent(request, user_agents):
    request.headers.pop('referer', None)
    request.headers['user-agent'] = choice(user_agents)
    # request.headers['Proxy-Authorization'] = basic_auth_header('ashaka', 'yDJFhm60')


def decode_cloudflare_email(encoded_email):
    """
    # Example usage:
    encoded_email = "ef82848d808781af968e878080c18c8082"
    decoded_email = decode_cloudflare_email(encoded_email)
    Explanation
    The first two characters (ef) are used as the XOR key.
    The rest of the string is processed in pairs of hexadecimal values.
    Each byte is XORed with the key to reveal the original character.
    The final result is the decoded email.
    """
    r = int(encoded_email[:2], 16)  # Extract the first byte as the key
    decoded_email = ''.join(chr(int(encoded_email[i:i + 2], 16) ^ r) for i in range(2, len(encoded_email), 2))
    return decoded_email
