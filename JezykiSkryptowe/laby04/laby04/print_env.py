# print all environment variables in sorted order

import os
import sys

env_variables = os.environ.keys()

filtered_env_variables = (
    [env for env in env_variables if any(arg in env for arg in sys.argv[1:])]
    if len(sys.argv) > 1
    else env_variables
)


if __name__ == "__main__":
    for key in sorted(filtered_env_variables):
        print(f"{key}={os.environ[key]}")
