import os
import locale
from bs4 import BeautifulSoup


locale.setlocale(locale.LC_MONETARY, '')


def open_nfd(a):
    print(a)
    file = os.path.join('nfd', a)
    file = open(file)
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
        print('CNPJ da nota de NFD corresponde ao CNPJ da NFE\n')


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
        # print(name)
        products_nfd = get_products_nfd(open_nfd())
        for product_nfd in products_nfd:
            try:
                if product_nfd['code'] == code:
                    products_compare.append(
                        {'code': code, 'name': name, 'unit': unit, 'price': price})
            except:
                print('Produto não encontrado nas duas NF ou códigos não correspondem')
    return products_nfd, products_compare


def products_compare(products, products_compare):
    for productA, productB in zip(products, products_compare):
        if productA['price'] != productB['price']:
            print()
            return f'''
            Produto encontrado nas duas NF contém divergencia: {productA['name']}\n
            Código do produto: {productA['code']}\n
            O valor da NFD é menor que o da NFE\n
            O valor da NFD é de: {productA['price']}\n
            O valor da NFE é de: {productB['price']}\n
            '''
        if productA['unit'] > productB['unit']:
            print()
            return f'''
            Produto encontrado nas duas NF: {productA['name']}\n
            Código do produto: {productA['code']}\n
            A quantidade devolvida é maior \n
            A quantidade da NFD foi: {productA['unit']}\n
            A quantidade da NFE foi: {productB['unit']}
            '''
        else:
            if productA['price'] == productB['price'] and productA['unit'] <= productB['unit']:
                print(f'''{productA['name']} - OK''')


def check_nf(status):
    if status == None:
        print('\nStatus NFS: NFS são semelhantes')
    else:
        print('Status NFS:', status)


def start():
    dirs = os.listdir('nfd')
    for dir in dirs:
        print(open_nfd(dir))
        folder_network = open_folder_network(get_cnpj_ref(open_nfd(dir)))
        find_xml = find_file_xml(folder_network)
        print(find_xml)
        #a = find_file_xml(open_folder_network(get_cnpj_ref(open_nfd(dir))))
        #b = open_nfe_network(a)
        #cnpj_compare(b)
        #c, d = get_products_compare(a)
        #ok = products_compare(c, d)
        #check_nf(ok)

    #open_nfd().close()


start()
