import os
import sys
from pathlib import PosixPath
from subprocess import Popen, PIPE, run


def run_command(command):
    """Runs a thing in the shell"""
    with Popen(command, stdout=PIPE, stderr=None, shell=True) as process:
        return process.communicate()[0].decode("utf-8")


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


def main():
    warden = WardenMyBits()
    if not warden.unlocked():
        warden.set_bw_session()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
