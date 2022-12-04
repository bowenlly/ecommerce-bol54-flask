import os
import sqlite3

DBNAME = 'database.db'

address_list = [
    {'address_id': 10001, 'street': '114 Abbott Ct.', 'city': 'Walkersville', 'state': 'MD', 'zip_code': '21793'},
    {'address_id': 10002, 'street': '6773 Oak Ridge Rd.', 'city': 'New Market', 'state': 'MD', 'zip_code': '21774'},
    {'address_id': 10003, 'street': '3566 Glen Abbey Drive', 'city': 'Chambersburg', 'state': 'MD',
     'zip_code': 17201},
    {'address_id': 10004, 'street': '5313 Brookville Rd', 'city': 'Gaithersburg', 'state': 'MD', 'zip_code': '20822'},
    {'address_id': 10005, 'street': '9932 McKinstry Mill Rd.', 'city': 'New Windsor', 'state': 'MD',
     'zip_code': '21776'},
    {'address_id': 10006, 'street': '91 Schofield Rd.', 'city': 'West Milford', 'state': 'NJ', 'zip_code': '07480'},
    {'address_id': 10007, 'street': '2114 Carroll Creek View Ct', 'city': 'Frederick', 'state': 'MD',
     'zip_code': '21702'},
    {'address_id': 10008, 'street': '11622 Creagerstown Rd.', 'city': 'Woodsboro', 'state': 'MD',
     'zip_code': '21798'},
    {'address_id': 10009, 'street': '10922 Green Valley Rd.', 'city': 'Union Bridge', 'state': 'MD',
     'zip_code': '21791'},
    {'address_id': 10010, 'street': 'P.O. Box 758', 'city': 'Mt. Airy', 'state': 'MD', 'zip_code': '21770'},
    {'address_id': 10011, 'street': 'P.O. Box 181', 'city': 'gaithersburg', 'state': 'MD', 'zip_code': '20844'},
    {'address_id': 10012, 'street': '8051 Sixes Bridge Rd.', 'city': 'Detour', 'state': 'MD', 'zip_code': '21757'},
    {'address_id': 10013, 'street': '11834 Creagerstown Rd.', 'city': 'Woodsboro', 'state': 'MD',
     'zip_code': '21798'},
    {'address_id': 10014, 'street': '17425 Sunshine Trail', 'city': 'Sabillasville', 'state': 'MD',
     'zip_code': '21780'},
    {'address_id': 10015, 'street': '18410 Comus Rd.', 'city': 'Dickerson', 'state': 'MD', 'zip_code': '20842'},
    {'address_id': 10016, 'street': '10642 Woodsboro Rd.', 'city': 'Woodsboro', 'state': 'MD', 'zip_code': '21798'},
    {'address_id': 10017, 'street': '18716 Lappans Rd.', 'city': 'Boonsboro', 'state': 'MD', 'zip_code': '21713'},
    {'address_id': 10018, 'street': '6246 Derby Drive', 'city': 'Frederick', 'state': 'MD', 'zip_code': '21702'},
    {'address_id': 10019, 'street': '6600 Coffman Farms Rd', 'city': 'Keedysville', 'state': 'MD',
     'zip_code': '21756'},
    {'address_id': 10020, 'street': '7839 West Hills Drive', 'city': 'Frederick', 'state': 'MD', 'zip_code': '21702'},
    {'address_id': 10021, 'street': '103 Locust Street', 'city': 'Frederick', 'state': 'MD', 'zip_code': '21702'},
    {'address_id': 10022, 'street': '1731 Monocacy Blvd.', 'city': 'Frederick', 'state': 'MD', 'zip_code': '21701'},
    {'address_id': 10023, 'street': '9640 Liberty Rd.', 'city': 'Frederick', 'state': 'MD', 'zip_code': '21701'},
    {'address_id': 10024, 'street': '200 East Patrick Street', 'city': 'Frederick', 'state': 'MD',
     'zip_code': '21702'}
]

region_list = [
    {'region_id': 20001, 'region_name': 'Shadyside', 'region_manager': 'Tom'},
    {'region_id': 20002, 'region_name': 'Squirrel Hill', 'region_manager': 'James'},
    {'region_id': 20003, 'region_name': 'Greenfield', 'region_manager': 'Jennifer'},
    {'region_id': 20004, 'region_name': 'Oakland', 'region_manager': 'John'},
    {'region_id': 20005, 'region_name': 'Downtown', 'region_manager': 'Joseph'},
    {'region_id': 20006, 'region_name': 'Bloomfield', 'region_manager': 'Lisa'},
    {'region_id': 20007, 'region_name': 'Hill District', 'region_manager': 'Nancy'}
]

products_list = [
    {'product_id': 1001, 'name': 'banana', 'inventory_amount': 69, 'price': 1.39, 'cost': 0.83,
     'product_kind': 'fruit'},
    {'product_id': 1002, 'name': 'orange', 'inventory_amount': 55, 'price': 2.79, 'cost': 1.83,
     'product_kind': 'fruit'},
    {'product_id': 1003, 'name': 'grape', 'inventory_amount': 0, 'price': 3.49, 'cost': 2.48,
     'product_kind': 'fruit'},
    {'product_id': 1004, 'name': 'apple', 'inventory_amount': 153, 'price': 2.49, 'cost': 1.55,
     'product_kind': 'fruit'},
    {'product_id': 1005, 'name': 'pork loin', 'inventory_amount': 23, 'price': 4.79, 'cost': 3.45,
     'product_kind': 'meat'},
    {'product_id': 1006, 'name': 'steak', 'inventory_amount': 43, 'price': 6.99, 'cost': 4.25,
     'product_kind': 'meat'},
    {'product_id': 1007, 'name': 'chicken', 'inventory_amount': 5, 'price': 17.99, 'cost': 13.45,
     'product_kind': 'meat'},
    {'product_id': 1008, 'name': 'lamb chops', 'inventory_amount': 15, 'price': 11.99, 'cost': 10.24,
     'product_kind': 'meat'},
    {'product_id': 1009, 'name': 'green cabbage', 'inventory_amount': 35, 'price': 0.99, 'cost': 0.45,
     'product_kind': 'vegetable'},
    {'product_id': 1010, 'name': 'taro', 'inventory_amount': 96, 'price': 2.39, 'cost': 1.25,
     'product_kind': 'vegetable'},
    {'product_id': 1011, 'name': 'radish', 'inventory_amount': 45, 'price': 1.09, 'cost': 0.55,
     'product_kind': 'vegetable'},
    {'product_id': 1012, 'name': 'potato', 'inventory_amount': 164, 'price': 1.09, 'cost': 0.46,
     'product_kind': 'vegetable'},
    {'product_id': 1013, 'name': 'salmon', 'inventory_amount': 26, 'price': 11.99, 'cost': 8.95,
     'product_kind': 'seafood'},
    {'product_id': 1014, 'name': 'raw shrimp', 'inventory_amount': 95, 'price': 8.99, 'cost': 6.48,
     'product_kind': 'seafood'},
    {'product_id': 1015, 'name': 'mussels', 'inventory_amount': 49, 'price': 7.99, 'cost': 4.26,
     'product_kind': 'seafood'},
    {'product_id': 1016, 'name': 'Danish cookies', 'inventory_amount': 12, 'price': 9.29, 'cost': 5.46,
     'product_kind': 'snack'},
    {'product_id': 1017, 'name': 'oreo vanilla cookie', 'inventory_amount': 46, 'price': 4.59, 'cost': 1.36,
     'product_kind': 'snack'},
    {'product_id': 1018, 'name': 'cola', 'inventory_amount': 211, 'price': 3.15, 'cost': 0.62,
     'product_kind': 'drink'},
    {'product_id': 1019, 'name': 'sprite', 'inventory_amount': 245, 'price': 4.26, 'cost': 0.,
     'product_kind': 'drink'},
    {'product_id': 1020, 'name': 'pepper', 'inventory_amount': 131, 'price': 3.49, 'cost': 0.36,
     'product_kind': 'seasoner'},
    {'product_id': 1021, 'name': 'salt', 'inventory_amount': 23, 'price': 4.22, 'cost': 0.21,
     'product_kind': 'seasoner'},
    {'product_id': 1022, 'name': 'curry', 'inventory_amount': 142, 'price': 3.49, 'cost': 0.46,
     'product_kind': 'seasoner'}
]

store_list = [
    {'store_id': 1, 'address_id': 10003, 'salesperson_number': 3, 'region': 20001},
    {'store_id': 2, 'address_id': 10007, 'salesperson_number': 4, 'region': 20002},
    {'store_id': 3, 'address_id': 10014, 'salesperson_number': 2, 'region': 20003},
    {'store_id': 4, 'address_id': 10022, 'salesperson_number': 3, 'region': 20004},
    {'store_id': 5, 'address_id': 10023, 'salesperson_number': 5, 'region': 20004},
    {'store_id': 6, 'address_id': 10013, 'salesperson_number': 2, 'region': 20005},
    {'store_id': 7, 'address_id': 10020, 'salesperson_number': 4, 'region': 20006},
    {'store_id': 8, 'address_id': 10019, 'salesperson_number': 3, 'region': 20007}
]

salespersons_list = [
    {'name': 'Justin', 'address_id': 10002, 'email': 'shjdh@gmail.com', 'job_title': 'sales associate',
     'store_assigned': 1, 'salary': 3000},
    {'name': 'Eric', 'address_id': 10011, 'email': 'fjijjah@gmail.com', 'job_title': 'cashier',
     'store_assigned': 2, 'salary': 3000},
    {'name': 'Anna', 'address_id': 10012, 'email': 'xiuvhi@gmail.com', 'job_title': 'customer service representative',
     'store_assigned': 3, 'salary': 3500},
    {'name': 'Nicole', 'address_id': 10018, 'email': 'oigfu@gmail.com', 'job_title': 'store manager',
     'store_assigned': 4, 'salary': 6000},
    {'name': 'Larry', 'address_id': 10021, 'email': 'djogj@gmail.com', 'job_title': 'assistant store manager',
     'store_assigned': 5, 'salary': 5000},
    {'name': 'Amy', 'address_id': 10024, 'email': 'oguoisof@gmail.com', 'job_title': 'inventory control specialist',
     'store_assigned': 6, 'salary': 4500}
]

customers_list = [
    {'customer_id': '10102', 'name': 'Jerry', 'address_id': 10001, 'kind': 'home'},
    {'customer_id': '10103', 'name': 'Eyecatchers', 'address_id': 10004, 'kind': 'business'},
    {'customer_id': '10104', 'name': 'Raemelton Farm', 'address_id': 10005, 'kind': 'business'},
    {'customer_id': '10105', 'name': 'Victoria', 'address_id': 10008, 'kind': 'home'},
    {'customer_id': '10106', 'name': 'Kyle', 'address_id': 10010, 'kind': 'home'}
]

home_customers_list = [
    {'customer_id': '10102', 'marriage': 'never married', 'gender': 'male', 'age': 24, 'income': '4200'},
    {'customer_id': '10105', 'marriage': 'married', 'gender': 'female', 'age': 30, 'income': '7500'},
    {'customer_id': '10106', 'marriage': 'never married', 'gender': 'female', 'age': 18, 'income': '0'}
]

business_customers_list = [
    {'customer_id': '10103', 'business_category': 'medical treatment', 'annual_income': '102250'},
    {'customer_id': '10104', 'business_category': 'stock farming', 'annual_income': '462530'}
]

transaction_list = [
    {'customer_id': '10102', 'order_id': 1, 'total_price': 43.32, 'date': '2022-01-12',
     'salesperson_name': 'Justin'},
    {'customer_id': '10105', 'order_id': 2, 'total_price': 18.92, 'date': '2022-05-23',
     'salesperson_name': 'Eric'},
    {'customer_id': '10106', 'order_id': 3, 'total_price': 166.70, 'date': '2022-09-30',
     'salesperson_name': 'Larry'}
]

sales_list = [
    {'order_id': 1, 'product_id': 1001, 'quantity': 5},
    {'order_id': 1, 'product_id': 1022, 'quantity': 2},
    {'order_id': 1, 'product_id': 1010, 'quantity': 1},
    {'order_id': 1, 'product_id': 1011, 'quantity': 2},
    {'order_id': 1, 'product_id': 1004, 'quantity': 1},
    {'order_id': 1, 'product_id': 1002, 'quantity': 3},
    {'order_id': 1, 'product_id': 1003, 'quantity': 4},
    {'order_id': 2, 'product_id': 1009, 'quantity': 7},
    {'order_id': 2, 'product_id': 1011, 'quantity': 9},
    {'order_id': 2, 'product_id': 1012, 'quantity': 2},
    {'order_id': 3, 'product_id': 1016, 'quantity': 4},
    {'order_id': 3, 'product_id': 1008, 'quantity': 6},
    {'order_id': 3, 'product_id': 1018, 'quantity': 11},
    {'order_id': 3, 'product_id': 1017, 'quantity': 5}
]
  
  
def generate_sql(data_list, table):
    data0 = data_list[0]
    cols = ", ".join('?'.format(k) for k in data0.keys())
    sql = 'INSERT INTO ' + table + '%s VALUES(%s)' % (tuple(data0.keys()), cols)
    data = [tuple(i.values()) for i in data_list]
    return sql, data


def bootstrap_db():

  if os.path.exists(DBNAME):
    os.remove(DBNAME)

  conn = sqlite3.connect(DBNAME)

  c = conn.cursor()

  cur = conn.cursor()
  
  table = '''
  create table Address(
      address_id varchar(8),
      street varchar(50),
      city varchar(20),
      state varchar(20),
      zip_code varchar(5),
      primary key (address_id)
  );

  create table Region(
      region_id varchar(8),
      region_name varchar(20),
      region_manager varchar(20),
      primary key (region_id)
  );

  create table Products(
      product_id varchar(8),
      name varchar(20),
      inventory_amount numeric(4, 0) check(inventory_amount >= 0),
      price numeric(6, 2) check(price >= 0),
      cost numeric(6, 2) check(cost >= 0),
      product_kind varchar(20),
      primary key (product_id)
  );

  create table Store(
      store_id varchar(8),
      address_id varchar(8),
      salesperson_number numeric(2, 0),
      region varchar(8),
      primary key (store_id),
      foreign key (region) references Region(region_id)
                    on delete cascade 
  );

  create table Salespersons(
      name varchar(20),
      address_id varchar(8),
      email varchar(40),
      job_title varchar(40),
      store_assigned varchar(20),
      salary numeric(8, 2) check(salary > 0),
      primary key (name),
      foreign key (address_id) references Address(address_id)
                           on delete cascade, 
      foreign key (store_assigned) references Store(store_id)
                           on delete cascade
  );

  create table Customers(
      customer_id varchar(8),  
      name varchar(20),
      address_id varchar(20),
      kind varchar(10),
      primary key (customer_id),
      foreign key (address_id) references Address(address_id)
                        on delete cascade 
  );

  create table Business_customers(
      customer_id varchar(8),
      business_category varchar(20),
      annual_income varchar(10),
      foreign key(customer_id) references Customers(customer_id)
  );

  create table Home_customers(
      customer_id varchar(8),
      marriage varchar(15),
      gender varchar(8),
      age int,
      income varchar(10),
      foreign key(customer_id) references Customers(customer_id)
  );

  create table Transactions(
      customer_id varchar(8),
      order_id varchar(8),
      total_price numeric(6, 2) check(total_price >= 0),
      date date,
      salesperson_name varchar(20),
      primary key (order_id),
      foreign key (customer_id) references Customers(customer_id)
                          on delete cascade,
      foreign key (salesperson_name) references Salespersons(name)
                          on delete cascade 
  );

  create table Sales(
      order_id varchar(8),
      product_id varchar(8),
      quantity numeric(3, 0),
      primary key (order_id, product_id),
      foreign key (order_id) references Transactions(order_id)
                    on delete cascade,
      foreign key (product_id) references Products(product_id)
                    on delete cascade 
  );
  '''

  for create in table.split(";"):
  
    cur.execute(create)
  


  sql, data = generate_sql(address_list, 'address')
  cur.executemany(sql, data)
  sql, data = generate_sql(region_list, 'region')
  cur.executemany(sql, data)
  sql, data = generate_sql(products_list, 'products')
  cur.executemany(sql, data)
  sql, data = generate_sql(store_list, 'store')
  cur.executemany(sql, data)
  sql, data = generate_sql(salespersons_list, 'salespersons')
  cur.executemany(sql, data)
  sql, data = generate_sql(customers_list, 'customers')
  cur.executemany(sql, data)
  sql, data = generate_sql(home_customers_list, 'home_customers')
  cur.executemany(sql, data)
  sql, data = generate_sql(business_customers_list, 'business_customers')
  cur.executemany(sql, data)
  sql, data = generate_sql(transaction_list, 'transactions')
  cur.executemany(sql, data)
  sql, data = generate_sql(sales_list, 'sales')
  cur.executemany(sql, data)

  conn.commit()

  conn.close()
  
if __name__ == '__main__':
    bootstrap_db()