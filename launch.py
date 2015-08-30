from __future__ import absolute_import

import alexandria
import sys

if __name__ == "__main__":
    debug = "--debug" in sys.argv
    alexandria.app.run(host="0.0.0.0", debug=debug, use_reloader=False)
