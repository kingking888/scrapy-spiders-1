SHELL = /bin/bash

.PHONY: help repo-init bootstrap tests update crawl crawl-equity crawl-reddit crawl-twitter crawl-reddit-comments crawl-audio crawl-google-trends crawl-companies-data swarm-init swarm-leave start-selenium build check
.DEFAULT_GOAL = help

VERSION := $(shell poetry run python -c "from importlib.metadata import version; print(version('agblox'))")

help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

repo-init:  ## Install pre-commit in repo
	pre-commit install

bootstrap:  ## Cold start
	poetry install --extras "dev"

tests:  ## Run tests.
	poetry run pytest

update:  bootstrap  ## Update spiders
	git pull

crawl:  ## Run spiders
	cd src && scrapy crawl accesswire.com
	cd src && scrapy crawl ag.purdue.edu
	cd src && scrapy crawl agfax.com
	cd src && scrapy crawl arstechnica.com
	cd src && scrapy crawl businesswire.com
	cd src && scrapy crawl bgr.com
	cd src && scrapy crawl cnet.com
	cd src && scrapy crawl soybeansandcorn.com
	cd src && scrapy crawl texascorn.org
#	https://github.com/agblox/scrapy-spiders/issues/113
#	cd src && scrapy crawl agupdate.com
	cd src && scrapy crawl cropwatch.unl.edu
	cd src && scrapy crawl moneycontrol.com
	# cd src && scrapy crawl growerspoint.com
	cd src && scrapy crawl thecropsite.com
	cd src && scrapy crawl kycorn.org
	cd src && scrapy crawl iowacorn.org
	cd src && scrapy crawl ilcorn.org
	cd src && scrapy crawl fieldcropnews.com
	cd src && scrapy crawl forkast.news
	cd src && scrapy crawl gizmodo.com
	cd src && scrapy crawl agriculturecom_cattle
	cd src && scrapy crawl agriculturecom_corn
	# cd src && scrapy crawl agriculturecom_crop_markets
	cd src && scrapy crawl agriculturecom_soy
	cd src && scrapy crawl agriculturecom_wheat
	cd src && scrapy crawl farmdocdaily
	# cd src && scrapy crawl babypips.com
	# cd src && scrapy crawl beefmagazine.com
	cd src && scrapy crawl canadiancattleman.ca
	cd src && scrapy crawl drovers.com
	cd src && scrapy crawl prnewswire.com
	# cd src && scrapy crawl foodbusinessnews.net
	# cd src && scrapy crawl extension.psu.edu
	cd src && scrapy crawl soygrowers.com
	cd src && scrapy crawl thebeefread.com
	cd src && scrapy crawl ussec.org
	# cd src && scrapy crawl world-grain.com
	# cd src && scrapy crawl reuters.com
	# cd src && scrapy crawl stocknews.com
	cd src && scrapy crawl tradingchartscorn
	cd src && scrapy crawl tradingchartssoy
	cd src && scrapy crawl tradingchartswheat
	cd src && scrapy crawl investopedia-company_news
	cd src && scrapy crawl fxstreet.com
	# cd src && scrapy crawl dailyfx
	# cd src && scrapy crawl investing.com
	cd src && scrapy crawl investors.fiskerinc.com
	cd src && scrapy crawl forexnews.world
	cd src && scrapy crawl fxempire.com
	cd src && scrapy crawl investorplace.com
	cd src && scrapy crawl insideevs.com
	cd src && scrapy crawl investors.waitr.com
	# cd src && scrapy crawl yahoo-finance
	cd src && scrapy crawl stocktwits.com
	cd src && scrapy crawl stockrover.com
	cd src && scrapy crawl via.news
	cd src && scrapy crawl tradersinsight.news
	cd src && scrapy crawl zerohedge.com
	make start-selenium && cd src && scrapy crawl morningstar.com
	cd src && scrapy crawl prnewswire.com

crawl-equity: ## Run equity spiders and twitter only
	cd src && scrapy crawl marketwatch
	cd src && scrapy crawl benzinga.com
	cd src && scrapy crawl theglobeandmail
	cd src && scrapy crawl zacks
	cd src && scrapy crawl cnbc
	cd src && scrapy crawl smarteranalyst
	make start-selenium && cd src && scrapy crawl ca.finance.yahoo.com
	make start-selenium && cd src && scrapy crawl gurufocus.com
	cd src && scrapy crawl fool
	cd src && scrapy crawl nasdaq

crawl-reddit:
	## Run reddit per-user spider
	cd src && scrapy crawl reddit.com
	## Run reddit per-ticker search spider
	cd src && scrapy crawl reddit.stocks.search
	## Collects comments for reddit posts after
	cd src && scrapy crawl reddit_comments

crawl-twitter:
	## Run twitter per-user spider
	cd src && scrapy crawl twitter
	## Run twitter per-ticker search spider
	cd src && scrapy crawl twitter_search

crawl-reddit-comments:
	cd src && scrapy crawl reddit_comments

crawl-audio:
	cd src && scrapy crawl podbean.com

crawl-google-trends: ## Run Google Trends spider only
	make start-selenium && cd src && scrapy crawl trends.google.com

crawl-companies-data: ## Spiders responsible for obtaining data for companies Model, ML
	cd src && scrapy crawl zacks_sp500

swarm-init:  ## create docker swarm
	sudo docker swarm init

swarm-leave:  ## stop container
	sudo docker swarm leave --force

start-selenium:  ## Start selenium standalone
	sudo docker stack deploy --compose-file docker-compose.yml selenium

build: ## build docker image
	DOCKER_BUILDKIT=1 COMPOSE_DOCKER_CLI_BUILD=1 VERSION=${VERSION} \
      docker build . --progress=plain \
      -t ${ECR_REGISTRY}/${ECR_REPO}:latest -t ${ECR_REGISTRY}/${ECR_REPO}:${VERSION} \
      --build-arg VERSION=${VERSION}

check:  ## Run pre-commit against all files
	pre-commit run --all-files
