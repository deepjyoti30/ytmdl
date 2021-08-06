# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.

## Branch

> TL;DR: Make the PR's to the `unstable` branch instead of the `master` branch.

Even though the default branch is set to `master`, the actual development happens in the `unstable` branch and thus, all the PR's should be made to the `unstable` branch. The `master` branch is directly used for beta builds (eg: the `-git` version in AUR).

## Git

- Make sure the commit message is short, simple and easy to understand.
- Add the description of the change on the commit body. Explain what you changed and why you changed it and so on.

## Python

Use [pylama](https://github.com/klen/pylama) for linting.

1.Methods / Functions

- Method names should be all lower case
- Words in an method name should be separated by an underscore
- Non-public method should begin with a single underscore
- Method name should be logical, it's name should indicate what it is doing

2.Class

- Class names should follow the UpperCaseCamelCase convention

3.Modules

- Module names should be all lowercase
- If more than one word, the words should be separated by an underscore
- It is preferrable to stick to single word for the module name

4.Constants

- Constant variables should be capitalized
- If more than one word, the words can be separated by an underscore
