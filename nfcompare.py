import tabula
import re
import os
from smb.SMBConnection import SMBConnection


def open_file():
    lista_tabelas = tabula.read_pdf('nfe 105 refe 6361.pdf', pages='all')
    coluna_cnpj = lista_tabelas[1].iloc[15].astype(str)[6]
    return coluna_cnpj


def get_cnpj(cnpj):
    cnpj = re.sub(r'\d{2}/\d{2}/\d{4}', '', cnpj)
    return cnpj


def get_items():
    lista_tabelas = tabula.read_pdf('nfe 105 refe 6361.pdf', pages='all')
    #coluna_cnpj = lista_tabelas[1].iloc[15].astype(str)[6]
    item, qtd = lista_tabelas[1].iloc[39].astype(
        str)[0], lista_tabelas[1].iloc[39].astype(str)[6]
    item1, qtd1 = lista_tabelas[1].iloc[40].astype(
        str)[0], lista_tabelas[1].iloc[40].astype(str)[6]
    item2, qtd2 = lista_tabelas[1].iloc[41].astype(
        str)[0], lista_tabelas[1].iloc[41].astype(str)[6]
    print(item, qtd.strip()[0])
    print(item1, qtd1.strip()[0])
    print(item2, qtd2.strip()[0])


def get_nfe_compare():
    folders = os.listdir('\\\\dmsrv-dts/XML_Danfe')
    cnpj = re.sub('[./-]', '', get_cnpj(open_file()))
    for folder in folders:
        if folder in cnpj:
            os.chdir(f'\\\\dmsrv-dts/XML_Danfe/{folder}/')
            new_folder = os.getcwd()
            if os.path.isdir(new_folder):
                print(f'Pasta encontrada: {os.getcwd()}')
                return os.getcwd()
            else:
                print(f'Pasta não encontrada!')


def open_nfe_compare(folder):
    print(folder)


def start():
    get_cnpj(open_file())
    get_items()
    open_nfe_compare(get_nfe_compare())


start()
