import os
import locale
from bs4 import BeautifulSoup


locale.setlocale(locale.LC_MONETARY, '')


def open_nfd():
    file = open('1200010006361.xml')
    return file


def get_cnpj_ref(file):
    soup = BeautifulSoup(file, 'xml')
    cnpj = soup.find('CNPJ').getText()
    return cnpj


def get_ref(file):
    soup = BeautifulSoup(file, 'xml')
    codigo_ref = soup.find('nNF').getText()
    print(codigo_ref)
    return codigo_ref


def get_info_products_nf(file):
    products = dict()
    soup = BeautifulSoup(file, 'xml')
    name_products, code_products, unit_products, price_products = soup.findAll(
        'xProd'), soup.findAll('cProd'), soup.findAll('qCom'), soup.findAll('vUnCom')
    for name, code, unit, price in zip(name_products, code_products, unit_products, price_products):
        name, code, unit, price = name.getText(), code.getText(), unit.getText(), price.getText()
        price = locale.currency(float(price))
        unit = int(float(unit))
        products.update({name: [code,  unit, price]})
    return products


def get_folder_network(cnpj):
    path = '\\\\dmsrv-dts/XML_Danfe/'
    folders = os.listdir(path)
    for folder in folders:
        if folder in cnpj:
            path = os.path.join(path, folder)
            print(f'Pasta com o CNPJ encontrada: \\\\{path}')
            return path


def get_xml_file(folders):
    code_ref = get_ref(open_nfd())
    for folder in folders:
        if code_ref in folder and '.xml' in folder:
            print(
                f'Arquivo XML com o codigo de referencia encontrado: {folder}')
            return folder


def get_doc_ref(path):
    folders = os.listdir(path)
    file_xml = os.path.join(path, get_xml_file(folders))
    if os.path.isfile(file_xml):
        return file_xml


def open_nfe_compare(file_xml):
    file = open(file_xml)
    soup = BeautifulSoup(file, 'xml')
    #print(soup)
    pass



def start():
    a = get_doc_ref(get_folder_network(get_cnpj_ref(open_nfd())))
    get_info_products_nf(open_nfd())
    open_nfd().close()
    open_nfe_compare(a)


start()
