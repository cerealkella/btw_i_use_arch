import os
from pathlib import PosixPath
from subprocess import Popen, PIPE


def set_bw_session():
    """Sets the BW_SESSION Environmental variable via the zsh custom file"""
    bw_session = os.getenv("BW_SESSION")
    omz_env = PosixPath("~/").expanduser().joinpath(".oh-my-zsh/custom/2_environment.zsh")

    if bw_session is None or bw_session == "":

        command = "bw unlock --raw"
        with Popen(command, stdout=PIPE, stderr=None, shell=True) as process:
            bw_session = process.communicate()[0].decode("utf-8")

    with open(omz_env, "w") as file_object:
        file_object.write(f'export BW_SESSION="{bw_session}"')
    return bw_session


def unset_bw_session():
    """Unsets the BW_SESSION Environment variable"""
    command = "unset BW_SESSION"
    with Popen(command, stdout=PIPE, stderr=None, shell=True) as process:
        process.communicate()[0].decode("utf-8")


set_bw_session()
