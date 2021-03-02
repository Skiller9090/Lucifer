"""
Lucifer's HTML Report System for HTML reporting features.

Contains:
    - HTMLTable: a class to create a table for the parent HTMLReport object.
    - HTMLReport: a class that gives an easy interface with an HTML report file.

"""
import os
import time


class HTMLTable:
    def __init__(self, parent):
        """This class allows for an easier syntax to creating the table in the
        HTMLReport class.

        @param parent: This is the parent object which is used to update currentHtml
        @type parent: HTMLReport
        """
        self.parent = parent
        self.tableID = "lucTab"

    def __enter__(self):
        """This sets up the table HTML top headings and adds it to the
        self.parent.currentHtml variable when entering a the with statement.

        @return: HTMLReport
        """
        self.parent.currentHtml += '<table style="width:100%" class="' + self.tableID + '">\n'
        return self.parent

    def __exit__(self, exc_type, exc_val, exc_tb):
        """This closes the table off in the self.parent.currentHtml when exiting
        the with statement.

        @param exc_type: default for __exit__ function
        @type exc_type: Any
        @param exc_val: default for __exit__ function
        @type exc_val: Any
        @param exc_tb: default for __exit__ function
        @type exc_tb: Any
        """
        self.parent.currentHtml += '</table>\n<br/><br/>'

    def __call__(self, tableID):
        """This initialises a table via a string argument for its id to allow
        for dynamic table class setting.

        @rtype: HTMLTable

        Args:
            tableID:
        """
        self.tableID = tableID
        return self


class HTMLReport:
    def __init__(self, name=str(time.time()), path="./reports/"):
        """This sets up an interface between LMI and a HTML report file.

        @param name: Name of the report file.
        @type name: str
        @param path: path to the directory where to store the report files.
        @type path: str
        """
        self.path = os.path.abspath(path)
        if not os.path.exists(self.path):
            os.makedirs(self.path, exist_ok=True)
        self.name = name if name.lower().endswith(".html") else (name + ".html")
        self.fullPath = os.path.abspath(os.path.join(path, self.name))
        self.fileHTML = ""
        self.currentHtml = ""
        self.useTable = HTMLTable(self)
        self.defaultReportStyle = """.lucTab {
            background: #ffffff;
        }\n
    .lucTab tr:nth-child(even) {
      background-color: #eee;
    }\n
    .lucTab tr:nth-child(odd) {
      background-color: #fff;
    }\n
    .lucTab th {
      color: white;
      background-color: black;
    }\n
    .lucTab caption {
      text-align: center;
      border: 2px solid #cccccc;
      margin-bottom: -0.2%;
      font-size: 180%;
      padding: 5px;
      letter-spacing: 2px;
      font-weight: bold;
      background: #ffffff;
    }\n
    .lucTitle {
        font-size: 100%;
        font-weight: bold;
        color: black;
        border: 3px solid black;
        background: #cccccc;
        padding: 0 1.5em;
        border-radius: 10px;
        line-height: 1em;
        width: 30em;
        text-align: center;
        margin: 1em auto;
    }\n
    .lucTitleCap {
       text-align: center;
       color: black;
       font-size: 0.75em;
       background: lightblue;
       border: 3px solid black;
       border-radius: 10px;
       width: 30em;
       margin: 1em auto;
    }\n
    .accordion {
      background-color: #eee;
      color: #444;
      cursor: pointer;
      padding: 18px;
      width: 100%;
      border: none;
      text-align: left;
      outline: none;
      font-size: 15px;
      transition: 0.4s;
    }\n
    .active, .accordion:hover {
      background-color: #ccc;
    }\n
    .accordion:after {
      content: '\\002B';
      color: #777;
      font-weight: bold;
      float: right;
      margin-left: 5px;
    }\n
    .active:after {
      content: "\\2212";
    }\n
    .panel {
      padding: 0 18px;
      background: #EFDCBE;
      max-height: 0;
      overflow: hidden;
      transition: max-height 0.2s ease-out;
    }\n
    body {
        background: #EFDCBE;
    }\n"""
        self.defaultReportScript = """\nconst acc = document.getElementsByClassName("accordion");
let i;\n
for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    this.classList.toggle("active");
    const panel = this.nextElementSibling;
    if (panel.style.maxHeight) {
      panel.style.maxHeight = null;
    } else {
      panel.style.maxHeight = panel.scrollHeight + "px";
    }
  });
}\n"""

    def newReport(self, name):
        """Creates or opens a file to be interfaced with by this class, takes
        name of file as the argument.

        @param name: The name of the report file.
        @type name: str
        """
        self.path = os.path.abspath(self.path)
        if not os.path.exists(self.path):
            os.makedirs(self.path, exist_ok=True)
        self.name = name if name.lower().endswith(".html") else (name + ".html")
        self.fullPath = os.path.abspath(os.path.join(self.path, self.name))
        self.fileHTML = ""
        self.loadFile()

    def loadFile(self):
        """Loads HTML from file and stores it into self.fileHTML"""
        if not os.path.exists(self.fullPath):
            self.createNewReport(self.fullPath)
        with open(self.fullPath, "r") as file:
            self.fileHTML = file.read()
        self.removeStyle()

    def createNewReport(self, path):
        """Takes path to the file as its argument and creates a new HTML report
        file with the default lucifer report header.

        @param path: the relative or absolute path to the new report file.
        @type path: str
        """
        os.makedirs((os.sep.join(path.split(os.sep)[:-1]) + os.sep), exist_ok=True)
        with open(path, "a+") as f:
            f.write(
                """<div class="lucTitle">
  <h1>
    Lucifer Report
  </h1>
  <p class="lucTitleCap"> Autogenerated by the Lucifer tool, created by Skiller9090 </p>
</div>\n"""
            )
            f.write("\n\n<style>\n" + self.defaultReportStyle + "</style>\n")

    def saveFile(self):
        """Saves the files HTML already loaded in this class, then appends
        default CSS and JavaScript to the end.
        """
        if not os.path.exists(self.fullPath):
            self.createNewReport(self.fullPath)
        with open(self.fullPath, "w") as f:
            f.write((self.fileHTML +
                     ("\n\n<style>\n" + self.defaultReportStyle + "</style>\n") +
                     "\n<script>" + self.defaultReportScript + "</script>\n"))

    def removeStyle(self):
        """Removes everything after <style> to only get the pure HTML, the CSS
        and JavaScript is added back and refreshed after save. This system
        allows for automatically updating CSS and JavaScript through different
        version too.
        """
        if "<style>" in self.fileHTML:
            self.fileHTML = self.fileHTML[:self.fileHTML.index("<style>")]

    def addTable(self, data):
        """Adds a table to the report by passing through the data of the table.

        @param data: this contains a tuple, first argument being title, the second being a 2d array of rows.
        @type data: (str, list)
        """
        title = data[0]
        array2d = data[1]
        headings = array2d.pop(0)
        self.currentHtml = ""
        self.currentHtml += "<button class='accordion'> " + str(title) + " </button>"
        self.currentHtml += "<div class='panel'>\n"
        with self.useTable("lucTab"):
            if title != "":
                self.currentHtml += "<caption class='collapsible'>" + str(title) + "</caption>\n"
            self.currentHtml += "<tr>\n"
            if headings:
                for head in headings:
                    self.currentHtml += "<th>" + str(head) + "</th>\n"
            self.currentHtml += "</tr>\n"
            for rowValues in array2d:
                self.currentHtml += "<tr>\n"
                for value in rowValues:
                    self.currentHtml += "<td>" + str(value) + "</td>\n"
                self.currentHtml += "</tr>\n"
        self.currentHtml += "</div>\n"
        self.fileHTML += "\n\n" + self.currentHtml
        self.saveFile()
