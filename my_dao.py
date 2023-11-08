from flask import Flask
from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver
from flask import render_template, request, redirect, url_for
import json

app = Flask(__name__)

#Kjri3Nql99OoG5YcsgOWxrsb8LYIpnasclZTaauvtc8
URI = "neo4j+s://17222aae.databases.neo4j.io"
AUTH = ("neo4j", "Kjri3Nql99OoG5YcsgOWxrsb8LYIpnasclZTaauvtc8")
def _get_connection() -> GraphDatabase:
   driver = GraphDatabase.driver(URI, auth=AUTH)
   driver.verify_connectivity()
   return driver
def node_to_json(node):
  node_properties = dict(node.items())
  return node_properties
def _get_connection() -> Driver:
   driver = GraphDatabase.driver(URI, auth=AUTH)
   driver.verify_connectivity()
   return driver

# CAR RELATED 
def create_car(make, model, reg, year):
    with _get_connection().session() as session:
        cars = session.run("CREATE (a:Car {make:$make, model:$model, reg:$reg, year:$year}) RETURN a;", make=make, model=model, reg=reg, year=year)
        nodes_json = [node_to_json(record["a"]) for record in cars]
        return nodes_json


def save_car(make, model, reg, year, status):
    with _get_connection().session() as session:
        cars = session.run("CREATE (a:Car {make:$make, model:$model, reg:$reg, year:$year, status:$status}) RETURN a;", make=make, model=model, reg=reg, year=year, status=status)
        nodes_json = [node_to_json(record["a"]) for record in cars]
        return nodes_json


def update_car(make, model, reg, year, status):
  with _get_connection().session() as session:
   cars = session.run("MATCH (a:Car{reg:$reg}) set a.make=$make, a.model=$model, a.year = $year, a.status = $status RETURN a;", reg=reg, make=make, model=model, year=year, status=status)
   nodes_json = [node_to_json(record["a"]) for record in cars]
   return nodes_json

def find_car(reg):
  with _get_connection().session() as session:
     cars = session.run("MATCH (a:Car) where a.reg=$reg RETURN a;", reg=reg)
     print(cars)
     nodes_json = [node_to_json(record["a"]) for record in cars]
     print(nodes_json)
     return nodes_json


def find_all_cars():
  with _get_connection().session() as session:
     cars = session.run("MATCH (a:Car) RETURN a;")
     nodes_json = [node_to_json(record["a"]) for record in cars]
     print(nodes_json)
     return nodes_json

def delete_car(reg):
  with _get_connection().session() as session:
    session.run("MATCH (a:Car {reg: $reg}) delete a;", reg=reg)
    return 

  





  








#Implementing Customers
def find_all_customers():
    with _get_connection().session() as session:
        customers = session.run("MATCH (c:Customer) RETURN c;")
        nodes_json = [node_to_json(record["c"]) for record in customers]
        return nodes_json

def find_customer(customer_id):
    with _get_connection().session() as session:
        customer = session.run("MATCH (c:Customer) WHERE ID(c) = $customer_id RETURN c;", customer_id=customer_id)
        return node_to_json(customer.single()["c"]) if customer.single() else None

def create_customer(name, age, address, customer_id):
    with _get_connection().session() as session:
        result = session.run("CREATE (c:Customer {name:$name, age:$age, address:$address, customer_id:$customer_id}) RETURN c;", name=name, age=age, address=address, customer_id=customer_id)
        return node_to_json(result.single()["c"])

def update_customer(customer_id, name, age, address):
    with _get_connection().session() as session:
        result = session.run("MATCH (c:Customer) WHERE ID(c) = $customer_id SET c.name = $name, c.age = $age, c.address = $address RETURN c;", customer_id=customer_id, name=name, age=age, address=address)
        return node_to_json(result.single()["c"])

def delete_customer(customer_id):
    with _get_connection().session() as session:
        session.run("MATCH (c:Customer) WHERE ID(c) = $customer_id DELETE c;", customer_id=customer_id)


#Implementing ordering of cars
def order_car(customer_id, car_reg):
    with _get_connection().session() as session:
        # Check if the customer has not booked other cars
        cars = session.run("MATCH (c:Customer {id: $customer_id})-[:BOOKED]->(car:Car {status: 'booked'}) RETURN car;",
                           customer_id=customer_id)
        if cars.single() is not None:
            # The customer has already booked a car, return an error message or handle it as needed
            return "Customer has already booked a car", 400

        # Change the status of the car with car_reg from 'available' to 'booked'
        result = session.run("MATCH (car:Car {reg: $car_reg, status: 'available'}) SET car.status = 'booked' RETURN car;",
                             car_reg=car_reg)
        car = result.single()
        if car:
            # Car successfully booked
            return "Car booked successfully"
        else:
            # Car with car_reg not found or not available, return an error message
            return "Car not found or not available", 404


def cancel_order_car(customer_id, car_reg):
    with _get_connection().session() as session:
        # Check if the customer has booked the car
        cars = session.run("MATCH (c:Customer {id: $customer_id})-[:BOOKED]->(car:Car {reg: $car_reg, status: 'booked'}) RETURN car;",
                           customer_id=customer_id, car_reg=car_reg)
        if cars.single() is not None:
            # The customer has booked the car, make the car available
            result = session.run("MATCH (car:Car {reg: $car_reg, status: 'booked'}) SET car.status = 'available' RETURN car;",
                                 car_reg=car_reg)
            car = result.single()
            if car:
                # Car successfully canceled
                return "Car booking canceled successfully"
        else:
            # Customer has not booked the car or the car is not currently booked
            return "Customer has not booked the car or car not booked currently", 404
        

#implementing renting cars
def rent_car(customer_id, car_reg):
    with _get_connection().session() as session:
        # Check if the customer has booked the car
        cars = session.run("MATCH (c:Customer {id: $customer_id})-[:BOOKED]->(car:Car {reg: $car_reg, status: 'booked'}) RETURN car;",
                           customer_id=customer_id, car_reg=car_reg)
        if cars.single() is not None:
            # The customer has booked the car, change the car status to 'rented'
            result = session.run("MATCH (car:Car {reg: $car_reg, status: 'booked'}) SET car.status = 'rented' RETURN car;",
                                 car_reg=car_reg)
            car = result.single()
            if car:
                # Car successfully rented
                return "Car rented successfully"
        else:
            # Customer has not booked the car or the car is not currently booked
            return "Customer has not booked the car or car not booked currently", 404
    
def return_car(customer_id, car_reg, car_status):
    with _get_connection().session() as session:
        # Check if the customer has rented the car
        cars = session.run("MATCH (c:Customer {id: $customer_id})-[:RENTED]->(car:Car {reg: $car_reg, status: 'rented'}) RETURN car;",
                           customer_id=customer_id, car_reg=car_reg)
        if cars.single() is not None:
            # The customer has rented the car, change the car status to 'available' or 'damaged' based on car_status
            if car_status == 'ok':
                result = session.run("MATCH (car:Car {reg: $car_reg, status: 'rented'}) SET car.status = 'available' RETURN car;",
                                     car_reg=car_reg)
            elif car_status == 'damaged':
                result = session.run("MATCH (car:Car {reg: $car_reg, status: 'rented'}) SET car.status = 'damaged' RETURN car;",
                                     car_reg=car_reg)
            car = result.single()
            if car:
                # Car successfully returned
                return f"Car returned successfully with status: {car_status}"
            else:
            # Customer has not rented the car or the car is not currently rented
              return "Customer has not rented the car or car not rented currently", 404
            



#Implementing Employee 

def find_employee(name):
    with _get_connection().session() as session:
        employee = session.run("MATCH (e:Employee) WHERE name(e) = $name RETURN e;", name=name)
        nodes_json = [node_to_json(record["e"]) for record in employee]
        return nodes_json

def find_all_employees():
    with _get_connection().session() as session:
        employees = session.run("MATCH (e:Employee) RETURN e;")
        nodes_json = [node_to_json(record["e"]) for record in employees]
        return nodes_json

def create_employee(name, address, branch):
    with _get_connection().session() as session:
        employees = session.run("CREATE (e:Employee {name: $name, address: $address, branch: $branch}) RETURN e;", name=name, address=address, branch=branch)
        nodes_json = [node_to_json(record["e"]) for record in employees]
        return nodes_json

def update_employee(name, address, branch):
    with _get_connection().session() as session:
        employees = session.run("MATCH (e:Employee) WHERE name(e) = $name SET e.name = $name, e.address = $address, e.branch = $branch RETURN e;", name=name, address=address, branch=branch)
        nodes_json = [node_to_json(record["e"]) for record in employees]
        return nodes_json

def delete_employee(name):
    with _get_connection().session() as session:
        session.run("MATCH (e:Employee) WHERE name(e) = $name DELETE e;", name=name)


