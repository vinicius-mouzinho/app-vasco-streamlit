import streamlit_authenticator as stauth
import yaml

def criar_autenticador():
    # Lista de usuários e nomes correspondentes
    usuarios = {
        'saulo.matos': 'Saulo',
        'edson.junior': 'Edson',
        'ian.carvalho': 'Ian',
        'vinicius.vieira': 'Vinícius',
        'daniel.brito': 'Daniel'
    }

    senha_hash = stauth.Hasher(['Sc0utVasco!*1898@'] * len(usuarios)).generate()

    # Monta o dicionário de credenciais
    usernames_dict = {
        usuario: {
            'name': nome,
            'password': senha_hash[i]
        } for i, (usuario, nome) in enumerate(usuarios.items())
    }

    config = {
        'credentials': {
            'usernames': usernames_dict
        },
        'cookie': {
            'name': 'login_scoutvasco',
            'key': 'chave_autenticacao_scout',
            'expiry_days': 1
        },
        'preauthorized': {
            'emails': []
        }
    }

    autenticador = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    return autenticador
