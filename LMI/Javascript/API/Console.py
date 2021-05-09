import inspect
from pprint import pformat

from js2py.pyjs import PyObjectWrapper, PyJsArray, PyJsObject, PyJs

from LMI.Table import generate_table
from ..Core import PyJsMethod


class Console(PyObjectWrapper):
    def __init__(self):
        super().__init__(self)
        self.vars = {}
        self.groupHeight = 0
        self.bindMethods()

    def __repr__(self):
        return f"<PyJsLucifer|{self.__class__.__name__}: {self.vars}>"

    def bindMethods(self):
        self.bindMethod("log", self.log)
        self.bindMethod("debug", self.debug)
        self.bindMethod("error", self.error)
        self.bindMethod("info", self.info)
        self.bindMethod("warn", self.warn)
        self.bindMethod("assert", self.console_assert)
        self.bindMethod("clear", self.clear)
        self.bindMethod("count", self.count)
        self.bindMethod("countReset", self.countReset)
        self.bindMethod("dir", self.dir)
        self.bindMethod("dirxml", self.dirxml)
        self.bindMethod("group", self.group)
        self.bindMethod("groupEnd", self.groupEnd)
        self.bindMethod("table", self.table)

    def bindMethod(self, name, func):
        self.put(name, PyJsMethod(func, self))

    def showMessage(self, mType, message, groups=True):
        display = mType + ": " + str(message)
        if groups:
            display = "\t" * self.groupHeight + display
        print(display)

    def log(self, message):
        self.showMessage("LOG", message)

    def error(self, message):
        self.showMessage("ERROR", message)

    def info(self, message):
        self.showMessage("INFO", message)

    def warn(self, message):
        self.showMessage("WARN", message)

    def console_assert(self, statement, errorObj):
        if not statement:
            print("Assert: " + str(errorObj))

    def clear(self):
        print("Attempted Clear")

    def count(self, label):
        label = label.value
        if label is None:
            label = "default"
        if "count" not in self.vars:
            self.vars["count"] = {}
        if label not in self.vars["count"]:
            self.vars["count"][label] = 0
        self.vars["count"][label] += 1
        print(f"{label}: {(self.vars['count'][label])}")

    def countReset(self, label):
        label = label.value
        if label is None:
            label = "default"
        if "count" not in self.vars:
            self.vars["count"] = {}
        self.vars["count"][label] = 0

    def debug(self, message):
        self.showMessage("DEBUG", message)

    def dir(self, obj):
        print(pformat(inspect.getmembers(obj)))

    def dirxml(self, _):
        self.error("Lucifer does not use XML or HTML at its core so no object hierarchy to show!")

    def group(self, label):
        if label.value is not None:
            self.showMessage("", "----- " + label.value + " -----")
        self.groupHeight += 1

    def groupEnd(self):
        if self.groupHeight > 0:
            self.groupHeight -= 1

    def table(self, data, columns):
        table = "No table could be generated with those inputs!"
        if isinstance(columns, PyJs):
            columns = columns.to_python()
        if isinstance(data, PyJsArray):
            data = data.to_list()
            isObject = False
            if len(data) > 0:
                isObject = (isinstance(data[0], PyJsObject) or isinstance(data[0], dict))
            if isObject:
                table = self.tableProcessObject({i: x for i, x in enumerate(data)}, columns=columns)
            else:
                column_amount = 0
                for i in range(len(data)):
                    if isinstance(data[i], PyJsArray):
                        data[i] = data[i].to_list()
                        if len(data[i]) > column_amount:
                            column_amount = len(data[i])
                    else:
                        data[i] = [data[i]]
                    data[i].insert(0, i)
                table = generate_table(data, headings=["(index)",
                                                       *(["Values"] if column_amount < 2
                                                         else list(map(str, range(column_amount))))])
        elif isinstance(data, PyJsObject):
            data = data.to_python().to_dict()
            isObject = False
            if len(data) > 0:
                isObject = (isinstance(list(data.values())[0], PyJsObject) or isinstance(list(data.values())[0], dict))
            if isObject:
                table = self.tableProcessObject(data, columns=columns)
            else:
                table = generate_table(list(zip(data.keys(), data.values())), headings=["(index)", "Values"])
        print(table)

    def tableProcessObject(self, data, columns=None):
        tableData = []
        headings = ["(index)"]
        for key, value in zip(data.keys(), data.values()):
            if isinstance(value, PyJsObject):
                value = value.to_python().to_dict()
            row = [key]
            for k, v in zip(value.keys(), value.values()):
                if columns is not None and k not in columns:
                    continue
                if k not in headings:
                    headings.append(k)
                headIndex = headings.index(k)
                if len(row) - 1 < headIndex:
                    row.extend(["" for x in range((headIndex + 1) - len(row))])
                row[headIndex] = v
            tableData.append(row)
        table = generate_table(tableData, headings=headings)
        return table

    """
    Unimplemented:
        - profile
        - profileEnd
        - time
        - timeEnd
        - timeLog
        - timeStamp
        - trace
    """
