# @file
# Script to Build OVMF UEFI firmware
#
# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: BSD-2-Clause-Patent
##
import os
import logging

from edk2toolext.environment import shell_environment
from edk2toolext.environment.uefi_build import UefiBuilder
from edk2toolext.invocables.edk2_platform_build import BuildSettingsManager
from edk2toolext.invocables.edk2_setup import SetupSettingsManager, RequiredSubmodule
from edk2toolext.invocables.edk2_update import UpdateSettingsManager

#
#==========================================================================
# PLATFORM BUILD ENVIRONMENT CONFIGURATION
#
class CommonPlatform():
    PackagesSupported = ("OvmfPkg",)
    ArchSupported = ("IA32", "X64")
    TargetsSupported = ("DEBUG", "RELEASE", "NOOPT")
    Scopes = ('ovmf', 'edk2-build')
    WorkspaceRoot = os.path.realpath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), ".."))


class SettingsManager(UpdateSettingsManager, SetupSettingsManager):

    def GetPackagesSupported(self):
        ''' return iterable of edk2 packages supported by this build.
        These should be edk2 workspace relative paths '''
        return CommonPlatform.PackagesSupported

    def GetArchitecturesSupported(self):
        ''' return iterable of edk2 architectures supported by this build '''
        return CommonPlatform.ArchSupported

    def GetTargetsSupported(self):
        ''' return iterable of edk2 target tags supported by this build '''
        return CommonPlatform.TargetsSupported

    def GetRequiredSubmodules(self):
        ''' return iterable containing RequiredSubmodule objects.
        If no RequiredSubmodules return an empty iterable
        '''
        rs=[]
        rs.append(RequiredSubmodule(
            "ArmPkg/Library/ArmSoftFloatLib/berkeley-softfloat-3", False))
        rs.append(RequiredSubmodule(
            "CryptoPkg/Library/OpensslLib/openssl", False))
        return rs

    def SetArchitectures(self, list_of_requested_architectures):
        ''' Confirm the requests architecture list is valid and configure SettingsManager
        to run only the requested architectures.

        Raise Exception if either list_of_requested_architectures contains an unsupported 
        architecture or more than 1 architecture specified
        '''
        unsupported = set(list_of_requested_architectures) - set(self.GetArchitecturesSupported())
        if(len(unsupported) > 0):
            errorString = ( "Unsupported Architecture Requested: " + " ".join(unsupported))
            logging.critical( errorString )
            raise Exception( errorString )
        self.ActualArchitectures = list_of_requested_architectures


    # ####################################################################################### #
    #                         Actual Configuration for Platform Build                         #
    # ####################################################################################### #
class PlatformBuilder( UefiBuilder, BuildSettingsManager):
    def __init__(self):
        UefiBuilder.__init__(self)

    def AddCommandLineOptions(self, parserObj):
        ''' Add command line options to the argparser '''
        parserObj.add_argument('-a', "--arch", dest="build_arch", type=str, default="IA32,X64",
            help="Optional - CSV of architecutre to build.  IA32 will use IA32 for Pei & Dxe. "
            "X64 will use X64 for both PEI and DXE.  IA32,X64 will use IA32 for PEI and "
            "X64 for DXE. default is IA32,X64")
        super().AddCommandLineOptions(parserObj)

    def RetrieveCommandLineOptions(self, args):
        '''  Retrieve command line options from the argparser '''
        self.arch = args.build_arch.upper().split(",")
        UefiBuilder.RetrieveCommandLineOptions(self, args)

    def GetWorkspaceRoot(self):
        ''' get WorkspacePath '''
        return CommonPlatform.WorkspaceRoot

    def GetPackagesPath(self):
        return ()

    def GetActiveScopes(self):
        ''' return tuple containing scopes that should be active for this process '''
        return CommonPlatform.Scopes

    def GetName(self):
        ''' Get the name of the repo, platform, or product being build '''
        ''' Used for naming the log file, among others '''
        return "OvmfPkg"

    def GetLoggingLevel(self, loggerType):
        ''' Get the logging level for a given type
        base == lowest logging level supported
        con  == Screen logging
        txt  == plain text file logging
        md   == markdown file logging
        '''
        return logging.DEBUG

    def SetPlatformEnv(self):
        logging.debug("PlatformBuilder SetPlatformEnv")

        arch = " ".join(self.arch)
        dscSuffix = "".join(self.arch)
        platform = "OvmfPkg/OvmfPkg" + dscSuffix + ".dsc"

        logging.debug("platform: \"" + platform + "\"")
        logging.debug("arch: \"" + arch + "\"")
        logging.debug( shell_environment.GetBuildVars().GetValue("PATH") )

        self.env.SetValue("PRODUCT_NAME",    "OVMF",    "Platform Hardcoded")
        self.env.SetValue("ACTIVE_PLATFORM", platform,  "From command line")
        self.env.SetValue("TARGET_ARCH",     arch,      "From command line")

        self.env.SetValue("LaunchBuildLogProgram", "Notepad", "default - will fail if already set", True)
        self.env.SetValue("LaunchLogOnSuccess",    "False",   "default - do not log when successful")
        self.env.SetValue("LaunchLogOnError",      "True",    "default - will fail if already set", True)

        return 0

    def PlatformPreBuild(self):
        return 0

    def PlatformPostBuild(self):
        return 0
