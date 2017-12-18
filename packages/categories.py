class Categories:
    def __init__(self, name, url, id_category):
        self.id_category = str(id_category)
        self.name = str(name)
        self.link_http = str(url)
        self.object_structure = {"name": "varchar(100)", "link_http": "varchar(200)", "id_category": "varchar(100)"}
        self.name_table = "Categories"
        self.create_dic()
    def create_dic(self):
        self.object_structure["name"] = self.name
        self.object_structure["link_http"] = self.link_http
        self.object_structure["id_category"] = self.id_category

    @property
    def get_object_structure(self):
        return self.object_structure

    @property
    def get_name_table(self):
        return self.name_table
