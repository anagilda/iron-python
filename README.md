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

## Running support scripts

1. Make sure you have [`Node.js`](https://nodejs.org/en/download/) and npm installed
   ([download](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) and install them, if not).

    You can check the versions like so:

    ```bash
    $ node --version
    v12.22.3
    ```

    ```bash
    $ npm --version
    6.14.13
    ```

2. Install the npm dependencies:

    ```bash
    cd scripts && npm install
    ```

### Iron Seal

Seal the cookie by providing a new token value (as found in the tokens mongo collection), and the password for encryption:

```bash
node iron_seal.js password="thepasswordmustbeatleast32characters" token="token-to-encrypt"
```
