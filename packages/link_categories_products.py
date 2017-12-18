class Link_categories_products:
    def __init__(self, id_product, id_category):
        self.id_product = id_product
        self.id_category = id_category
        self.name_table = "Link_categories_products"
        self.object_structure = {"id_category": "int(10)", "id_product": "int(10)"}
        self.create_dic()

    def create_dic(self):
        self.object_structure["id_product"] = str(self.id_product)
        self.object_structure["id_category"] = str(self.id_category)

    @property
    def get_object_structure(self):
        return self.object_structure

    @property
    def get_name_table(self):
        return self.name_table
