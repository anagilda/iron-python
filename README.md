# iron-python

Use iron-encrypted messages across projects.

The purpose of this project is to allow decryption of an `iron`-encapsulated
token, which was created with node.js, using Python.

The original implementation [`@hapi/iron`](https://github.com/hapijs/iron) provides
a way to deal with encapsulated tokens.
As useful as it is, it's written only in JavaScript, and the alternative here presented
is meant fo cross-language codebases.
