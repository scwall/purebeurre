import requests
from packages.recovery.categories import Categories
from packages.recovery.Products import Products


def url_request(url, number):
    url = str(url) + "/" + str(number) + ".json"
    r = requests.get(url)
    return r.json()

def recovery(cursor,connection):

    url = "https://fr.openfoodfacts.org/categories.json"
    r = requests.get(url)
    categories_dic = r.json()

    for categorie in categories_dic['tags']:
        obj_categorie = Categories(cursor,connection,categorie['id'][3:])
        obj_categorie.insert_databases()
        url = (categorie['url'])
        number_page = 1
        final_page = True

        while final_page is True:
            products_dic = url_request(url, number_page)
            if len(products_dic["products"]) < 20:
                final_page = False
            for product in products_dic["products"]:
                try:
                    print(product["product_name_fr"])
                    obj_product = Products(cursor,connection,product["product_name_fr"],product["generic_name"],product["nutrition_grade_fr"],product["stores"],product["url"])
                    obj_product.insert_databases()

                except:
                    pass

            number_page += 1


