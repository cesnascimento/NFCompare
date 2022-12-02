import os
import locale
from bs4 import BeautifulSoup


locale.setlocale(locale.LC_MONETARY, '')


def open_nfd():
    file = open('cosmoprime.xml')
    return file


def get_cnpj_ref(file):
    soup = BeautifulSoup(file, 'lxml')
    cnpj = soup.findAll('cnpj')[1].getText()
    return cnpj


def get_code_ref(file):
    soup = BeautifulSoup(file, 'lxml')
    code_ref = soup.find('refnfe').getText()
    code_ref = code_ref[30:34]
    return code_ref


def get_products_nfd(file):
    products = list()
    soup = BeautifulSoup(file, 'lxml')
    name_products, code_products, unit_products, price_products = soup.findAll(
        'xprod'), soup.findAll('cprod'), soup.findAll('qcom'), soup.findAll('vuncom')
    for name, code, unit, price in zip(name_products, code_products, unit_products, price_products):
        name, code, unit, price = name.getText(
        ), code.getText(), unit.getText(), price.getText()
        price = locale.currency(float(price))
        unit = int(float(unit))
        products.append({'code': code, 'name': name,
                        'unit': unit, 'price': price})
    return products


def open_folder_network(cnpj):
    path = '\\\\dmsrv-dts/XML_Danfe/'
    folders = os.listdir(path)
    for folder in folders:
        if folder in cnpj:
            path = os.path.join(path, folder)
            print(f'Pasta com o CNPJ encontrada: {path}')
            return path


def get_file_xml(folders):
    code_ref = get_code_ref(open_nfd())
    for folder in folders:
        if code_ref in folder and '.xml' in folder:
            print(
                f'Arquivo XML com o codigo de referencia encontrado: {folder}')
            return folder


def find_file_xml(path):
    folders = os.listdir(path)
    file_xml = os.path.join(path, get_file_xml(folders))
    if os.path.isfile(file_xml):
        return file_xml
    else:
        print('Arquivo XML não encontrado!')


def open_nfe_network(file_xml):
    file = open(file_xml)
    soup = BeautifulSoup(file, 'xml')
    cnpj_nfe = soup.find('CNPJ').getText()
    return cnpj_nfe


def cnpj_compare(cnpj_nfe):
    if cnpj_nfe == get_cnpj_ref(open_nfd()):
        print('CNPJ da nota de NFD corresponde ao CNPJ da NFE')


def get_products_compare(file_xml):
    products_compare = list()
    file = open(file_xml)
    soup = BeautifulSoup(file, 'xml')
    name_products, code_products, unit_products, price_products = soup.findAll(
        'xProd'), soup.findAll('cProd'), soup.findAll('qCom'), soup.findAll('vUnCom')
    for name, code, unit, price in zip(name_products, code_products, unit_products, price_products):
        name, code, unit, price = name.getText(
        ), code.getText(), unit.getText(), price.getText()
        price = locale.currency(float(price))
        unit = int(float(unit))
        products_compare.append(
            {'code': code, 'name': name, 'unit': unit, 'price': price})
    return products_compare


def products_compare(products, products_compare):
    for productA in products:
        for productB in products_compare:
            if productA['code'] != productB['code']:
                pass
            else:
                if productA['code'] == productB['code']:
                    print()
                    print(
                        f'''Produto encontrado nas duas NF: {productA['name']} ''')
                    print(f'''Código: {productA['code']} ''')
                    if productA['price'] == productB['price']:
                        print(f'''Valor: {productA['price']} ''')
                    else:
                        print('O valor da NFD é menor que o da NFE')
                        print(f'''O valor da NFD é de: {productA['price']}''')
                        print(f'''O valor da NFE é de: {productB['price']}''')
                    if productA['unit'] <= productB['unit']:
                        print(f'''Quantidade devolvida: {productA['unit']} ''')
                    else:
                        print('A quantidade devolvida é maior')
                        print(f'''A quantidade comprada foi: {productB['unit']}''')
                        print(f'''A quantidade devolvida foi: {productA['unit']}''')


def start():
    a = find_file_xml(open_folder_network(get_cnpj_ref(open_nfd())))
    b = open_nfe_network(a)
    cnpj_compare(b)
    get_products_compare(a)
    products_compare(get_products_nfd(open_nfd()), get_products_compare(a))
    get_code_ref(open_nfd())
    get_products_nfd(open_nfd())

    open_nfd().close()


start()
