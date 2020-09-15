
def start():
    from lucifer.ArgParse import LuciferParser
    from lucifer.Manager import LuciferManager
    from lucifer import Errors
    try:
        luciferManager = LuciferManager()
        parser = LuciferParser(luciferManager, description="Lucifer")

        parser.add_lucifer_args()

        parser.args = parser.parse_args()
        # parser.check_args()

        parser.run()
    except Exception as e:
        Errors.checkErrors(e)
