import re
from urllib.parse import urlparse, parse_qs

import usaddress
from nameparser import HumanName

from fast_people_search.fast_people_search.utils.text_utils import clean


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


def get_address_parts(address):
    if not address:
        return {}
    address1, city, state, zip_code = '', '', '', ''

    for value, key in usaddress.parse(address):
        value = value.replace(',', '') + ' '
        if key in ['OccupancyIdentifier', 'Recipient']:
            continue
        if key == 'PlaceName':
            if len(value.strip()) == 2:
                continue
            city += value
        elif key == 'StateName':
            state += value
        elif key == 'ZipCode':
            zip_code += value
        else:
            address1 += value

    address_item = {}
    address_item['street address'] = clean(address1)
    address_item['city'] = clean(city)
    address_item['state'] = state.strip().upper()
    address_item['zip code'] = zip_code.strip()
    return address_item


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
    decoded_email = ''.join(chr(int(encoded_email[i:i+2], 16) ^ r) for i in range(2, len(encoded_email), 2))
    return decoded_email
