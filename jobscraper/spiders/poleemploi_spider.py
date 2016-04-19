# -*- coding: utf-8 -*-

"""
poleemploi_spider

A spider for Pole Emploi

:copyright: (c) 2016 by Taurus Olson <taurusolson@gmail.com>
:license: MIT

"""

import scrapy
import urlparse
from jobscraper.items import JobScraperItem


class PoleEmploiSpider(scrapy.Spider):
    name = 'pole_emploi'
    QUERY = 'python'
    start_urls = ['http://candidat.pole-emploi.fr/candidat/rechercheoffres/resultats/A_{query}_FRANCE_01___P__________INDIFFERENT_______________________'.format(query=QUERY)]
    URL = u'http://candidat.pole-emploi.fr/'


    JOBS_CSS = 'div#offrescartezone div.result-page table.definition-table'

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
        jobscraper_item['contract'] = job.css('td[itemprop=employmentType]::text').extract_first() 
        jobscraper_item['salary'] = job.css('span[itemprop=baseSalary]::text').extract_first().strip() 
        jobscraper_item['company'] = job.css('p[class=description]::text').extract_first() 
        return jobscraper_item

    def parse(self, response):
        for jobs in response.css(PoleEmploiSpider.JOBS_CSS):
            for job in jobs.css('tr[itemtype="http://schema.org/JobPosting"]'):
                url = self.get_url(job)
                request = scrapy.Request(url, self.parse_job_page)
                yield request
