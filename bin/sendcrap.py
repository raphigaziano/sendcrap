#!/usr/bin/env python
# Windows version.
# Stoopid windows don't need no stinking shebang, but will bitch for
# its .py extension.
import sys
try:
    from sendcrap import sendcrap
except ImportError:
    # Dev run. Ugly :/
    import os
    if os.getcwd() not in sys.path:
        sys.path.insert(0, os.getcwd())
    from sendcrap import sendcrap

sys.exit(sendcrap.main())
