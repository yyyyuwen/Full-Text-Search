
import xml.etree.ElementTree as ET
import os

if __name__=="__main__":
    # fileDir = './'
    # fileExt = '.xml'
    # filelist = [_ for _ in os.listdir(fileDir)if _.endswith(fileExt)]
    # for file in filelist:
    tree = ET.parse('./test2.xml')
    root = tree.getroot()
    Article = root.findall("PubmedArticle")
    for elem in Article:
        print('標題：', elem.find("MedlineCitation").find("Article").find("ArticleTitle").text) #標題
        print("Abstract")
        for article in elem.find("MedlineCitation").find("Article").findall("Abstract"): #內文位置 
            if article.find('AbstractText') is None:
                print('pass')
                continue
            else:
                print('123')
                abs = article.find('AbstractText')
                print(abs.attrib)
                if 'Label' in abs.attrib:
                    print(abs.attrib['Label'],"：")
                print(abs.text)

            # else:
            #     for part in abs:
            #         if 'Label' in part.attrib: #屬性
            #             print('123')
            #             print(part.attrib['Label'],"：")
            #         print(part.text)