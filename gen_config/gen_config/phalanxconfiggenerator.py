#!/usr/bin/env python3

# Run this with no arguments.  It will generate the values files in the
# directory above the one where this script lives.
#
# This is handy because, as long as we're specifying the Telegraf TOML
# directly, which we have to do because telegraf-ds hasn't been updated to
# template version 2, we can't do the input and output splitting we want to
# do.

import glob
import json
import logging
import os
import re
import sys
import yaml

from os.path import basename
from pathlib import Path
from typing import Any, Dict, Set, Tuple

LOGLEVEL = {"CRITICAL": 50,
            "ERROR": 40,
            "WARNING": 30,
            "INFO": 20,
            "DEBUG": 10,
            "NOTSET": 0
            }

class PhalanxConfigGenerator(object):
    """
    The PhalanxConfigGenerator parses the science-platform configurations
    to determine what services run in which environments.  It should then be
    subclassed for particular applications to generate configuration files to
    write.

    A subclass (corresponding to a particular Phalanx application) must do the
    following: set self.output_path (generally,
    self.phalanx_root + "/services/<application_name>") and provide
    an implementation of the build_config() method to generate configuration
    for each instance of the application.
    """
    def __init__(self, *args, **kwargs) -> None:
        loglevel_str=kwargs.get("loglevel","warning")
        self.debug=kwargs.get("debug",False)
        if self.debug:
            loglevel_str="debug"
        loglevel_str=loglevel_str.upper()
        loglevel=LOGLEVEL.get(loglevel_str, 30)
        logging.basicConfig(encoding='utf-8',level=loglevel)
        self.log = logging.getLogger()
        self.template_re = re.compile('(\{\{.*?\}\})')
        self.instances: Dict[str,Any] = {}
        self.applications: Tuple(str) = tuple()
        self.config: Dict[str,str] = {}
        self.namespaces: Dict[str,Set[str]] = {}
        self.phalanx_root: str = kwargs.get("phalanx_root","")
        if not self.phalanx_root:
            try:
                me = Path.resolve(Path(__file__))
                # gen_config/gen_config
                self.phalanx_root = str(me.parents[2])
            except NameError:
                me = Path.resolve(Path(sys.argv[0]))
                # gen_config
                self.phalanx_root = str(me.parents[1])
        self.dry_run: bool = kwargs.get("dry_run", False)
        self.load_phalanx()
        self.log.debug(f"Phalanx root: {self.phalanx_root}")
        self.log.debug(f"Applications: {self.applications}")

    def _get_science_platform_path(self) -> str:
        """Convenience method to extract the science-platform root directory.
        """
        me = Path.resolve(Path(sys.argv[0]))
        # ./..[telegraf-ds]/..[services]/science-platform
        sp_path = self.phalanx_root + "/science-platform"
        return sp_path

    def load_phalanx(self) -> None:
        """Populate our instance attributes with data from our yaml."""
        self.instances = self.find_instances()
        self.applications = self.find_applications()
        self.namespaces = self.find_app_namespaces()
        
    def find_instances(self) -> Dict[str,Any]:
        """Read the science-platform config to determine which instances
        there are."""
        val_path = self._get_science_platform_path()
        val_files = glob.glob(val_path + "/values-*yaml")
        inst_settings = dict()
        for v in val_files:
            iname = v.split('-')[-1][:-5]
            with open(v) as f:
                inst_settings[iname] = yaml.safe_load(f)
        # ArgoCD is not specified but implicitly present everywhere.
        for inst in inst_settings:
            inst_settings[inst]["argocd"] = { "enabled": True }
        return inst_settings

    def find_applications(self) -> Tuple[str]:
        """Find all the defined applications from science-platform config."""
        val_path = self._get_science_platform_path()
        val_file = val_path + "/values.yaml"
        applications = tuple()
        # ArgoCD is implicitly present everwhere
        applications += ("argocd",)
        with open(val_file) as f:
            apps=yaml.safe_load(f)
        for app in apps:
            if "enabled" not in apps[app]:
                continue
            applications += (app,)
        return applications

    def find_app_namespaces(self) -> Dict[str,Set[str]]:
        """From our list of applications, parse the application YAML for each
        to determine whether it has namespaces, and create that mapping.
        """
        apps = self.applications
        ns = {}
        for app in apps:
            ns[app] = self.parse_app_template(app)
        return ns
            
    def parse_app_template(self, app:str) -> Set[str]:
        """Read the application definition to extract its namespace(s) if any.
        """
        # In general, if there's a namespace defined for the app, there's
        # only one and it's the app name with _ replaced by -, so all this
        # is kind of superfluous.
        val_path = self._get_science_platform_path()
        namespaces = set()
        if app == "vault_secrets_operator":
            # The namespace is precreated so the read secret can be
            # preinstalled.
            namespaces.add("vault-secrets-operator")
            return namespaces
        if app == "argocd":
            # Implicitly present at all deployments, not specified.
            namespaces.add("argocd")
            return namespaces
        dashapp = app.replace('_', '-')
        app_file = f"{val_path}/templates/{dashapp}-application.yaml"
        detemplated_contents = self.strip_templates(app_file)
        app_docs=yaml.safe_load_all(detemplated_contents)
        for doc in app_docs:
            kind = doc.get("kind","")
            if kind != "Namespace":
                continue
            ns = doc["metadata"]["name"]
            namespaces.add(ns)
        return namespaces

    def strip_templates(self, app_file:str) -> str:
        """The config "YAML" is actually Helm-templated yaml.  For our
        purposes, just stripping all the templates out works fine.
        """
        contents = ""
        with open(app_file) as f:
            while True:
                inp_l = f.readline()
                if not inp_l:
                    break
                outp_l = re.sub(self.template_re,'', inp_l)
                contents += outp_l
        return contents

    def build_config(self) -> None:
        """This must be defined in a subclass to build the configuration for
        the particular service.  The configuration should be stored in
        self.config, as a dict whose key is a string representing the
        instance name, and whose value is a string holding the yaml for
        that instance's config.  Use "generic" for the top-level values.yaml.
        """
        raise NotImplementedError()

    def write_config(self) -> None:
        """Write the configuration files, unless self.dry_run is set, in which
        case, just print their contents to stdout."""
        if self.dry_run:
            val_path = "DRY-RUN"
        else:
            if not self.output_path:
                raise RuntimeError(
                    "self.output_path must be defined in order to write config")
            val_path = self.output_path
        for instance in self.config:
            if instance == "generic":
                val_file = f"{val_path}/values.yaml"
            else:
                env_name = self.instances[instance]["environment"]
                val_file = f"{val_path}/values-{env_name}.yaml"
            if self.dry_run:
                print(f"---- begin {val_file} ----")
                print(self.config[instance])
                print(f"------ end {val_file} ----")
            else:
                # Don't write if there's no config to write
                if self.config[instance]:
                    with open(val_file,"w") as f:
                        f.write(self.config[instance])

    def run(self) -> None:
        self.build_config()
        self.write_config()
