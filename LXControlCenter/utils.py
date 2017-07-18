#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#  lx-control-center
#
#       Copyright 2016 (c) Julien Lavergne <gilir@ubuntu.com>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import logging
import xdg.BaseDirectory
import xdg.DesktopEntry
import xdg.IniFile
import xdg.Locale
import os.path
try:
    import configparser as configparser
except:
    import ConfigParser as configparser

class Utils(object):
    def load_xdgfile(self,path):
        xdgfile = None
        try:
            xdgfile = xdg.DesktopEntry.DesktopEntry(path)
        except:
            logging.error("load_xdgfile: error, %s is not a desktop file" % path)
        return xdgfile

    def load_inifile(self,path):
        inifile = None
        inifile = configparser.ConfigParser()
        inifile.optionxform = str
        try:
            inifile.read_file(open(path))
        except:
            try:
                inifile.readfp(open(path))
            except:
                logging.error("load_inifile: error, when loading %s as a ini file" % path)
        return inifile

    def load_setting(self, keyfile, group, key, default_value, type_to_get):
        return_value = default_value
        if (keyfile.has_section(group)):
            if (keyfile.has_option(group, key)):
                if(type_to_get == "list"):
                    return_value = keyfile.get(group,key).split(";")
                    return_value.pop()

                elif (type_to_get == "float"):
                    return_value = keyfile.getfloat(group,key)

                elif (type_to_get == "int"):
                    return_value = keyfile.getint(group,key)

                elif (type_to_get == "boolean"):
                    return_value = keyfile.getboolean(group,key)

                elif (type_to_get == "string"):
                    new_key = key
                    for lang in xdg.Locale.langs:
                        langkey = "%s[%s]" % (key, lang)
                        if (keyfile.has_option(group, langkey)):
                           new_key =  langkey
                    return_value = keyfile.get(group, new_key)
                else:
                    return_value = keyfile.get(group,key)

        return return_value

    def load_configuration_file (self, directory, name, local = False):
        """ Set configuration path to self.settings_path"""

        config_dirs = xdg.BaseDirectory.xdg_config_dirs

        return_path = None

        for path in config_dirs:
            test_path = os.path.join(path, directory, name)
            if(os.path.exists(test_path)):
                return_path = test_path
                break

        if (local == True):
            if (return_path == None):
                return_path = os.path.join(os.getcwd(), "data",name)

        logging.debug("load_configuration_file : return_path = %s" % return_path)

        return return_path
