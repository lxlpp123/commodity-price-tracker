# -*- coding: utf-8 -*-
import argparse
import ujson as json
import sqlite3 as sqlite
import os


def greeting():
    print("*********************** Welcome to Price Tracker System ***********************")
    print("*                                                                             *")
    print("*******************************************************************************")


def create_product_db(db):
    conn = sqlite.connect(db)
    cur = conn.cursor()
    try:
        cur.execute('CREATE TABLE product (\
            id           INTEGER   PRIMARY KEY, \
            link         TEXT      not null, \
            product_name TEXT      not null, \
            shop_name    TEXT      not null, \
            price        REAL      not null, \
            tb_price     REAL, \
            tm_price     REAL, \
            jd_price     REAL, \
            create_time  TIMESTAMP not null)')
    except sqlite.OperationalError as e:
        print(e)
    finally:
        cur.close()
    print("create {}".format(db))


def create_tag_db(db):
    conn = sqlite.connect(db)
    cur = conn.cursor()
    try:
        cur.execute('CREATE TABLE tag (\
            id          INTEGER   PRIMARY KEY, \
            name        TEXT      not null, \
            create_time TIMESTAMP not null)')
    except sqlite.OperationalError as e:
        print(e)
    finally:
        cur.close()
    print("create {}".format(db))


def create_routine_spider_db(db):
    conn = sqlite.connect(db)
    cur = conn.cursor()
    try:
        cur.execute('CREATE TABLE commodity (\
            id         INTEGER   PRIMARY KEY, \
            price      REAL      not null, \
            tb_price   REAL, \
            tm_price   REAL, \
            jd_price   REAL, \
            createTime TIMESTAMP not null)')
    except sqlite.OperationalError as e:
        print(e)
    finally:
        cur.close()
    print("create {}".format(db))


def init_db(conf_fn, force):
    greeting()

    f = open(conf_fn, "r")
    conf = json.load(f)
    f.close()
    root = conf["database"]["dir"]
    
    if os.path.exists("{}/product.db".format(root)):
        if force:
            os.remove("{}/product.db".format(root))
            create_product_db("{}/product.db".format(root))
    else:
        create_product_db("{}/product.db".format(root))

    if os.path.exists("{}/tag.db".format(root)):
        if force:
            os.remove("{}/tag.db".format(root))
            create_tag_db("{}/tag.db".format(root))
    else:
        create_tag_db("{}/tag.db".format(root))

    if os.path.exists("{}/routine_spider.db".format(root)):
        if force:
            os.remove("{}/routine_spider.db".format(root))
            create_routine_spider_db("{}/routine_spider.db".format(root))
    else:
        create_routine_spider_db("{}/routine_spider.db".format(root))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", help="initialize the database if not exists", action="store_true")
    parser.add_argument("--force_init", help="initialize the databases", action="store_true")
    parser.add_argument("--conf", help="config file", nargs='?', type=str, const=1, default="./conf/config.json")
    
    args = parser.parse_args()
    if args.init:
        init_db(args.conf, False)
    elif args.force_init:
        init_db(args.conf, True)
    else:
        print("unknown input")
