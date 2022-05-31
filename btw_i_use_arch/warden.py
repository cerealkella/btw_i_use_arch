import os
import sys
import json
from pathlib import PosixPath
from subprocess import Popen, PIPE, run, call


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
                    alias = {"alias": match[jx]["value"],
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


class WardenMyBits:
    zsh_file = "00_bitwarden.zsh"
    tempfile = PosixPath("/tmp/").joinpath(zsh_file)
    omz_symlink = (
        PosixPath("~/").expanduser().joinpath(".oh-my-zsh/custom").joinpath(zsh_file)
    )

    def symlink_valid(self):
        """Determines if bitwarden temp file exists and has a valid symlink"""
        if self.tempfile.is_file() and self.omz_symlink.is_file():
            return self.omz_symlink.resolve() == self.tempfile
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
            print("Logging in...")
            bw_session = run_command("bw login --raw")
        else:
            print("Logged in, unlocking BitWarden session...")
            bw_session = run_command("bw unlock --raw")
        with open(self.tempfile, "w") as file_object:
            file_object.write(f'export BW_SESSION="{bw_session}"')
        os.symlink("/tmp/00_bitwarden.zsh", self.omz_symlink)
        return bw_session

    def get_ssh_aliases(self):
        """gets ssh aliases"""
        command = ["/usr/bin/bw", "list", "items", "--search", "ssh"
        ]
        output = run(command, capture_output=True)
        output_json = json.loads(output.stdout.decode("utf-8"))
        aliases = iterate_struct(output_json, "ssh")
        for alias in aliases:
            print(alias)


def main():
    warden = WardenMyBits()
    if not warden.unlocked():
        warden.set_bw_session()
    jason = warden.get_ssh_aliases()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
