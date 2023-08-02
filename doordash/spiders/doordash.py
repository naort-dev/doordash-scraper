import requests
import csv
from requests.auth import AuthBase
import json
import sys


def doordash(storeId):
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
	        "storeId": storeId
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
	response = requests.post(url, cookies={'X-CSRFToken': 'MKp9Os0ao3HiPO9ybnSFdDy7HrrodcxiFOWVhuhjaHEybo28kCAfBwMOWp6b78BU'}, data = json.dumps(body), headers = headers)
	
	allMenus = response.json()['data']['storeMenus']['allMenus']
	items = [['Item', 'Price', 'Description', 'Category', 'Menu']]
	for menu in allMenus:
	# self.body['variables']['menuId'] = menu['id']
		# print(menu['id'])
		body['variables']['menuId'] = menu['id']
		response = requests.post(url, cookies={'X-CSRFToken': 'MKp9Os0ao3HiPO9ybnSFdDy7HrrodcxiFOWVhuhjaHEybo28kCAfBwMOWp6b78BU'}, data = json.dumps(body), headers = headers)
		for category in response.json()['data']['storeMenus']['currentMenu']['menuCategories']:
			for item in category['items']:
				itemmenu = [item['name'], float(item['price']) / 100, item['description'].encode('utf-8'), category['title'], menu['subtitle']]
				items.append(itemmenu)
	csv.register_dialect('myDialect',
	quoting=csv.QUOTE_ALL,
	skipinitialspace=True)
	with open('{}.csv'.format(storeId), 'w') as f:
	    writer = csv.writer(f, dialect='myDialect')
	    for row in items:
	    	print(row)
	        writer.writerow(row)
	f.close()
	print("Completed Successfully")
        # yield scrapy.Request(self.url, cookies={'X-CSRFToken': 'MKp9Os0ao3HiPO9ybnSFdDy7HrrodcxiFOWVhuhjaHEybo28kCAfBwMOWp6b78BU'}, body=json.dumps(self.body), callback=self.parse_detail, headers = self.headers, method="POST", meta={"menu_title": menu['subtitle']})

	# print(response.json())

if __name__ == '__main__':
	doordash(sys.argv[1])