import pymysql

from sqlalchemy import create_engine




def make_engine(user, host, pw, db):
    engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                           .format(user=user,
                                   host=host,
                                   pw=pw,
                                   db=db))
    return engine







def connect_bbdd():
    username = 'admin'
    password = 'Trip2021'
    host = 'database-1.cgms0uqi3vl9.eu-west-1.rds.amazonaws.com'
    port = 3306

    db = pymysql.connect(host=host,
                         user=username,
                         password=password,
                         cursorclass=pymysql.cursors.DictCursor)

    use_database = '''USE data_tripulaciones_2021'''

    cursor = db.cursor()

    cursor.execute(use_database)

    return db, cursor

def create_bbdd(cursor):
    create_db = "CREATE DATABASE data_tripulaciones_2021"
    cursor.execute(create_db)

def create_tables(cursor):
    create_table_courses = "CREATE TABLE tags(tag_id VARCHAR(50), " \
                           "num_jobs INT, primary key (tag_id))"

    cursor.execute(create_table_courses)

    create_table_professions = "CREATE TABLE professions(profession_id VARCHAR(50), " \
                           "salary_range INT, primary key (profession_id))"

    cursor.execute(create_table_professions)




"""create_db = '''CREATE DATABASE data_tripulaciones_2021'''
cursor.execute(create_db)"""

"""drop_table_courses = '''
DROP TABLE courses
'''

cursor.execute(drop_table_courses)"""

"""create_table_courses = '''
CREATE TABLE courses(
course_id VARCHAR(50),
num_jobs INT,
primary key (course_id)
)
'''

"""


def insert_courses(cursor, courses):
    for course in courses:
        select_courses = "SELECT * FROM courses where course_id=%s"

        cursor.execute(select_courses, [course])

        result = cursor.fetchall()

        if len(result) == 0:
            insert_courses = '''
                             INSERT INTO courses (course_id) VALUES (%s)
                             '''
            cursor.execute(insert_courses, [course.lower()])


def get_courses(cursor):
    select_courses = 'SELECT * FROM courses'
    cursor.execute(select_courses)
    result = cursor.fetchall()

    return result


"""courses = ['Javascript', 'HTML', 'jQuery']
cursor = connect_bbdd()

insert_courses(cursor, courses)

print(get_courses(cursor))

delete_table_courses = '''
delete from courses
'''

cursor.execute(delete_table_courses)"""
