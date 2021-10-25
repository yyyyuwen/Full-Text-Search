#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 16:07:05 2020

@author: leeyuwen
"""
import sys
import os
import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
from Fulltext_Search import Ui_fulltext_search
from functools import partial
import re
import json

class AppWindow(QDialog, Ui_fulltext_search):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Open.clicked.connect(self.load_file)
        self.searchButton.clicked.connect(self.search_file)
        
    def load_file(self):
        self.file = QtWidgets.QFileDialog.getOpenFileName(None, "選取文件", os.getcwd(), "XML Files(*.xml);;JSON Files(*.json)") #回傳file[0]為絕對路徑 file[1]為是哪個格式的檔案
        # 判斷為XML or JSON
        file_format = self.file[0].split('.', 1)
        print(file_format[1])
        self.showFile.setText('')
        if file_format[1] == 'xml':
            tree = ET.parse(self.file[0])
            root = tree.getroot()
            Article = root.findall("PubmedArticle")
            self.titleList.clear()
            for elem in Article:
                print('標題：', elem.find("MedlineCitation").find("Article").find("ArticleTitle").text) #標題
                # 新增按鈕
                btn = QtWidgets.QPushButton('{0}'.format(elem.find("MedlineCitation").find("Article").find("ArticleTitle").text))
                btn.clicked.connect(partial(self.add_XmlTitle, elem))
                item = QtWidgets.QListWidgetItem()
                # 將item新增到list
                self.titleList.addItem(item)
                item.setSizeHint(QtCore.QSize(12, 30)) # 調整item大小
                # 將widget新增到item
                self.titleList.setItemWidget(item, btn)
        elif file_format[1] == 'json':
            self.titleList.clear()
            with open(self.file[0], 'rb') as json_file:
                json_data = json.load(json_file)
                data_list = []
                for data in json_data:
                    fullname = data.get('full_name')
                    username = data.get('username')
                    text = data.get('tweet_text')
                    one_note = fullname + '@' + username + '\n' + text + '\n'
                    data_list.append(one_note)
                count_List = '\n'.join(data_list)
                print(count_List)
                # 新增按鈕
                btn = QtWidgets.QPushButton('Twitter')
                btn.clicked.connect(partial(self.add_JsonTitle, count_List))
                item = QtWidgets.QListWidgetItem()
                # 將item新增到list
                self.titleList.addItem(item)
                item.setSizeHint(QtCore.QSize(12, 30)) # 調整item大小
                # 將widget新增到item
                self.titleList.setItemWidget(item, btn)
        else:
            print('Choose File.')

    def add_XmlTitle(self, elem):
        # 獲取button
        button = self.sender()
        # 獲取到物件
        s = self.titleList
        item = self.titleList.indexAt(button.pos())
        print(item)
        # 獲取位置
        print(item.row())
        text_list = []
        self.showFile.setText('')
        for article in elem.find("MedlineCitation").find("Article").findall("Abstract"): #內文位置 
                self.showFile.setText('{0}\n'.format(elem.find("MedlineCitation").find("Article").find("ArticleTitle").text))
                text_list.append(elem.find("MedlineCitation").find("Article").find("ArticleTitle").text)
                if article.find('AbstractText') is None: #####顯示不出來
                    print('pass')
                    self.showFile.setText('no file.')
                    continue
                else:
                    file = article.findall('AbstractText')
                    for abs in file:
                        if 'Label' in abs.attrib:
                            # self.showFile.setText('<font style =\'background:red;\'>test</font> string')
                            self.showFile.append('{0} ：'.format(abs.attrib['Label']))
                            text_list.append(abs.attrib['Label'])
                        self.showFile.append(abs.text)
                        text_list.append(abs.text)
                        self.showFile.append('\n')
        count_numList = ' '.join(text_list)
        # print([i.split(' ')[0] for i in count_numList])
        self.characters.setText('Number of characters: {0} characters.'.format(len(count_numList)))
        self.words.setText('Number of words: {0} words.'.format(len(count_numList.split(' '))))
        self.sentences.setText('Number of sentences: {0} sentences.'.format(len(count_numList.split('.'))))

    def add_JsonTitle(self, text):
        # 獲取button
        button = self.sender()
        # 獲取到物件
        s = self.titleList
        item = self.titleList.indexAt(button.pos())
        print(item)
        # 獲取位置
        print(item.row())
        self.showFile.setText(text) #秀文字出來
        self.characters.setText('Number of characters: {0} characters.'.format(len(text)))
        self.words.setText('Number of words: {0} words.'.format(len(text.split(' '))))
        self.sentences.setText('Number of sentences: {0} sentences.'.format(len(text.split('.'))))

    def search_file(self):
        text = self.searchText.toPlainText()
        article = self.showFile.toPlainText()

        article = article.replace('<', '&lt;')
        article = article.replace('>', '&gt;')

        article_list = []
        for match in re.finditer(str(text).lower(), str(article).lower()):
            article_list.append(match.span())

        searched_str = [char for char in article]
        num = 0
        for word_idx in article_list:
            print(word_idx)
            print(word_idx[0])
            searched_str.insert(int(word_idx[0]) + num, '<font style =\'background:red;\'>')
            searched_str.insert(int(word_idx[0]) + num + len(text) + 1, '</font>')
            num += 2
                
        new_article = ''.join(searched_str)
        # print(new_article)
        new_article = new_article.replace('\n', '<br>')
        print(new_article)
        self.showFile.setText(new_article)

    # def search_file(self):
    #     text = self.searchText.toPlainText()
    #     search_char = [char for char in text]
    #     article = self.showFile.toPlainText()
    #     searched_str = [char for char in article]
    #     match_idx = []
    #     # print(search_char)
    #     # print(searched_str)
    #     if len(search_char) == 1:
    #         for char in search_char:
    #             for i in range(len(searched_str)):
    #                 if searched_str[i].lower() == char.lower():
    #                     match_idx.append(i)

    #         for i in match_idx:
                # searched_str[i] = '<font style =\'background:red;\'>{0}</font>'.format(searched_str[i])
            
    #         full_text = ''
    #         for char in searched_str:
    #             if char == '\n':
    #                 full_text += '<br>'
    #             else:
    #                 full_text += str(char)
    #         self.showFile.setText(full_text)
    #         # self.showFile.setText(''.join(str(i) for i in searched_str))
        


        

        
    

def main():
    
    app = QtWidgets.QApplication(sys.argv)
    fulltext_search = AppWindow()
    # ui = Ui_fulltext_search()
    # ui.setupUi(fulltext_search)
    fulltext_search.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()