# remote-gym: Hosting Gym-environments remotely

This is a module to run Gym environments remotely, to enable splitting environment hosting and agent training into separate processes (or even separate machines).
Communication between the two processes is executed by using TLS and the gRPC protocol.

Adapted `dm_env_rpc` for `Gym.env` environments.

## Usage

### Main Features

- Use the `create_remote_environment_server` method to start a `Gym.env` environment as a remotely running environment.
- Use the `RemoteEnvironment` class to manage the connection to a remotely running environment (from `create_remote_environment_server`) and provide the standardized `Gym.env` interface to your agents through a `RemoteEnvironment` object.
- Basically: `remote-gym` is to `Gym.env` as what `dm_env_rpc` is to `dm_env`.

### Getting Started

In [this example script](exploration/start_remote_environment.py) you can see how to start a remotely running environment.

In [this accompanying script](exploration/start_environment_interaction.py) you can see how to connect to and interact with the previously started environment from a separate process.

For a quick impression in this README, find a minimal environment hosting and environment interaction example below.

First process:

```py
import logging

from remote_gym import create_remote_environment_server

server = create_remote_environment_server(
    default_args={
        "entrypoint": "exploration/remote_environment_entrypoint.py",
    },
    # IP of the machine hosting the remote environment; can also be 0.0.0.0
    url=YOUR_SERVER_IP,
    # port the remote environment should use on the hosting machine
    port=PORT_FOR_REMOTE_ENVIRONMENT_TO_LISTEN,
    # not using a tuple but setting this completely to None is also possible in case only a local connection is required
    server_credentials_paths=("path/to/server.pem", "path/to/server-key.pem", "optional/path/to/ca.pem"),
)

try:
   server.wait_for_termination()
except Exception as e:
   server.stop(None)
   logging.exception(e)
```

With an `entrypoint.py` like this:

```py
import gymnasium as gym

def create_environment(enable_rendering: bool, env_id: int, **kwargs) -> gym.Env:
    return gym.make("Acrobot-v1")
```

Second process:

```py
from remote_gym import RemoteEnvironment

environment = RemoteEnvironment(
    url=YOUR_SERVER_IP,
    port=PORT_FOR_REMOTE_ENVIRONMENT_TO_RUN_ON,
    # not using a tuple but setting this completely to None is also possible in case only a local connection is required
    client_credentials_paths=("path/to/ca.pem", "optional/path/to/client.pem", "optional/path/to/client-key.pem"),
    # can be set to "human" or "rgb_array" if `enable_rendering` was set to True in remote environment hosting process
    render_mode=None,
)

done = False
episode_reward = 0
environment.reset()
while not done:
    action = environment.action_space.sample()
    _observation, reward, terminated, truncated, _info = environment.step(action)
    episode_reward += reward
    done = terminated or truncated
```

### Rendering

To preserve server resources and prevent network slowdowns, it is recommended to only enable rendering if required.
Renderings are automatically transferred from the remote management server to the RemoteEnvironment together with the
observation if the `render_mode` of the hosted environment is `rgb_array`.
The `render_mode` of the hosted environment should be controlled by the `entrypoint_kwargs` passed to the entrypoint.

## Set-Up

### Install all dependencies in your development environment

To set up your local development environment, please run:

```
poetry install
```

Behind the scenes, this creates a virtual environment and installs `remote_gym` along with its dependencies into a new virtualenv. Whenever you run `poetry run <command>`, that `<command>` is actually run inside the virtualenv managed by poetry.

You can now import functions and classes from the module with `import remote_gym`.

### Set-up for connecting the agent training process to remote environments running on a separate machine

Authenticating the communication channel via the connection of one machine to the other requires TLS (formerly SSL)
authentication.
This is achieved by using a [self-signed certificate](https://en.wikipedia.org/wiki/Self-signed_certificate),
meaning the certificate is not signed by a publicly trusted certificate authority (CA) but by a locally created CA.

> See https://github.com/joekottke/python-grpc-ssl for more details and a more in-depth tutorial on how to create the self-signed certificates.

All required configuration files to create a self-signed certificate chain can be found in the [ssl folder](/ssl).

1. The root certificate of the certificate authority (`ca.pem`) is created by following command:

   ```
   cfssl gencert -initca ca-csr.json | cfssljson -bare ca
   ```

1. The server certificate (`server.pem`) and respective private key (`server-key.pem`) is created by following command:

   ```
   cfssl gencert -ca="ca.pem" -ca-key="ca-key.pem" -config="ca-config.json" server-csr.json | cfssljson -bare server
   ```

Make sure to add all known hostnames of the machine hosting the remote environment. You can now test, whether the
client is able to connect to the server by running both example scripts.

- [`start_remote_environment`](/exploration/start_remote_environment.py) `-u SERVER.IP.HERE -p 56765  --server_certificate path\to\server.pem --server_private_key path\to\server-key.pem`
- [`start_environment_interaction`](/exploration/start_environment_interaction.py) `-u SERVER.IP.HERE -p 56765 --root_certificate path\to\ca.pem`

If the connection is not successful and the training is not starting, you can investigate on the server
(remote environment hosting machine) which IP is unsuccessfully attempting a TLS authentication to your IP by using
the [Wireshark tool](https://www.wireshark.org/download.html) with the filter `tcp.flags.reset==1 or tls.alert_message.level`.

Afterward you can add this IP to your hostnames to the [server SSL config file](/ssl/server-csr.json).

3. Optional for client authentication on the machine connecting to the remote environment:

   Create a client certificate (`client.pem`) and respective private key `client-key.pem` by running following command:

   ```
   cfssl gencert -ca="ca.pem" -ca-key="ca-key.pem" -config="ca-config.json" client-csr.json | cfssljson -bare client
   ```

Then you can use all certificates and keys:

- [`start_remote_environment`](/exploration/start_remote_environment.py) `-u SERVER.IP.HERE -p 56765  --root_certificate path\to\ca.pem --server_certificate path\to\server.pem --server_private_key path\to\server-key.pem`
- [`start_environment_interaction`](/exploration/start_environment_interaction.py) `-u SERVER.IP.HERE -p 56765 --root_certificate path\to\ca.pem --client_certificate path\to\client.pem --client_private_key path\to\client-key.pem`

## Development

### Notebooks

You can use your module code (`src/`) in Jupyter notebooks without running into import errors by running:

```
poetry run jupyter notebook
```

or

```
poetry run jupyter-lab
```

This starts the jupyter server inside the project's virtualenv.

Assuming you already have Jupyter installed, you can make your virtual environment available as a separate kernel by running:

```
poetry add ipykernel
poetry run python -m ipykernel install --user --name="remote-gym"
```

Note that we mainly use notebooks for experiments, visualizations and reports. Every piece of functionality that is meant to be reused should go into module code and be imported into notebooks.

### Contributions

Before contributing, please set up the pre-commit hooks to reduce errors and ensure consistency

```
pip install -U pre-commit
pre-commit install
```

If you run into any issues, you can remove the hooks again with `pre-commit uninstall`.

## License

© Alexander Zap, Alex Kalaverin

# Tasks

## lint

Requires: venv, update

Runs all defined pre-commit hooks.

```bash
.venv/bin/pre-commit run --config ci/.pre-commit-config.yaml --color always --all
```

## force-update

Run: once
Requires: venv

Update all pre-commit hook versions to latest releases.

```bash

    .venv/bin/pre-commit autoupdate --config ci/.pre-commit-config.yaml --color always

    uncommited="$(git diff --cached --name-only | sort -u | tr '\n' ' ' | xargs)"
    changes="$(git ls-files --deleted --modified --exclude-standard)"
    changes="$(printf "$changes" | sort -u | tr '\n' ' ' | xargs)"

    if [[ "$uncommited" =~ "\bci/\.pre-commit-config\.yaml\b" ]] || [[ "$changes" =~ "\bci/\.pre-commit-config\.yaml\b" ]]; then
        xc add-precommit
    fi
```

## publish

Run: once
Requires: venv, update

Input: mode
Environment: mode=patch

Bumps project new version, build and publish the package to repository.

```bash

xc bump "$mode"

.venv/bin/poetry build
.venv/bin/poetry publish

```

## clean

Run: once

Clean up the project working directory: remove build/, .venv/, and .ruff_cache/ directories, as well as all .pyc files and __pycache__ directories.

```bash

    rm -rf build/ || true
    rm -rf .ruff_cache/ || true

    find . -name "*.pyc" -delete || true
    find . -name "__pycache__" -type d -exec rm -rf {} + || true
```

## clean-all

Run: once

Clean up the project working directory: remove build/, .venv/, and .ruff_cache/ directories, as well as all .pyc files and __pycache__ directories.

```bash

    xc clean
    rm log/* || true
    rm -rf .venv/ || true
```

## venv

Run: once

Make virtualenv for project build & test tools, install pre-push hook.

```bash

    if [ ! -d ".venv" ]; then
        virtualenv --python python3.9 ".venv"
        .venv/bin/python -m pip install --upgrade pip
        .venv/bin/python -m pip install --upgrade \
            pipdeptree \
            poetry \
            pre-commit \
            tomli tomli_w

        .venv/bin/poetry config virtualenvs.create false
        .venv/bin/poetry install || .venv/bin/poetry update

        .venv/bin/pre-commit install \
            --config ci/.pre-commit-config.yaml \
            --color always \
            --hook-type pre-push \
            --install-hooks \
            --overwrite
    else
        [ -f ".venv/bin/activate" ]

    fi
```

## update

Run: once

Autoupdate pre-commit hooks if the last update was more than 7 days ago.

```bash

    ctime="$(date +%s)"
    mtime="$(git log -1 --format=%ct ci/.pre-commit-config.yaml)"

    result=$(((7*86400) - (ctime - mtime)))

    if [ "$result" -le 0 ]; then
        xc force-update
    fi
```

## bump

Run: once
Requires: venv

Inputs: mode
Environment: mode=patch

Prepare and commit a version update in a Git repository. Checks for uncommitted changes, ensures the current branch is master, verifies if there are any changes since the last tag, and bumps the version number.

After validating the readiness for an update, it prompts to proceed. Once confirmed, the script updates the pyproject.toml and .pre-commit-config.yaml files if necessary, commits the changes, tags the new version, and pushes the updates to the remote repository.

```bash
#!/bin/zsh

    uncommited="$(git diff --cached --name-only | sort -u | tr '\n' ' ' | xargs)"
    if [ -n "$uncommited" ]; then
        echo "uncommited changes found"
        exit 1
    fi

    #

    branch="$(git rev-parse --quiet --abbrev-ref HEAD 2>/dev/null)"
    if [ -z "$branch" ]; then
        exit 1
    elif [ "$branch" == "master" ]; then
        echo "using main master mode"
    else
        exit 1
    fi

    #

    changes="$(git ls-files --deleted --modified --exclude-standard)"
    changes="$(printf "$changes" | sort -u | tr '\n' ' ' | xargs)"

    if [ "$changes" == "README.md" ]; then
        echo "pipeline development mode"
    elif [ -n "$changes" ]; then
        echo "uncommited changes found"
        exit 1
    fi

    git fetch --tags --force
    current="$(git tag --list | sort -rV | head -n 1)" || retval="$?"
    if [ "$retval" -eq 128 ]; then
        current="0.0.0"
    elif [ "$retval" -gt 0 ]; then
        echo "something goes wrong on last used git tag fetch"
        exit "$retval"
    fi
    [ -z "$current" ] && exit 1

    if [ "$current" = '0.0.0' ]; then
        amount="1"
    else
        amount="$(git rev-list --count $current..HEAD)"
    fi

    uncommited="$(git diff --cached --name-only | sort -u | tr '\n' ' ' | xargs)"

    if [ "$amount" -eq 0 ] && [ -z "$uncommited" ]; then
        echo "no changes since $current"
        exit 1
    fi

    version="$(bump "$mode" "$current")"
    [ -z "$version" ] && exit 1

    revision="$(git rev-parse "$version" 2>/dev/null)" || retval="$?"

    if [ "$retval" -eq 128 ]; then
        echo "future tag $revision not found, continue"

    elif [ -z "$retval" ] && [ -n "$revision" ]; then

        echo "future tag $version already set to commit $revision, sync with remote branch!"
        exit 1

    else
        echo "something went wrong, version: '$version' revision: '$revision', retval: '$retval'"
        exit 2
    fi

    # non destructive stop here

    if [ -d "tests/" ]; then
        # xc test  # TODO: need fix tests!
    fi

    xc lint || true  # TODO: fix style!

    git-restore-mtime --skip-missing || echo "datetime restoration failed, return: $?, skip"
    ls -la
    echo "we ready for bump $current -> $version, press ENTER twice to proceed or ESC+ENTER to exit"

    counter=0
    while : ; do
        read -r key

        if [[ $key == $'\e' ]]; then
            exit 1

        elif [ -z "$key" ]; then
            counter=$((counter + 1))
            if [ "$counter" -eq 2 ]; then
                break
            fi
        fi
    done

    # actions starts here

    xc add-precommit

    xc update-pyproject "$current" "$version"
    xc add-pyproject

    uncommited="$(git diff --cached --name-only | sort -u | tr '\n' ' ' | xargs)"
    if [ -n "$uncommited" ]; then
        git commit -m "$branch: $version"
    fi

    git tag -a "$version" -m "$version"
    git push --tags
    git push origin "$branch"

    echo "version updated to $version"
```

## add-precommit

Requires: venv

Check and format ci/.pre-commit-config.yaml. If any changes are made, it stages the file for the next commit.

```bash

    file="ci/.pre-commit-config.yaml"

    .venv/bin/pre-commit run check-yaml --config "$file" --color always --file "$file" || value="$?"

    while true; do
        value="0"
        .venv/bin/pre-commit run yamlfix --config "$file" --color always --file "$file" || value="$?"

        if [ "$value" -eq 0 ]; then
            break

        elif [ "$value" -eq 1 ]; then
            continue

        else
            exit "$value"

        fi
    done

    uncommited="$(git diff --cached --name-only | sort -u | tr '\n' ' ' | xargs)"
    changes="$(git ls-files --deleted --modified --exclude-standard)"
    changes="$(printf "$changes" | sort -u | tr '\n' ' ' | xargs)"

    if [[ "$uncommited" =~ "\bci/\.pre-commit-config\.yaml\b" ]] || [[ "$changes" =~ "\bci/\.pre-commit-config\.yaml\b" ]]; then
        git add "$file"
        git commit -m "(ci/cd): autoupdate pre-commit"
    fi
```

## add-pyproject

Requires: venv

Check and format pyproject.toml. If any changes are made, it stages the file for the next commit.

```bash

    file="pyproject.toml"

    .venv/bin/pre-commit run check-toml --config ci/.pre-commit-config.yaml --color always --file "$file" || value="$?"

    while true; do
        value="0"
        .venv/bin/pre-commit run pretty-format-toml --config ci/.pre-commit-config.yaml --color always --file "$file" || value="$?"

        if [ "$value" -eq 0 ]; then
            break

        elif [ "$value" -eq 1 ]; then
            continue

        else
            exit "$value"

        fi
    done

    changes="$(git diff "$file")" || exit "$?"
    changes="$(printf "$changes" | wc -l)"
    if [ "$changes" -ne 0 ]; then
        git add "$file"
    fi
```

## update-pyproject

Run: once
Requires: venv

Update version in pyproject.toml file based on provided old and new version tags. It validates the version format and ensures the current tag matches the project's version before writing the new version.

```python
#!.venv/bin/python
from os import environ
from sys import argv, exit
from re import match
from pathlib import Path

import tomli_w

try:
    import tomllib as reader
except ImportError:
    import tomli as reader

ROOT = Path(environ['PWD'])

def get_version(string):
    try:
        return match(r'^(\d+\.\d+\.\d+)$', string).group(1)
    except Exception:
        print(f'could not parse version from {string}')
        exit(3)

if __name__ == '__main__':
    try:
        current_tag = get_version(argv[1])
        version_tag = get_version(argv[2])
    except IndexError:
        print('usage: xc update-pyproject <old_tag> <new_tag>')
        exit(1)

    path = ROOT / 'pyproject.toml'
    try:
        with open(path, 'rb') as fd:
            data = reader.load(fd)

    except Exception:
        print(f'could not load {path}')
        exit(2)

    try:
        current_ver = get_version(data['tool']['poetry']['version'])
        print(f'project version: {current_ver}')

    except KeyError:
        print(f'could not find version in {data}')
        exit(2)

    if current_tag != current_ver:
        if current_ver == version_tag:
            print(f'current version {current_ver} == {version_tag}, no update needed')
            exit(0)

        print(f'current tag {current_tag} != {current_ver} current version')
        exit(4)

    data['tool']['poetry']['version'] = version_tag

    try:
        with open(path, 'wb') as fd:
            tomli_w.dump(data, fd)

        print(f'project version -> {version_tag}')

    except Exception:
        print(f'could not write {path} with {data=}')
        exit(5)
```

## test

Run: once
Requires: venv

```bash

    .venv/bin/poetry run pytest -svx
```
