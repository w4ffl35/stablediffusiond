import os
import logger
from settings import SCRIPTS, GENERAL

SCRIPTS_ROOT = GENERAL["sd_scripts"]
PYTHON_PATH = GENERAL["sd_python_path"]


# run python script from console
def run_script(script_name, user_options):
    # build list of all user options
    option_overrides = {}
    for option in user_options:
        option_overrides[option[0]] = option[1]

    if SCRIPTS.__contains__(script_name):
        logger.info(f"Running script {script_name}...")
        # iterate over script arguments and build command line options
        options = ""
        for option in SCRIPTS[script_name]:
            val = option[1]
            if option[0] in option_overrides:
                val = option_overrides[option[0]]
            options += f"--{option[0]} {val} "

        # call the script
        os.system(f"{PYTHON_PATH} {SCRIPTS_ROOT}{script_name}.py {options}")
    else:
        logger.error(f"Script {script_name} not found in script settings")


run_script("txt2img", [
])
