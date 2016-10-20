#!/bin/bash
set -eo pipefail

redis_port=${PORT:-6379}
redis_host=${HOST:-localhost}

exec {redis_socket}<>/dev/tcp/$redis_host/$redis_port

read_reply() {
    local reply
    local size
    local part

    read -n 1 -u $redis_socket replycode # the first character describes what comes next

    case $replycode in
        -) # Error
            read -u $redis_socket reply
            reply="\e[0;31m(error) $reply\e[0m" # the crazy text here means: "paint it red"
            ;;
        +) # Regular String, response value follows on the same line
            read -u $redis_socket reply
            ;;
        :) # Integer, Response value follows on the same line
            read -u $redis_socket reply
            reply="(integer) $reply"
            ;;
        \$) # Bulk string. Size follows on the same line. Next line contains `size` characters.
            read -u $redis_socket size # reads the size
            size=${size:0:${#size}-1} # eliminates last \r character. Needed for arithmetic comparison

            if [ $size -ge 0 ]; then
                # Only read the next line if the "size" is not "-1", which means "missing" value
                read -u $redis_socket reply
            else
                reply="(nil)"
            fi

            ;;
        \*) # Array. Size follows on the same line. There will be `size` more replies following
            read -u $redis_socket size
            size=${size:0:${#size}-1} # eliminates last \r character. Needed for arithmetic comparison

            reply=""
            for (( i=0; i < $size; i++ )); do # Bash has c-style for loops!
                reply="$reply$i) $(read_reply)\n" # Array replies are recursive.
            done
            ;;
        *) # Fallback...
            echo 'I DONT KNOW WHAT IM DOING. I DIE NOW'
            cat <&${redis_socket}
            ;;
    esac
    echo -e $reply
}

echo 'Loading test data into Redis...'

# TODO

# while :
# do
#     read -ep "mimi-redis> " command
#
#     if [ "$command" == "exit" ]; then break; fi;
#     if [ -z "$command"  ]; then continue; fi;
#
#    echo $command >&${redis_socket}
#
#     read_reply
# done

echo "Bye bye!"

exec {redis_socket}>&- # closes the =redis_socket= file descriptor
