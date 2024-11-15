import pytest
from homework1.src.shell_emulator import ShellEmulator
import tarfile


@pytest.fixture
def setup_emulator(tmp_path):
    # Создаем временные файлы для тестирования
    fs_path = tmp_path / "virtual_fs.tar"
    log_path = tmp_path / "session_log.json"

    # Создаем виртуальную файловую систему (файл tar)
    with tarfile.open(fs_path, "w") as tar:
        tar.addfile(tarfile.TarInfo("dir1/"))
        tar.addfile(tarfile.TarInfo("dir1/file1.txt"))
        tar.addfile(tarfile.TarInfo("dir2/"))

    # Инициализируем эмулятор с тестовым пользователем и виртуальной ФС
    emulator = ShellEmulator("testuser", str(fs_path), str(log_path))
    return emulator, log_path


def test_ls_command(setup_emulator, capsys):
    emulator, _ = setup_emulator

    # Имитируем добавление директории для корректной проверки
    emulator._file_system["/"] = ["dir1", "dir2"]  # Примерная структура файловой системы

    emulator.ls()
    captured = capsys.readouterr()

    # Проверяем, что список файлов/директорий содержит "dir1" и "dir2"
    assert "dir1" in captured.out
    assert "dir2" in captured.out


def test_cd_command(setup_emulator, capsys):
    emulator, _ = setup_emulator

    # Успешный переход в подкаталог
    emulator.cd("dir1")
    captured = capsys.readouterr()
    assert "Changed directory to /dir1" in captured.out

    # Переход в несуществующий каталог
    emulator.cd("nonexistent")
    captured = capsys.readouterr()
    assert "Directory nonexistent not found" in captured.out


def test_pwd_command(setup_emulator, capsys):
    emulator, _ = setup_emulator

    emulator.pwd()
    captured = capsys.readouterr()
    assert "Current directory: /" in captured.out

    emulator.cd("dir1")
    emulator.pwd()
    captured = capsys.readouterr()
    assert "Current directory: /dir1" in captured.out


def test_cp_command(setup_emulator, capsys):
    emulator, _ = setup_emulator

    emulator.cp("dir1/file1.txt", "dir2/file1_copy.txt")
    captured = capsys.readouterr()
    assert "Copied dir1/file1.txt to dir2/file1_copy.txt" in captured.out

    # Попытка скопировать несуществующий файл
    emulator.cp("nonexistent.txt", "dir2/")
    captured = capsys.readouterr()
    assert "Source file nonexistent.txt does not exist." in captured.out


def test_whoami_command(setup_emulator, capsys):
    emulator, _ = setup_emulator

    emulator.whoami()
    captured = capsys.readouterr()
    assert "User: testuser" in captured.out


def test_exit_command(setup_emulator, capsys):
    emulator, log_path = setup_emulator

    # Ожидаем, что выполнение команды exit завершит программу
    with pytest.raises(SystemExit):
        emulator.exit()

