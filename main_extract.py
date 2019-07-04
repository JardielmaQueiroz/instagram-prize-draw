from Utils.Utils import exist_user
from Extract.InsertUser import insert_user
from Extract.Extract import start_extract


if __name__ == "__main__":
    username = input("Digite o usuário que deseja extrair: ")
    password = input("Digite a sua senha: ")
    print("Atualizando/Cadastrando seu usuário...")
    if not insert_user(username, password):
        print('Usuário ou senha inválidos!')
        exit()

    type_of_extraction = int(
        input("O que deseja extrair (Seguidores - 1 / Seguindo - 2)?: "))
    option = int(input("Extrair Novos - 1 / Atualizar - 2 / Deletar - 3: "))

    print("\nExtraindo de " + username)
    start_extract(username, type_of_extraction, option)
