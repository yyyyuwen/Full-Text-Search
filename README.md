#  Full Text Search
###### tags: `NCKU` `python` `生醫資訊`

## 安裝
* Python3
* PyQt5 5.15.4
* Qt Designer 
* xml.etree.ElementTree

## 大致流程
![](https://i.imgur.com/k6Eix4R.png)


## 檔案格式
* XML : 利用`xml.etree.ElementTree`來讀取.xml檔案，並取得ArticleTitle(標題)、AbstractText(內文)。
* json: 利用`json`來讀取.json檔，並取得full_name、username、tweet_text(內文)這三個key的value來表示。

## PyQT5

1. 先用Qt Designer設計好介面並產生一個`.ui`檔
2. 於存在`.ui`檔的目錄下輸入指令`pyuic5 -x example.ui -o example_ui.py`即可產生一個`.py`檔
[用 Qt Designer 來設計 PyQt GUI 應用程式界面](https://zhung.com.tw/article/用qt-designer來設計pyqt-gui應用程式界面/)
![](https://i.imgur.com/isCpNao.png)



### [調整QListWidgetItem大小](https://vimsky.com/zh-tw/examples/detail/python-ex-PyQt5.Qt-QListWidgetItem-setSizeHint-method.html)
```python=
btn = QtWidgets.QPushButton('Twitter')
# button click事件
btn.clicked.connect(partial(self.add_JsonTitle, count_List))
item = QtWidgets.QListWidgetItem()
# 將item新增到list
self.titleList.addItem(item)
item.setSizeHint(QtCore.QSize(12, 30)) # 調整item大小
# 將widget新增到item
self.titleList.setItemWidget(item, btn)
```
未調整
![](https://i.imgur.com/dLYUUrM.png)

調整後
![](https://i.imgur.com/ghGLyRb.png)


### Button 事件
#### 傳入多值
因為需要透過click事件傳入文章資料，所以我們可以利用`functools`裡頭的`partial`函數來處理
```python=
button.clicked.connect(partial(self.funtion, 欲傳入參數)) 
```
另外還有利用`lambda`來傳遞的方法在[連結](https://blog.csdn.net/fengyu09/article/details/39498777)裡面。
#### 透過點選來獲取當前value
在button點選事件中，用`button = self.sender()` 獲取按鈕物件
參考: [QListWidget實現點選按鈕來獲取當前行](https://iter01.com/445540.html)


### PyQT功能
#### QTextEdit和QTextBrowser之選擇
此次專題顯示文件使用QTextBrowser，而search框使用QTextEdit的原因是QTextEdit可以做讀寫的動作，而顯示文件因不需要輸入所以使用QTextBrowser。
參考：[QTextEdit和QTextBrowser差異](https://blog.csdn.net/qq_38463737/article/details/107628113)


#### QTextBrowser可用[HTML格式顯示](https://blog.csdn.net/weixin_30439067/article/details/97708413?utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1.no_search_link&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1.no_search_link)
<font color = red>注意：轉成HTML格式一些符號格式也需要更改</font>


| 原 | 更改 | 
| -------- | -------- | 
| `\n`     | `<br>`   | 
| `<`      | `&lt;`   | 
| `>`      | `&gt;`   | 

    > 寫入（會重置）:`QTextBrowser.setText('輸入')`
    > 追加（不會重置）: `QTextBrowser.append('輸入')`


#### QLineEdit、textEdit獲取輸入框内容
    > str1= self.lineEdit.text() # 單行顯示
## Python 一些語法紀錄

#### 加句子至string中的方法：
* insert
```python=
# str.insert(index, 要插入的句子)
aList = [123, 'xyz', 'zara', 'abc']
aList.insert( 3, 2009)
# output = [123, 'xyz', 'zara', 2009, 'abc']
```
* 直接加
```python= 
line = 'Kong Panda'
index = line.find('Panda')
output_line = line[:index] + 'Fu ' + line[index:]
# output = 'Kong Fu Panda'
```
#### Number of char/words/sentences:
```python=
# 利用空格、句點區分
self.characters.setText('Number of characters: {0} characters.'.format(len(text)))
self.words.setText('Number of words: {0} words.'.format(len(text.split(' '))))
self.sentences.setText('Number of sentences: {0} sentences.'.format(len(text.split('.'))))

```

#### Python find all index in string：
使用正規表示式`re.finditer`來查找，與 `re.findall` 相比的額外資訊，比如有關字串中匹配位置的資訊（索引）。Return **an iterator** yielding match **objects** over all non-overlapping matches for the RE pattern in string. 
> match.span(): 回傳一個tuple(start(), end())
> match.group(): 回傳匹配值

並統一用小寫`str(text).lower()`來做搜尋比對。

## Demo
* 在當前目錄下輸入 `python3 main.py`
* 點選Load File可以選擇要XML或是json格式
![](https://i.imgur.com/jAYAUL7.png)

* Load File後，Title會顯示在右側欄位中，點選Title後可以顯示內文。
![](https://i.imgur.com/nkha4AU.png)


* 利用Text Search搜尋文字，點選search button後可以搜尋關鍵字。
![](https://i.imgur.com/CkZWjgW.png)


## 參考資料
[HighLighting potions of text in QPlainTextEdit](https://stackoverflow.com/questions/57636321/highlighting-portions-of-text-in-qplaintextedit)


[python多層list到str的轉換 和 str中換行符\n的保存](https://blog.csdn.net/Joey_yk/article/details/89882081)

[How to convert a list of characters into a string in Python](https://www.kite.com/python/answers/how-to-convert-a-list-of-characters-into-a-string-in-python)
> Use `str.join()`
> 
> Call **str.join(iterable)** with the empty string "" as str and a list as iterable to join each character into a string.
> ```python=
> a_list = ["a", "b", "c"]
> a_string = "".join(a_list)
> # output = abc
> ```

Python dict.get()方法
http://tw.gitbook.net/python/dictionary_get.html

Python replace()方法
https://www.runoob.com/python/att-string-replace.html

Python split()方法
https://www.runoob.com/python/att-string-split.html

[re — Regular expression operations](https://docs.python.org/3/library/re.html)
[使用 re.finditer 迭代匹配](http://www.tastones.com/zh-tw/stackoverflow/python-language/regular-expressions-regex/iterating_over_matches_using_re.finditer/)
[深入理解 Python 的 re 模組](https://www.gushiciku.cn/pl/gz9L/zh-tw)
