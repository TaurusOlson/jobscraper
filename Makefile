#
# Makefile
# Taurus Olson, 2016-04-19 02:11
#

create_db:
	@cd jobscraper && scrapy crawl pole_emploi
	@echo 'Created the database'

clean_db:
	@rm -r data/*.db
	@echo 'Removed all databases.'

# vim:ft=make
