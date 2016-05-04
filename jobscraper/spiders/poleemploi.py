# -*- coding: utf-8 -*-

"""
poleemploi

A spider for Pole Emploi

:copyright: (c) 2016 by Taurus Olson <taurusolson@gmail.com>
:license: MIT

"""

import scrapy
import urlparse
from jobscraper.items import JobScraperItem


class PoleEmploiSpider(scrapy.Spider):
    name = 'pole_emploi'
    URL = u'http://candidat.pole-emploi.fr/'
    JOBS_CSS = 'div#offrescartezone div.result-page table.definition-table'

    def __init__(self, keyword=''):
        if not keyword:
            keyword = 'python'

        self.start_urls = ['http://candidat.pole-emploi.fr/candidat/rechercheoffres/resultats/A_{keyword}_FRANCE_01___P__________INDIFFERENT_______________________'.format(keyword=keyword)]

    def get_url(self, selector):
        url = selector.css('a::attr(href)').extract_first()
        if url.find('http') == 0:
            return url
        parsed_uri = urlparse.urlparse(PoleEmploiSpider.URL)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        return "{domain}/{found_url}".format(domain=domain, found_url=url)

    def get_address(self, selector):
        """Return the zip_code and the city

        * 31 - TOULOUSE will give zip_code, city = ('31', 'TOULOUSE')
        * 69 - Rhone will give zip_code, city = ('69', 'Rhone')
        * Ile de France will give zip_code, city = ('', 'Ile de France')
        
        """
        address = selector.css('li[itemprop=addressRegion]::text').extract_first() 
        if len(address.split('-')) >= 2:
            zip_code = address.split('-')[0].strip()
            city = address.split('-')[1:]
            city = '-'.join(x.strip().capitalize() for x in city)
        else:
            zip_code, city = None, address.strip().capitalize()
        return zip_code, city

    def parse_job_page(self, job):
        jobscraper_item = JobScraperItem()
        jobscraper_item['title'] = job.css('h4[itemprop=title]::text').extract_first()
        jobscraper_item['url'] = job.url 
        jobscraper_item['desc'] = job.css('#offre-body p[itemprop=description]::text').extract_first() 
        zip_code, city = self.get_address(job)
        jobscraper_item['zip_code'] = zip_code
        jobscraper_item['city'] = city
        jobscraper_item['publication_date'] = job.css('span[itemprop=datePosted]::text').extract_first() 
        jobscraper_item['contract'] = job.css('span[itemprop=employmentType]::text').extract_first() 
        jobscraper_item['salary'] = job.css('span[itemprop=baseSalary]::text').extract_first().strip() 
        jobscraper_item['company'] = job.css('p[class=description]::text').extract_first() 
        return jobscraper_item

    def parse(self, response):
        # Set the maximum number of job offers per page to 100
        form_request = scrapy.FormRequest.from_response(response,
                formxpath="//form[@id='ajouterAuClasseur']",
                formdata={'nombreLignesMax': '100'},
                callback=self.after_select_max_jobs)
        yield form_request

    def after_select_max_jobs(self, response):
        for jobs in response.css(PoleEmploiSpider.JOBS_CSS):
            for job in jobs.css('tr[itemtype="http://schema.org/JobPosting"]'):
                url = self.get_url(job)
                request = scrapy.Request(url, self.parse_job_page)
                yield request



