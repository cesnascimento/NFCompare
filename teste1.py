import os
import locale
import smtplib
from bs4 import BeautifulSoup



locale.setlocale(locale.LC_MONETARY, '')


def open_nfd(nf):
    file = os.path.join('nfd', nf)
    file = open(file)
    return file


def open_nf_xml(file):
    soup = BeautifulSoup(file, 'lxml')
    return soup


def get_data_nf(soup):
    cnpj = soup.findAll('cnpj')[1].getText()
    code_ref = soup.find('refnfe').getText()[30:34]
    return cnpj, code_ref


def get_products_nfd(soup):
    products = list()
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


def get_folder_network(cnpj):
    path = '\\\\dmsrv-dts/XML_Danfe/'
    folders = os.listdir(path)
    for folder in folders:
        if folder in cnpj:
            path = os.path.join(path, folder)
            print()
            print(f'Pasta com o CNPJ encontrada: {path}')
            return path


def get_file_nfe(path, code_ref):
    folders = os.listdir(path)
    for folder in folders:
        if code_ref in folder and '.xml' in folder:
            file_xml = os.path.join(path, folder)
            print(
                f'Arquivo XML com o codigo de referencia encontrado:\n{file_xml}')
            return file_xml


def open_file_xml(file_xml):
    file = open(file_xml)
    soup = BeautifulSoup(file, 'xml')
    cnpj_nfe = soup.find('CNPJ').getText()
    return cnpj_nfe


def cnpj_compare(cnpj_nfd, cnpj_nfe):
    if cnpj_nfe == cnpj_nfd:
        print('CNPJ da nota de NFD corresponde ao CNPJ da NFE\n')


def get_products_compare(products_nfd, nfe_xml):
    products_compare = list()
    file = open(nfe_xml)
    soup = BeautifulSoup(file, 'xml')
    name_products, code_products, unit_products, price_products = soup.findAll(
        'xProd'), soup.findAll('cProd'), soup.findAll('qCom'), soup.findAll('vUnCom')
    for name, code, unit, price in zip(name_products, code_products, unit_products, price_products):
        name, code, unit, price = name.getText(
        ), code.getText(), unit.getText(), price.getText()
        price = locale.currency(float(price))
        unit = int(float(unit))
        for product_nfd in products_nfd:
            try:
                if product_nfd['code'] == code:
                    products_compare.append(
                        {'code': code, 'name': name, 'unit': unit, 'price': price})
            except:
                print(
                    'O codigo do produto não consta clearem nenhum dos dois documentos')
    return products_nfd, products_compare


def product_compare(products_nfd, products_compare):
    for product_nfd, product_nfe in zip(products_nfd, products_compare):
        if product_nfd['price'] != product_nfe['price']:
            print()
            return f'''
            Produto encontrado nas duas NF contém divergencia: {product_nfd['name']}\n
            Código do produto: {product_nfd['code']}\n
            O valor da NFD é menor que o da NFE\n
            O valor da NFD é de: {product_nfd['price']}\n
            O valor da NFE é de: {product_nfe['price']}\n
            '''
        elif product_nfd['unit'] > product_nfe['unit']:
            print()
            return f'''
            Produto encontrado nas duas NF contém divergencia: {product_nfd['name']}\n
            Código do produto: {product_nfd['code']}\n
            A quantidade devolvida é maior \n
            A quantidade da NFD foi: {product_nfd['unit']}\n
            A quantidade da NFE foi: {product_nfe['unit']}
            '''
        else:
            if product_nfd['price'] == product_nfe['price'] and product_nfd['unit'] <= product_nfd['unit']:
                print(f'''{product_nfd['name']} - OK''')


def check_nf(status):
    if status == None:
        print('\nStatus NFS: NFS são semelhantes')
    else:
        print('Status NFS:', status)


def send_email(cnpj):
    mailserver = smtplib.SMTP('smtp.office365.com',587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.login('cnascimento@dermage.com.br', '#')
    mailserver.sendmail('cnascimento@dermage.com.br','cesarfnt@gmail.com',f'\npython email {cnpj}')
    mailserver.quit()

def start():
    dirs = os.listdir('nfd')
    for dir in dirs:
        nf_xml = open_nf_xml(open_nfd(dir))
        cnpj, code_ref = get_data_nf(nf_xml)
        folder_network = get_folder_network(cnpj)
        file_nfe = get_file_nfe(folder_network, code_ref)
        cnpj_nfe = open_file_xml(file_nfe)
        file_nfd = get_products_nfd(nf_xml)
        cnpj_compare(cnpj, cnpj_nfe)
        product_nfd, product_nfe = get_products_compare(file_nfd, file_nfe)
        status = product_compare(product_nfd, product_nfe)
        check_nf(status)
        send_email(cnpj)
        open_nfd(dir).close()


start()
