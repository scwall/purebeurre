# Purebeurre
Software for the company "Pur beurre"

## Getting Started

The software will analitics a database for compare and  find, some products of substitution healthier at than user request.

### Prerequisites

- [python 3.5 or more](https://www.python.org/downloads/)
- [mariadb](https://mariadb.org/download/)



### Installing

```
Install python
Install mariadb on the computer
Launch the script create_db_subsitution.sql for création the database or launch script recovery.py immediately 
Launch the script "recovery.py" for the recovery the data of site openfoodfact and wait it recovery all data
Launch the script "main.py" for consult the products and categories

```

## How to use "Pure beurre"
At the launch of the application:

You will have the choice to go through the food selection, or find my substitute foods.

In the food selection function you will have to:

- Selecting the food category

To select a food category, you will be given several proposals, you only need to enter the number of the category you have chosen.
 
- Select the food of your choice

**Several proposals**  will be associated with one number. you just need to enter the number

The program will then propose you a substitute, its description and a store where you can buy it, a **link** will be displayed to get more information about the food in question

You will then have the possibility to save your choice and do a new search or return to the main menu to consult for example to find your saved substitute foods, to start a new search, or simply to leave the menu. 

The user will be able to save his or her product, which will be registered to retrieve it later.



## Built With

* [python 3.5](https://www.python.org/) - The programming language 
* [mariadb](https://mariadb.org/) - The database
* [api openfoodfacts](https://fr.openfoodfacts.org/) - Used api , for to fill database


## Authors

* **Pascal de Sélys** - *Initial work* - [scwall](https://github.com/scwall)

## License

This project is licensed under the GNU License

## Acknowledgments

I would like to thank my teacher for his advice,my classmates, my wife for her patient, and the cactus, because it is nice my cactus