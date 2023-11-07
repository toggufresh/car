from project import app
from flask import Flask, request, redirect, url_for
from project.controllers.my_dao import *


@app.route('/save_car', methods=['POST'])
def save_car_info():
  record = json.loads(request.data)
  print(record)

@app.route('/get_cars', methods=['GET'])
def query_records():
   return findAllCars()

@app.route('/update_car/<make>/<model>/<reg>/<year>/<status>', methods=['PUT'])
def update_car_info(make, model, reg, year, status):
    return update_car(make, model, reg, year, status)


@app.route('/delete_car/<string:reg>', methods=['DELETE'])
def delete_car_info(reg):
    delete_car(reg)
    return findAllCars()

@app.route('/get_cars_by_reg_number/<string:car_reg>', methods=['GET'])
def find_car_by_reg_number(car_reg):
    return findCarByReg(car_reg)

@app.route('/create_car/<string:make>/<string:model>/<string:car_reg>/<int:year>/<string:status>', methods=['POST'])
def create_car_info(make, model, car_reg, year, status):
    cars = create_car(make, model, car_reg, year, status)
    return cars


#Implementing Customer database
@app.route('/create_customer/<string:name>/<int:age>/<string:address>', methods=['POST'])
def create_customer_info(name, age, address):
    new_customer = createCustomer(name, age, address)
    return jsonify(new_customer)

@app.route('/get_customers', methods=['GET'])
def query_customers():
    customers = findAllCustomers()
    return {'customers': customers}

@app.route('/get_customer/<int:customer_id>', methods=['GET'])
def get_customer_by_id(customer_id):
    customer = findCustomerById(customer_id)
    return customer

@app.route('/update_customer/<int:customer_id>/<string:name>/<int:age>/<string:address>', methods=['PUT'])
def update_customer_info(customer_id, name, age, address):
    updated_customer = updateCustomer(customer_id, name, age, address)
    return jsonify(updated_customer), 200

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

@app.route('/findEmployeeById', methods=['GET'])
def query_employees():
    return findAllEmployees()

@app.route('/update_employee/<int:employee_id>/<string:name>/<string:address>/<string:branch>', methods=['PUT'])
def update_employee_info(employee_id, name, address, branch):
    updated_employee = updateEmployee(employee_id, name, address, branch)
    return jsonify(updated_employee), 200

@app.route('/delete_employee', methods=['DELETE'])
def delete_employee_info(employee_id):
    deleteEmployee(employee_id)
    return "Employee deleted"



#Implementing ordering of cars
@app.route('/order_car/<int:customer_id>/<string:car_reg>', methods=['POST'])
def order_car_info(customer_id, car_reg):
    result = order_car(customer_id, car_reg)
    return result


#Implementing cancellation of cars
@app.route('/cancel_order_car/<int:customer_id>/<int:car_reg>', methods=['POST'])
def cancel_order_car_info(customer_id, car_reg):
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
@app.route('/return_car/<int:customer_id>/<string:car_reg>/<string:car_status>', methods=['PUT'])
def return_car_info():
    result = return_car(customer_id, car_reg, car_status)
    return result