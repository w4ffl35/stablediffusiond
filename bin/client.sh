SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# escape the $@ to prevent shell expansion
/home/$USER/miniconda3/envs/ldm/bin/python  $SCRIPT_DIR/send.py "$@"