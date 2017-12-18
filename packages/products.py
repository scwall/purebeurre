class Product:
    def __init__(self, name, description, nutrition_grade, shop, link_http,categories_tags):
        self.categories_tags = categories_tags
        self.name = name
        self.description = description
        self.nutrition_grade = nutrition_grade
        self.shop = shop
        self.link_http = link_http
        self.name_table = "Products"
        self.object_structure = {"name": "varchar(100)", "description": "text",
                                 "nutrition_grade": "char(1)","shop":"varchar(40)",
                                 "link_http":"varchar(200)"}
        self.create_dic()
    def create_dic(self):
        self.object_structure["name"] = self.name
        self.object_structure["description"] = self.description
        self.object_structure["nutrition_grade"] = self.nutrition_grade
        self.object_structure["shop"] = self.shop
        self.object_structure["link_http"] = self.link_http
    @property
    def get_object_structure(self):

        return self.object_structure

    @property
    def get_name_table(self):
        return self.name_table

    @property
    def get_categories_tags(self):
        return self.categories_tags
