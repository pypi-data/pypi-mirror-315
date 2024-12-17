from abc import ABC, abstractmethod
import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from rusta_crawler.spiders.rusta_spider import NewEcomSpider
from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings as settings
# from rusta_crawler.spiders.rusta_spider import settings as settings
# from scrapy.settings import Settings
from scrapy.spiders import Spider
import argparse



# Step 1: Define the Spider interface
class Spider(ABC):
    @abstractmethod
    def create(self):
        pass

# Step 2: Create concrete classes
class NewSiteSpider(Spider):
    def create(self, *args, **kwargs) -> NewEcomSpider:
        return NewEcomSpider
    
# Step 3: Define the SpiderFactory class
class SpiderFactory(ABC):
    @abstractmethod
    def create_spider(self,  *args, **kwargs) -> Spider:
        pass

# Step 4: Implement concrete factories
class NewEcomSpiderFactory(SpiderFactory):

    def create_spider(self, *args, **kwargs) -> Spider:
        return NewSiteSpider()


# Client code
def create_spider(factory: SpiderFactory, *args, **kwargs) -> None:
    from scrapy.utils.project import get_project_settings as settings
    from scrapy.settings import Settings
    crawler_settings = Settings()
    crawler_settings.set("REQUEST_FINGERPRINTER_IMPLEMENTATION", "2.7")
    spider_factory = factory.create_spider(*args, **kwargs)
    sp = spider_factory.create()
    # process = CrawlerProcess(settings=crawler_settings)

    process = CrawlerProcess(settings=crawler_settings)
    crawler = process.create_crawler(sp)
    
    if kwargs.get('ctr'):
        ctr = kwargs.get('ctr')
        for c in ctr:
            kwargs['ctr'] = c
            process.crawl(sp, **kwargs)
    else:
        spider = process.crawl(crawler , sp, **kwargs)
        print(spider)
        
    process.start()
    # stats_obj = crawler.stats
    stats_dict = crawler.stats.get_stats()
    if stats_dict.get('log_count/ERROR'):
        result = "Failed"
    elif stats_dict.get('downloader/response_status_count/200') and stats_dict.get('httpcompression/response_count'):
        status_count = stats_dict.get('downloader/response_status_count/200')
        response_count = stats_dict.get('httpcompression/response_count')
        result = "Success" if status_count == response_count else "Failed"
    return result

def run_new_ecom_site_spider(scrape_type, ctr=None, debug=None):
    
    if ctr:
        ctr = [c.upper() for c in ctr]
    kwargs = { "ctr": ctr, "scrape": scrape_type, "debug": debug, "ITEM_PIPELINES": {"rusta_crawler.pipelines.RustaCrawlerPipeline": 300}}
    new_site_factory = NewEcomSpiderFactory()  
    return create_spider(new_site_factory, **kwargs)

def list_of_strings(arg):
    return arg.split(',')
 
def main(args):
   
    import logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    result = None
    if args.scrape in ['week', 'rolling']:
        logger.info(f"SPIDER FACTORY - Running spider for {args.scrape}")
        result = run_new_ecom_site_spider(scrape_type=args.scrape)
    elif args.scrape == 'active' and args.ctr:
        for ctr in args.ctr:
            if ctr.upper() not in ['SE', 'NO', 'FI', 'DE']:
                parser.error(f"Invalid country code: {ctr}")
        logger.info(f"SPIDER FACTORY - Running spider for {ctr}")
        result = run_new_ecom_site_spider(ctr=args.ctr, scrape_type=args.scrape, debug=args.debug)
    else:
        parser.error("Please provide required arguments")
    print(result)
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Scrapy spiders with common input.')
    parser.add_argument('--scrape', type=str, help='week rolling active', required=True)
    parser.add_argument('--ctr', type=list_of_strings, help='Countries. SE NO DE FI. For multiple countries seperate with "," ', required=False)
    parser.add_argument('--debug', type=str, required=False)
    args = parser.parse_args()

    main(args)    
