# Contributing

## Styleguide

### Linting/verifying your source code

You can refactor your code for it being properly formatted and adheres to coding style by running:

```bash
source venv/bin/activate
black *
```

## Creating Branches And Merge
All branches are creating from the develop branch and merging into the develop by the pull request. The develop branch merging in the master and putting the release tag for the release deploying.

### Name Format
The name has a special format that includes a **type** and **subject**:

```
<type>/<subject>
```

Samples:

```
feature/change-models
```
```
fix/01235
```
```
refactor/change-user-models
```

#### Type
Must be one of the following:

* **feature**: A new feature
* **fix**: A bug fix
* **hotfix**: A hot fix
* **performance**: A code change that improves performance
* **refactor**: A code change that neither fixes a bug or adds a feature
* **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
* **test**: Adding missing tests or correcting existing tests

#### Subject

The subject contains relevant issues, or a succinct description of the change.


## Submitting Pull Request

### Name Format
The name has a special format that includes a **type** and **subject**:

```
[<type>] <subject>
```

Samples:

```
[FEATURE] Camera filters
```
```
[BUGFIX] FW-1234
```
```
[RELEASE] x.x.x
```

#### Type
Must be one of the following:

- **CHORE**: Build process or auxiliary tool changes	
- **DOCS**: Documentation only changes
- **FEATURE**: A new feature
- **BUGFIX**: A bug fix
- **PERFOMANCE**: A code change that improves performance
- **REFACTOR**: A code change that neither fixes a bug or adds a feature
- **STYLE**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- **TEST**: Adding missing tests or correcting existing tests
- **RELEASE**: A new release
- **HOTFIX**: A hot fix

#### Subject

The subject contains relevant issues, or a succinct description of the change.

### Description Format

Each pull request description consists of a **current behavior** and a **new behavior**.

```
What is the current behavior?
<current behavior>

What is the new behavior?
<new behavior>
```

#### Current Behavior

Please describe the current behavior that you are modifying.

#### New Behavior

Please describe the new behavior.

### Commit Message Format
The message has a special format that includes a **type** and **subject**:

The line of the commit message cannot be longer 120 characters! This allows the message to be easier
to read on TFS as well as in various git tools.

#### Revert
If the commit reverts a previous commit, it should begin with `revert: `, followed 
by the header of the reverted commit. In the body it should say: `This reverts commit <hash>.`, 
where the hash is the SHA of the commit being reverted.

#### Type
Must be one of the following:

* **chore**: Build process or auxiliary tool changes	
* **docs**: Documentation only changes
* **feat**: A new feature
* **fix**: A bug fix
* **perf**: A code change that improves performance
* **refactor**: A code change that neither fixes a bug or adds a feature
* **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
* **test**: Adding missing tests or correcting existing tests

#### Subject
The subject contains a succinct description of the change:

* use the imperative, present tense: "change" not "changed" nor "changes"
* don't capitalize the first letter
* no dot (.) at the end

## Release
For Pull Requests of type [RELEASE] use Semantic Versioning for the Subject.

A normal version number must take the form X.Y.Z where X, Y, and Z are non-negative integers, and must not contain leading zeroes.

* X is the major version
* Y is the minor version
* Z is the patch version

Each element must increase numerically.
For instance: 1.9.0 -> 1.10.0 -> 1.11.0.
```
[RELEASE] 1.9.0
[RELEASE] 1.10.0
[RELEASE] 1.11.0
```

#### Major version

Major version X (X.y.z) must be incremented if any backwards incompatible changes are introduced.

It may also include minor and patch level changes.

Patch and minor version must be reset to 0 when major version is incremented.

#### Minor version
Minor version Y (x.Y.z) must be incremented if new, backwards compatible functionality is introduced.

It may be incremented if substantial new functionality or improvements are introduced within the private code.

It may include patch level changes.

Patch version must be reset to 0 when minor version is incremented.

#### Patch version
Patch version Z (x.y.Z) must be incremented if only backwards compatible bug fixes are introduced.

A bug fix is defined as an internal change that fixes incorrect behavior.

## Main branches

### Master
This branch contains the current Production version.

All pull requests in this branch are of type [RELEASE].

### Backup
To be able to easily and quickly roll back the version of the code in the `master` branch to the previous Release, `backup` branch is used.

It is necessary to update this branch in accordance with the current `master` branch before each Release in the `master` branch.

### Develop
This branch contains code under development.

This version of the code is deployed to the development server for checking before being included in the branch `master` and deployed to the Production server.
