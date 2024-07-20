## start ssh server:
# sshd
## stop ssh server and ongoing sessions:
# pkill sshd

alias l='ls -a'
alias c='clear'
alias e='exit'
alias a='ani-cli'
alias pkg-backup='pkg list-installed | tee pkg_list-installed.txt'

if [[ ! "$TERM" =~ "screen" ]]; then
    tmux attach -t default || tmux new -s default
fi
