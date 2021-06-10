from selenium import webdriver
import time
import AWS_database


def driver_chrome(path):
    # CARGAR DRIVER CHROME

    options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(executable_path=path, options=options)

    driver.maximize_window()

    return driver


def open_glassdoor(driver):
    # ACCEDER A LA PAGINA WEB

    url = 'https://www.glassdoor.es/index.htm'

    driver.get(url)

    time.sleep(2)


def accept_cookie(driver):
    # ACEPTAR COOKIES

    cookies = driver.find_elements_by_id('onetrust-accept-btn-handler')[0]

    cookies.click()

    time.sleep(2)


def init_session(driver):
    # BOTON INICIAR SESION

    iniciar_sesion = driver.find_elements_by_class_name('d-none.d-lg-block.p-0.LockedHomeHeaderStyles__signInButton')[0]

    iniciar_sesion.click()


def login(username, password, driver):
    # LOGIN
    username_input = driver.find_element_by_id('userEmail')
    username_input.send_keys(username)

    password_input = driver.find_element_by_id('userPassword')
    password_input.send_keys(password)

    sign_in = driver.find_elements_by_class_name('gd-ui-button.minWidthBtn.css-8i7bc2')[1]
    sign_in.click()

    time.sleep(2)


def get_profession(cursor):
    # FUNCION PARA BUSCAR PERFILES EN LA BASE DE DATOS
    select_profession = "SELECT * FROM professions where salary_range is null"
    cursor.execute(select_profession)
    result = cursor.fetchall()

    profesiones = []

    for perfil in result:
        profesiones.append(perfil['profession_id'])

    return profesiones


def rango_salarial(perfil, driver):
    # FUNCION PARA EXTRAER LOS SUELDOS DE LOS PERFILES CREADOS
    puesto = perfil.replace(' ', '-')
    parche = puesto.lower()

    contador = str(len(perfil) + 7)

    link = 'https://www.glassdoor.es/Sueldos/españa-' + parche + \
           'full-stack-developer-sueldo-SRCH_IL.0,6_IN219_KO7,' + contador + \
           '.htm?clickSource=searchBtn'

    driver.get(link)

    time.sleep(2)

    sueldo = driver.find_elements_by_class_name('css-17fpxj7')[0].text  # si pone sueldo en España

    return sueldo


def update_database(cursor, diccionario):
    # UPDATE BASE DE DATOS
    sentencia_update = 'UPDATE professions SET salary_range = %s WHERE profession_id = %s'

    for i, j in enumerate(diccionario['Profesion']):
        profesion = j
        sueldo = diccionario['Salario'][i]

        sueldo = sueldo.replace('.', '')
        sueldo = sueldo.replace(' € / año', '')
        sueldo = int(sueldo)

        cursor.execute(sentencia_update, [sueldo, profesion])


def scrap_glassdoor():
    chrome_driver = r'C:\\Bootcamp\\chromedriver.exe'

    driver = driver_chrome(chrome_driver)

    open_glassdoor(driver)

    accept_cookie(driver)

    init_session(driver)

    # LOGEARSE
    username = 'john_ds99@outlook.com'
    password = 'vUgrH8D6lCKY6XasC6dZ'

    login(username, password, driver)

    db, cursor = AWS_database.connect_bbdd()

    salarios = []

    profesiones = get_profession(cursor)

    for perfil in profesiones:
        nuevo = rango_salarial(perfil, driver)
        salarios.append(nuevo)

    # DICCIONARIO PERFIL RANGO SALARIAL

    diccionario = {
        'Profesion': profesiones,
        'Salario': salarios
    }

    update_database(cursor, diccionario)

    if driver is not None:
        driver.quit()

    db.commit()

    db.close()

    print('################ Fin scrap glassdoor ######################')

