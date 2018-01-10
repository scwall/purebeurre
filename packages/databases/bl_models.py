from packages.databases.models import Categories,Products,Link_category_product
class CategoriesBL:

    connection = None

    @classmethod
    def set_connection(cls, connection):
        cls.connection = connection

    @classmethod
    def get_categories_by_tags(cls, tags_list):
        return cls.connection.connect.query(Categories).filter(Categories.id_category.in_(tags_list)).all()

    @classmethod
    def get_categories(cls):
        return cls.connection.connect.query(Categories).all()

    @classmethod
    def get_categories_numbers(cls, start, end):
        return cls.connection.connect.query(Categories).order_by(Categories.id)[start:end]

    @classmethod
    def get_category(cls, id):
        return cls.connection.connect.query(Categories).filter(Categories.id == id)

    @classmethod
    def update_category(cls, id):
        pass

    @classmethod
    def delete_category(cls, id):
        pass


class ProductsBL:
    connection = None

    @classmethod
    def set_connection(cls, connection):
        cls.connection = connection

    @classmethod
    def get_products(cls):
        return cls.connection.connect.query(Products).all()

    @classmethod
    def get_products_numbers(cls, start, end):
        return cls.connection.connect.query(Products).order_by(Products.id)[start:end]

    @classmethod
    def get_category(cls, id):
        return cls.connection.connect.query(Products).filter(Products.id == id)

    @classmethod
    def update_category(cls, id):
        pass

    @classmethod
    def delete_category(cls, id):
        pass
