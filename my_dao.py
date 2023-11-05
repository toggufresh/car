from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver

# Kjri3Nql99OoG5YcsgOWxrsb8LYIpnasclZTaauvtc8
URI = "17222aae.databases.neo4j.io"
AUTH = ("neo4j", "Kjri3Nql99OoG5YcsgOWxrsb8LYIpnasclZTaauvtc8")
def _get_connection() -> GraphDatabase:
   driver = GraphDatabase.driver(URI, auth=AUTH)
   driver.verify_connectivity()
   return driver

# Use the execute_query function to execute custom queries in the Neo4j database.
# This allows for flexibility in performing actions such as creating, updating, or deleting records
# with dynamic queries that may not be covered by specific functions.

    
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

def update_car(make, model, reg, year, capacity):
  with _get_connection().session() as session:
   cars = session.run("MATCH (a:Car{reg:$reg}) set a.make=$make, a.model=$model, a.year = $year, a.capacity = $capacity RETURN a;", reg=reg, make=make, model=model, year=year, capacity=capacity)
   nodes_json = [node_to_json(record["a"]) for record in cars]

   updated_car = save_car(nodes_json)
   return updated_car
  


def save_car(make, model, reg, year, capacity):
    with _get_connection().session() as session:
        cars = session.run("CREATE (a:Car {make:$make, model:$model, reg:$reg, year:$year, capacity:$capacity}) RETURN a;", make=make, model=model, reg=reg, year=year, capacity=capacity)
        nodes_json = [node_to_json(record["a"]) for record in cars]
        return nodes_json

def delete_car(reg):
  with _get_connection().session() as session:
    session.run("MATCH (a:Car {reg: $reg}) delete a;", reg=reg)
    return 

def create_car(make, model, reg, year, capacity):
    with _get_connection().session() as session:
        cars = session.run("CREATE (a:Car {make:$make, model:$model, reg:$reg, year:$year, capacity:$capacity}) RETURN a;", make=make, model=model, reg=reg, year=year, capacity=capacity)
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


#Implementing cancellation of cars

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
        


#implementing returning cars
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


