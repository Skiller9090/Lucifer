from lucifer.ArgParse import LuciferParser
from lucifer.Manager import LuciferManager
from argparse import SUPPRESS

luciferManager = LuciferManager()
parser = LuciferParser(luciferManager, description="Lucifer")

parser.add_argument("-l", "--log-commands", dest="logger_loc", help="Enables Command Logging To File",
                    action="store", required=False)
parser.add_argument("-g", "--gui", help="Enables The Gui Mode",
                    action="store_true", required=False)
parser.add_argument("-a", "--auto-set-vars", dest="auto_set_vars", help="Enables Auto Setting of Vars On Module Load",
                    action="store_true", required=False)

parser.args = parser.parse_args()
# parser.check_args()

parser.check_logging()
parser.check_autoset()
parser.check_gui()

luciferManager.end()
