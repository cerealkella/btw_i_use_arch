import subprocess
import os
import shutil
from pathlib import PosixPath
import wget
import tarfile
import configparser


class Install:
    """Installer Class for btw_i_use_arch"""

    def __init__(self):
        self._base_user_dir = PosixPath("~/").expanduser()
        self._email = ""

    def _git_config(self):
        """
        Configure Git Global Settings
        """
        git_config = self._base_user_dir.joinpath(".gitconfig")
        if git_config.exists():
            config = configparser.ConfigParser()
            config.read(git_config)
            self._email = config["user"]["email"]
            return True
        else:
            print("Run Git Dev Setup!")
            return False

    def SSH_Keys(self):
        """Create SSH keys for Github, Gitlab or miscellaneous servers \nsubprocess.run(f"ssh-keygen -t ed25519 -C {self._email}", shell=True)"""
        add_keys = input("Do you want to create SSH keys? (Y/N) ")
        while add_keys.lower() == "y":
            print("Okay, adding SSH keys...")
            print(
                """Accept the default key name unless
                     adding multiple git services."""
            )
            print("Best practice is to generate a secure passphrase.")
            if self._git_config():
                """
                > ssh-keygen -t ed25519 -C {self._email}", shell=True)
                """
                subprocess.run(f"ssh-keygen -t ed25519 -C {self._email}", shell=True)
            else:
                return -1
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
                key_name = input("What did you call it? e.g. gitlab/github: ")
            subprocess.run(f"ssh-add ~/.ssh/{key_name}", shell=True)
            subprocess.run(
                f"xclip -selection clipboard < ~/.ssh/{key_name}.pub", shell=True
            )
            print(f"Contents of {key_name}.pub were copied to the clipboard")
            print("Ok. Now add it the server to which you're connecting.")
            print("For Gitlab/Github, look under profile > SSH Keys.")
            print("Paste that into the appropriate dialog box in the web UI.")
            print("Creating keys to connect to a remote server?")
            print("Add contents of the .pub file to ~/.ssh/authorized_keys")
            print("Ensure the local ~/.ssh/config file references the server")
            ssh_config = self._base_user_dir.joinpath(".ssh/config")
            if ssh_config.exists():
                print("Existing .ssh/config file. Skipping this part. UPDATE MANUALLY")
            else:
                print("Copying the ssh config file to the ~.ssh/ folder...")
                print("You'll want to ensure the variables are set correctly!")
                shutil.copyfile(src="config/ssh_config.conf", dst=ssh_config)
            add_keys = input("Add an additional SSH key? (Y/N) ")
        return 0

    def Install_VSCode_Extensions(self):
        """Install vscode extensions from vscode-extensions.txt"""
        if input("Do you want to install VSCode Extensions? (Y/N) ").lower() == "y":
            with open("packages/vscode-extensions.txt") as f:
                extensions = [line.rstrip() for line in f]
            for ext in extensions:
                subprocess.run(f"code --install-extension {ext}", shell=True)
        else:
            print("Skipping vscode extension installation.")
        return 0

    def First_Install_System_Updates(self):
        """Install OS Updates using pacman. Run these first!"""
        return (subprocess.run("sudo pacman -Syyu", shell=True)).returncode

    def Install_Packages(self):
        """Install a whole lotta stuff using yay. Ensure yay is installed! (https://www.tecmint.com/install-yay-aur-helper-in-arch-linux-and-manjaro/)"""
        return (subprocess.run("yay -S - < packages/pkglist.txt --needed", shell=True)).returncode

    def ZSH_Config_File_Deploy(self):
        custom_files = ["aliases.zsh", "environment.zsh"]
        for cf in custom_files:
            print(f"Copying custom file {cf} to .oh-my-zsh/custom...")
            shutil.copyfile(src=f"config/{cf}", dst=f"{self._base_user_dir}/.oh-my-zsh/custom/{cf}")
        print("Done!")
        print("Manual edits may be necessary for the custom files to be useful!")
        return 0

    def Install_Oh_My_ZSH(self):
        """Installs oh-my-zsh and sets zsh to default shell and copies base .zsh config file"""
        commands = [
            'sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"',
            "git clone https://github.com/zsh-users/zsh-autosuggestions ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions",
            "git clone https://github.com/zsh-users/zsh-syntax-highlighting ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting",
            "git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k",
        ]
        for command in commands:
            subprocess.run(command, shell=True)
        print("Copying .zshrc to base user home folder...")
        shutil.copyfile(src="config/.zshrc", dst=f"{self._base_user_dir}/.zshrc")
        self.ZSH_Config_File_Deploy()
        return 0

    def VSCode_Theme_Set(self):
        """Changes theme and terminal for Code - OSS"""
        destination = f"{self._base_user_dir}/.config/Code - OSS/User/settings.json"
        shutil.copyfile(src="config/code-settings.json", dst=destination)
        return 0

    def Konsole_Theme_Set(self):
        """Changes font for Konsole Terminal Theme"""
        destination = f"{self._base_user_dir}/.local/share/konsole/Breath2.profile"
        shutil.copyfile(src="config/konsole.conf", dst=destination)
        return 0

    def SSH_Service_Daemon_Enable(self):
        """SSH Daemon is disabled by default on Arch-based Systems. Enable it."""
        subprocess.run("systemctl status sshd.service", shell=True)
        print("")
        if input("Enable SSH Daemon? (Y/N) ").lower() == "y":
            commands = [
                "sudo systemctl enable sshd.service",
                "sudo systemctl start sshd.service",
            ]
            for command in commands:
                subprocess.run(command, shell=True)
        else:
            print("Skip enabling ssh service.")
        return 0

    def Install_Video_Drivers_NVIDIA_Nonfree(self):
        """(Manjaro) Install NVIDIA nonfree graphics drivers https://wiki.manjaro.org/index.php?title=Configure_Graphics_Cards"""
        if (
            input("This will install the nonfree NVIDIA driver. Continue? (Y/N) ").lower()
            == "y"
        ):
            print("Okay, installing the nonfree graphics driver...")
            subprocess.run("sudo mhwd -a pci nonfree 0300", shell=True)
            print("You'll want to reboot for this to take effect")
        else:
            print("Skipping nonfree driver installation.")
        return 0

    def NetExtender_PPPD_Fix(self):
        """Fix pppd permissions for NetExtender to work.\nOnly necessary if planning to use SonicWall VPN"""
        if input("Are you planning to use NetExtender? (Y/N) ").lower() == "y":
            print("Okay, fixing pppd service permissions...")
            subprocess.run("sudo chmod 4755 /usr/sbin/pppd", shell=True)
            print("Fixed 'em - NetExtender should work now")
        else:
            print("Skipping pppd service permissions fix.")
        return 0

    def Steam_Custom_Proton(self):
        """Pull down the latest Steam Custom Proton version."""
        """
        Note: Will not create entire directory structure if not found, only
        the "compatibilitytools.d" subdirectory. Ensure proper directory
        structure is in place prior to running.

        Github Repo:
        https://github.com/GloriousEggroll/proton-ge-custom
        Latest Version:
        https://github.com/GloriousEggroll/proton-ge-custom/releases/latest
        """
        print(
            """This module installs a custom version [5.21-GE-1] of Proton for Steam.
                It requires that you have logged into steam at least once to build the
                directory structure. Hit Ctrl+C if you haven't logged in yet. """
        )
        tarball = "https://github.com/GloriousEggroll/proton-ge-custom/releases/download/6.15-GE-2/Proton-6.15-GE-2.tar.gz"
        filename = wget.download(tarball)
        proton_path = PosixPath("~/.steam/root/compatibilitytools.d").expanduser()
        if proton_path.exists():
            pass
        else:
            proton_path.mkdir()
        tar = tarfile.open(filename)
        tar.extractall(path=proton_path)
        os.remove(filename)
        return 0

    def Joplin_Installation(self):
        """Run Joplin Notes installer"""
        commands = [
            "wget -O - https://raw.githubusercontent.com/laurent22/joplin/dev/Joplin_install_and_update.sh | bash",
        ]
        for command in commands:
            subprocess.run(command, shell=True)
        return 0

    def Laptop_Touchpad_Gestures(self):
        """Add Mac-like gestures for laptop touchpads: https://github.com/bulletmark/libinput-gestures"""
        if input("Are you planning to use touchpad gestures? (Y/N) ").lower() == "y":
            print("Okay, adding user to input group...")
            subprocess.run("sudo gpasswd -a $USER input", shell=True)
            print("Copying config file...")
            # subprocess.run("cp config/libinput-gestures.conf $HOME/.config", shell=True)
            shutil.copyfile(src="config/libinput-gestures.conf", dst=f"{self._base_user_dir}/.config/libinput-gestures.conf")
            print("Setting libinput-gestures to automatically start...")
            subprocess.run("libinput-gestures-setup autostart", shell=True)
            subprocess.run("libinput-gestures-setup start", shell=True)
            print("Enabled gestures!")
        else:
            print("Skipping touchpad gestures.")
        return 0

    def Setup_Git_for_Dev(self):
        """Configure git"""
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
            self.SSH_Keys()
            if input("Set up ssh-agent as a service? (Y/N) ").lower() == "y":
                service_path = PosixPath(
                    "~/.config/systemd/user/ssh-agent.service"
                ).expanduser()
                if not service_path.parent.is_dir():
                    service_path.parent.mkdir(parents=True)
                shutil.copyfile(src="config/ssh-agent.conf", dst=f"{service_path}")
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
            print("E.g. git clone git@github:kellerjustin/btw_i_use_arch")
        else:
            print("Skipping git setup stuff.")
        return 0

    def Supervisor_Setup(self):
        """Set up supervisor service using rest_uploader as a template"""
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
        return 0

    def Stop_Firefox_From_Trying_to_Remember_Passwords(self):
        """Make Firefox stop trying to remember passwords. Bitwarden handles those!"""
        destination_folder = f"{self._base_user_dir}/.mozilla/firefox/"
        dirs = next(os.walk(destination_folder))[1]
        for d in dirs:
            if "default-release" in d:
                destination = f"{destination_folder}/{d}/user.js"
        shutil.copyfile(src="config/firefox-user.js", dst=destination)
        print(f"Copied user.js to {destination}")
        return 0

    def VirtualBox_Installation(self):
        """Optional Installation of VirtualBox, make sure kernel matches!"""
        subprocess.run("yay -S linux510-virtualbox-host-modules virtualbox virtualbox-ext-oracle", shell=True)
        subprocess.run("sudo gpasswd -a $USER vboxusers", shell=True)
        print("Reboot for the changes to take effect!")
        return 0

    def eXit(self):
        """Exit application!"""
        return -1
