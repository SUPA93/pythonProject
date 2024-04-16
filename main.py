from instagrapi import Client

# Configuration initiale et connexion
client = Client()
with open("bots.txt", "r") as f:
    username, password = f.read().splitlines()
client.login(username, password)

# Saisie et traitement de l'input utilisateur
input_value = input("Entrez l'URL ou le nom d'utilisateur Instagram : ")
username = input_value.replace('https://www.instagram.com/', '').strip('/')
user_info = client.user_info_by_username(username)
user_id = user_info.pk

# Récupération des posts 1 = dernier. 10 = les 10 ders
posts = client.user_medias(user_id, amount=1)

# Vérifier s'il y a des posts
if posts:
    for post in posts:
        caption = getattr(post, 'caption', 'Pas de légende disponible')
        print(f"ID de la publication: {post.pk}, Légende: {caption}, Nombre de likes: {post.like_count}")

        # Vérification si le post est déjà liké
        if not client.media_info(post.pk).has_liked:
            try:
                client.media_like(post.pk)
                print("Publication aimée avec succès.")
            except Exception as e:
                print(f"Erreur lors du like de la publication: {e}")
        else:
            print("Publication déjà aimée.")

        # Vérification si le post est déjà commenté
        already_commented = any(comment.text == "Super post !" for comment in client.media_comments(post.pk))
        if not already_commented:
            try:
                client.media_comment(post.pk, "Super post !")
                print("Commentaire ajouté avec succès.")
            except Exception as e:
                print(f"Erreur lors de l'ajout d'un commentaire: {e}")
        else:
            print("Commentaire 'Super post !' déjà ajouté.")
else:
    print("Aucun post disponible.")

# Vérification si l'utilisateur est déjà suivi
current_user_following = client.user_following(client.user_id_from_username(username))
if user_id not in current_user_following:
    try:
        client.user_follow(user_id)
        print("Abonnement au profil réussi.")
    except Exception as e:
        print(f"Erreur lors de l'abonnement au profil: {e}")
else:
    print("Déjà abonné au profil.")
