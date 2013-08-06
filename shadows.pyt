# -*- coding: utf-8 -*-

import imp
import os

found_mod = imp.find_module('make_shadows', [os.path.dirname(__file__)])
make_shadows = imp.load_module('make_shadows', *found_mod)

Toolbox = make_shadows.Toolbox
MakeShadows = make_shadows.MakeShadows
