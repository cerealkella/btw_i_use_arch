import os
import tempfile
import sys
import json
from pathlib import Path, PosixPath
from appdirs import AppDirs
from uuid import uuid4
from subprocess import Popen, PIPE, run
import keyring


def run_command(command):
    """Runs a thing in the shell"""
    with Popen(command, stdout=PIPE, stderr=None, shell=True) as process:
        return process.communicate()[0].decode("utf-8")


def get_servername(match_term, uris):
    ix = 0
    while ix < len(uris):
        try:
            if uris[ix]["uri"].split()[0] == match_term:
                return uris[ix]["uri"].split()[1]
            ix += 1
        except KeyError:
            pass


def iterate_struct(struct, match_term):
    ix = 0
    array_of_aliases = []
    while ix < len(struct):
        try:
            jx = 0
            match = struct[ix]["fields"]
            print(match)
            # print(len(match))
            while jx < len(match):
                if match[jx]["name"] == "alias":
                    alias = {
                        "alias": match[jx]["value"],
                        "username": struct[ix]["login"]["username"],
                        "password": struct[ix]["login"]["password"],
                        # "server": struct[ix]["login"]["uris"][0]["uri"],
                        "server": get_servername("ssh", struct[ix]["login"]["uris"]),
                    }
                    array_of_aliases.append(alias)
                    # print(struct[ix]["name"])
                    # print(array_of_aliases)
                jx += 1
        except KeyError:
            pass
        ix += 1
    return array_of_aliases


def get_datadir() -> Path:
    """Find datadir, create it if it doesn't exist"""
    datadir = Path(AppDirs(__package__).user_data_dir)
    try:
        datadir.mkdir(parents=True)
    except FileExistsError:
        pass
    return datadir


class WardenMyBits:
    zsh_file = "00_bitwarden.zsh"
    mp_file = f"{uuid4().hex}.txt"
    temp_zsh_file = PosixPath(tempfile.gettempdir()).joinpath(zsh_file)
    temp_mp_file = get_datadir().joinpath(mp_file)
    omz_symlink = (
        PosixPath("~/").expanduser().joinpath(".oh-my-zsh/custom").joinpath(zsh_file)
    )
    omz_aliases = (
        PosixPath("~/").expanduser().joinpath(".oh-my-zsh/custom/50_aliases.zsh")
    )

    def unlock_vault(self):
        """Writes out a password file, unlocks vault, & promptly deletes the file
        requires the BitWarden Master Password to be stored in the keyring
        Run the following, with "bw_mp" set as the service_name and "bitwarden.com"
        as the username (username is not needed):
        import keyring
        keyring.set_password('bw_mp', 'bitwarden.com', 'your long super secure pw')
        """
        with open(self.temp_mp_file, "w") as file_object:
            file_object.write(keyring.get_password("bw_mp", "bitwarden.com"))
            file_object.close()
        bw_session = run_command(f"bw unlock --passwordfile {self.temp_mp_file} --raw")
        os.remove(self.temp_mp_file)
        return bw_session

    def symlink_valid(self):
        """Determines if bitwarden temp file exists and has a valid symlink"""
        if self.temp_zsh_file.is_file() and self.omz_symlink.is_file():
            return self.omz_symlink.resolve() == self.temp_zsh_file
        else:
            return False

    def remove_symlink(self, force=False):
        """Removes symlink if broken, pass force=True to force removal of symlink"""
        if not self.symlink_valid() or force:
            if self.omz_symlink.is_file():
                self.omz_symlink.unlink()
            run_command("unset BW_SESSION")
        else:
            print("Valid symlink, not removing!")

    def unlocked(self):
        unlock_check = ["bw", "sync"]
        if (
            run(unlock_check, capture_output=True).stdout.decode("utf-8")
            == "Syncing complete."
        ):
            return True
        else:
            return False

    def set_bw_session(self):
        """Sets the BW_SESSION Environment variable via the zsh custom file"""
        print("Bitwarden vault not unlocked!")
        print("Setting BW_SESSION files & variables...")
        self.remove_symlink(force=True)
        command = ["bw", "login", "--check"]
        output = run(command, capture_output=True)
        if output.stderr.decode("utf-8") == "You are not logged in.":
            # ensure API keys are stored in environment variables
            # Copy keys from Bitwarden Vault to custom zsh file
            # ~/.oh-my-zsh/custom/1_environment.zsh
            # https://bitwarden.com/help/personal-api-key/
            print("Logging in...")
            run_command("bw login --apikey")
        else:
            print("Logged in, unlocking BitWarden session...")
        bw_session = self.unlock_vault()
        with open(self.temp_zsh_file, "w") as file_object:
            file_object.write(f'export BW_SESSION="{bw_session}"')
        try:
            os.symlink("/tmp/00_bitwarden.zsh", self.omz_symlink)
        except FileExistsError:
            # symlink already exists
            pass
        return bw_session

    def get_ssh_aliases(self):
        """gets ssh aliases"""
        command = ["/usr/bin/bw", "list", "items", "--search", "ssh"]
        output = run(command, capture_output=True)
        output_json = json.loads(output.stdout.decode("utf-8"))
        aliases = iterate_struct(output_json, "ssh")
        alias_text = ""
        for alias in aliases:
            keyring.set_password(alias["alias"], alias["username"], alias["password"])
            alias_text += f"""alias {alias["alias"]}="keyring get {alias["alias"]} {alias["username"]} | /usr/bin/xsel -ib && ssh {alias["server"]} -l {alias["username"]}" """
            alias_text += "\r"
            print(alias_text)
        with open(self.omz_aliases, "w") as file_object:
            file_object.write(alias_text)


def main():
    warden = WardenMyBits()
    if not warden.unlocked():
        warden.set_bw_session()
    # warden.get_ssh_aliases()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
