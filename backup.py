#!/usr/bin/env python3
import os
import platform
import tarfile
import zipfile
import datetime

def detect_os():
    """
    Détecte le système d'exploitation.
    Retourne par exemple "Linux", "Windows", "Darwin" (MacOS).
    """
    return platform.system()

def get_home_directory():
    """
    Retourne le chemin du répertoire personnel de l'utilisateur.
    """
    return os.path.expanduser("~")

def create_backup_archive(os_type, home_dir, backup_dir=None):
    """
    Crée une archive compressée du répertoire personnel.
    
    Selon l'OS, on utilisera :
      - tar.gz pour Linux/MacOS (os_type "Linux", "Darwin" ou "MacOS")
      - zip pour Windows (os_type "Windows")
      
    :param os_type: Le système d'exploitation détecté (ex: "Linux", "Windows").
    :param home_dir: Le chemin du répertoire à sauvegarder.
    :param backup_dir: Répertoire de destination pour l'archive (par défaut, le répertoire courant).
    :return: Le chemin complet de l'archive créée.
    :raises ValueError: Si l'OS n'est pas supporté.
    """
    if backup_dir is None:
        backup_dir = os.getcwd()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    if os_type in ["Linux", "Darwin", "MacOS"]:
        archive_name = f"backup_{timestamp}.tar.gz"
        archive_path = os.path.join(backup_dir, archive_name)
        with tarfile.open(archive_path, "w:gz") as tar:
            # On sauvegarde tout le contenu du répertoire personnel
            tar.add(home_dir, arcname=os.path.basename(home_dir))
    elif os_type == "Windows":
        archive_name = f"backup_{timestamp}.zip"
        archive_path = os.path.join(backup_dir, archive_name)
        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(home_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, home_dir)
                    zipf.write(file_path, arcname=rel_path)
    else:
        raise ValueError(f"OS non supporté: {os_type}")
    return archive_path

def prompt_backup():
    """
    Propose à l'utilisateur de créer une archive de sauvegarde de son répertoire personnel.
    Si l'utilisateur accepte (réponse "o" ou "oui"), l'archive est créée et son chemin est affiché.
    """
    os_type = detect_os()
    home_dir = get_home_directory()
    response = input(f"Voulez-vous créer une archive de sauvegarde de votre répertoire personnel ({home_dir}) ? (o/n) : ")
    if response.lower() in ['o', 'oui']:
        archive_path = create_backup_archive(os_type, home_dir)
        print(f"Sauvegarde créée: {archive_path}")
    else:
        print("Opération annulée.")

if __name__ == "__main__":
    prompt_backup()
