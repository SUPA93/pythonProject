import time
from instagrapi import Client

try:
    with open("bots.txt", "r") as f:
        username, password = f.read().splitlines()
except Exception as e:
    print(f"Erreur de lecture txt: (e)")
    exit()

client = Client()
try:
    client.login(username, password)
except Exception as e:
    print(f"Erreur de connection: (e)")
    time.sleep(5)
input_value = input("Entrez l'URL ou le nom d'utilisateur Instagram : ")
username = input_value.replace('https://www.instagram.com/', '').strip('/')
# version de chat jépété
# username = input_value.split('instagram.com/')[-1].strip('/').split('?')[0]

try:
    user_info = client.user_info_by_username(username)
    user_id = user_info.pk
    time.sleep(5)
except Exception as e:
    print(f"Erreur lors de la récupération des infos user: (e)")
    exit()
# ici si tu veux le dernier post c'est 1 sinon tu peux mettre les 10 derniers avec 10 par ex
posts = client.user_medias(user_id, amount=1)

for post in posts:
    # print(f"ID de la publication: {post.pk},  Nombre de likes: {post.like_count}")

    try:
        # Pour liker une publication
        client.media_like(post.pk)
        print("Publication aimée avec succès.")
    except Exception as e:
        print(f"Erreur lors du like de la publication: {e}")
        time.sleep(5)
    try:
        # Pour s'abonner au profil
        client.user_follow(user_id)
        print("Abonnement au profil réussi.")
    except Exception as e:
        print(f"Erreur lors de l'abonnement au profil: {e}")
        time.sleep(8)
    try:
        # Pour commenter une publication
        client.media_comment(post.pk, "Super post !")
        print("Commentaire ajouté avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'ajout d'un commentaire: {e}")

print("Tout est OK")
