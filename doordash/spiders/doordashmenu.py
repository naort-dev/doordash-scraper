import scrapy
import urllib
import json
from doordash.items import DoordashItem
import datetime
import time
import pdb

class DoordashMenu(scrapy.Spider):
    name = "doordash_menu"
    url = "https://api-consumer-client.doordash.com/graphql"

    headers = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
         'Content-Type': 'application/json',
         'Credentials': 'include'
    }
    body = {
        "operationName": "menu",
        "variables": {
            # "storeId": "360",
            # "storeId": "2693"
            "storeId": "7980"
            # "menuId": "223199"
        },
        "query":'''
              query menu($storeId: ID!, $menuId: ID) {
                storeInformation(storeId: $storeId) {
                  id
                  name
                  description
                  isGoodForGroupOrders
                  offersPickup
                  offersDelivery
                  deliveryFee
                  sosDeliveryFee
                  numRatings
                  averageRating
                  shouldShowStoreLogo
                  isConsumerSubscriptionEligible
                  headerImgUrl
                  coverImgUrl
                  distanceFromConsumer
                  providesExternalCourierTracking
                  fulfillsOwnDeliveries
                  isDeliverableToConsumerAddress
                  priceRange
                  business {
                    id
                    name
                    __typename
                  }
                  address {
                    street
                    printableAddress
                    lat
                    lng
                    city
                    state
                    __typename
                  }
                  status {
                    asapAvailable
                    scheduledAvailable
                    asapMinutesRange
                    asapPickupMinutesRange
                    __typename
                  }
                  merchantPromotions {
                    id
                    minimumOrderCartSubtotal
                    newStoreCustomersOnly
                    deliveryFee
                    __typename
                  }
                  storeDisclaimers {
                    id
                    disclaimerDetailsLink
                    disclaimerLinkSubstring
                    disclaimerText
                    displayTreatment
                    __typename
                  }
                  __typename
                }
                storeMenus(storeId: $storeId, menuId: $menuId) {
                  allMenus {
                    id
                    name
                    subtitle
                    isBusinessEnabled
                    timesOpen
                    __typename
                  }
                  currentMenu {
                    id
                    timesOpen
                    hoursToOrderInAdvance
                    isCatering
                    minOrderSize
                    menuCategories {
                      ...StoreMenuCategoryFragment
                      items {
                        ...StoreMenuListItemFragment
                        __typename
                      }
                      __typename
                    }
                    __typename
                  }
                  __typename
                }
                storeCrossLinks(storeId: $storeId) {
                  trendingStores {
                    ...StoreCrossLinkItemFragment
                    __typename
                  }
                  trendingCategories {
                    ...StoreCrossLinkItemFragment
                    __typename
                  }
                  topCuisinesNearMe {
                    ...StoreCrossLinkItemFragment
                    __typename
                  }
                  nearbyCities {
                    ...StoreCrossLinkItemFragment
                    __typename
                  }
                  __typename
                }
              }

            fragment StoreMenuCategoryFragment on StoreMenuCategory {
              id
              subtitle
              title
              __typename
            }

            fragment StoreMenuListItemFragment on StoreMenuListItem {
              id
              description
              isTempDeactivated
              price
              imageUrl
              name
              __typename
            }

            fragment StoreCrossLinkItemFragment on StoreCrossLinkItem {
              name
              url
              __typename
            }

        '''
    }
    def start_requests(self):
        yield scrapy.Request(self.url, cookies={'X-CSRFToken': 'MKp9Os0ao3HiPO9ybnSFdDy7HrrodcxiFOWVhuhjaHEybo28kCAfBwMOWp6b78BU'}, body=json.dumps(self.body), callback=self.parse_menu, headers = self.headers, method="POST")
        # yield scrapy.Request(url, body=urllib.urlencode(body), callback=self.parse_detail, headers = headers, method="POST")


    def parse_menu(self, response):

      allMenus = json.loads(response.body)['data']['storeMenus']['allMenus']
      for menu in allMenus:
        self.body['variables']['menuId'] = menu['id']
        print(menu['id'])
        yield scrapy.Request(self.url, cookies={'X-CSRFToken': 'MKp9Os0ao3HiPO9ybnSFdDy7HrrodcxiFOWVhuhjaHEybo28kCAfBwMOWp6b78BU'}, body=json.dumps(self.body), callback=self.parse_detail, headers = self.headers, method="POST", meta={"menu_title": menu['subtitle']})

    def parse_detail(self, response):
    #       Item = scrapy.Field()
    # Description = scrapy.Field()
    # Price = scrapy.Field()
    # Category = scrapy.Field()
    # Menu = scrapy.Field()
      # print(json.loads(response.body)['data']['storeMenus']);
        # print(json.loads(response.body)['data']['storeMenus']['currentMenu']['menuCategories'])
      for category in json.loads(response.body)['data']['storeMenus']['currentMenu']['menuCategories']:
          for item in category['items']:
              menu = DoordashItem()
              menu['Item'] = item['name']
              menu['Price'] = float(item['price']) / 100
              menu['Description'] = item['description']
              menu['Category'] = category['title']
              menu['Menu'] = response.meta['menu_title']
              yield menu
      
        # pdb.set_trace()
        # print(json.dumps(json.loads(response.body)['data'], indent = 4))
