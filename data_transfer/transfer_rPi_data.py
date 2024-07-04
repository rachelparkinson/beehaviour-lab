import hashlib
import logging
import sys
from datetime import date
from pathlib import Path
from stat import S_ISDIR, S_ISREG
from typing import List, Union

import click
import paramiko
import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
YAML_FILE = SCRIPT_DIR / "rPis.yaml"

# Set up logging
file_handler = logging.FileHandler(
    filename=f"{date.today()}_transfer_rPi_data.log", level=logging.DEBUG
)
stdout_handler = logging.StreamHandler(stream=sys.stdout, level=logging.INFO)
handlers = [file_handler, stdout_handler]
LOGGING_FMT = "%(asctime)s - %(levelname)s - %(message)s"
LOGGING_DATE_FMT = "%d-%b-%y %H:%M:%S"
logging.basicConfig(
    level=logging.DEBUG, format=LOGGING_FMT, datefmt=LOGGING_DATE_FMT, handlers=handlers
)
logger = logging.getLogger(__name__)


def get_ssh_client(user: str, ip: str) -> Union[paramiko.SSHClient, bool]:
    """
    Get an SSH client object for the given user and IP address.

    Args:
        user (str): The username for SSH connection.
        ip (str): The IP address of the remote server.

    Returns:
        Union[paramiko.SSHClient, bool]: An SSH client object if the connection is successful, False otherwise.
    """
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=user, timeout=10)
        return client
    except Exception as e:
        logger.error(f"Failed to connect to {ip}: {e}")
        return False


def check_accessibility(user: str, ip: str) -> bool:
    """
    Check the accessibility of a remote server using SSH.

    Args:
        user (str): The username for SSH connection.
        ip (str): The IP address of the remote server.

    Returns:
        bool: True if the server is accessible, False otherwise.
    """
    client = get_ssh_client(user, ip)
    if client:
        client.close()
        return True
    else:
        return False


def transfer_file(
    ftp_client: paramiko.SFTPClient,
    source_path: str,
    destination_path: Union[str, Path],
) -> bool:
    """
    Transfer a file from the remote server to the local machine.

    Args:
        ftp_client (paramiko.SFTPClient): An SFTP client object.
        source_path (str): The path of the file on the remote server.
        destination_path (Union[str, Path]): The path to save the file on the local machine.

    Returns:
        bool: True if the file is transferred successfully, False otherwise.
    """
    try:
        ftp_client.get(source_path, destination_path)
        return True
    except Exception as e:
        logger.error(f"Failed to transfer file {source_path}: {e}")
        return False


def get_local_checksum(filepath: Union[str, Path], sum_type: str = "md5") -> str:
    """
    Calculate the checksum of a local file.

    Args:
        filepath (Union[str, Path]): The path of the file.
        sum_type (str, optional): The type of checksum to calculate. Defaults to "md5".

    Returns:
        str: The checksum value.
    """
    with open(filepath, "rb") as f:
        digest = hashlib.file_digest(f, sum_type)
    return digest.hexdigest()


def get_remote_checksum(
    ssh_client: paramiko.SSHClient,
    remote_filepath: Union[str, Path],
    sum_type: str = "md5",
) -> str:
    """
    Calculate the checksum of a remote file.

    Args:
        ssh_client (paramiko.SSHClient): An SSH client object.
        remote_filepath (Union[str, Path]): The path of the file on the remote server.
        sum_type (str, optional): The type of checksum to calculate. Defaults to "md5".

    Returns:
        str: The checksum value.
    """
    if sum_type == "md5":
        command = f"md5sum {remote_filepath.as_posix()}"
    elif sum_type == "sha256":
        command = f"sha256sum {remote_filepath.as_posix()}"
    else:
        raise ValueError("Unsupported checksum type. Use 'md5' or 'sha256'.")
    stdin, stdout, stderr = ssh_client.exec_command(command)
    result = stdout.read().decode().strip()
    error = stderr.read().decode().strip()

    if error:
        logger.error(f"Error executing checksum command: {error}")

    checksum = result.split()[0]

    return checksum


def create_local_folders(
    ftp_client: paramiko.SFTPClient, source_dir: Union[str, Path], destination_dir: Path
) -> List[Path]:
    """
    Create local folders based on the directory structure of the remote server.

    Args:
        ftp_client (paramiko.SFTPClient): An SFTP client object.
        source_dir (Union[str, Path]): The path of the source directory on the remote server.
        destination_dir (Path): The path of the destination directory on the local machine.

    Returns:
        List[Path]: A list of created local directories.
    """
    dir_list = []
    source_dir = Path(source_dir).as_posix()
    for entry in ftp_client.listdir_attr(source_dir):
        mode = entry.st_mode
        if S_ISDIR(mode):
            new_dir = Path(destination_dir, entry.filename)
            logger.info(f"Creating directory at {new_dir}")
            new_dir.mkdir(exist_ok=True)
            dir_list.append(new_dir)
    return dir_list


def transfer_files_in_dir(
    ftp_client: paramiko.SFTPClient, source_dir: Path, dest_dir: Path
) -> None:
    """
    Transfer files from a source directory to a destination directory.

    Args:
        ftp_client (paramiko.SFTPClient): An SFTP client object.
        source_dir (Path): The path of the source directory on the remote server.
        dest_dir (Path): The path of the destination directory on the local machine.
    """
    source_subdir = Path(source_dir, dest_dir.name).as_posix()
    logging.debug(f"transfer_files_in_dir - Source subdir: {source_subdir}")
    for entry in ftp_client.listdir_attr(source_subdir):
        mode = entry.st_mode
        if S_ISREG(mode):
            source_filepath = Path(source_subdir, entry.filename).as_posix()
            destination_filepath = Path(dest_dir, entry.filename)
            logger.info(f"Transferring {source_filepath} to {destination_filepath}")
            transferred = transfer_file(
                ftp_client, source_filepath, destination_filepath
            )
            if not transferred:
                logger.warning(f"Failed to transfer file {source_filepath}")


def transfer_subdirectories(
    ftp_client: paramiko.SFTPClient, source_dir: Path, destination_dir: Path
) -> bool:
    """
    Transfer subdirectories from the remote server to the local machine.

    Args:
        ssh_client (paramiko.SSHClient): An SSH client object.
        source_dir (Path): The path of the source directory on the remote server.
        destination_dir (Path): The path of the destination directory on the local machine.

    Returns:
        bool: True if the directories are transferred successfully, False otherwise.
    """
    logger.info(
        f"Transferring subdirectories. Source: {source_dir}, Dest: {destination_dir}"
    )
    try:
        dir_list = create_local_folders(ftp_client, source_dir, destination_dir)
        for dest_subdir in dir_list:
            transfer_files_in_dir(ftp_client, source_dir, dest_subdir)
        return True
    except Exception as e:
        logger.error(f"Failed to transfer directories: {e}")
        return False


def transfer_all_directories(
    ssh_client: paramiko.SSHClient, source_dir: Path, destination_dir: Path
) -> bool:
    """
    Transfer all directories from the remote server to the local machine.

    Args:
        ssh_client (paramiko.SSHClient): An SSH client object.
        source_dir (Path): The path of the source directory on the remote server.
        destination_dir (Path): The path of the destination directory on the local machine.

    Returns:
        bool: True if the directories are transferred successfully, False otherwise.
    """
    logger.info(
        f"Transferring all directories. Source: {source_dir}, Dest: {destination_dir}"
    )
    try:
        ftp_client = ssh_client.open_sftp()
        # Get the list of directories in the source directory
        dir_list = create_local_folders(ftp_client, source_dir, destination_dir)
        for dest_subdir in dir_list:
            source_subdir = Path(source_dir, dest_subdir.name).as_posix()
            logger.info(
                f"Transfer all directories: Source subdir: {source_subdir}, dest subdir {dest_subdir}"
            )
            transfer_subdirectories(ftp_client, source_subdir, dest_subdir)
        ftp_client.close()
        return True
    except Exception as e:
        logger.error(f"Failed to transfer directories: {e}")
        return False


@click.command()
@click.option("--user", required=True, help="User to use for SSH connection.")
@click.option(
    "--central-storage", required=True, type=Path, help="CENTRAL_STORAGE location."
)
def main(user, central_storage):
    logger.info(f"User: {user}")
    with open(YAML_FILE) as f:
        rpis = yaml.safe_load(f)
    ip = rpis[user]
    ssh_client = get_ssh_client(user, ip)
    source_dir = Path(
        f"/home/{user}/myssd/"
    ).as_posix()  # Source directory on the remote server
    logger.info(f"Source dir: {source_dir}, Central Storage: {central_storage}")
    result = transfer_all_directories(ssh_client, source_dir, central_storage)
    ssh_client.close()
    logger.info(f"Transfer result: {result}")


if __name__ == "__main__":
    main()
