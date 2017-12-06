from packages.categories import Categories
from packages.databases.add_information_function import add_information_connection
from packages.products import Products
print(add_information_connection())
categories = Categories()
categories.recovery("https://fr.openfoodfacts.org/categories.json")
product = Products()
product.recovery()