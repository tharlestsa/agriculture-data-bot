 
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['data']


attributes = ["cnpj", "razao_social", "nome_fantasia", "sif", "num_processo", "situacao", "data_reserva", "data_reserva", "data_registro", "logradouro", "bairro", "municipio", "uf", "cep", "fone", "email", "site", "area", "classes", "ocorrencias"]

attributesXpath = {
    "cnpj": "/html/body/form/table/tbody/tr[3]/td/table[1]/tbody/tr[1]/td[2]/input[2]",
    "razao_social": "/html/body/form/table/tbody/tr[3]/td/table[1]/tbody/tr[2]/td[2]/input",
    "nome_fantasia": "/html/body/form/table/tbody/tr[3]/td/table[1]/tbody/tr[1]/td[4]/input",
    "sif": "/html/body/form/table/tbody/tr[3]/td/table[2]/tbody/tr[2]/td/div[1]/table[1]/tbody/tr/td[2]/input",
    "num_processo": "/html/body/form/table/tbody/tr[3]/td/table[2]/tbody/tr[2]/td/div[1]/table[2]/tbody/tr/td[2]/input",
    "situacao": "/html/body/form/table/tbody/tr[3]/td/table[2]/tbody/tr[2]/td/div[1]/table[2]/tbody/tr/td[4]/input",
    "data_reserva": "/html/body/form/table/tbody/tr[3]/td/table[2]/tbody/tr[2]/td/div[1]/table[1]/tbody/tr/td[4]/input", 
    "data_registro": "/html/body/form/table/tbody/tr[3]/td/table[2]/tbody/tr[2]/td/div[1]/table[1]/tbody/tr/td[6]/input",
    "logradouro": "/html/body/form/table/tbody/tr[3]/td/table[2]/tbody/tr[2]/td/div[1]/table[3]/tbody/tr[2]/td[2]/input",
    "bairro": "/html/body/form/table/tbody/tr[3]/td/table[2]/tbody/tr[2]/td/div[1]/table[3]/tbody/tr[3]/td[2]/input",
    "municipio": "/html/body/form/table/tbody/tr[3]/td/table[2]/tbody/tr[2]/td/div[1]/table[3]/tbody/tr[4]/td[2]/input",
    "uf": "/html/body/form/table/tbody/tr[3]/td/table[2]/tbody/tr[2]/td/div[1]/table[3]/tbody/tr[4]/td[4]/input",
    "cep": "/html/body/form/table/tbody/tr[3]/td/table[2]/tbody/tr[2]/td/div[1]/table[3]/tbody/tr[3]/td[4]/input",
    "fone": "/html/body/form/table/tbody/tr[3]/td/table[2]/tbody/tr[2]/td/div[1]/table[4]/tbody/tr[1]/td[2]/input",
    "email": "/html/body/form/table/tbody/tr[3]/td/table[2]/tbody/tr[2]/td/div[1]/table[4]/tbody/tr[2]/td[2]/a",
    "site": "/html/body/form/table/tbody/tr[3]/td/table[2]/tbody/tr[2]/td/div[1]/table[4]/tbody/tr[3]/td[2]/input",
    "area": "/html/body/form/table/tbody/tr[3]/td/table[2]/tbody/tr[2]/td/div[2]/table/tbody/tr[2]/td/input",
    "classes": "/html/body/form/table/tbody/tr[3]/td/table[2]/tbody/tr[2]/td/div[3]/table/tbody/tr[_classe_]/td/input",
    "ocorrencias": [
        "/html/body/form/table/tbody/tr[3]/td/table[2]/tbody/tr[2]/td/div[4]/table/tbody/tr[_oco_date_]/td[1]/input",
        "/html/body/form/table/tbody/tr[3]/td/table[2]/tbody/tr[2]/td/div[4]/table/tbody/tr[_oco_desc_]/td[2]/textarea"
    ]
}

def getElement(driver, xpath):
    element = ""

    try:
        element = driver.find_element(By.XPATH, xpath)
    except Exception as e:
        element = None;
        pass

    return element


def getValue(driver, attribute):

    value = ""

    try:
        if(attribute == 'email'):
            value = getElement(driver, attributesXpath[attribute]).text
        elif (attribute == 'classes'):
            classes = []
            for classe in range(2, 61, 1):
                clas = getElement(driver, attributesXpath[attribute].replace('_classe_', str(classe)))
                if(clas):
                    classes.append(clas.get_attribute('value'))
            value = classes
        elif (attribute == 'ocorrencias'):
            ocorrencias = []
            for ocorrencia in range(2, 61, 1):
                oco_dt = getElement(driver, attributesXpath[attribute][0].replace('_oco_date_', str(ocorrencia)))
                oco_desc = getElement(driver, attributesXpath[attribute][1].replace('_oco_desc_', str(ocorrencia)))
                if(oco_dt and oco_desc):
                    ocorrencias.append({"data": oco_dt.get_attribute('value'), "ocorrencia": oco_desc.text})

            value = ocorrencias
        
        else:
            value = getElement(driver, attributesXpath[attribute]).get_attribute('value')
    except Exception as e:
        value = None;
        pass

    return value




driver = webdriver.Firefox(executable_path='/home/tharles/.geckodriver/geckodriver')

for id in range(1, 30001, 1):
    try:
        driver.get("http://sigsif.agricultura.gov.br/sigsif_cons/!ap_estabelec_nacional_detalhe?id_estabelecimento="+ str(id))
        time.sleep(0.500)
        frigorifico = {}
        frigorifico['estabelecimento_id'] = id
        for attribute in attributes:
            frigorifico[attribute] = getValue(driver, attribute)

        if (frigorifico['cnpj']):
            db.frigorificos.insert_one(frigorifico)
            print(frigorifico['razao_social'])
        
    except Exception as e:
        pass
    
driver.close()
