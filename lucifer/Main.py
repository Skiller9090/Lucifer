def start():
    from lucifer.ArgParse import LuciferParser
    from lucifer.Manager import LuciferManager
    from lucifer import uniglobal
    from lucifer import Errors
    from LMI import LMI

    try:
        uniglobal.luciferManager = LuciferManager()
        LMI.init()

        parser = LuciferParser(uniglobal.luciferManager, description="Lucifer")
        parser.add_lucifer_args()
        parser.args = parser.parse_args()

        parser.run()

    except Exception as e:
        Errors.checkErrors(e)
