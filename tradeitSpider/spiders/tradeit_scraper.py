import scrapy
import json

class TradeitScraperSpider(scrapy.Spider):
    name = "tradeit_scraper"
    allowed_domains = ["tradeit.gg"]
    api_url = "https://tradeit.gg/api/v2/inventory/data?gameId=730&offset={}&limit=160&sortType=Popularity&searchValue=&minFloat=0&maxFloat=1&showTradeLock=true&onlyTradeLock=false&colors=&showUserListing=true&stickerName=&context=store&fresh=false&isForStore=1"
    

    async def start(self):
        print("START REQUESTS CALLED")
        start_offset = 0
        first_url = self.api_url.format(start_offset)

        yield scrapy.Request(
            url = first_url,
            callback = self.parse,
            meta = {'current offset' : start_offset}
            )
            
        
        

    def parse(self, response):
        
        data = json.loads(response.text)
        
        item_list = data.get("items", [])

        for item in item_list:
            yield{
                "Name" : item.get("name"),
                "Price" : item.get("price"),
                "Store Price" : item.get("sitePrice"),
                "Store Base Price" : item.get("storeBasePrice")
            }
        offset = response.meta['current offset']
        offset += 160

        if offset < 1000:
            next_url = self.api_url.format(offset)

            yield scrapy.Request(
                url=next_url, 
                callback=self.parse, 
                meta={'current offset': offset}
            )

        


