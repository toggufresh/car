from flask import Flask
from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver
from flask import render_template, request, redirect, url_for
from project import app
import json

app = Flask(__name__)

URI = "URI WITH HTTPS"
AUTH = ("USERNAME", "PASSWORD")
def _get_connection() -> GraphDatabase:
   driver = GraphDatabase.driver(URI, auth=AUTH)
   driver.verify_connectivity()
   return driver

def node_to_json(node):
  node_properties = dict(node.items())
  return node_properties

def findAllCars():
  with _get_connection().session() as session:
     cars = session.run("MATCH (a:Car) RETURN a;")
     nodes_json = [node_to_json(record["a"]) for record in cars]
     print(nodes_json)
     return nodes_json
  
def findCarByReg(reg):
  with _get_connection().session() as session:
     cars = session.run("MATCH (a:Car) where a.reg=$reg RETURN a;", reg=reg)
     print(cars)
     nodes_json = [node_to_json(record["a"]) for record in cars]
     print(nodes_json)
     return nodes_json
  
def _get_connection() -> Driver:
   driver = GraphDatabase.driver(URI, auth=AUTH)
   driver.verify_connectivity()
   return driver


def node_to_json(node):
  node_properties = dict(node.items())
  return node_properties

def update_car(make, model, reg, year, status):
    with _get_connection().session() as session:
        cars = session.run(
            "MATCH (a:Car {reg: $reg}) SET a.make = $make, a.model = $model, a.year = $year, a.status = $status RETURN a;",
            reg=reg, make=make, model=model, year=year, status=status
        )
        nodes_json = [node_to_json(record["a"]) for record in cars]
        return nodes_json

  


def save_car(make, model, reg, year, status):
    with _get_connection().session() as session:
        cars = session.run("CREATE (a:Car {make:$make, model:$model, reg:$reg, year:$year, status:$status}) RETURN a;", make=make, model=model, reg=reg, year=year, status=status)
        nodes_json = [node_to_json(record["a"]) for record in cars]
        return nodes_json

def delete_car(reg):
  with _get_connection().session() as session:
    session.run("MATCH (a:Car {reg: $reg}) delete a;", reg=reg)
    return 

def create_car(make, model, reg, year, status):
    with _get_connection().session() as session:
        cars = session.run("CREATE (a:Car {make:$make, model:$model, reg:$reg, year:$year, status:$status}) RETURN a;", make=make, model=model, reg=reg, year=year, status=status)
        nodes_json = [node_to_json(record["a"]) for record in cars]
        return nodes_json


#Implementing Customers
def findAllCustomers():
    with _get_connection().session() as session:
        customers = session.run("MATCH (c:Customer) RETURN c;")
        nodes_json = [node_to_json(record["c"]) for record in customers]
        return nodes_json

def findCustomerById(customer_id):
    with _get_connection().session() as session:
        customer = session.run("MATCH (c:Customer) WHERE ID(c) = $customer_id RETURN c;", customer_id=customer_id)
        return node_to_json(customer.single()["c"]) if customer.single() else None

def createCustomer(name, age, address):
    with _get_connection().session() as session:
        result = session.run("CREATE (c:Customer {name:$name, age:$age, address:$address}) RETURN c;", name=name, age=age, address=address)
        return node_to_json(result.single()["c"])

def updateCustomer(customer_id, name, age, address):
    with _get_connection().session() as session:
        result = session.run("MATCH (c:Customer) WHERE ID(c) = $customer_id SET c.name = $name, c.age = $age, c.address = $address RETURN c;", customer_id=customer_id, name=name, age=age, address=address)
        return node_to_json(result.single()["c"])

def deleteCustomer(customer_id):
    with _get_connection().session() as session:
        session.run("MATCH (c:Customer) WHERE ID(c) = $customer_id DELETE c;", customer_id=customer_id)


#Implementing Employee 

def findEmployeeById(employee_id):
    with _get_connection().session() as session:
        employee = session.run("MATCH (e:Employee) WHERE ID(e) = $employee_id RETURN e;", employee_id=employee_id)
        nodes_json = [node_to_json(record["e"]) for record in employee]
        return nodes_json

def findAllEmployees():
    with _get_connection().session() as session:
        employees = session.run("MATCH (e:Employee) RETURN e;")
        nodes_json = [node_to_json(record["e"]) for record in employees]
        return nodes_json

def createEmployee(name, address, branch):
    with _get_connection().session() as session:
        employees = session.run("CREATE (e:Employee {name: $name, address: $address, branch: $branch}) RETURN e;", name=name, address=address, branch=branch)
        nodes_json = [node_to_json(record["e"]) for record in employees]
        return nodes_json

def updateEmployee(employee_id, name, address, branch):
    with _get_connection().session() as session:
        employees = session.run("MATCH (e:Employee) WHERE ID(e) = $employee_id SET e.name = $name, e.address = $address, e.branch = $branch RETURN e;", employee_id=employee_id, name=name, address=address, branch=branch)
        nodes_json = [node_to_json(record["e"]) for record in employees]
        return nodes_json

def deleteEmployee(employee_id):
    with _get_connection().session() as session:
        session.run("MATCH (e:Employee) WHERE ID(e) = $employee_id DELETE e;", employee_id=employee_id)


#Implementing ordering of cars
def order_car(customer_id, car_reg):
    with _get_connection().session() as session:
        cars = session.run("MATCH (c:Customer {id: $customer_id})-[:BOOKED]->(car:Car {status: 'booked'}) RETURN car;",
                           customer_id=customer_id)
        if cars.single() is not None:
            return "Customer has already booked a car", 400

        result = session.run("MATCH (car:Car {reg: $car_reg, status: 'available'}) SET car.status = 'booked' RETURN car;",
                             car_reg=car_reg)
        car = result.single()
        if car:
            return "Car booked successfully"
        else:
            return "Car not found or not available", 404


#Implementing cancellation of cars

def cancel_order_car(customer_id, car_reg):
    with _get_connection().session() as session:
        cars = session.run("MATCH (c:Customer {id: $customer_id})-[:BOOKED]->(car:Car {reg: $car_reg, status: 'booked'}) RETURN car;",
                           customer_id=customer_id, car_reg=car_reg)
        if cars.single() is not None:
            result = session.run("MATCH (car:Car {reg: $car_reg, status: 'booked'}) SET car.status = 'available' RETURN car;",
                                 car_reg=car_reg)
            car = result.single()
            if car:
                return "Car booking canceled successfully"
        else:
            return "Customer has not booked the car or car not booked currently", 404

#Implementing renting cars
def rent_car(customer_id, car_reg):
    with _get_connection().session() as session:
        cars = session.run("MATCH (c:Customer {id: $customer_id})-[:BOOKED]->(car:Car {reg: $car_reg, status: 'booked'}) RETURN car;",
                           customer_id=customer_id, car_reg=car_reg)
        if cars.single() is not None:
            result = session.run("MATCH (car:Car {reg: $car_reg, status: 'booked'}) SET car.status = 'rented' RETURN car;",
                                 car_reg=car_reg)
            car = result.single()
            if car:
                return "Car rented successfully"
        else:
            return "Customer has not booked the car or car not booked currently", 404

#Implementing returning cars
def return_car(customer_id, car_reg, car_status):
    with _get_connection().session() as session:
        cars = session.run(
            "MATCH (c:Customer {id: $customer_id})-[:RENTED]->(car:Car {reg: $car_reg, status: 'rented'}) RETURN car;",
                            customer_id=customer_id, car_reg=car_reg)
        result = session.run("MATCH (car:Car {reg: $car_reg, status: 'rented'}) SET car.status = 'damaged' RETURN car;",
                             car_reg=car_reg)
        car = result.single()
        if car:
            return f"Car returned successfully with status: {car_status}"
        else:
            return "Customer has not rented the car or car not rented currently", 404


