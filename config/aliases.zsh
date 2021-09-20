# updates!
alias updoots="yay -Syyu"

# Source Reload
alias sourcemyshit="source ~/.zshrc"

# RDP
alias rdp="xfreerdp /v:$RDP_HOST /u:$DOMAIN_USERNAME /d:$DOMAIN /p:(bw get password 6c5f769f-b631-43a6-825d-a9bc014e7c96) /f"

# Bitwarden setup
alias wardenmybits="python $HOME/btw_i_use_arch/btw_i_use_arch/warden.py"

# SimpleHelp App
alias simplehelp_app="'$HOME/.JWrapper/JWrapper-SimpleHelp Technician/SimpleHelp TechnicianLinLauncher64' JWVAPP SimpleHelp_Technician"
alias simplehelp="bw get password 'Simplehelp Admin' | xclip -sel clip && simplehelp_app"
