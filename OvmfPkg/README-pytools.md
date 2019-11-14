# Building OVMF with EDK2 Pytools

## Setup

### The Usual

* [Download & Install Python 3.x](https://www.python.org/downloads/)
* [Download & Install git](https://git-scm.com/download/)
* [Configure Git for EDK II](https://github.com/tianocore/tianocore.github.io/wiki/Windows-systems#github-help)
* [Download/Checkout the EDK II source tree from Github](https://github.com/tianocore/tianocore.github.io/wiki/Windows-systems#download)
  * Do __not___ follow the EDK II Compile Tools and Build instructions

### Differences from EDK Classic Build

* Build BaseTools using "`C:\git\edk2>python BaseTools\Edk2ToolsBuild.py [-t <ToolChainTag>]`"
  * This replaces "`edksetup Rebuild`" from the classic build system
  * For Windows `<ToolChainTag>` examples, refer to [Windows ToolChain Matrix](https://github.com/tianocore/tianocore.github.io/wiki/Windows-systems-ToolChain-Matrix), defaults to `VS2017` if not specified

* **No Action:** Manual install & setup of NASM and iASL is __not__ required, it is handled by the Pytools build system

### Install Pytools Build

* For each workspace, consider creating & using a [Python Virtual Environment](https://docs.python.org/3/library/venv.html)
* `pip install --upgrade edk2-pytool-extensions`

### Initialize dependencies (one time)

`stuart_setup -c OvmfPkg\PlatformBuild.py`

NOTE: this initializes required submodules and installs & configures both NASM and iASL

### Update dependencies (when they change)

`stuart_update -c OvmfPkg\PlatformBuild.py`

NOTE: do this every time you change the Pytools dependencies or pull (which may bring dependency changes)

## Building

OVMF has [3 versions](https://github.com/tianocore/tianocore.github.io/wiki/How-to-build-OVMF#choosing-which-version-of-ovmf-to-build)

To build them using Pytools:

First set the `TOOL_CHAIN_TAG` environment variable or pass it on the commandlines below using "`TOOL_CHAIN_TAG=<value>`" syntax.

| Platform | Commandline |
| -------- | ----------- |
| OvmfPkgIa32X64.dsc | `stuart_build -c OvmfPkg\PlatformBuild.py [TOOL_CHAIN_TAG=<TOOL_CHAIN_TAG>]`<BR>__OR__<BR>`stuart_build -c OvmfPkg\PlatformBuild.py -a IA32,X64 [TOOL_CHAIN_TAG=<TOOL_CHAIN_TAG>]`         |
| OvmfPkgIa32.dsc    | `stuart_build -c OvmfPkg\PlatformBuild.py -a IA32 [TOOL_CHAIN_TAG=<TOOL_CHAIN_TAG>]` |
| OvmfPkgX64.dsc     | `stuart_build -c OvmfPkg\PlatformBuild.py -a X64 [TOOL_CHAIN_TAG=<TOOL_CHAIN_TAG>]`  |

## References

[Installing Pytools](https://github.com/tianocore/edk2-pytool-extensions/blob/master/docs/using.md#installing)
