import os
import tempfile
import tarfile
import zipfile
import platform
import shutil
from backup import detect_os, get_home_directory, create_backup_archive

def test_detect_os():
    os_name = detect_os()
    # On s'attend à ce que la valeur retournée soit une chaîne non vide
    assert isinstance(os_name, str)
    assert os_name in ["Linux", "Windows", "Darwin", "MacOS"]

def test_get_home_directory():
    home_dir = get_home_directory()
    assert isinstance(home_dir, str)
    # Le répertoire personnel doit exister
    assert os.path.isdir(home_dir)

def test_create_backup_archive_linux_like():
    # On simule un environnement "Linux" ou "Darwin"
    os_type = "Linux"
    # Crée un répertoire temporaire qui va servir de "répertoire personnel" fictif
    with tempfile.TemporaryDirectory() as tmp_home:
        # Crée quelques fichiers dans ce répertoire temporaire
        file_path = os.path.join(tmp_home, "test.txt")
        with open(file_path, "w") as f:
            f.write("Contenu de test")
        # Crée un répertoire temporaire pour l'archive
        with tempfile.TemporaryDirectory() as tmp_backup:
            archive_path = create_backup_archive(os_type, tmp_home, tmp_backup)
            # L'archive doit exister et avoir l'extension .tar.gz
            assert os.path.isfile(archive_path)
            assert archive_path.endswith(".tar.gz")
            # Vérification rapide : ouverture de l'archive tar.gz
            with tarfile.open(archive_path, "r:gz") as tar:
                members = tar.getnames()
                # On s'attend à retrouver le nom du répertoire temporaire (sauvegardé avec son basename)
                assert os.path.basename(tmp_home) in members[0]

def test_create_backup_archive_windows():
    # On simule un environnement "Windows"
    os_type = "Windows"
    with tempfile.TemporaryDirectory() as tmp_home:
        file_path = os.path.join(tmp_home, "test.txt")
        with open(file_path, "w") as f:
            f.write("Contenu de test")
        with tempfile.TemporaryDirectory() as tmp_backup:
            archive_path = create_backup_archive(os_type, tmp_home, tmp_backup)
            # L'archive doit exister et avoir l'extension .zip
            assert os.path.isfile(archive_path)
            assert archive_path.endswith(".zip")
            # Vérification rapide : ouverture de l'archive zip
            with zipfile.ZipFile(archive_path, "r") as zipf:
                names = zipf.namelist()
                # On s'attend à retrouver le fichier créé
                assert "test.txt" in names

def test_create_backup_archive_os_non_supporte():
    # Pour un OS non supporté, la fonction doit lever une ValueError.
    try:
        create_backup_archive("OS_Inconnu", "/some/path")
    except ValueError as e:
        assert "OS non supporté" in str(e)
    else:
        assert False, "ValueError non levée pour un OS non supporté."
