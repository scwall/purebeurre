from packages.databases.models import Categories, Products, Link_category_product, SaveProducts


class ConnectionQuery:
    connection = None

    @classmethod
    def set_connection(cls, connection):
        cls.connection = connection


class CategoriesQuery(ConnectionQuery):

    @classmethod
    def get_categories_by_tags(cls, tags_list):
        return cls.connection.connect.query(Categories).filter(Categories.id_category.in_(tags_list)).all()

    @classmethod
    def get_categories(cls):
        return cls.connection.connect.query(Categories).all()

    @classmethod
    def get_categorie_id(cls, id):
        return cls.connection.connect.query(Categories).filter(Categories.id == str(id)).one()

    @classmethod
    def get_categories_numbers(cls, start, end):
        return cls.connection.connect.query(Categories).order_by(Categories.id)[start:end]

    @classmethod
    def get_categories_on_product(cls, id):
        return cls.connection.connect.query(Categories).filter(Products.id == str(id)).all()

    @classmethod
    def get_categories_count(cls):
        return cls.connection.connect.query(Categories).count()


class ProductsQuery(ConnectionQuery):

    @classmethod
    def get_products(cls):
        return cls.connection.connect.query(Products).all()

    @classmethod
    def get_products_numbers(cls, start, end):
        return cls.connection.connect.query(Products).order_by(Products.id)[start:end]

    @classmethod
    def get_product_on_category(cls, id, start, end):
        return cls.connection.connect.query(Products).filter(Products.id == Link_category_product.product_id).filter(
            Link_category_product.category_id == str(id))[start:end]

    @classmethod
    def get_product_id(cls, id):
        return cls.connection.connect.query(Products).filter(Products.id == id).one()

    @classmethod
    def get_product_best_grade(cls, id,start,end):
        return cls.connection.connect.query(Products).filter(Products.id == Link_category_product.product_id).filter(
            Link_category_product.category_id == id).filter(Products.nutrition_grade == "a")[start:end]

    @classmethod
    def get_save_product_numbers(cls, start, end):
        return cls.connection.connect.query(Products).order_by(SaveProducts.date).filter(
            SaveProducts.id_product == Products.id)[start:end]

    @classmethod
    def get_products_count(cls):
        return cls.connection.connect.query(Products).count()


class SaveProductsQuery(ConnectionQuery):
    @classmethod
    def get_save_product_numbers(cls, start, end):
        return cls.connection.connect.query(SaveProducts).order_by(SaveProducts.date).filter(
            SaveProducts.id_product == Products.id)[start:end]

    @classmethod
    def get_save_count(cls):
        return cls.connection.connect.query(SaveProducts).count()
