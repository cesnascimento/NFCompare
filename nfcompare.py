# -*- coding:utf-8 -*-
import os
import locale
from time import sleep
from O365 import Account, Connection, FileSystemTokenBackend
from bs4 import BeautifulSoup


locale.setlocale(locale.LC_MONETARY, '')


def open_nfd(nf):
    file = os.path.join('nfd', nf)
    file = open(file, encoding='UTF-8')
    return file


def open_nf_xml(file):
    soup = BeautifulSoup(file, 'lxml')
    return soup


def get_name(soup):
    name = soup.find('xnome').getText()
    fant = soup.find('xfant').getText()
    cnpj_nfd = soup.find('cnpj').getText()
    return name, fant, cnpj_nfd


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
        return 'CNPJ da nota de NFD corresponde ao CNPJ da NFE\n'


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
                    'O codigo do produto não consta em nenhum dos dois documentos')
    return products_nfd, products_compare


def product_compare(products_nfd, products_compare):
    list_alert, msg = list(), ''
    for product_nfd, product_nfe in zip(products_nfd, products_compare):
        if product_nfd['price'] != product_nfe['price']:
            print()
            list_alert.append(f'''
            <strong>Produto encontrado nas duas NF contém divergência:</strong> {product_nfd['name']}<br/>
            Código do produto: {product_nfd['code']}<br/>
            O valor da NFD é menor que o da NFE<br/>
            O valor da NFD é de: {product_nfd['price']}<br/>
            O valor da NFE é de: {product_nfe['price']}
            ''')
        if product_nfd['unit'] > product_nfe['unit']:
            print()
            list_alert.append(f'''
            <strong>Produto encontrado nas duas NF contém divergência:</strong> {product_nfd['name']}<br/>
            Código do produto: {product_nfd['code']}<br/>
            A quantidade devolvida é maior <br/>
            A quantidade da NFD foi: {product_nfd['unit']}<br/>
            A quantidade da NFE foi: {product_nfe['unit']}
            ''')
        else:
            if product_nfd['price'] == product_nfe['price'] and product_nfd['unit'] <= product_nfd['unit']:
                msg = msg+f'''{product_nfd['name']} - <strong>OK ✓</strong><br>'''
    return list_alert, msg


def check_nf(list_alert, list_products, msg=''):
    if len(list_alert) > 0:
        for alert in list_alert:
            msg = msg+'\n'+alert
    if len(list_products) > 0:
        list_products
    return msg, list_products


def refresh_token():
    credentials = ('3ba13a6c-e200-4e7c-ace1-b17f47f410df',
                   '_lr8Q~-6NPRbD2CU4zszbZMfMkrki7IE5zRKCbau')
    token_backend = FileSystemTokenBackend(
        token_path=os.getcwd(), token_filename='o365_token.txt'
    )
    account = Account(credentials, token_backend=token_backend)
    if not account.is_authenticated:
        account.authenticate(scopes=['basic', 'message_all'])

    connection = Connection(credentials, token_backend=token_backend, scopes=[
                            'basic', 'message_all'])
    connection.refresh_token()

    print("Outlook autenticado.")
    return account


def send_email(account, code_ref, folder_network, file_nfe, cnpjs_compare, msg_a, msg_b, name, fant, cnpj_nfd):
    if account.is_authenticated == True:
        m = account.new_message()
        m.to.add('cowlfnt@gmail.com')
        m.subject = f'Confêrencia NFD - {code_ref} - {name}'
        body = f"""
            <html>
                <body>
                    <center><h1>Relatório do Robô NFCompare</h1></center>
                    <br/>
                    <strong>Pasta com o CNPJ encontrada:</strong> {folder_network}
                    <p>
                    <strong>Arquivo XML com o codigo de referencia encontrado:</strong> {file_nfe}
                    </p>
                    <p>
                    <strong><h2>Dados da loja</h2></strong><br>
                    <strong>Razão Social:</strong> {name}<br/>
                    <strong>Nome Fantasia:</strong> {fant}<br/>
                    <strong>CNPJ:</strong> {cnpj_nfd}<br/>
                    </p>
                    <p>
                    <strong>{cnpjs_compare}</strong>
                    </p>
                    <p>
                    {msg_a}
                    </p>
                    <p>
                    {msg_b}
                    </p>
                </body>
            </html>"""
        m.body = body
        m.send()
        print('Email Enviado')
    else:
        print('Outlook não conectado')


def delete_nfd(dir):
    os.remove(os.path.join('nfd', dir))


def start():
    dirs = os.listdir('nfd')
    for dir in dirs:
        try:
            nf_xml = open_nf_xml(open_nfd(dir))
            name, fant, cnpj_nfd = get_name(nf_xml)
            cnpj, code_ref = get_data_nf(nf_xml)
            folder_network = get_folder_network(cnpj)
            file_nfe = get_file_nfe(folder_network, code_ref)
            cnpj_nfe = open_file_xml(file_nfe)
            file_nfd = get_products_nfd(nf_xml)
            cnpjs_compare = cnpj_compare(cnpj, cnpj_nfe)
            product_nfd, product_nfe = get_products_compare(file_nfd, file_nfe)
            a, b = product_compare(product_nfd, product_nfe)
            msg_a, msg_b = check_nf(a, b)
            open_nfd(dir).close()
            send_email(refresh_token(), code_ref, folder_network, file_nfe,
                       cnpjs_compare, msg_a, msg_b, name, fant, cnpj_nfd)
            sleep(10)
            delete_nfd(dir)
        except:
            print(f'O robô não consegue abrir este arquivo XML: {dir}')
            pass


start()
