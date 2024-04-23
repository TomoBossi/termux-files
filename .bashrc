## start ssh server:
# sshd
## stop ssh server:
# ps -A
# kill <pid_sshd>
sshd-stop() {
	kill $(cat /data/data/com.termux/files/usr/var/run/sshd.pid)
}

alias la='ls -a'

if [[ ! "$TERM" =~ "screen" ]]; then
    tmux attach -t default || tmux new -s default
fi
