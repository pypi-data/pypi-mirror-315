# ~/thisgoeshardasfuck/thisgoeshardasfuck/__init__.py

import sys
import webbrowser

def __call__():
    webbrowser.open("https://media-assets.grailed.com/prd/listing/temp/475038f0fd3e440f88333473e4cd06ac")
    print("this goes hard as fuck.")

# Make the module callable
sys.modules[__name__] = __call__
