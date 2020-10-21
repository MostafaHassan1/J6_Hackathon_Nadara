import pymysql
import json
from pymysql.constants import CLIENT

# Database Connection Configuration
HOST = 'localhost'
USER = 'root'
PASSWORD = 'My.Birth@171998'
CHARSET = 'utf8mb4'
DBNAME = 'j6_hackathon'
PORT = 3306


def createDatabase():
    """- Creates the required database with all the necessary table(s) by running the MySQL forward engineer script for the scheme\n
    - Resets the database if it has been already created
    """
    conn = pymysql.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        port=3306,
        cursorclass=pymysql.cursors.DictCursor,
        client_flag=CLIENT.MULTI_STATEMENTS
    )

    # SQL Statement to create a database
    sql = """
    DROP SCHEMA IF EXISTS `{}` ;

    CREATE SCHEMA IF NOT EXISTS `{}` DEFAULT CHARACTER SET utf8 ;
    SHOW WARNINGS;
    USE `{}` ;

    DROP TABLE IF EXISTS `{}`.`people_faces_datasets` ;

    SHOW WARNINGS;
    CREATE TABLE IF NOT EXISTS `{}`.`people_faces_datasets` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` NVARCHAR(255) NOT NULL,
    `dataset` TEXT NOT NULL,
    PRIMARY KEY (`id`))
    ENGINE = InnoDB;
    """.format(DBNAME, DBNAME, DBNAME, DBNAME, DBNAME)
    sql = sql.replace("\n", "")
    try:
        # Create a cursor object
        with conn.cursor() as cursor:
            # Execute the create database SQL statment through the cursor instance
            cursor.execute(sql)
            conn.commit()

            sqlQuery = "SHOW DATABASES"
            cursor.execute(sqlQuery)
            databaseList = cursor.fetchall()
            for database in databaseList:
                if database['Database'] == DBNAME:
                    print(database, 'has been successfully created!')
                    break

    except Exception as e:
        print("Database creation failed: {}".format(e))

    finally:
        conn.close()


def insertPersonWithDataset(name, dataset):
    """Inserts a person and his dataset\n
    argument -- name: The name of the person to be inserted\n
    argument -- dataset: the dataset of the person to be inserted
    """
    conn = pymysql.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DBNAME,
        port=3306,
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO people_faces_datasets (name, dataset) VALUES ('{}', '{}')".format(
                name, json.dumps(dataset))
            cursor.execute(sql)
            conn.commit()
            print("Insertion Success!")

    except Exception as e:
        conn.rollback()
        print('Insertion Failed!', e)
    conn.close()


def getAllPeople():
    """Fetches all the people\n
    Return: a tuple: (list of all the datasets, list of all the names)\n
    - Both of the lists have the same indexing so thier nth elements correspond to the same nth row
    """
    conn = pymysql.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DBNAME,
        port=PORT,
        cursorclass=pymysql.cursors.DictCursor)

    try:
        with conn.cursor() as cursor:
            sql = "SELECT name, dataset FROM people_faces_datasets"
            cursor.execute(sql)
            data = cursor.fetchall()
            list_of_datasets, list_of_names = [], []

            for i in range(0, len(data)):
                list_of_names.append(data[i]['name'])
                list_of_datasets.append(json.loads(data[i]['dataset']))

            print("Fetching Success!")

    except Exception as e:
        conn.rollback()
        print('Fetching Failed:\n', e)

    conn.close()

    return list_of_datasets, list_of_names

def testInsertion():
    data = [-0.06413651,  0.05275547,  0.11465468, -0.06868585, -0.12905313, -0.06219113, -0.08105582, -0.05795766,  0.14002423, -0.14891383, 0.16809663,  0.03969061, -0.24029616,  0.01072336,  0.01820949, 0.20016633, -0.11752109, -0.12041475, -0.0686784,  0.02890174, 0.01413991, -0.00092969, -0.00206049,  0.05478341, -0.07208329, -0.38025042, -0.09110465, -0.03197921, -0.04670967,  0.00347318, -0.1002866,  0.02906058, -0.1258755, -0.06500086,  0.08338613, 0.14355671, -0.08919339, -0.08197339,  0.20867996,  0.01007678, -0.2455171, -0.03276137,  0.07985185,  0.2051305,  0.24185342, 0.0678556,  0.08049953, -0.09811792,  0.18532458, -0.34516171, 0.03625763,  0.09210046,  0.05877451,  0.06729918,  0.12198181, -0.13268434,  0.0351983,  0.13155086, -0.17172278, -0.04020822, 0.00662367, -0.09220872, -0.03645555, -0.07874616, 0.27311197, 0.1041171, -0.13304791, -0.09074535,  0.16285834, -0.18031871, -0.09120225,  0.01239933, -0.09920017, -0.15501264, -0.33115372, -0.01934731,  0.39288402,  0.15537588, -0.15778066,  0.06874227, -0.0653723, -0.03062057,  0.07541025,  0.05756121, -0.02222584, 0.01667677, -0.08238429, -0.01497209,  0.27893612, -0.08270567, 0.05658919,  0.18633389,  0.03200752,  0.08384499,  0.0460855, 0.0695291, -0.09776485, -0.05492003, -0.22801645, -0.05175924, 0.05780323, -0.02099415,  0.0295985,  0.10740275, -0.26527831, 0.09936604, -0.03858019, -0.04595775,  0.04024224, -0.01442718, -0.16451956, -0.08263291,  0.13128407, -0.21504368,  0.14097233, 0.18843487, -0.03240553,  0.11317647,  0.10367718,  0.0171592, -0.02866501, -0.07389878, -0.15731311, -0.09558592,  0.10734915, 0.03525282,  0.05941724,  0.0096033]
    
    insertPersonWithDataset(name='Mostafa', dataset=data)


def testRead():
    datasets, names = getAllPeople()

    print('\n\n\n\n', type(datasets), datasets, '\n\n', names)

if __name__ == "__main__":

    createDatabase()

