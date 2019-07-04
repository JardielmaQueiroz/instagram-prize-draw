import os
from AutoComment.AutoComment import AutoComment
from Utils.Utils import create_list_comment, load_file, exist_user, get_user


if __name__ == '__main__':
    username = input("Digite seu usuario: ")
    profile_username = input("Digite o perfil do sorteio: ")
    photo = input("Digite o codigo da publicação: ")
    quant = int(input("Digite a quantidade de usuários por comentário: "))
    type_users = int(input(
        "Comentar usando os usuários que você segue (Seguindo) - 1 / Comentar usando os usuários que seguem você (Seguidores) - 2: "))

    if exist_user(username):
        user = get_user(username)
        lst_of_comment_to_do = create_list_comment(quant, type_users, user.id)
        if not (type_users != 1 and type_users != 2):
            path = os.path.join('MadeComments', profile_username +
                                "_" + photo + "_" + username + ".txt")
            lst_of_comment_made = load_file(path)

            auto = AutoComment(user.username, user.password,
                               photo, profile_username)
            if auto.verify_coditions():
                print("Iniciando os comentários!")
                auto.start_comment(lst_of_comment_to_do,
                                   lst_of_comment_made, path)
            else:
                print("Erro na verificação das condições")
        else:
            print("Opção inválida! Escolha entre 1 ou 2!")
    else:
        print("Usuário não encontrado! utilize o programa de extração (main_extract.py)!")
