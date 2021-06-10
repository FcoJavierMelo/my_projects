from flask import Flask, request
import AWS_database_original

application = app = Flask(__name__)

application.config["JSON_SORT_KEYS"] = False


def simple_response_tags(tags, data_tags):
    response_tags = []
    for tag in tags:
        for data_tag in data_tags:
            if data_tag['tag_id'] == tag.lower():
                response_tags.append(data_tag['num_jobs'])

    return response_tags


def simple_response_professions(professions, data_professions):
    response_professions = []
    for profession in professions:
        for data_profession in data_professions:
            if data_profession['profession_id'] == profession.lower():
                response_professions.append(data_profession['salary_range'])

    return response_professions


@application.route('/', methods=['GET'])
def home():
    return "<h1>API Tripulaciones 2021</p>"


@application.route('/api/v1/courses/new_courses', methods=['POST'])
def new_courses():
    db, cursor = AWS_database_original.connect_bbdd()

    query_parameters = request.get_json()

    tags = query_parameters.get('tags')
    professions = query_parameters.get('professions')

    AWS_database_original.insert_tags(cursor, tags)
    AWS_database_original.insert_professions(cursor, professions)

    db.commit()

    return {'status': 'ok'}


@application.route('/api/v1/courses/get_courses', methods=['GET'])
def get_courses():
    db, cursor = AWS_database_original.connect_bbdd()

    query_parameters = request.get_json()

    tags = query_parameters.get('tags')
    professions = query_parameters.get('professions')

    data_tags = AWS_database_original.get_links_one_tag(cursor, tags)
    data_professions = AWS_database_original.get_professions(cursor, professions)

    return {'tags': data_tags,
            'professions': data_professions}


@application.route('/api/v1/courses/get_courses_simple', methods=['GET'])
def get_courses_simple():
    db, cursor = AWS_database_original.connect_bbdd()

    query_parameters = request.get_json()

    tags = query_parameters.get('tags')
    professions = query_parameters.get('professions')

    data_tags = AWS_database_original.get_links_one_tag(cursor, tags)
    data_professions = AWS_database_original.get_professions(cursor, professions)

    response_tags = simple_response_tags(tags, data_tags)

    response_professions = simple_response_professions(professions, data_professions)

    return {'tags': response_tags,
            'professions': response_professions}


if __name__ == '__main__':
    application.run(debug=True)
