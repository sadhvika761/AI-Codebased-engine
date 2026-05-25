import zipfile

import pytest

from backend.utils.repo_loader import RepoLoader


def test_load_from_zip_rejects_path_traversal(tmp_path):
    archive_path = tmp_path / "repo.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        archive.writestr("../escape.py", "print('bad')")

    loader = RepoLoader(data_dir=str(tmp_path / "repos"))

    with pytest.raises(ValueError):
        loader.load_from_zip(str(archive_path), "repo")


def test_load_from_zip_flattens_single_top_level_folder(tmp_path):
    archive_path = tmp_path / "repo.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        archive.writestr("project/main.py", "print('ok')")

    loader = RepoLoader(data_dir=str(tmp_path / "repos"))
    repo_path = loader.load_from_zip(str(archive_path), "repo")

    assert (repo_path / "main.py").exists()
    assert not (repo_path / "project").exists()
