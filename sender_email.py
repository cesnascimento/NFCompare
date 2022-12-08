from O365 import Account, FileSystemTokenBackend

credentials = ('3ba13a6c-e200-4e7c-ace1-b17f47f410df',
               '_lr8Q~-6NPRbD2CU4zszbZMfMkrki7IE5zRKCbau')
account = Account(credentials)
if account.authenticate(scopes=['basic', 'message_all']):
   print('Authenticated!')
print(account.is_authenticated)
print(account.connection.refresh_token)
m = account.new_message()
m.to.add('cowlfnt@gmail.com')
m.subject = f'Confêrencia NFD - a'
body = f"""
        <html>
            <body>
                <center><h1>Relatório do Robô NFCompare</h1></center>
                <br/>
                <strong>Pasta com o CNPJ encontrada:</strong> a
                <p>
                <strong>Arquivo XML com o codigo de referencia encontrado:</strong> a
                </p>
                <p>
                <strong>a</strong>
                </p>
                <p>
                a
                </p>
                <p>
                a
                </p>
            </body>
        </html>"""
m.body = body
m.send()
