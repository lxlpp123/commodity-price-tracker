# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox


'''
QMessageBox.information 信息框
QMessageBox.question    问答框
QMessageBox.warning     警告框
QMessageBox.critical    危险框
QMessageBox.about       关于框
'''
class BaseDialog(QDialog):
    '''
    基类对话框
    '''
    def __init__(self):
        super(BaseDialog, self).__init__()


class BaseFileDialog(QFileDialog):
    '''
    基类文件对话框
    '''
    def __init__(self):
        super(BaseFileDialog, self).__init__()


class ExistingDirectory(BaseFileDialog):
    '''
    打开文件夹对话框
    '''
    def __init__(self):
        super(ExistingDirectory, self).__init__()

    def existing_directory(self, *args, **kwargs):
        return self.getExistingDirectory(*args, **kwargs)


class OpenFileDialog(BaseFileDialog):
    '''
    单选文件对话框
    '''
    def __init__(self):
        super(OpenFileDialog, self).__init__()

    def open_file(self, *args, **kwargs):
        return self.getOpenFileName(*args, **kwargs)


class OpenFilesDialog(BaseFileDialog):
    '''
    多选文件对话框
    '''
    def __init__(self):
        super(OpenFilesDialog, self).__init__()

    def open_files(self, *args, **kwargs):
        return self.getOpenFileNames(*args, **kwargs)


class SaveFileDialog(BaseFileDialog):
    '''
    保存文件对话框
    '''
    def __init__(self):
        super(SaveFileDialog, self).__init__()

    def save_file(self, *args, **kwargs):
        return self.getSaveFileName(*args, **kwargs)


class MessageDialog(QMessageBox):
    '''
    消息对话框，继承自QMessageBox
    '''
    def __init__(self):
        super(MessageDialog, self).__init__()
