from packages.databases.add_information_function import add_information_connection
from packages.databases.databases import Database
from packages.research.research_foods import Research_foods

research = Research_foods()
test = research.show_category("all")

for category in test:
    print(category.id,category.name)







