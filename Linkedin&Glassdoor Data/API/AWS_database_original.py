import pymysql
import copy


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


def insert_tags(cursor, tags):
    for tag in tags:
        select_tags = "SELECT * FROM tags where tag_id=%s"

        cursor.execute(select_tags, [tag.lower()])

        result = cursor.fetchall()

        if len(result) == 0:
            insert_tags = '''
                             INSERT INTO tags (tag_id) VALUES (%s)
                             '''
            cursor.execute(insert_tags, [tag.lower()])


def insert_professions(cursor, professions):
    for profession in professions:
        select_professions = "SELECT * FROM professions where profession_id=%s"

        cursor.execute(select_professions, [profession.lower()])

        result = cursor.fetchall()

        if len(result) == 0:
            insert_professions = '''
                             INSERT INTO professions (profession_id) VALUES (%s)
                             '''
            cursor.execute(insert_professions, [profession.lower()])


def get_tags(cursor, tags):
    select_tags = 'SELECT tag_id, IFNULL(num_jobs, 0) as num_jobs FROM tags WHERE tag_id IN '
    in_clause = '('
    for tag in tags:
        in_clause += '%s,'
    in_clause = in_clause[:-1] + ')'

    select_tags += in_clause

    cursor.execute(select_tags, tags)
    result = cursor.fetchall()

    return result


def get_links_one_tag(cursor, tags):
    lista_tags = get_tags(cursor, tags)
    lista = copy.deepcopy(lista_tags)
    for tag in lista:
        tag_id = tag['tag_id']
        select_link = "SELECT  link, nombre_empresa FROM jobs where tag = %s"
        cursor.execute(select_link, [tag_id])
        result = cursor.fetchall()  # lista de diccionarios (Json)
        tag['jobs'] = result
    return lista


def get_professions(cursor, professions):
    select_professions = 'SELECT profession_id, IFNULL(salary_range, 0) as salary_range FROM professions WHERE profession_id IN '
    in_clause = '('
    for profession in professions:
        in_clause += '%s,'
    in_clause = in_clause[:-1] + ')'
    select_professions += in_clause
    cursor.execute(select_professions, professions)
    result = cursor.fetchall()

    return result
