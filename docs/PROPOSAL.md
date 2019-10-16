# Proposed Architecture for SST Elements

This document highlights current issues with SST Elements in regards to their interdependencies, build processes and legacy.

## Table of Contents

- [Issues](#issues)
  - [Installation Procedure](#installation-procedure)
  - [Documentation and Testing](#documentation-and-testing)
- [Proposed Installation Procedure](#proposed-installation-procedure)
  - [1. Separate the Elements](#1.-separate-the-elements)
  - [2. Refactor the SST Elements Repository](#2.-refactor-the-sst-elements-repository)
    - [2.1 Repositories for Individual Elements](#2.1-repositories-for-individual-elements)
    - [2.2 SST Elements Installer](#2.2-sst-elements-installer)
      - [Installation](#installation)
  - [3. Enforce Consistent Documentation, Testing and Code Style Guidelines](#3.-enforce-consistent-documentation,-testing-and-code-style-guidelines)

## Issues

### Installation Procedure

The current release of SST (SST 9.0.0) provides the option to install its supported elements via download from their website. The contents of the download solely consist of the source code available on the master branch of their [GitHub repository](https://github.com/sstsimulator/sst-elements) unpacked by running the provided configuration script, `autogen.sh`. The script relies on [GNU M4](https://www.gnu.org/software/m4/) and other dependencies, and generates (along with `configure.ac`) the configurations required to run the Autoconf script, `configure`. The Autoconf script generates all the Makefile configurations for the elements, and the root Makefile is used to install the elements into the user's systems.

The issue with the current installation procedure, albeit the familiar C++ library installation steps of `./configure && make install` are preserved, is that ALL the elements are downloaded and installed into the system. Installing every supported elements bloats the users' systems with unnecessary and unwanted code. The installation process may take up to 30 minutes.

No instructions for removing the installation exist at this time. Invoking the `clean` target on the auto-generated root Makefile is insufficient as the process leaves SST to point to elements with invalid paths and many residue files remain.

### Documentation and Testing

The downloaded contents also provide an ineffective `INSTALL` file. Furthermore, testing the elements is very difficult due to the lack of documentation and proper test scripts.

## Proposed Installation Procedure

The rest of the document briefly discusses possible solutions to the aforementioned issues along with some optional enhancements to secure the lifetime and legacy of the project.

### 1. Separate the Elements

Modify the installation process such that users are able to specify which elements to install into their systems.

[Development is already under way](https://github.com/lpsmodsim/sst-elements/tree/standalone) to separate each of the SST elements. The elements that have dependencies on other elements have mostly been separated, with the exception of those suspected to have cyclic dependencies.

### 2. Refactor the SST Elements Repository

#### 2.1 Repositories for Individual Elements

Once all the elements are properly separated and considered stable standalone libraries, they can be moved out of the main SST Elements repository to their individual repositories. Hosting all the separate elements on a single main repository does not introduce a solution to the issue with bloating a user's system with unwanted code.

The repositories can be grouped in a GitHub organization. This method allows third parties to contribute their elements in a convenient manner as ownership transfer grants the administrators immediate access to the repository's contents, issues, pull requests, releases, project boards, and settings.

Custom elements may also be hosted on an individual user's repository if they do not intend to transfer ownership. The user will still be required to "register" their element with the SST maintainers by adding their repository as a trusted element.

#### 2.2 SST Elements Installer

The main SST Elements repository can now host ONLY the source code of the SST Elements Installer. The installer will provide the users the capability to manage the elements on their systems. When installing a target element, the installer will locate the repository and download the necessary contents to install the element along with its dependencies.

##### Installation

Add SST Elements Installer as an optional tool during the installation of SST core.

### 3. Enforce Consistent Documentation, Testing and Code Style Guidelines
