from libs.LuciferArgParse import VAAETParser
from libs.LuciferManager import LuciferManager

luciferManager = LuciferManager()
parser = VAAETParser(luciferManager, description="Lucifer")
parser.add_argument("-g", "--gui", help="Enables The Gui Mode",
                    action="store_true", required=False)
parser.add_argument("-a", "--auto_set_vars", help="Enables Auto Setting of Vars On Module Load",
                    action="store_true", required=False)
parser.args = parser.parse_args()
# parser.check_args()

parser.check_autoset()
parser.check_gui()


luciferManager.end()
