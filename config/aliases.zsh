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

# GitHub SSH Passphrase to clipboard Example (laptop)
# example to find id:
# bw list items --search github | jq ".[0].id"
alias github_passphrase="bw get item '89c604f4-a57b-4df4-882f-a9bc014e7c96' | jq '.fields[0].value' | xclip -sel clip"
# GitLab
alias gitlab_passphrase="bw get item 'f1f1ca3f-135d-426c-8250-a9bc014e7c96' | jq '.fields[0].value' | xclip -sel clip"
