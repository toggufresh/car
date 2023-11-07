from project import app
from project.controllers.my_dao import *

@app.route('/save_car', methods=['POST'])
def save_car_info():
  record = json.loads(request.data)
  print(record)


@app.route('/find_all_cars', methods=['GET'])
def query_records():
   return find_all_cars()


@app.route('/update_car', methods=['PUT'])
def update_car_info():
  record = json.loads(request.data)
  print(record)
  return update_car(record['make'], record['model'], record['car_reg'], record['status'])


@app.route('/delete_car', methods=['DELETE'])
def delete_car_info():
  record = json.loads(request.data)
  car_reg = record.get('car_reg')
  print(record)
  delete_car(car_reg)
  return f'{car_reg} has been deleted succesfully.\n{find_all_cars()}'


@app.route('/find_car', methods=['POST'])
def find_car_by_reg_number():
   record = json.loads(request.data)
   car = record.get('car_reg')
   print(record)
   return find_car(car)


@app.route('/create_car', methods=['POST'])
def create_car_info():
    data = json.loads(request.data)
    make = data.get('make')
    model = data.get('model')
    car_reg = data.get('car_reg')
    status = data.get('status')
    new_car = create_car(make, model, car_reg, status)
    return new_car

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
    customer_id = data.get("customer_id")
    car_reg = data.get("car_reg")
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
@app.route('/return_car/', methods=['POST'])
def return_car_info():
    data = json.loads(request.data)
    customer_id = data.get('customer_id')
    car_reg = data.get('car_reg')
    status = data.get('status')
    if customer_id is None or car_reg is None or status is None:
        return "Please provide customer_id, car_reg, and car_status.", 400
    else:
        result = return_car(customer_id, car_reg, status)
        return result

#Implementing Customer database
@app.route('/create_customer', methods=['POST'])
def create_customer_info():
    data = json.loads(request.data)
    name = data.get('name')
    age = data.get('age')
    address = data.get('address')
    new_customer = create_customer(name, age, address)
    return new_customer

@app.route('/find_all_customers', methods=['GET'])
def query_customers():
    return find_all_employees()

@app.route('/find_customer', methods=['GET'])
def get_customer_by_id():
    data = json.loads(request.data)
    customer_id = data.get('customer_id')
    return find_customer(customer_id)
    

@app.route('/update_customer', methods=['POST'])
def update_customer_info():
    data = json.loads(request.data)
    customer_id = data.get('customer_id')
    name = data.get('name')
    age = data.get('age')
    address = data.get('address')
    updated_customer = update_customer(customer_id, name, age, address)
    return updated_customer

@app.route('/delete_customer', methods=['DELETE'])
def delete_customer_info():
    data = json.loads(request.data)
    customer_id = data.get('customer_id')
    customer = find_customer(customer_id)
    if customer:
        delete_customer(customer_id)
        return {'Customer has been deleted.'}
    else:
        return {'Error. Could not find customer in database.'}


#Implementing Employee

@app.route('/create_employee', methods=['POST'])
def create_employee_info():
    data = json.loads(request.data)
    name = data.get('name')
    address = data.get('address')
    branch = data.get('branch')
    employees = create_employee(name, address, branch)
    return employees

@app.route('/update_employee', methods=['PUT'])
def update_employee_info():
    data = json.loads(request.data)
    name = data.get('name')
    address = data.get('address')
    branch = data.get('branch')
    updated_employee = update_employee(name, address, branch)
    return updated_employee

@app.route('/delete_employee', methods=['DELETE'])
def delete_employee_info():
    data = json.loads(request.data)
    name = data.get('name')
    employee = find_employee(name)
    if employee:
        delete_employee(name)
    return f'Employee"{name} deleted.\n{data}'


@app.route('/find_all_employees', methods=['GET'])
def query_employees():
    return find_all_employees()

@app.route('/find_employee', methods=['GET'])
def find_employee_info():
    name = request.get_json('name')
    employees = find_employee(name)
    if employees:
        return employees
    else:
        return 'Employee not found'



