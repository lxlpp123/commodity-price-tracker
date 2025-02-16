# -*- coding: utf-8 -*-

import logging
Logger = logging.getLogger("TBTracker")
Logger.setLevel(logging.DEBUG)
InfoHandler = logging.FileHandler("logs/info.log")
InfoHandler.setLevel(logging.INFO)
INFOFORMATTER = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s]: %(message)s')
InfoHandler.setFormatter(INFOFORMATTER)
Logger.addHandler(InfoHandler)
ErrHandler = logging.FileHandler("logs/error.log")
ErrHandler.setLevel(logging.ERROR)
ERRORFORMATTER = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] File "%(filename)s", line %(lineno)d: %(message)s')
ErrHandler.setFormatter(ERRORFORMATTER)
Logger.addHandler(ErrHandler)

import math
import matplotlib.dates as mdate
import matplotlib.pyplot as plt
import os
import random
import requests
import sqlite3 as sqlite
import sys
import xlwt
import yaml

from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0'
HEADERS = {'user-agent': USER_AGENT}
DCAP = dict(DesiredCapabilities.PHANTOMJS)
DCAP["phantomjs.page.settings.userAgent"] = USER_AGENT
DCAP["phantomjs.page.settings.loadImages"] = False

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DRIVER = webdriver.PhantomJS(desired_capabilities=DCAP, service_args=[
    '--load-images=no',  # 禁止加载图片
    '--disk-cache=yes',  # 开启浏览器缓存
    '--ignore-ssl-errors=true',  # 忽略HTTPS错误
    '--ssl-protocol=TLSv1'])
DRIVER.set_window_size(1280, 1024)


from PyQt5.QtCore import QEvent
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QVariant
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import qApp
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QSlider
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QTreeWidget
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtWidgets import QTreeWidgetItemIterator
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from utils import *
from gui.button import *
from gui.canvas import *
from gui.dialog import *


class TBTrackerMainWindow(QWidget):
    def __init__(self):
        super(TBTrackerMainWindow, self).__init__()
        self.create_main_window()

    def create_main_window(self):
        self.setWindowTitle("商品数据追踪系统")
        self.setWindowIcon(QIcon('TBTracker_Ui/Spider.ico'))
        self.width, self.height = get_current_screen_size()
        self.setMinimumSize(self.width, self.height)
        self.setMaximumSize(self.width, self.height)
        self.set_widgets()
        self.setLayout(self.layout)

        self.show_product_id()
        self.show_database()
        self.plot_product_tree()

    def set_widgets(self):
        labelFont = QFont()
        labelFont.setPointSize(12)

        self.table_1_Font = QFont()
        self.table_1_Font.setPointSize(10)
        self.table_1_Font.setStyleName("Bold") 
        self.table_2_Font = QFont()
        self.table_2_Font.setPointSize(12)
        self.table_2_Font.setStyleName("Bold")
        # *****************************************************************************************
        firstWidget = QWidget()

        self.searchLineEdit = QLineEdit()
        searchButton = SearchButton()
        searchButton.clicked.connect(self.call_spider)

        searchRegionLayout = QHBoxLayout()
        searchRegionLayout.setContentsMargins(240, 0, 240, 0)
        searchRegionLayout.setSpacing(20)
        searchRegionLayout.addWidget(self.searchLineEdit)
        searchRegionLayout.addWidget(searchButton)
        
        self.taobaoDataTable = QTableWidget(0, 4)
        self.taobaoDataTable.horizontalHeader().hide()
        self.taobaoDataTable.verticalHeader().hide()
        self.taobaoDataTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.taobaoDataTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.productIDTable = QTableWidget(0, 1)
        self.productIDTable.setHorizontalHeaderLabels(["已有商品标签"])
        self.productIDTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.productIDTable.setSelectionMode(QAbstractItemView.NoSelection)
        self.productIDTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tableRegionLayout = QHBoxLayout()
        tableRegionLayout.addWidget(self.taobaoDataTable)
        tableRegionLayout.addWidget(self.productIDTable)
        tableRegionLayout.setStretchFactor(self.taobaoDataTable, 3)
        tableRegionLayout.setStretchFactor(self.productIDTable, 1)

        self.progressBar = QProgressBar()
        
        self.addProductIDLineEdit = QLineEdit()
        addProductIDButton = AddButton()
        addProductIDButton.clicked.connect(self.add_product_id)
        self.attachProductIDLineEdit = QLineEdit()
        attachProductIDButton = AttachButton()
        attachProductIDButton.clicked.connect(self.attach_product_id)
        importDataButton = ImportButton()
        importDataButton.clicked.connect(self.import_data)

        dataOperateLayout = QHBoxLayout()
        dataOperateLayout.addStretch()
        dataOperateLayout.addWidget(self.addProductIDLineEdit)
        dataOperateLayout.addSpacing(5)
        dataOperateLayout.addWidget(addProductIDButton)
        dataOperateLayout.addSpacing(25)
        dataOperateLayout.addWidget(self.attachProductIDLineEdit)
        dataOperateLayout.addSpacing(5)
        dataOperateLayout.addWidget(attachProductIDButton)
        dataOperateLayout.addSpacing(25)
        dataOperateLayout.addWidget(importDataButton)

        firstWidgetLayout = QVBoxLayout()
        firstWidgetLayout.setSpacing(10)
        firstWidgetLayout.addLayout(searchRegionLayout)
        firstWidgetLayout.addLayout(tableRegionLayout)
        firstWidgetLayout.addWidget(self.progressBar)
        firstWidgetLayout.addLayout(dataOperateLayout)

        firstWidget.setLayout(firstWidgetLayout)
        # *****************************************************************************************
        secondWidget = QWidget()

        self.DBTable = QTableWidget(0, 6)
        self.DBTable.setHorizontalHeaderLabels(["商品标识", "标题", "店铺名", "价格", "淘宝价", "是否删除数据？"])
        self.DBTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.DBTable.setSelectionMode(QAbstractItemView.NoSelection)
        self.DBTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.insertButton = InsertButton()
        self.insertButton.clicked.connect(self.add_data)
        deleteButton = DeleteButton()
        deleteButton.clicked.connect(self.delete_data)

        DBOperateLayout = QHBoxLayout()
        DBOperateLayout.addStretch()
        DBOperateLayout.setSpacing(20)
        DBOperateLayout.addWidget(self.insertButton)
        DBOperateLayout.addWidget(deleteButton)

        secondWidgetLayout = QVBoxLayout()
        secondWidgetLayout.setSpacing(10)
        secondWidgetLayout.addWidget(self.DBTable)
        secondWidgetLayout.addLayout(DBOperateLayout)

        secondWidget.setLayout(secondWidgetLayout)
        # *****************************************************************************************
        thirdWidget = QWidget()

        self.productTree = QTreeWidget()
        self.productTree.setColumnCount(2)
        self.productTree.setHeaderLabels(['商品标识','商品数量'])
        self.productTree.header().setSectionResizeMode(QHeaderView.Stretch)
        self.productTree.setSelectionMode(QAbstractItemView.NoSelection)
        productTreeLayout = QHBoxLayout()
        productTreeLayout.addWidget(self.productTree)

        upLayout = QHBoxLayout()
        upLayout.setSpacing(20)
        upLayout.addLayout(productTreeLayout)

        globalSelectButton = GlobalSelectButton()
        globalSelectButton.clicked.connect(self.select_global)
        allSelectButton = AllSelectButton()
        allSelectButton.clicked.connect(self.select_all)
        removeButton = DeleteButton()
        removeButton.clicked.connect(self.remove_data)
        exportButton = ExportButton()
        exportButton.clicked.connect(self.export_data)
        dataExportLayout = QHBoxLayout()
        dataExportLayout.addStretch()
        dataExportLayout.setSpacing(20)
        dataExportLayout.addWidget(globalSelectButton)
        dataExportLayout.addWidget(allSelectButton)
        dataExportLayout.addWidget(removeButton)
        dataExportLayout.addWidget(exportButton)

        thirdWidgetLayout = QVBoxLayout()
        thirdWidgetLayout.setSpacing(20)
        thirdWidgetLayout.setContentsMargins(50, 20, 50, 20)
        thirdWidgetLayout.addLayout(upLayout)
        thirdWidgetLayout.addLayout(dataExportLayout)
        
        thirdWidget.setLayout(thirdWidgetLayout)
        # *****************************************************************************************
        fourthWidget = QWidget()

        self.historyDataCanvas = HistoryDataCanvas()
        historyDataLayout = QVBoxLayout()
        historyDataLayout.addWidget(self.historyDataCanvas)

        self.selectCommodityButton = SelectCommodityButton()
        self.monthlyDataButton = MonthlyDataButton()
        self.yearlyDataButton = YearlyDataButton()
        manualUpdateButton = ManualUpdateButton()
        manualUpdateButton.clicked.connect(self.manual_update)
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.setSpacing(30)
        buttonLayout.addWidget(self.selectCommodityButton)
        buttonLayout.addWidget(self.monthlyDataButton)
        buttonLayout.addWidget(self.yearlyDataButton)
        buttonLayout.addWidget(manualUpdateButton)
        
        fourthWidgetLayout = QVBoxLayout()
        fourthWidgetLayout.setSpacing(10)
        fourthWidgetLayout.setContentsMargins(50, 0, 50, 10)
        fourthWidgetLayout.addLayout(historyDataLayout)
        fourthWidgetLayout.addLayout(buttonLayout)

        fourthWidget.setLayout(fourthWidgetLayout)
        # *****************************************************************************************
        self.tabWidget = QTabWidget()
        self.tabWidget.addTab(firstWidget, "数据爬虫")
        self.tabWidget.addTab(secondWidget, "数据后台")
        self.tabWidget.addTab(thirdWidget, "数据导出")
        self.tabWidget.addTab(fourthWidget, "数据跟踪")

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(50, 20, 50, 13)
        self.layout.addWidget(self.tabWidget)

    def closeEvent(self, event):
        pass
    
    @staticmethod
    def remove_pics():
        root_dir = 'TBTracker_Temp'
        for root, dirs, files in os.walk(root_dir):
            Logger.info('正在删除图片')
            for filename in files:
                if filename != "__init__.py":
                    os.remove(root+'/'+filename)
            Logger.info('图片删除完毕!')

    def find_out_real_price(self, i, shop_url, match_price):
        price, taobao_price = '', ''
        try:
            DRIVER.get(shop_url)
            Logger.info("第{0}家店铺的商品页面读取成功".format(i))

            try:
                price = WebDriverWait(DRIVER, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'originPrice'))).text.lstrip("￥").strip()
            except Exception as e:
                pass
            try:
                taobao_price = WebDriverWait(DRIVER, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'J_actPrice'))).text.lstrip("￥").strip()
            except Exception as e:
                pass
            
            if price == '' and taobao_price == '':
                try:
                    J_StrPriceModBox = WebDriverWait(DRIVER, 10).until(
                        EC.presence_of_element_located((By.ID, 'J_StrPriceModBox')))
                    try:
                        price = WebDriverWait(J_StrPriceModBox, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'tb-rmb-num'))).text.strip()
                    except Exception as e:
                        try:
                            price = WebDriverWait(J_StrPriceModBox, 10).until(
                                EC.presence_of_element_located((By.CLASS_NAME, 'tm-price'))).text.strip()
                        except Exception as e:
                            pass
                except Exception as e:
                    pass
                try:
                    J_PromoPrice = WebDriverWait(DRIVER, 10).until(
                        EC.presence_of_element_located((By.ID, 'J_PromoPrice')))
                    try:
                        taobao_price = WebDriverWait(J_PromoPrice, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'tb-rmb-num'))).text.strip()
                    except Exception as e:
                        try:
                            taobao_price = WebDriverWait(J_PromoPrice, 10).until(
                                EC.presence_of_element_located((By.CLASS_NAME, 'tm-price'))).text.strip()
                        except Exception as e:
                            pass
                except Exception as e:
                    pass
                
                if price == '' and taobao_price == '':
                    try:
                        tm_price_panel = WebDriverWait(DRIVER, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'tm-price-panel')))
                        price = WebDriverWait(tm_price_panel, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'tm-price'))).text.strip()
                    except Exception as e:
                        pass
                    try:
                        tm_promo_panel = WebDriverWait(DRIVER, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'tm-promo-panel')))
                        taobao_price = WebDriverWait(tm_promo_panel, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'tm-price'))).text.strip()
                    except Exception as e:
                        pass   
        except Exception as e:
            Logger.error(e)
            Logger.warn('第{0}家店铺的商品页面读取失败'.format(i))
            Logger.warn(shop_url)
        finally:
            if price == '' and taobao_price != '':
                price = taobao_price
            elif price != '' and taobao_price == '':
                taobao_price = price
            elif price == '' and taobao_price == '':
                price = taobao_price = match_price
        
        return price, taobao_price

    def call_spider(self):
        searchWord = self.searchLineEdit.text().strip()
        if searchWord != '':
            Logger.info('''
                        
                          ┏┓　　　┏┓
                        ┏┛┻━━━┛┻┓
                        ┃　　　　　　　┃
                        ┃　　　━　　　┃
                        ┃　┳┛　┗┳　┃
                        ┃　　　　　　　┃
                        ┃　　　┻　　　┃
                        ┃　　　　　　　┃
                        ┗━┓　　　┏━┛
                        　　┃　　　┃神兽保佑
                        　　┃　　　┃代码无BUG！
                        　　┃　　　┗━━━┓
                        　　┃　　　　　　　┣┓
                        　　┃　　　　　　　┏┛
                        　　┗┓┓┏━┳┓┏┛
                        　　　┃┫┫　┃┫┫
                        　　　┗┻┛　┗┻┛ 
                        
                        ''')
            self.remove_pics()
            try:
                webDriver = webdriver.PhantomJS(desired_capabilities=DCAP, service_args=[
                    '--load-images=no',  # 禁止加载图片
                    '--disk-cache=yes',  # 开启浏览器缓存
                    '--ignore-ssl-errors=true',  # 忽略HTTPS错误
                    '--ssl-protocol=TLSv1'])
                webDriver.set_window_size(1280, 1024)
                try:
                    Logger.info("模拟登录淘宝网")
                    webDriver.get("https://www.taobao.com/")
                    try:
                        search_combobox = WebDriverWait(webDriver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'search-combobox-input-wrap')))
                        search_input = WebDriverWait(search_combobox, 10).until(
                            EC.presence_of_element_located((By.ID, 'q')))
                        # 发送搜索词
                        search_input.send_keys(searchWord.strip())

                        search_button_wrap = WebDriverWait(webDriver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'search-button')))
                        search_button = WebDriverWait(search_button_wrap, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'btn-search')))
                        search_button.click()
                        try:
                            Logger.info('搜索成功，正在返回搜索结果')
                            mainsrp_itemlist = WebDriverWait(webDriver, 10).until(
                                EC.presence_of_element_located((By.ID, 'mainsrp-itemlist')))
                            m_itemlist = WebDriverWait(mainsrp_itemlist, 10).until(
                                EC.presence_of_element_located((By.CLASS_NAME, 'm-itemlist')))
                            items = WebDriverWait(m_itemlist, 10).until(
                                EC.presence_of_all_elements_located((By.CLASS_NAME, 'items')))[0]
                            allItems = WebDriverWait(items, 10).until(
                                EC.presence_of_all_elements_located((By.CLASS_NAME, 'J_MouserOnverReq'))
                            )
                            
                            self.returnCNT = len(allItems)
                            Logger.info('总共返回{0}个搜索结果'.format(self.returnCNT))

                            self.taobaoDataTable.clearContents()
                            self.taobaoDataTable.setRowCount(self.returnCNT * 6)  ## TODO

                            imageLabel = [QLabel() for _ in range(self.returnCNT)]
                            titleItem = [QTableWidgetItem() for _ in range(self.returnCNT)]
                            shopItem = [QTableWidgetItem("店铺：") for _ in range(self.returnCNT)]
                            shopValueItem = [QTableWidgetItem() for _ in range(self.returnCNT)]
                            sourceItem = [QTableWidgetItem("来源地：") for _ in range(self.returnCNT)]
                            sourceValueItem = [QTableWidgetItem() for _ in range(self.returnCNT)]
                            priceItem = [QTableWidgetItem("价格：") for _ in range(self.returnCNT)]
                            priceValueItem = [QTableWidgetItem() for _ in range(self.returnCNT)]
                            tbPriceItem = [QTableWidgetItem("淘宝价：") for _ in range(self.returnCNT)]
                            tbPriceValueItem = [QTableWidgetItem() for _ in range(self.returnCNT)]
                            dealItem = [QTableWidgetItem("付款人数：") for _ in range(self.returnCNT)]
                            dealValueItem = [QTableWidgetItem() for _ in range(self.returnCNT)]
                            isJoinedItem = [QTableWidgetItem("是否加入价格跟踪队列？") for _ in range(self.returnCNT)]
                            checkItem = [QTableWidgetItem() for _ in range(self.returnCNT)]
                            self.URLList = []

                            for (j, item) in enumerate(allItems):
                                try:
                                    # 抓取商品图
                                    Logger.info('正在爬取第{0}家店铺的数据'.format(j + 1))
                                    pic_box = WebDriverWait(item, 10).until(
                                        EC.presence_of_element_located((By.CLASS_NAME, 'pic-box')))
                                    itemPic = WebDriverWait(pic_box, 10).until(
                                        EC.presence_of_element_located((By.CLASS_NAME, 'J_ItemPic')))
                                    itemPic_id = itemPic.get_attribute('id')
                                    itemPic_data_src = itemPic.get_attribute('data-src')
                                    if not itemPic_data_src.startswith("https:"):
                                        itemPic_data_src = "https:" + itemPic_data_src
                                    itemPic_alt = itemPic.get_attribute('alt').strip()
                                    if itemPic_id == '':
                                        random_serial = ''
                                        for _ in range(12):
                                            random_serial += str(random.randint(0, 10))
                                        itemPic_id = "J_Itemlist_Pic_" + random_serial
                                    Logger.info("正在爬取第{0}家店铺的商品图片".format(j + 1))
                                    try:
                                        stream = requests.get(itemPic_data_src, timeout=10, headers=HEADERS)
                                    except requests.RequestException as e:
                                        Logger.error(e)
                                    finally:
                                        Logger.info("第{0}家店铺的商品图片爬取完毕".format(j + 1))
                                        try:
                                            im = Image.open(BytesIO(stream.content))
                                            if im.mode != 'RGB':
                                                im = im.convert('RGB')
                                            im.save("TBTracker_Temp/{0}.jpeg".format(itemPic_id))
                                            Logger.info("第{0}家店铺的商品图片保存完毕".format(j + 1))
                                            self.taobaoDataTable.setSpan(j * 6, 0, 6, 1)
                                            imageLabel[j].setPixmap(QPixmap.fromImage(QImage("TBTracker_Temp/{0}.jpeg".format(itemPic_id)).scaled(int(230 * 0.7), int(230 * 0.7))))
                                            imageLabel[j].setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                                            self.taobaoDataTable.setCellWidget(j * 6, 0, imageLabel[j])
                                        except Exception as e:
                                            Logger.error(e)
                                    
                                    ctx_box = WebDriverWait(item, 10).until(
                                        EC.presence_of_element_located((By.CLASS_NAME, 'ctx-box')))
                                    # 抓取商品价格和店铺网址
                                    row_row_2 = WebDriverWait(ctx_box, 10).until(
                                        EC.presence_of_element_located((By.CLASS_NAME, 'row-2')))
                                    item_price_and_link = WebDriverWait(row_row_2, 10).until(
                                        EC.presence_of_element_located((By.TAG_NAME, 'a'))
                                    )
                                    item_match_price = item_price_and_link.get_attribute('trace-price')
                                    item_link = item_price_and_link.get_attribute('href')
                                    if not item_link.startswith("https:"):
                                        item_link = "https:" + item_link
                                    self.URLList.append(item_link)

                                    status_code = requests.get(item_link).status_code
                                    Logger.info(status_code)
                                    if status_code == 200:
                                        item_title = itemPic_alt
                                        # 淘宝价格有时候会为空，暂时性的解决方案
                                        item_price, item_taobao_price = self.find_out_real_price(j + 1, item_link, item_match_price)
                                        if item_taobao_price == '':
                                            item_taobao_price = item_price
                                        Logger.info('第{0}家店铺的商品价格和链接爬取完毕'.format(j + 1))
                                        self.taobaoDataTable.setSpan(j * 6, 1, 1, 2)
                                        titleItem[j].setData(Qt.DisplayRole, QVariant(item_title))
                                        titleItem[j].setFont(self.table_1_Font)
                                        titleItem[j].setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                                        self.taobaoDataTable.setItem(j * 6, 1, titleItem[j])

                                        priceItem[j].setFont(self.table_2_Font)
                                        priceItem[j].setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                                        self.taobaoDataTable.setItem(j * 6 + 3, 1, priceItem[j])
                                        priceValueItem[j].setData(Qt.DisplayRole, QVariant(item_price))
                                        self.taobaoDataTable.setItem(j * 6 + 3, 2, priceValueItem[j])

                                        tbPriceItem[j].setFont(self.table_2_Font)
                                        tbPriceItem[j].setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                                        self.taobaoDataTable.setItem(j * 6 + 4, 1, tbPriceItem[j])
                                        tbPriceValueItem[j].setData(Qt.DisplayRole, QVariant(item_taobao_price))
                                        self.taobaoDataTable.setItem(j * 6 + 4, 2, tbPriceValueItem[j])
                                    else:
                                        Logger.warn('第{0}家店铺的商品价格和链接爬取失败'.format(j + 1))
                                    # 抓取商品交易量
                                    row_row_1 = WebDriverWait(ctx_box, 10).until(
                                        EC.presence_of_element_located((By.CLASS_NAME, 'row-1')))
                                    item_deal = WebDriverWait(row_row_1, 10).until(
                                        EC.presence_of_element_located((By.CLASS_NAME, 'deal-cnt'))).text.strip()
                                    Logger.info('第{0}家店铺的商品交易量爬取完毕'.format(j + 1))
                                    dealItem[j].setFont(self.table_2_Font)
                                    dealItem[j].setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                                    self.taobaoDataTable.setItem(j * 6 + 5, 1, dealItem[j])
                                    dealValueItem[j].setData(Qt.DisplayRole, QVariant(item_deal))
                                    self.taobaoDataTable.setItem(j * 6 + 5, 2, dealValueItem[j])
                                    # 抓取店铺名和店铺所在地
                                    row_row_3 = WebDriverWait(ctx_box, 10).until(
                                        EC.presence_of_element_located((By.CLASS_NAME, 'row-3')))
                                    item_shop_name = WebDriverWait(row_row_3, 10).until(
                                        EC.presence_of_all_elements_located((By.TAG_NAME, 'span')))[4].text.strip()
                                    Logger.info('第{0}家店铺的商铺名爬取完毕'.format(j + 1))
                                    shopItem[j].setFont(self.table_2_Font)
                                    shopItem[j].setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                                    self.taobaoDataTable.setItem(j * 6 + 1, 1, shopItem[j])
                                    shopValueItem[j].setData(Qt.DisplayRole, QVariant(item_shop_name))
                                    self.taobaoDataTable.setItem(j * 6 + 1, 2, shopValueItem[j])

                                    item_location = WebDriverWait(row_row_3, 10).until(
                                        EC.presence_of_element_located((By.CLASS_NAME, 'location'))).text.strip()
                                    Logger.info('第{0}家店铺的货源地爬取完毕'.format(j + 1))
                                    if item_location == '':
                                        item_location = "抓取为空"
                                    sourceItem[j].setFont(self.table_2_Font)
                                    sourceItem[j].setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                                    self.taobaoDataTable.setItem(j * 6 + 2, 1, sourceItem[j])
                                    sourceValueItem[j].setData(Qt.DisplayRole, QVariant(item_location))
                                    self.taobaoDataTable.setItem(j * 6 + 2, 2, sourceValueItem[j])

                                    isJoinedItem[j].setFont(self.table_1_Font)
                                    isJoinedItem[j].setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                                    self.taobaoDataTable.setItem(j * 6, 3, isJoinedItem[j])
                                    self.taobaoDataTable.setSpan(j * 6 + 1, 3, 5, 1)
                                    checkItem[j].setCheckState(False)
                                    self.taobaoDataTable.setItem(j * 6 + 1, 3, checkItem[j])

                                    self.progressBar.setValue(math.ceil(((j + 1)/self.returnCNT) * 100))                              
                                except Exception as e:
                                    Logger.error(e)
                            
                            webDriver.quit()
                            DRIVER.quit()
                            Logger.info("数据爬取完毕")
                            messageDialog = MessageDialog()
                            messageDialog.information(self, "消息提示", "数据爬取完毕!")
                        except NoSuchElementException as e:
                            webDriver.quit()
                            DRIVER.quit()
                            Logger.error(e)
                    except NoSuchElementException as e:
                        webDriver.quit()
                        DRIVER.quit()
                        Logger.error(e)
                except TimeoutException as e:
                    webDriver.quit()
                    DRIVER.quit()
                    Logger.error(e)
            except WebDriverException as e:
                Logger.error(e)
        else:
            messageDialog = MessageDialog()
            messageDialog.warning(self, "消息提示", "请先输入搜索词!")
        
    def add_product_id(self):
        productID = self.addProductIDLineEdit.text().strip()
        if productID != '':
            conn = sqlite.connect('TBTracker_DB/TBTrackerTag.db')
            c = conn.cursor()
            c.execute('select count(*) from tag where TagName="{}"'.format(productID))
            count = c.fetchone()[0]
            if count == 0:
                c.execute('insert into tag values ("{}", "{}")'.format(productID, get_current_system_time()))
                conn.commit()
                c.close()
                messageDialog = MessageDialog()
                messageDialog.information(self, "消息提示", "标签入库成功!")
            else:
                messageDialog = MessageDialog()
                messageDialog.information(self, "消息提示", "标签已经存在!")
        else:
            messageDialog = MessageDialog()
            messageDialog.warning(self, "消息提示", "请先填写商品标签!")

    def attach_product_id(self):
        self.productID = self.attachProductIDLineEdit.text()
        messageDialog = MessageDialog()
        messageDialog.information(self, "消息提示", "标签标注成功!")

    def import_data(self):
        try:
            for j in range(self.returnCNT):
                flag = self.taobaoDataTable.item(j * 6 + 1, 3).checkState()
                if flag == 2:
                    conn = sqlite.connect('TBTracker_DB/TBTracker.db')
                    c = conn.cursor()
                    c.execute('insert into product values ("{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(
                        self.productID,
                        self.URLList[j],
                        self.taobaoDataTable.item(j * 6, 1).text(),
                        self.taobaoDataTable.item(j * 6 + 1, 2).text(),
                        self.taobaoDataTable.item(j * 6 + 3, 2).text(),
                        self.taobaoDataTable.item(j * 6 + 4, 2).text(), 
                        get_current_system_time()))
                    conn.commit()
                    c.close()
            messageDialog = MessageDialog()
            messageDialog.information(self, "消息提示", "        数据成功入库!        ") 

            self.show_database()
        except AttributeError as e:
            messageDialog = MessageDialog()
            messageDialog.warning(self, "消息提示", "未选择任何待导入的数据！") 

    def show_product_id(self):
        conn_1 = sqlite.connect('TBTracker_DB/TBTrackerTag.db')
        c_1 = conn_1.cursor()
        conn_2 = sqlite.connect('TBTracker_DB/TBTracker.db')
        c_2 = conn_2.cursor()

        c_1.execute('select * from tag')
        tagQueries = c_1.fetchall()
        CNT = len(tagQueries)
        _CNT = CNT

        for j in range(CNT):
            c_2.execute('select count(*) from product where ProductName="{}"'.format(tagQueries[j][0]))
            cnt = c_2.fetchone()
            if cnt[0] == 0:
                c_1.execute('delete from tag where TagName="{}"'.format(tagQueries[j][0]))
                conn_1.commit()
                _CNT -= 1

        CNT = _CNT
        self.productIDTable.setRowCount(CNT)
        for j in range(CNT):
            self.productIDTable.setItem(j, 0, QTableWidgetItem(tagQueries[j][0]))

        c_1.close()
        c_2.close()

    def show_database(self):
        conn = sqlite.connect('TBTracker_DB/TBTracker.db')
        c = conn.cursor()
        c.execute('select * from product order by CreateTime desc')
        queries = c.fetchall()
        self.DBCNT = len(queries)
        c.close()
        self.DBTable.setRowCount(self.DBCNT)
        for j in range(self.DBCNT):
            self.DBTable.setItem(j, 0, QTableWidgetItem(queries[j][0]))
            self.DBTable.setItem(j, 1, QTableWidgetItem(queries[j][2]))
            self.DBTable.setItem(j, 2, QTableWidgetItem(queries[j][3]))
            self.DBTable.setItem(j, 3, QTableWidgetItem(queries[j][4]))
            self.DBTable.setItem(j, 4, QTableWidgetItem(queries[j][5]))
            flag = QTableWidgetItem()
            flag.setCheckState(False)
            self.DBTable.setItem(j, 5, flag)

    def add_data(self):
        pass

    def delete_data(self):
        notDeleteCNT = 0
        for j in range(self.DBCNT):
            flag = self.DBTable.item(j, 5).checkState()
            if flag == Qt.Checked:
                conn = sqlite.connect('TBTracker_DB/TBTracker.db')
                c = conn.cursor()
                c.execute('delete from product where ProductName="{}" and Title="{}" and ShopName="{}" and Price="{}"'.format(
                    self.DBTable.item(j, 0).text(), 
                    self.DBTable.item(j, 1).text(), 
                    self.DBTable.item(j, 2).text(), 
                    self.DBTable.item(j, 3).text()))
                conn.commit()
                c.close()
            else:
                notDeleteCNT += 1
        if notDeleteCNT == self.DBCNT:
            messageDialog = MessageDialog()
            messageDialog.warning(self, "消息提示", "          无效操作!          ")
        else:
            self.show_database()

    def plot_product_tree(self):
        conn = sqlite.connect('TBTracker_DB/TBTrackerTag.db')
        c = conn.cursor()
        c.execute('select * from tag')
        tagQueries = c.fetchall()
        c.close()

        conn = sqlite.connect('TBTracker_DB/TBTracker.db')
        c = conn.cursor()
        roots = [QTreeWidgetItem(self.productTree) for _ in range(len(tagQueries))]
        for i, tagQuery in enumerate(tagQueries):
            roots[i].setText(0, tagQuery[0])
            roots[i].setFont(0, self.table_2_Font)
            roots[i].setCheckState(0, False)

            c.execute('select ShopName from product where ProductName="{}"'.format(tagQuery[0]))
            shopNames = list(set([query[0] for query in c.fetchall()]))
            childs = [QTreeWidgetItem(roots[i]) for _ in range(len(shopNames))]
            for j, child in enumerate(childs):
                child.setText(0, shopNames[j])
                child.setFont(0, self.table_1_Font)
                child.setCheckState(0, False)
                c.execute('select count(*) from product where ProductName="{}" and ShopName="{}"'.format(tagQuery[0], shopNames[j]))
                child.setText(1, str(c.fetchone()[0]))
            
            self.productTree.addTopLevelItem(roots[i])

        c.close()

    def select_global(self):
        currentTopLevelItemIndex = 0
        it = QTreeWidgetItemIterator(self.productTree)
        while it.value():
            if it.value() is self.productTree.topLevelItem(currentTopLevelItemIndex):
                currentTopLevelItemIndex += 1
                it.value().setCheckState(0, Qt.Checked)
                for _ in range(it.value().childCount()):
                    it = it.__iadd__(1)
                    it.value().setCheckState(0, Qt.Checked)
            it = it.__iadd__(1)

    def select_all(self):
        currentTopLevelItemIndex = 0
        it = QTreeWidgetItemIterator(self.productTree)
        while it.value():
            if it.value() is self.productTree.topLevelItem(currentTopLevelItemIndex):
                currentTopLevelItemIndex += 1
                if it.value().checkState(0) == Qt.Checked:
                    for _ in range(it.value().childCount()):
                        it = it.__iadd__(1)
                        it.value().setCheckState(0, Qt.Checked)
            it = it.__iadd__(1)

    def remove_data(self):
        conn = sqlite.connect('TBTracker_DB/TBTracker.db')
        c = conn.cursor()

        currentTopLevelItemIndex = 0
        it = QTreeWidgetItemIterator(self.productTree)
        while it.value():
            if it.value() is self.productTree.topLevelItem(currentTopLevelItemIndex):
                currentTopLevelItemIndex += 1
            else:
                if it.value().checkState(0) == Qt.Checked:
                    c.execute('delete from product where ProductName="{}" and ShopName="{}"'.format(
                        it.value().parent().text(0),
                        it.value().text(0)))
                    conn.commit()
            it = it.__iadd__(1)
        c.close()
        
        self.show_database()

    def export_data(self):
        mainDirectory = check_os()
        currentFileDialog = SaveFileDialog()
        fileName, filetype = currentFileDialog.save_file(self, caption="手动保存数据", directory=mainDirectory, filter="Excel Files (*.xlsx)")

        conn = sqlite.connect('TBTracker_DB/TBTracker.db')
        c = conn.cursor()

        currentTopLevelItemIndex = 0
        exportDataList = []
        it = QTreeWidgetItemIterator(self.productTree)
        while it.value():
            if it.value() is self.productTree.topLevelItem(currentTopLevelItemIndex):
                currentTopLevelItemIndex += 1
            else:
                if it.value().checkState(0) == Qt.Checked:
                    c.execute('select * from product where ProductName="{}" and ShopName="{}"'.format(
                        it.value().parent().text(0),
                        it.value().text(0)))
                    queries = c.fetchall()
                    exportDataList += queries
            it = it.__iadd__(1)
        c.close()
        
        excel = xlwt.Workbook()
        sheet = excel.add_sheet('商品数据', cell_overwrite_ok=True)
        sheet.write(0, 0, "商品标识")
        sheet.write(0, 1, "URL")
        sheet.write(0, 2, "标题")
        sheet.write(0, 3, "店铺名")
        sheet.write(0, 4, "价格")
        sheet.write(0, 5, "淘宝价")
        sheet.write(0, 6, "上次更新时间")
        for i, data in enumerate(exportDataList):
            sheet.write(i + 1, 0, data[0])
            sheet.write(i + 1, 1, data[1])
            sheet.write(i + 1, 2, data[2])
            sheet.write(i + 1, 3, data[3])
            sheet.write(i + 1, 4, data[4])
            sheet.write(i + 1, 5, data[5])
            sheet.write(i + 1, 6, data[6])
        excel.save("{}.xlsx".format(fileName))

    def plot_history_data(self, dateList, priceList):
        dateList = generate_date_list((2016, 12, 1), (2017, 1, 1))
        priceList = [random.randint(100, 300) for _ in range(len(dateList))]
        
        self.historyDataCanvas.axes.plot_date(dateList, priceList, 'r-o', linewidth=2)
        self.historyDataCanvas.axes.xaxis_date()
        self.historyDataCanvas.axes.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d'))
        self.historyDataCanvas.axes.set_xticks(dateList)
        self.historyDataCanvas.axes.set_xticklabels(dateList, rotation=90, fontsize=6)
        self.historyDataCanvas.axes.set_xlabel("时间轴", fontproperties=FONT, fontsize=10)
        self.historyDataCanvas.axes.set_yticks([100 * i for i in range(11)])
        self.historyDataCanvas.axes.set_ylabel("价格数据/￥", fontproperties=FONT, fontsize=10)
        self.historyDataCanvas.axes.set_title("商品历史数据图", fontproperties=FONT, fontsize=14)
        self.historyDataCanvas.draw()

    def select_commodity(self):
        pass

    def select_month(self):
        pass

    def select_year(self):
        pass

    def manual_update(self):
        import subprocess
        child = subprocess.Popen(["sudo", "python3", "TBTracker_RoutineSpider.py"])
        child.wait()
        messageDialog = MessageDialog()
        messageDialog.information(self, "消息提示", "手动更新完毕!")
    
    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonPress:
            pass
        return QWidget.eventFilter(self, source, event)
        

class TBTrackerAddDataWindow(QWidget):
    def __init__(self):
        super(TBTrackerAddDataWindow, self).__init__()
        self.create_main_window()

    def create_main_window(self):
        self.setWindowTitle("添加数据")
        self.setWindowIcon(QIcon('TBTracker_Ui/Spider.ico'))
        self.setMinimumSize(500, 350)
        self.setMaximumSize(500, 350)
        self.set_widgets()
        self.setLayout(self.layout)

    def set_widgets(self):
        self.productIDLineEdit = QLineEdit()
        self.URLLineEdit = QLineEdit()
        self.titleLineEdit = QLineEdit()
        self.shopNameLineEdit = QLineEdit()
        self.priceLineEdit = QLineEdit()
        self.taobaoPriceLineEdit = QLineEdit()
        self.createTimeLineEdit = QLineEdit()

        inputLayout = QGridLayout()
        inputLayout.addWidget(QLabel("商品标识"), 0, 0, 1, 1)
        inputLayout.addWidget(self.productIDLineEdit, 0, 1, 1, 3)
        inputLayout.addWidget(QLabel("URL"), 1, 0, 1, 1)
        inputLayout.addWidget(self.URLLineEdit, 1, 1, 1, 3)
        inputLayout.addWidget(QLabel("标题"), 2, 0, 1, 1)
        inputLayout.addWidget(self.titleLineEdit, 2, 1, 1, 3)
        inputLayout.addWidget(QLabel("店铺名"), 3, 0, 1, 1)
        inputLayout.addWidget(self.shopNameLineEdit, 3, 1, 1, 3)
        inputLayout.addWidget(QLabel("价格"), 4, 0, 1, 1)
        inputLayout.addWidget(self.priceLineEdit, 4, 1, 1, 3)
        inputLayout.addWidget(QLabel("淘宝价"), 5, 0, 1, 1)
        inputLayout.addWidget(self.taobaoPriceLineEdit, 5, 1, 1, 3)

        self.confirmButton = ConfirmButton()
        self.confirmButton.clicked.connect(self.confirm)
        cancelButton = CancelButton()
        cancelButton.clicked.connect(self.cancel)

        operateLayout = QHBoxLayout()
        operateLayout.addStretch()
        operateLayout.setSpacing(20)
        operateLayout.addWidget(self.confirmButton)
        operateLayout.addWidget(cancelButton)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(50, 20, 50, 20)
        self.layout.setSpacing(10)
        self.layout.addLayout(inputLayout)
        self.layout.addLayout(operateLayout)

    def confirm(self):
        pass

    def cancel(self):
        self.close()

class TBTrackerSelectCommodityWindow(QWidget):
    def __init__(self):
        super(TBTrackerSelectCommodityWindow, self).__init__()
        self.create_main_window()

    def create_main_window(self):
        self.setWindowTitle("选择商品")
        self.setWindowIcon(QIcon('TBTracker_Ui/Spider.ico'))
        self.setMinimumSize(700, 350)
        self.setMaximumSize(700, 350)
        self.set_widgets()
        self.setLayout(self.layout)

    def set_widgets(self):
        self.pull_all_commodities()

        self.confirmButton = ConfirmButton()
        cancelButton = CancelButton()
        cancelButton.clicked.connect(self.cancel)
        operateLayout = QHBoxLayout()
        operateLayout.addStretch()
        operateLayout.setSpacing(20)
        operateLayout.addWidget(self.confirmButton)
        operateLayout.addWidget(cancelButton)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(40, 20, 40, 20)
        self.layout.setSpacing(10)
        self.layout.addWidget(self.commodityTable)
        self.layout.addLayout(operateLayout)

    def confirm(self):
        pass

    def cancel(self):
        self.close()

    def pull_all_commodities(self):
        conn = sqlite.connect('TBTracker_DB/TBTracker.db')
        c = conn.cursor()
        c.execute('select Title from product')
        titleQueries = c.fetchall()
        c.close()

        self.commodityTable = QTableWidget(len(titleQueries), 2)
        self.commodityTable.horizontalHeader().hide()
        self.commodityTable.verticalHeader().hide()
        self.commodityTable.setSelectionMode(QAbstractItemView.NoSelection)
        self.commodityTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.commodityTable.setColumnWidth(0, 25)
        self.commodityTable.setColumnWidth(1, 577)

        radioButtonList = [QRadioButton() for i in range(len(titleQueries))]
        commodityList =  [QTableWidgetItem(titleQueries[i][0]) for i in range(len(titleQueries))]
        for i in range(len(titleQueries)):
            self.commodityTable.setCellWidget(i, 0, radioButtonList[i])
            self.commodityTable.setItem(i, 1, commodityList[i])


class TBTrackerSelectMonthWindow(QWidget):
    def __init__(self):
        super(TBTrackerSelectMonthWindow, self).__init__()
        self.create_main_window()

    def create_main_window(self):
        self.setWindowTitle("选择月份")
        self.setWindowIcon(QIcon('TBTracker_Ui/Spider.ico'))
        self.setMinimumSize(250, 100)
        self.setMaximumSize(250, 100)
        self.set_widgets()
        self.setLayout(self.layout)

    def set_widgets(self):
        self.monthComboBox = QComboBox()
        monthList = ["一月份数据", "二月份数据", "三月份数据", "四月份数据",
                     "五月份数据", "六月份数据", "七月份数据", "八月份数据",
                     "九月份数据", "十月份数据", "十一月份数据", "十二月份数据"] 
        self.monthComboBox.addItems(monthList)

        self.confirmButton = ConfirmButton()
        cancelButton = CancelButton()
        cancelButton.clicked.connect(self.cancel)
        operateLayout = QHBoxLayout()
        operateLayout.addStretch()
        operateLayout.setSpacing(20)
        operateLayout.addWidget(self.confirmButton)
        operateLayout.addWidget(cancelButton)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20,10)
        self.layout.setSpacing(10)
        self.layout.addWidget(self.monthComboBox)
        self.layout.addLayout(operateLayout)

    def confirm(self):
        pass

    def cancel(self):
        self.close()


class TBTrackerSelectYearWindow(QWidget):
    def __init__(self):
        super(TBTrackerSelectYearWindow, self).__init__()
        self.create_main_window()

    def create_main_window(self):
        self.setWindowTitle("选择年份")
        self.setWindowIcon(QIcon('TBTracker_Ui/Spider.ico'))
        self.setMinimumSize(250, 100)
        self.setMaximumSize(250, 100)
        self.set_widgets()
        self.setLayout(self.layout)

    def set_widgets(self):
        self.yearComboBox = QComboBox()
        self.get_year_range()
        self.yearComboBox.addItems(self.yearList)

        self.confirmButton = ConfirmButton()
        cancelButton = CancelButton()
        cancelButton.clicked.connect(self.cancel)
        operateLayout = QHBoxLayout()
        operateLayout.addStretch()
        operateLayout.setSpacing(20)
        operateLayout.addWidget(self.confirmButton)
        operateLayout.addWidget(cancelButton)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 10)
        self.layout.setSpacing(10)
        self.layout.addWidget(self.yearComboBox)
        self.layout.addLayout(operateLayout)

    def confirm(self):
        pass

    def cancel(self):
        self.close()

    def get_year_range(self):
        import datetime
        current_year = datetime.datetime.now().year
        self.yearList = [str(x) for x in range(2017, current_year + 1)]
    