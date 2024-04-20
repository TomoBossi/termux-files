if [[ ! "$TERM" =~ "screen" ]]; then
    tmux attach -t default || tmux new -s default
fi
