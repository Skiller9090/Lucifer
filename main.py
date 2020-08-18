from lucifer.ArgParse import LuciferParser
from lucifer.Manager import LuciferManager

luciferManager = LuciferManager()
parser = LuciferParser(luciferManager, description="lucifer")
parser.add_argument("-g", "--gui", help="Enables The Gui Mode",
                    action="store_true", required=False)
parser.add_argument("-a", "--auto_set_vars", help="Enables Auto Setting of Vars On Module Load",
                    action="store_true", required=False)
parser.args = parser.parse_args()
# parser.check_args()

parser.check_autoset()
parser.check_gui()


luciferManager.end()
