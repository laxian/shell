#! /usr/bin/env python3
# -*- encoding: utf-8 -*-

import subprocess
from tkinter import *
from tkinter import ttk

# You can change logDir to the path that contains a list of files you want to dump
logDir = "/sdcard/logs_folder/com.segway.robot.algo.${host_part_2}go_nav_app"

display_column_count = 8  # start from 1,so 5 means 4 columns


def getFileList():
    out = subprocess.Popen(['adb', 'shell', 'ls', logDir],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()
    raw_out = str(stdout, encoding="utf-8")
    print("raw_out", raw_out)
    if len(raw_out) == 0:
        print('raw_out lenght is 0')
        return []
    else:

        files_array = raw_out.split()
        return files_array


class DumpSomePathLog:

    def __init__(self, logDir, filesArray, root):
        self.logDir = logDir
        self.root = root
        self.root.title("get files in " + logDir)
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.filesArray = filesArray
        self.filesCount = len(self.filesArray)
        # print('self.filesCount ', self.filesCount)
        label_content = "Info: get %d file(s)" % self.filesCount
        self.createLabel(mainframe, label_content)
        self.createFunctionWidgets(mainframe)
        self.createFilesWidget(mainframe)
        self.optimizeDisplay(mainframe)

    def selectAllItems(self):
        print('selectAllItems')
        for selectState in self.selectStates:
            selectState.set(1)

    def unselectAllItems(self):
        print('unselect all items')
        for selectState in self.selectStates:
            selectState.set(0)

    def dumpLogs(self):
        # print('dumpLogs')
        file_index = 0
        for selectState in self.selectStates:

            if selectState.get() == 1:
                self.dumpFile(self.logDir + '/' + self.filesArray[file_index])
            file_index = file_index + 1

    def dumpFile(self, file_name):
        print('dump file ', file_name)
        out = subprocess.Popen(['adb', 'pull', file_name],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
        stdout, stderr = out.communicate()
        # raw_out = str(stdout, encoding="utf-8")
        # print(type(raw_out))

    def delete_file(self, file_name):
        print('delete file {}'.format(file_name))
        out = subprocess.Popen(['adb', 'shell', 'rm', file_name],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
        stdout, stderr = out.communicate()
        raw_out = str(stdout, encoding="utf-8")
        print(type(raw_out))

    def createLabel(self, mainframe, infoStr):
        self.infoLabelText = StringVar()
        self.infoLabelText.set(infoStr)
        self.infoLabel = ttk.Label(mainframe, textvariable=self.infoLabelText)
        self.infoLabel.grid(column=1, row=1, sticky=W)
        self.nextWidgetRowIndex = 3

    def createFunctionWidgets(self, mainframe):
        ttk.Button(mainframe, text="selectAllItems", command=self.selectAllItems) \
            .grid(column=1, row=2, sticky=W)
        ttk.Button(mainframe, text="unselectAllItems", command=self.unselectAllItems) \
            .grid(column=2, row=2, sticky=W)
        dump_button = ttk.Button(mainframe, text="dumpLogs", command=self.dumpLogs)
        self.root.bind('<Return>', lambda e: dump_button.invoke())
        dump_button.grid(column=3, row=2, sticky=W)
        self.root.bind('<Key-Escape>', lambda e: self.root.quit())
        self.root.bind('<KeyPress-d>', lambda e: self.delete_logs())

    def createFilesWidget(self, mainframe):
        file_iter_index = 0
        self.checkButtons = []
        self.selectStates = []
        self.nextWidgetColumnIndex = 1
        for fileName in self.filesArray:
            # print('fileName',fileName,' rowIndex ',fileNameDisplayRowIndex)
            file_iter_index = file_iter_index + 1
            if file_iter_index == self.filesCount:
                chk_value = IntVar(value=1)
                print('set true default')
                self.selectStates.append(chk_value)
                check_button = ttk.Checkbutton(mainframe, text=fileName, variable=chk_value)
            else:
                chk_value = IntVar(value=0)
                self.selectStates.append(chk_value)
                check_button = ttk.Checkbutton(mainframe, text=fileName, variable=chk_value)

            check_button.grid(column=self.nextWidgetColumnIndex, row=self.nextWidgetRowIndex, sticky=W)
            self.nextWidgetColumnIndex = self.nextWidgetColumnIndex + 1
            if self.nextWidgetColumnIndex == display_column_count:
                self.nextWidgetRowIndex = self.nextWidgetRowIndex + 1
                self.nextWidgetColumnIndex = 1
            self.checkButtons.append(check_button)

    def optimizeDisplay(self, mainframe):
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def delete_logs(self):
        file_index = 0
        for selectState in self.selectStates:
            if selectState.get() == 1:
                self.delete_file(self.logDir + '/' + self.filesArray[file_index])
            file_index = file_index + 1


def local_log():
    files_array = getFileList()
    if len(files_array) == 0:
        print('No file found in ', logDir)
    else:
        root = Tk()
        DumpSomePathLog(logDir, files_array, root)
        root.mainloop()


if __name__ == '__main__':
    local_log()
