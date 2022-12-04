#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sqlite3
import datetime
from random import randint

from flask import Flask, request, render_template, jsonify

# Support for gomix's 'front-end' and 'back-end' UI.
app = Flask(__name__, static_folder='public', template_folder='views')

# Set the app secret key from the secret environment variables.
app.secret = os.environ.get('SECRET')


DBNAME = 'database.db'


def get_products(id=''):
  conn = sqlite3.connect(DBNAME)
  
  conn.row_factory = sqlite3.Row
  
  c = conn.cursor()
  
  if id == '':
    c.execute('SELECT * FROM products')
  else:
    c.execute('SELECT * FROM products WHERE product_id={}'.format(id))
    
  ret = c.fetchall()
  
  unpacked = [{k: item[k] for k in item.keys()} for item in ret]
  
  conn.commit()

  conn.close()  
  
  return unpacked

def get_customers(id=''):
  conn = sqlite3.connect(DBNAME)
  
  conn.row_factory = sqlite3.Row
  
  c = conn.cursor()
  
  if id == '':
    c.execute('SELECT * FROM (SELECT * FROM customers INNER JOIN Home_customers) c INNER JOIN address ON c.address_id = address.address_id')
  else:
    c.execute('SELECT * FROM (SELECT * FROM customers INNER JOIN Home_customers) c INNER JOIN address ON c.address_id = address.address_id WHERE c.customer_id={}'.format(id))
    
  ret = c.fetchall()
  
  unpacked = [{k: item[k] for k in item.keys()} for item in ret]
  
  conn.commit()

  conn.close()  
  
  return unpacked

def get_transactions(id=''):
  conn = sqlite3.connect(DBNAME)
  
  conn.row_factory = sqlite3.Row
  
  c = conn.cursor()
  
  if id == '':
    c.execute('SELECT * FROM transactions')
  else:
    c.execute('SELECT * FROM transactions WHERE order_id={}'.format(id))
    
  ret = c.fetchall()
  
  unpacked = [{k: item[k] for k in item.keys()} for item in ret]
  
  conn.commit()

  conn.close()  
  
  return unpacked

def filter_products(dic):
  filter = set()

  search = ''
  if dic['keyword'] != '':
      search = " name like '%" + dic['keyword'] + "%'"
  filter.add(search)

  categories = ''
  if dic['product_kind'] != '':
      categories = " product_kind = '%s'" % dic['product_kind']
  filter.add(categories)

  price_range = ''
  if dic['price_range'] == '1':
      price_range = ' price <= 2 '
  elif dic['price_range'] == '2':
      price_range = ' price > 2 and price <= 5 '
  elif dic['price_range'] == '3':
      price_range = ' price > 5 and price <= 10 '
  elif dic['price_range'] == '4':
      price_range = ' price > 10 '
  filter.add(price_range)

  if "" in filter:
    filter.remove("")

  conn = sqlite3.connect(DBNAME)

  conn.row_factory = sqlite3.Row

  c = conn.cursor()
  
  if filter:  
    sql = '''
    SELECT name, inventory_amount, price, product_kind 
    FROM Products
    where {}
    '''.format("and".join(filter))
  else:
    sql = '''
    SELECT name, inventory_amount, price, product_kind 
    FROM Products
    '''
    
  c.execute(sql)

  ret = c.fetchall()

  unpacked = [{k: item[k] for k in item.keys()} for item in ret]

  conn.commit()

  conn.close()

  print(unpacked)

  return unpacked
  
  
def get_region_volume():
  conn = sqlite3.connect(DBNAME)

  conn.row_factory = sqlite3.Row

  c = conn.cursor()

  sql = '''
  select r.region_id, r.region_name, a.sales_volumn from
  (select sa.store_assigned, sum(s.quantity) as sales_volumn from sales as s, 
  transactions as t, salespersons as sa
  where t.order_id = s.order_id 
  and t.salesperson_name = sa.name
  group by s.order_id) as a, store as st, region as r
  where st.store_id = a.store_assigned 
  and st.region = r.region_id
  '''

  c.execute(sql)

  ret = c.fetchall()

  unpacked = [{"region_name": [item["region_name"] for item in ret], "sales_volumn": [item["sales_volumn"] for item in ret]} ]

  conn.commit()

  conn.close()

  return unpacked

def get_popular_kind():
  conn = sqlite3.connect(DBNAME)

  conn.row_factory = sqlite3.Row

  c = conn.cursor()
  
  sql = '''
  select sum(t.sales_volumn) as sales_volume, sum(t.sales_revenue) as sales_revenue, t.product_kind from 
  (select a.product_id, b.name, sum(a.quantity) as sales_volumn, b.price*sum(a.quantity) as sales_revenue, (b.price - b.cost)*sum(a.quantity) as profit, b.product_kind
  from sales as a
  left join
  products as b
  on a.product_id = b.product_id
  group by a.product_id) t
  group by t.product_kind
  order by t.sales_volumn desc
  limit 1;
  '''
  c.execute(sql)

  ret = c.fetchall()

  unpacked = [{k: item[k] for k in item.keys()} for item in ret]
  
  conn.commit()

  conn.close()

  return unpacked

def get_sales():
  conn = sqlite3.connect(DBNAME)

  conn.row_factory = sqlite3.Row

  c = conn.cursor()
  
  sql = '''
  select a.product_id, b.name, sum(a.quantity) as sales_volume, round(b.price*sum(a.quantity), 2) as sales_revenue, 
  round((b.price - b.cost)*sum(a.quantity), 2) as profit, b.product_kind
  from sales as a
  left join
  products as b
  on a.product_id = b.product_id
  group by a.product_id;
  '''
  c.execute(sql)

  ret = c.fetchall()

  unpacked = [{k: item[k] for k in item.keys()} for item in ret]
  
  conn.commit()

  conn.close()

  return unpacked
  
def update_products(dic):
  conn = sqlite3.connect(DBNAME)

  conn.row_factory = sqlite3.Row

  c = conn.cursor()
  
  sql = 'UPDATE Products SET price = ' + dic['price'] + ', name = "' + dic['name'] + '", inventory_amount = ' + dic['inventory_amount'] + ' WHERE product_id = ' + "'" + \
        dic['product_id'] + "'"
  
  c.execute(sql)
  
  conn.commit()

  conn.close()


def insert(data_list, table, many=False):  
  if many:
    data0 = data_list[0]
    data = [tuple(i.values()) for i in data_list]
  else:
    data0 = data_list
    data = tuple(data0.values())
  cols = ", ".join('?'.format(k) for k in data0.keys())
  sql = 'INSERT INTO ' + table + '%s VALUES(%s)' % (tuple(data0.keys()), cols)
  return sql, data
  
def insert_personal_info(dic):
  conn = sqlite3.connect(DBNAME)

  conn.row_factory = sqlite3.Row

  cur = conn.cursor()
  # insert into address table
  address_dict = {'street': dic['street'], 'city': dic['city'], 'state': dic['state'], 'zip_code': dic['zipcode']}
  sql, data = insert(address_dict, 'Address')
  cur.execute(sql, data)
  conn.commit()

  # get address id
  cur1 = conn.cursor()
  get_add_id = '''
  select max(address_id) from Address
  '''
  cur1.execute(get_add_id)
  address_id = cur1.fetchall()[0][0]
  cur1.close()

  # insert into customers table
  cus_dict = {'customer_id': dic['customer_id'], 'name': dic['name'], 'address_id': address_id, 'kind': dic['kind']}
  sql, data = insert(cus_dict, 'Customers')
  cur.execute(sql, data)

  sql = ''
  # insert into home_c or bus_c
  kind = dic['kind']
  if kind == 'home':
      home_dic = {'customer_id': dic['customer_id'], 'marriage': dic['marriage'], 'gender': dic['gender'],
                  'age': dic['age'], 'income': dic['income']}
      sql, data = insert(home_dic, 'Home_customers')
  elif kind == 'business':
      bus_dic = {'customer_id': dic['customer_id'], 'business_category': dic['business_category'],
                 'annual_income': dic['annual_income']}
      sql, data = insert(bus_dic, 'Business_customers')

  cur.execute(sql, data)
  conn.commit()
  cur.close()
  conn.close()
  
def insert_order(dic):
  conn = sqlite3.connect(DBNAME)

  conn.row_factory = sqlite3.Row

  cur = conn.cursor()

  # generate salesperson
  cur.execute('select name from salespersons')
  name = []
  for row in cur.fetchall():
      name += list(row)
  random = randint(0, len(name) - 1)

  # get current date
  time = datetime.date.today()

  # insert transaction
  tran_dict = {'customer_id': dic['customer_id'], 'total_price': dic['total'],
               'date': time, 'salesperson_name': name[random]}
  sql, data = insert(tran_dict, 'Transactions')
  cur.execute(sql, data)
  conn.commit()

  # get order id
  cur1 = conn.cursor()
  get_add_id = '''
  select max(order_id) from Transactions
  '''
  cur1.execute(get_add_id)
  order_id = cur1.fetchall()[0][0]
  cur1.close()

  # insert sales
  product_ids = list(dic['order'].keys())
  quantity = list(dic['order'].values())
  sales_dict = []
  for i in range(len(quantity)):
      sales_dict.append({'order_id': order_id, 'product_id': int(product_ids[i]), 'quantity': float(quantity[i])})
  sql, data = insert(sales_dict, 'Sales', many=True)
  cur.executemany(sql, data)

  # update inventory
  for i in range(len(quantity)):
      cur2 = conn.cursor()
      get_current_inv = 'select inventory_amount from products where product_id = ' + str(product_ids[i])
      cur2.execute(get_current_inv)
      curr_inv = cur2.fetchall()[0][0]
      update_inv = 'update Products set inventory_amount = ' + str(curr_inv - int(quantity[i])) + ' where product_id = ' + \
                   product_ids[i]
      cur2.execute(update_inv)
      conn.commit()

  conn.commit()
  cur.close()
  conn.close()
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'POST':
    data = None
    if request.is_json:
      data = request.get_json()["data"]
      insert_personal_info(data)
      
  return jsonify(get_customers())

@app.route('/products', methods=['GET', 'POST'])
def products():
  if request.method == 'POST':
    data = None
    if request.is_json:
      data = request.get_json()["data"]
      print(data)

  return jsonify(get_products())

@app.route('/products/<product_id>', methods=['GET', 'POST'])
def products2(product_id):

    if request.method == 'POST':
      data = None
      if request.is_json:
        data = request.get_json()["data"]
        update_products(data)
        
    return jsonify(get_products(product_id))

@app.route('/users/<user_id>', methods=['GET', 'POST'])
def user2(user_id):

    if request.method == 'POST':
      data = None
      if request.is_json:
        data = request.get_json()["data"]
        # update_products(data)
        
    return jsonify(get_customers(user_id))
  
@app.route('/admin', methods=['GET'])
def admin():
  data = get_region_volume()
  data2 = get_popular_kind()
  res = {
    "regions":data,
    "category":data2
  }
  return jsonify(res)

@app.route('/sales', methods=['GET'])
def sales():
  data = get_sales()
  return jsonify(data)
  
@app.route('/cart', methods=['POST'])
def cart():
  res = []
  if request.method == 'POST':
    data = None
    if request.is_json:
      data = request.get_json()
      for p in data["data"]:
        res += get_products(p)

    return jsonify(res)

  
@app.route('/search', methods=['POST'])
def search():
  if request.method == 'POST':
    data = None
    if request.is_json:
      data = request.get_json()["data"]
      res = filter_products(data)
    return jsonify(res)
  
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
  if request.method == 'POST':
    data = None
    if request.is_json:
      data = request.get_json()["data"]
      print(data)
      insert_order(data)

  return jsonify(get_transactions())
  

if __name__ == '__main__':
  app.run()