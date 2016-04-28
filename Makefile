#
# Makefile
# Taurus Olson, 2016-04-19 02:11
#

create_db:
	@cd jobscraper && scrapy crawl pole_emploi
	@echo 'Created the database'

remove_db:
	@rm -r data/jobs.db
	@echo 'Removed the database.'

# vim:ft=make
