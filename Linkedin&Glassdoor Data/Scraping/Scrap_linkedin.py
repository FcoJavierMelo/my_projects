import time
import pandas as pd
from selenium import webdriver
import AWS_database

def insert_jobs(engine, df):

    df.to_sql('jobs',
              con = engine,
              if_exists = 'append',
              index = False)


def delete_jobs_by_tag(cursor, tag):
    delete_jobs = 'delete FROM jobs WHERE tag= %s'
    cursor.execute(delete_jobs, [tag])


def info_collect(driver):
    title = driver.find_element_by_class_name('topcard__content-left')

    puesto = title.find_element_by_class_name('topcard__title')

    link = title.find_element_by_tag_name('a').get_attribute('href')

    puesto = puesto.text

    empresa = title.find_elements_by_class_name('topcard__flavor')

    dias = title.find_elements_by_class_name('topcard__flavor--metadata.posted-time-ago__text')

    solicitantes = title.find_elements_by_class_name('num-applicants__caption')

    datos_cabecera_oferta = [link,
                             empresa[0].text,
                             puesto,
                             empresa[1].text,
                             dias[0].text,
                             solicitantes[0].text]

    job_desc = driver.find_elements_by_class_name('description__text.description__text--rich')

    job_desc1 = [job_desc[0].text[:-14]]

    job_desc = driver.find_elements_by_class_name('job-criteria__item')

    lista = []

    for desc in job_desc:
        lineas = desc.find_elements_by_class_name('job-criteria__text.job-criteria__text--criteria')
        cadena = ''
        for linea in lineas:
            cadena += linea.text + ' '
        lista.append(cadena)

    info_df = datos_cabecera_oferta + lista + job_desc1

    return info_df


def search_cont(driver, jobs_list):
    content = driver.find_element_by_class_name("jobs-search__results-list")
    content_list = content.find_elements_by_class_name("result-card__full-card-link")
    counter = 0
    for i in range(15):
        time.sleep(1.5)
        content_list[i].click()
        time.sleep(2)
        info_df = info_collect(driver)
        if len(info_df) == 11:  # Solo ofertas con todos los campos rellenos
            titulos_col = ['link',
                           'nombre_empresa',
                           'puesto_ofertado',
                           'ubicacion',
                           'tiempo_activa',
                           'num_solicitudes',
                           'nivel_experiencia',
                           'sector',
                           'tipo_jornada',
                           'funciones_laborales',
                           'descripcion']

            df_prueba = pd.DataFrame([info_df], columns=titulos_col)
            jobs_list = jobs_list.append(df_prueba, ignore_index=True)
            # time.sleep(3)
            content = driver.find_element_by_class_name("jobs-search__results-list")
            content_list = content.find_elements_by_class_name("result-card__full-card-link")
            counter += 1
        if counter == 1:
            break
    return jobs_list


def open_chrome_browser(path):
    chrome_driver = path

    options = webdriver.ChromeOptions()  # Añadimos un dic con todas las opciones de configuración de Chrome.

    #  options.add_argument('headless')

    # Headless hace que el web scrapping vaya viendo lo que hace o no.

    # Podemos configurar diversas opciones en líneas sucesivas.

    driver = webdriver.Chrome(executable_path=chrome_driver, options=options)

    driver.maximize_window()

    return driver


def courses_request(driver, courses):
    jobs_result = pd.DataFrame()
    n_ofertas = []

    for course in courses:
        link_linkedin = 'https://www.linkedin.com/jobs/search?keywords=' + course + '&location=Espa%C3%B1a&trk' \
                                                                                    '=public_jobs_jobs-search' \
                                                                                    '-bar_search' \
                                                                                    '-submit&position=1&pageNum=0&f_TPR' \
                                                                                    '=r604800'#r2592000

        driver.get(link_linkedin)

        time.sleep(1.5)

        botones = driver.find_elements_by_class_name(
            'artdeco-global-alert-action.artdeco-button.artdeco-button--inverse.artdeco-button--2.artdeco-button'
            '--primary')

        for boton in botones:
            if boton.text == 'Aceptar cookies':
                boton.click()

        num_ofertas = driver.find_element_by_class_name('results-context-header__job-count').text
        print(num_ofertas)
        n_ofertas.append(num_ofertas)
        jobs_list = pd.DataFrame()
        jobs = pd.DataFrame()

        jobs_list = search_cont(driver, jobs_list)
        jobs = jobs.append(jobs_list, ignore_index=True)
        jobs['tag'] = course.lower()
        print(jobs['tag'])
        jobs_result = jobs_result.append(jobs)



    jobs_result.to_csv('offers.csv', index=False)

    return n_ofertas , jobs_result


def scrap_linkedin(courses):
    driver = open_chrome_browser(r'C:\\Bootcamp\\chromedriver.exe')

    n_ofertas, jobs_result = courses_request(driver, courses)

    if driver is not None:
        driver.quit()

    return n_ofertas, jobs_result


def update_tags(cursor, db):

    select_tag = "SELECT * FROM tags where num_jobs is null LIMIT 5" #selecciona todas las celdas nulas
    cursor.execute(select_tag)
    result = cursor.fetchall() #lista de diccionarios (Json)

    courses = []
    print(result)

    for index in result:
        courses.append(index['tag_id'])

        delete_jobs_by_tag(cursor, index['tag_id'])

    db.commit()

    n_offers , jobs_results = scrap_linkedin(courses)

    engine = AWS_database.make_engine('admin',
                                        'database-1.cgms0uqi3vl9.eu-west-1.rds.amazonaws.com',
                                        'Trip2021',
                                        'data_tripulaciones_2021')

    insert_jobs(engine, jobs_results)

    for index, value in enumerate(result):
        a = n_offers[index]
        a = a.replace('.','')
        a = a.replace('+', '')
        b = value['tag_id']
        sql = 'UPDATE tags SET num_jobs  = %s WHERE tag_id = %s'
        cursor.execute(sql, [a,b])
        db.commit()

def final_scrap_linkedin():
    db, cursor = AWS_database.connect_bbdd()

    update_tags(cursor, db)

    db.commit()

    db.close()

    print('################ Fin scrap linkedin ######################')


