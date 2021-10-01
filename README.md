# iron-python

Use iron-encrypted messages across projects.

The purpose of this project is to allow decryption of an `iron`-encapsulated
token, which was created with node.js, using Python.

The original implementation [`@hapi/iron`](https://github.com/hapijs/iron) provides
a way to deal with encapsulated tokens.
As useful as it is, it's written only in JavaScript, and the alternative here presented
is meant fo cross-language codebases.

## Setting up the project

1. Clone the project, and move into its root directory.

    ```bash
    git clone git@github.com:anagilda/iron-python.git
    cd iron-python
    ```

2. Install a fresh new virtual environment, and activate it.

    ```bash
    python3 -m venv ./venv
    source venv/bin/activate
    ```

3. Install the necessary requirements.

    ```bash
    pip install -r requirements.txt
    ```
