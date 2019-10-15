# Proposed Architecture for SST Elements

## Table of Contents

- [Current Installation Procedure](#current-installation-procedure)
- [Proposed Installation Procedure](#proposed-installation-procedure)
  - [Separate the Elements](#separate-the-elements)
  - [Move the Elements into Individual Repositories](#move-the-elements-into-individual-repositories)
  - [Replace the Contents of the Main SST Elements Repository with the SST Elements Installer](#replace-the-contents-of-the-main-sst-elements-repository-with-the-sst-elements-installer)
  - [Add SST Elements Installer as an Optional Tool During the Installation of SST Core](add-sst-elements-installer-as-an-optional-tool-during-the-installation-of-sst-core)
  - [Enforce Strict Documentation, Testing and Code Style Guidelines](#enforce-strict-documentation,-testing-and-code-style-guidelines)

## Current Installation Procedure

The current release of SST (SST 9.0.0) provides the option to install its supported elements via download from their website. The contents of the download solely consist of the source code available on the master branch of their [GitHub repository](https://github.com/sstsimulator/sst-elements) unpacked by running the provided configuration script, `autogen.sh`. The script relies on GNU M4 and other dependencies, and generates (along with `configure.ac`) the configurations required to run the Autoconf script, `configure`. The Autoconf script generates all the Makefile configurations for the elements, and the root Makefile is used to install the elements into the user's systems.

The issue with the current installation procedure, albeit the familiar C++ library installation steps of `./configure && make install` are preserved, is that ALL the elements are downloaded and installed into the system. Installing every supported elements bloats the users' systems with unnecessary and unwanted code. The installation itself may take up to 25 minutes.

The contents also provide an ineffective `INSTALL` file. Furthermore, testing the elements is very difficult due to the lack of documentation and proper test scripts.

## Proposed Installation Procedure

### Separate the Elements

Development is already under way to separate each of the SST elements in the [`standalone` branch of lpsmodsim's fork](https://github.com/lpsmodsim/sst-elements/tree/standalone). The elements that have dependencies on other elements have mostly been separated, with the exception of those suspected to have cyclic dependencies.

### Move the Elements into Individual Repositories

Once all the elements are properly separated and considered a stable standalone element, they can be moved out of the main SST Elements repository to their individual repositories. Hosting all the separate elements on a single main repository does not introduce a solution to the issue with bloating a user's system with unwanted code.

The repositories can be grouped in a GitHub organization. This method allows third parties to contribute their elements in a convenient manner as transfership grants the administrators immediate access to the repository's contents, issues, pull requests, releases, project boards, and settings.

Custom elements may also be hosted on an individual user's repository if they do not intend to transfer ownership. The user will still be required to "register" their element with the SST maintainers by adding their repository as a trusted element.

### Replace the Contents of the Main SST Elements Repository with the SST Elements Installer

The main SST Elements repository can now host ONLY the source code of the SST Elements Installer. The installer will provide the users the capability to manage the elements on their systems. When installing a target element, the installer will locate the repository and download the necessary contents to install the element along with its dependencies.

### Add SST Elements Installer as an Optional Tool During the Installation of SST Core

### Enforce Strict Documentation, Testing and Code Style Guidelines

