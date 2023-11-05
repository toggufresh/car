from project import app
import json
from flask import request
from project.models.my_dao import *
# C:\Users\OhRLD\Downloads\__MACOSX\flask-mvc-example\project\venv\Scripts\activate


@app.route('/save_car', methods=['POST'])
def save_car_info():
  record = json.loads(request.data)
  print(record)


@app.route('/get_cars', methods=['GET'])
def query_records():
   return findAllCars()



@app.route('/update_car', methods=['PUT'])
def update_car_info():
  record = json.loads(request.data)
  print(record)
  return update_car(record['make'], record['model'], record['reg'], record['year'], record['capacity'])

@app.route('/delete_car', methods=['DELETE'])
def delete_car_info():
  record = json.loads(request.data)
  print(record)
  delete_car(record['reg'])
  return findAllCars()

@app.route('/get_cars_by_reg_number', methods=['POST'])
def find_car_by_reg_number():
   record = json.loads(request.data)
   print(record)
   print(record['reg'])
   return findCarByReg(record['reg'])

@app.route('/create_car', methods=['POST'])
def create_car_info():
    data = json.loads(request.data)
    make = data.get('make')
    model = data.get('model')
    reg = data.get('reg')
    year = data.get('year')
    capacity = data.get('capacity')
    cars = create_car(make, model, reg, year, capacity)
    return cars
  
#Implementing Customer database
@app.route('/create_customer', methods=['POST'])
def create_customer_info():
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    address = data.get('address')
    new_customer = createCustomer(name, age, address)
    return new_customer

@app.route('/get_customers', methods=['GET'])
def query_customers():
    customers = findAllCustomers()
    return {'customers': customers}

@app.route('/get_customer/<int:customer_id>', methods=['GET'])
def get_customer_by_id(customer_id):
    customer = findCustomerById(customer_id)
    return customer

@app.route('/update_customer/<int:customer_id>', methods=['PUT'])
def update_customer_info(customer_id):
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    address = data.get('address')
    updated_customer = updateCustomer(customer_id, name, age, address)
    return updateCustomer

@app.route('/delete_customer/<int:customer_id>', methods=['DELETE'])
def delete_customer_info(customer_id):
    customer = findCustomerById(customer_id)
    if customer:
        deleteCustomer(customer_id)


#Implementing Employee

@app.route('/create_employee', methods=['POST'])
def create_employee_info():
    data = request.get_json()
    name = data.get('name')
    address = data.get('address')
    branch = data.get('branch')
    employees = createEmployee(name, address, branch)
    return employees

@app.route('/get_employee', methods=['GET'])
def query_employees():
    return findAllEmployees()

@app.route('/update_employee', methods=['PUT'])
def update_employee_info():
    data = request.get_json()
    employee_id = data.get('employee_id')
    name = data.get('name')
    address = data.get('address')
    branch = data.get('branch')
    employees = updateEmployee(employee_id, name, address, branch)
    return employees

@app.route('/delete_employee', methods=['DELETE'])
def delete_employee_info(employee_id):
    deleteEmployee(employee_id)
    return "Employee deleted"



#implementing ordering of cars




@app.route('/order_car', methods=['POST'])
def order_car_info():
    data = json.loads(request.data)
    customer_id = data.get('customer_id')
    car_reg = data.get('car_reg')

    if customer_id is None or car_reg is None:
        return "Please provide both customer_id and car_reg.", 400
    
    else:
        result = order_car(customer_id, car_reg)
        return result

#Implementing cancellation of cars

@app.route('/cancel_order_car', methods=['POST'])
def cancel_order_car_info():
    data = json.loads(request.data)
    customer_id = data.get('customer_id')
    car_reg = data.get('car_reg')

    if customer_id is None or car_reg is None:
        return "Please provide both customer_id and car_reg.", 400

    result = cancel_order_car(customer_id, car_reg)

    return result

#implementing renting cars
@app.route('/rent_car', methods=['POST'])
def rent_car_info():
    data = json.loads(request.data)
    customer_id = data.get('customer_id')
    car_reg = data.get('car_reg')

    if customer_id is None or car_reg is None:
        return "Please provide both customer_id and car_reg.", 400

    else:
        result = rent_car(customer_id, car_reg)
        return result


#Implementing returning cars
@app.route('/return_car', methods=['POST'])
def return_car_info():
    data = json.loads(request.data)
    customer_id = data.get('customer_id')
    car_reg = data.get('car_reg')
    car_status = data.get('car_status')

    if customer_id is None or car_reg is None or car_status is None:
        return "Please provide customer_id, car_reg, and car_status.", 400

    else:
        result = return_car(customer_id, car_reg, car_status)
        return result