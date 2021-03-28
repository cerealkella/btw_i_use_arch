import subprocess
import os
from pathlib import PosixPath
import wget
import tarfile
import configparser


class Install():
    """Installer Class for btw_i_use_arch"""
    def __init__(self):
        self._base_user_dir = PosixPath("~/").expanduser()
        self._email = ""

    def git_config(self):
        """
        Configure Git Global Settings
        """
        git_config = f"{self._base_user_dir}/.gitconfig"
        if git_config.exists():
            config = configparser.ConfigParser()
            config.read("/home/justin/.gitconfig")
            self.email = config["user"]["email"]

    def ssh_keys(self):
        """Create SSH keys for Github, Gitlab or miscellaneous servers"""
        add_keys = input("Do you want to create SSH keys? (Y/N) ")
        while add_keys.lower() == "y":
            print("Okay, adding SSH keys...")
            print("Accept the default key name unless adding multiple git services.")
            print("You'll also probably want to generate a secure passphrase for it.")
            subprocess.run(f"ssh-keygen -t ed25519 -C {self._email}", shell=True)
            print("Ok, cool. Now add it to gitlab / github under profile > SSH Keys.")
            print("Starting the ssh-agent...")
            subprocess.run('eval "$(ssh-agent -s)"', shell=True)
            print("Adding private key to the agent...")
            key_name = "id_ed25519"
            if (
                input(
                    f"Did you call it something other than {key_name} (Y/N)? "
                ).lower()
                == "y"
            ):
                key_name = input("What did you call it? e.g. gitlab / github: ")
            subprocess.run(f"ssh-add ~/.ssh/{key_name}", shell=True)
            print("Ok, cool. Now add it to gitlab / github under profile > SSH Keys.")
            subprocess.run(
                f"xclip -selection clipboard < ~/.ssh/{key_name}.pub", shell=True
            )
            print(
                f"The contents of the {key_name}.pub file were copied to your clipboard"
            )
            print(
                """Go ahead and paste that into the appropriate dialog box in the web UI. If
                creating keys to connect to a remote server, add contents of the .pub file to
                ~/.ssh/authorized_keys
                Ensure the local ~/.ssh/config file references the server properly.
                """
            )
            ssh_config = PosixPath("~/.ssh/config").expanduser()
            if ssh_config.exists():
                print("Existing .ssh/config file. Skipping this part. UPDATE MANUALLY")
            else:
                print("Copying the ssh config file to the ~.ssh/ folder...")
                print("You'll want to ensure the variables are set correctly!")
                subprocess.run(f"cp config/ssh_config.conf {ssh_config}", shell=True)
            add_keys = input("Do you want to add an additional SSH key? (Y/N) ")

    def install_vscode_exts(self):
        """Install VSCODE Extensions from vscode-extensions.txt"""
        if input("Do you want to install VSCode Extensions? (Y/N) ").lower() == "y":
            with open("vscode-extensions.txt") as f:
                extensions = [line.rstrip() for line in f]
            for ext in extensions:
                subprocess.run(f"code --install-extension {ext}", shell=True)
        else:
            print("Skipping vscode extension installation.")

    def install_omz(self):
        """
        oh-my-zsh
        The oh-my-zsh script switches the default
        shell to zsh, so I believe the following line is unnecessary:
        # "chsh -s $(which zsh)",
        """
        if input("Install Oh-My-Zsh? (Y/N) ").lower() == "y":
            commands = [
                'sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"',
                "git clone https://github.com/zsh-users/zsh-autosuggestions ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions",
                "git clone https://github.com/zsh-users/zsh-syntax-highlighting ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting",
                "cp config/.zshrc $HOME/.zshrc",
            ]
            for command in commands:
                subprocess.run(command, shell=True)
        else:
            print("Skipping omz installation.")

    def enable_ssh(self):
        """
        SSH Daemon disabled by default on Manjaro Systems
        Enable it
        """
        if input("Enable SSH Daemon? (Y/N) ").lower() == "y":
            commands = [
                "sudo systemctl enable sshd.service",
                "sudo systemctl start sshd.service",
            ]
            for command in commands:
                subprocess.run(command, shell=True)
        else:
            print("Skip enabling ssh service.")

    def install_nvidia_nonfree(self):
        """
        Optionally install nonfree graphics card...
        https://wiki.manjaro.org/index.php?title=Configure_Graphics_Cards
        """
        if (
            input("Would you like to install the nonfree nvidia driver? (Y/N) ").lower()
            == "y"
        ):
            print("Okay, installing the nonfree graphics driver...")
            subprocess.run("sudo mhwd -a pci nonfree 0300", shell=True)
            print("You'll want to reboot for this to take effect")
        else:
            print("Skipping nonfree driver installation.")

    def fix_pppd(self):
        """
        Optionally fix pppd permissions for NetExtender to work
        Only necessary if planning to use SonicWall NetExtender
        to connect to a VPN
        """
        if input("Are you planning to use NetExtender? (Y/N) ").lower() == "y":
            print("Okay, fixing pppd service permissions...")
            subprocess.run("sudo chmod 4755 /usr/sbin/pppd", shell=True)
            print("Fixed 'em - NetExtender should work now")
        else:
            print("Skipping pppd service permissions fix.")

    def custom_steam_proton(self):
        """
        Pull down the latest Steam Custom Proton version.
        Note: Will not create entire directory structure if not found, only
        the "compatibilitytools.d" subdirectory. Ensure proper directory
        structure is in place prior to running.

        Github Repo:
        https://github.com/GloriousEggroll/proton-ge-custom
        Latest Version:
        https://github.com/GloriousEggroll/proton-ge-custom/releases/latest
        """
        print(
            """This modules installs a custom version [5.21-GE-1] of Proton for Steam.
                It requires that you have logged into steam at least once to build the
                directory structure. Choose 'N' if you haven't logged in yet. """
        )
        if (
            input(
                "Do you want to install a custom Proton version for Steam (Y/N) "
            ).lower()
            == "y"
        ):
            tarball = "https://github.com/GloriousEggroll/proton-ge-custom/releases/download/5.21-GE-1/Proton-5.21-GE-1.tar.gz"
            filename = wget.download(tarball)
            proton_path = PosixPath("~/.steam/root/compatibilitytools.d").expanduser()
            if proton_path.exists():
                pass
            else:
                proton_path.mkdir()
            tar = tarfile.open(filename)
            tar.extractall(path=proton_path)
            os.remove(filename)
            return True
        else:
            print("Skipping custom Steam Proton installation.")

    def install_joplin(self):
        """
        Run Joplin Notes installer
        """
        commands = [
            "wget -O - https://raw.githubusercontent.com/laurent22/joplin/dev/Joplin_install_and_update.sh | bash",
        ]
        for command in commands:
            subprocess.run(command, shell=True)
        return 0

    def touchpad_gestures(self):
        """
        Optionally add gestures for laptop touchpads
        """
        if input("Are you planning to use touchpad gestures? (Y/N) ").lower() == "y":
            print("Okay, adding user to input group...")
            subprocess.run("sudo gpasswd -a $USER input", shell=True)
            print("Copying config file...")
            subprocess.run("cp config/libinput-gestures.conf $HOME/.config", shell=True)
            print("Setting libinput-gestures to automatically start...")
            subprocess.run("libinput-gestures-setup autostart", shell=True)
            subprocess.run("libinput-gestures-setup start", shell=True)
            print(
                "Enable gestures! ref: https://github.com/bulletmark/libinput-gestures"
            )
        else:
            print("Skipping touchpad gestures.")

    def git_dev_setup(self):
        """
        Configure git
        """
        if input("Do you need to set up git to do devstuff? (Y/N) ").lower() == "y":
            git_config = PosixPath("~/.gitconfig").expanduser()
            if git_config.exists():
                config = configparser.ConfigParser()
                config.read("/home/justin/.gitconfig")
                email = config["user"]["email"]
                print(f"Existing .gitconfig file for {email}. Skipping this part.")
            else:
                print("Let's set up the git global config!")
                name = input("What is your name: ")
                print(f"Cool. Thank you, {name}.")
                email = input("A'ight then, what's your email addy: ")
                print(f"Name = {name}")
                print(f"Email = {email}")
                print("I'M NOT DOING ERROR HANDLING FOR THIS SO RE-RUN IT IF IT BOMBS")
                print("Setting git global variables...")
                print("Setting git global name...")
                p = subprocess.run(f"git config --global user.name {name}", shell=True)
                print(p)
                print("Setting git global email...")
                p = subprocess.run(
                    f"git config --global user.email {email}", shell=True
                )
                print(p)
                print("Okay, we're done. Run this again if you screwed up.")
            """
            Optionally create SSH keys for github / gitlab
            https://docs.github.com/en/github/authenticating-to-github/adding-a-new-ssh-key-to-your-github-account
            https://docs.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent
            """
            print("SSH Keys make authentication for Github / Gitlab much simpler.")
            self.ssh_keys()
            if input("Set up ssh-agent as a service? (Y/N) ").lower() == "y":
                service_path = PosixPath(
                    "~/.config/systemd/user/ssh-agent.service"
                ).expanduser()
                subprocess.run(
                    f"cp config/ssh-agent.conf {service_path}",
                    shell=True,
                )
                # SSH Agent Socket
                # https://stackoverflow.com/questions/18880024/start-ssh-agent-on-login
                zshrc = PosixPath("~/.zshrc").expanduser()
                with open(zshrc, "a") as file_object:
                    file_object.write(
                        """\nexport SSH_AUTH_SOCK="$XDG_RUNTIME_DIR/ssh-agent.socket" """
                    )
                print("Setting ssh-agent to automatically start...")
                subprocess.run("systemctl --user enable ssh-agent", shell=True)
                subprocess.run("systemctl --user start ssh-agent", shell=True)
                print("Done configuring ssh-agent!")
            print("Clone repos using ssh now!")
            print("E.g. git clone git@gitlab:cerealkella/app-installer")
        else:
            print("Skipping git setup stuff.")

    def supervisor(self):
        """Set up supervisor service
        Using rest_uploader as a template"""
        if input("Set up rest_uploader as a supervisor service? (Y/N) ").lower() == "y":
            print("rest_uploader is the service which will auto-upload files to Joplin")
            print("Requires the following:")
            print("1. Joplin is installed")
            print("2. rest_uploader virtualenv exists")
            print("3. ~/.joplin_upload and ~/.joplin_upload/imported folders exist")
            # supervisor_path for ubuntu systems:
            # supervisor_path = "/etc/supervisor/conf.d/"
            supervisor_path = "/etc/supervisor.d/"
            subprocess.run(
                f"sudo cp config/rest_uploader.ini {supervisor_path}",
                shell=True,
            )
            subprocess.run("sudo supervisord", shell=True)
            subprocess.run("sudo supervisorctl reread", shell=True)
            subprocess.run("sudo supervisorctl update", shell=True)
            # start the supervisord daemon
            subprocess.run("sudo systemctl start supervisord.service", shell=True)
            # enable the service so it starts on restart
            subprocess.run("sudo systemctl enable supervisord.service", shell=True)

    def exit(self):
        """Exit application!"""
        return 0
