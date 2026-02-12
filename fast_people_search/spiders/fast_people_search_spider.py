import json
import re
from copy import deepcopy

from scrapy import Request, Spider
from scrapy.crawler import CrawlerProcess

from fast_people_search.fast_people_search.utils import *
from fast_people_search.fast_people_search.static_fields import *
from fast_people_search.fast_people_search.services.proxy_service import get_scrapeops_url


class FastPeopleSearchSpider(Spider):
    name = 'fast_people_search_spider'
    base_url = 'https://www.fastpeoplesearch.com'
    person_url_t = 'https://www.fastpeoplesearch.com/people/{name}_{address}'
    address_t = '{streetAddress}, {addressLocality}, {addressRegion}, {postalCode}'
    input_persons_filepath = 'PERSONS.csv'

    csv_headers = [
        "name", "full name", "aka", "sur names", "age", "owners", "emails",
        "full address", "street address", "city", "state", "zip code", *get_phone_cols(),
    ]

    feeds = {
        'scraped_person_results.json': {
            'format': 'json',
            'encoding': 'utf8',
            'store_empty': False,
            'fields': csv_headers,
            'overwrite': True,
            'indent': 4,
        }
    }

    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 2,
        'FEEDS': feeds,
    }

    headers = {
        'authority': 'www.fastpeoplesearch.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }

    handle_httpstatus_list = [
        400, 401, 402, 403, 404, 405, 406, 407, 409, 412,
        500, 501, 502, 503, 504, 505, 506, 507, 509,
    ]

    req_meta = {
        'handle_httpstatus_list': handle_httpstatus_list
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start(self):
        for person in get_csv_rows(self.input_persons_filepath)[:1]:
            if not person or not clean(person['NAME']):
                continue
            name = re.sub(punctuation_re, '', person['NAME'] or '').strip().replace(' ', '-')
            address = re.sub(punctuation_re, '', person['ADDRESS'] or '').strip().replace(' ', '-')

            url = self.person_url_t.format(name=name, address=address).lower()
            person['name'] = person.pop('NAME').strip()

            meta = deepcopy(req_meta)
            meta['person'] = person
            yield Request(self.get_proxy_url(url), meta=meta, dont_filter=True, headers=self.headers)

    @retry_invalid_response
    def parse(self, response):
        """
        We could not find any results based on your search criteria:
        """
        peoples_age = [e for e in response.css('div :contains("Age:")::text').getall()
                       if clean(e) and clean(e).isdigit()]

        data = response.css('[type="application/ld+json"]::text').getall()
        if not data:
            log_info(f"No results found for: {get_actual_url(response)}")
            return

        try:
            records = json.loads(data[2])
        except Exception as IndexError:
            records = json.loads([rec for rec in data if 'HomeLocation' in rec][0])

        for i, person in enumerate(records):
            item = deepcopy(response.meta['person'])
            item['emails'] = ''
            item['phone number 1'] = ''
            item['phone number 2'] = ''
            item['full name'] = person['name']
            item['age'] = peoples_age[i] if peoples_age[i:] else ''
            item['aka'] = ', '.join(person.get('additionalName') or [])
            item['sur names'] = self.get_sur_names(item['name'], person)

            if not person.get('telephone'):
                log_info(f"Phone number not found -> {item}")
                continue
            item.update(self.get_phones_numbers(person['telephone'] or []))

            item['addresses'] = self.get_addresses(person)
            item.update(item['addresses'][0])

            # if self.filter_person.is_inserted_in_master(item):
            #     continue
            meta = deepcopy(req_meta)
            meta['person'] = item
            yield response.follow(url=self.get_proxy_url(person['url']), callback=self.parse_person,
                                  meta=meta, dont_filter=True, headers=self.headers)

    @retry_invalid_response
    def parse_person(self, response):
        person = response.meta['person']
        person['age'] = self.get_age(response) or ''
        person['emails'] = self.get_emails(response) or ''

        if not person['aka']:
            person['aka'] = self.get_aka_from_details_page(response)

        for address in person.pop('addresses', []):
            person.update(address)
            yield person

    def get_proxy_url(self, url):
        return get_scrapeops_url(url)

    def get_phones_numbers(self, phone_numbers):
        phones = {}
        for i, p in enumerate(phone_numbers[:15], start=1):
            if not p:
                continue
            phones[f'phone number {i}'] = p
        return phones

    def get_addresses(self, person):
        addresses = []

        for addr in person['HomeLocation'] or []:
            a = addr['address'] or {}

            addr_parts = [a.get('streetAddress'), a.get('addressLocality'),
                          a.get('addressRegion'), a.get('postalCode')]

            item = {}
            item['full address'] = ', '.join(e for e in addr_parts if e)
            item['street address'] = a.get('streetAddress') or ''
            item['city'] = a.get('addressLocality') or ''
            item['state'] = a.get('addressRegion') or ''
            item['zip code'] = a.get('postalCode') or ''
            item['city, state'] = f'{item["city"]}, {item["state"]}'

            addresses.append(item)

        return addresses

    def get_age(self, response):
        return response.css('#age-header::text').re_first(r'\d+')

    def get_emails(self, response):
        emails = response.css('.detail-box-email h3:contains("@")::text').getall()
        return ', '.join(e for e in emails if clean(e)) or self.get_decoded_emails(response)

    def get_decoded_emails(self, response):
        return ', '.join(decode_cloudflare_email(ef) for ef in
                         response.css('.detail-box-email ::attr(data-cfemail)').getall())

    def get_sur_names(self, search_name, person):
        surnames = {get_name_parts(n)['last name'] for n in person.get('additionalName') or []}
        surnames.add(get_name_parts(search_name)['last name'])
        surnames.add(get_name_parts(person['name'])['last name'])
        return ', '.join(sn for sn in surnames if clean(sn))

    def get_aka_from_details_page(self, response):
        css = '#aka-links .detail-box-content h3::text'
        return ', '.join(clean(e) for e in response.css(css).getall() if clean(e))


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(FastPeopleSearchSpider)
    process.start()
