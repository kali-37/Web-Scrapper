from bs4 import BeautifulSoup
import requests
import re
item_generated={}

search_term = input("What product do you want to search for? ")
url = f"https://www.newegg.com/p/pl?d={search_term}&N=4131"
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

page_text = doc.find(class_="list-tool-pagination-text").strong
pages = int(re.findall(r'\d+',str(page_text))[1])
items_found = {}

for page in range(1, pages+1):
	url = f"https://www.newegg.com/p/pl?d={search_term}&N=4131&page={page}"
	page = requests.get(url).text
	doc = BeautifulSoup(page, "html.parser")
	div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")	
	pattern=re.compile(search_term, re.IGNORECASE)
	items = div.find_all(text=pattern)

	for item in items:
		parent=item.parent
		price_parent=item.find_parent(class_="item-container")
		if price_parent.find(class_="price-current").strong is not None:
			price=price_parent.find(class_="price-current").strong.string

		if parent.name=="a":
			link=parent['href']

		item_generated[item]={"price":int(price.replace(",","")),"link":link}
		# it creates dictionary with as , 
		# {item_name:{"price":price,"link":link}


sorted_items=sorted(item_generated.items(),key=lambda x: x[1]["price"])

# item_generated.items() will return a python~"list" of python~"tuples"
# Above command will sort the dictionary based on the price of the item in ascending order
# Here, x[1] means {"price":price,"link":link}
# And, x[0] means item_name
# so we are sorting the dictionary based on the price of the item so x[1]["price"] is used
# key means based on what we want to sort the dictionary
# Here, lambda is used to pass the value of price to the sorted function
# if our dictonary had only price then we don't need to use lambda anymore. 


for item in sorted_items:
	print(item[0])
	print("PRICE: $ ",item[1]["price"])
	print("LINK: ", item[1]["link"])
	print()
