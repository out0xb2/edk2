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
class SettingsManager(UpdateSettingsManager, SetupSettingsManager, BuildSettingsManager):
    def __init__(self):
        pass
   #self.ActualArchitectures = ["IA32"]   # default to IA32 if no architecture specified

    def GetPackagesSupported(self):
        ''' return iterable of edk2 packages supported by this build.
        These should be edk2 workspace relative paths '''
        return ("OvmfPkg",)

    def GetArchitecturesSupported(self):
        ''' return iterable of edk2 architectures supported by this build '''
        return ("IA32","X64","IA32 X64")

    def GetTargetsSupported(self):
        ''' return iterable of edk2 target tags supported by this build '''
        return ("DEBUG", "RELEASE", "NOOPT")

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

    def GetPackagesPath(self):
        return ()

    def GetActiveScopes(self):
        ''' return tuple containing scopes that should be active for this process '''
        return ('ovmf','edk2-build')

    def GetWorkspaceRoot(self):
        ''' get WorkspacePath '''
        SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
        return os.path.realpath(os.path.join(SCRIPT_PATH,".."))

    def SetArchitectures(self, list_of_requested_architectures):
        ''' Confirm the requests architecture list is valid and configure SettingsManager
        to run only the requested architectures.

        Raise Exception if either list_of_requested_architectures contains an unsupported 
        architecture or more than 1 architecture specified
        '''
        supportedArchitectures = self.GetArchitecturesSupported()
        if(len(list_of_requested_architectures) > 1):
            errorString = (
                "Exactly 1 architecture must be specified: " + ", ".join(supportedArchitectures ))
            logging.critical( errorString )
            raise Exception( errorString )

        unsupported = set(list_of_requested_architectures) - set(supportedArchitectures)
        if(len(unsupported) > 0):
            errorString = ( "Unsupported Architecture Requested: " + " ".join(unsupported))
            logging.critical( errorString )
            raise Exception( errorString )

        # !!! HOWTO: recommended mechanism to pass to UefiBuilder ?

    # ####################################################################################### #
    #                             Extra CmdLine configuration                                 #
    # ####################################################################################### #

    def AddCommandLineOptions(self, parserObj):
        ''' Add command line options to the argparser '''
        pass

    def RetrieveCommandLineOptions(self, args):
        '''  Retrieve command line options from the argparser '''
        pass


    # ####################################################################################### #
    #                         Actual Configuration for Platform Build                         #
    # ####################################################################################### #
class PlatformBuilder( UefiBuilder ):

    def SetPlatformEnv(self):
        logging.debug("PlatformBuilder SetPlatformEnv")

        self.env.SetValue("PRODUCT_NAME",    "OVMF",                    "Platform Hardcoded")
        self.env.SetValue("ACTIVE_PLATFORM", "OvmfPkg/OvmfPkgIa32.dsc", "Platform Hardcoded")
        self.env.SetValue("TARGET_ARCH",     "IA32",                    "Platform Hardcoded")
        self.env.SetValue("TOOL_CHAIN_TAG",  "VS2017",                  "Default tool chain")

        self.env.SetValue("LaunchBuildLogProgram", "Notepad", "default - will fail if already set", True)
        self.env.SetValue("LaunchLogOnSuccess",    "False",   "default - do not log when successful")
        self.env.SetValue("LaunchLogOnError",      "True",    "default - will fail if already set", True)

        return 0

    def SetPlatformEnvAfterTarget(self):
        return 0

    def PlatformPreBuild(self):
        return 0

    def PlatformPostBuild(self):
        return 0
