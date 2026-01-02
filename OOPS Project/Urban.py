from abc import ABC,abstractmethod
import csv 
import json

class Vehicle(ABC):
    def __init__(self,vehicle_id,model,battery_percentage,maintenance_status,rental_price):
        self.vehicle_id=vehicle_id
        self.model=model
        self.set_battery_percentage(battery_percentage) 
        self.__maintenance_status=maintenance_status
        self.set_rental_price(rental_price)
    def __eq__(self, other):
        if isinstance(other,Vehicle):
             return self.vehicle_id == other.vehicle_id
        return False

            
    @abstractmethod
    def calculate_trip_cost(self,distance):
        pass
    def get_maintenance_status(self) :
        return self.__maintenance_status
    
    def set_maintenance_status(self,maintenance_status):
        self.__maintenance_status =maintenance_status

    def get_battery_percentage(self) :
        return self.__battery_percentage
    
    def set_battery_percentage(self,battery_percentage) :
        if 0<=battery_percentage<=100:
           self.__battery_percentage=battery_percentage
        else:   
            raise ValueError("value is invaild")
        
    def get_rental_price(self) :
        return self.__rental_price
    
    def set_rental_price(self,rental_price) :
        if  rental_price>0:
           self.__rental_price=rental_price
        else:   
            raise ValueError("value is invaild")
    
    def get_type(self):
        return self.__class__.__name__
    def __str__(self):
        return f"ID: {self.vehicle_id}, Model: {self.model}, Battery: {self.get_battery_percentage()}%"

class ElectricCar(Vehicle):
    def __init__(self,vehicle_id,model,battery_percentage,maintenance_status,rental_price,seating_capacity):
        super().__init__(vehicle_id,model,battery_percentage,maintenance_status,rental_price)
        self.seating_capacity=seating_capacity
    def calculate_trip_cost(self,distance):
        return (5+(distance*0.50))

            

class ElectricScotter(Vehicle):
    def __init__(self,vehicle_id,model,battery_percentage,maintenance_status,rental_price,max_speed_limit):
        super().__init__(vehicle_id,model,battery_percentage,maintenance_status,rental_price)
        self.max_speed_limit = max_speed_limit
    def calculate_trip_cost(self,distance):
            return (1 +(0.15*distance))
    
class fleethub:
    def __init__(self):
      self.dic_hub = {}
    def add_hub(self):
         hub_name =input("Enter the hub name: ")
         if hub_name in self.dic_hub:
             print("hub name already exit")
         else:
             self.dic_hub[hub_name]=[]
    def  add_vehicle(self,hub_name):
        if hub_name not in self.dic_hub:
            print("hub not exit")
            return
        

        Vehicle_name = input("Enter the name of vehicle car/scotter: ")
        Vehicle_id = input("enter the  Vehicle_id: ")
        existing_id = [v for v in self.dic_hub[hub_name] if v.vehicle_id == Vehicle_id]
        if existing_id:
            print("already exit")
            return

        model =input("enter the  model: ")
        
        maintenance_status =input("enter the  maintenance_status: ")
        try:
            battery_percentage = int(input("enter battery percentage: "))
            rental_price = int(input("enter rental price: "))
        except ValueError:
           print("Please enter numbers only")
           return


        if Vehicle_name == "car":
            seating_capcity = input("enter the seating capcity")
            Vehicl=ElectricCar(Vehicle_id,model,battery_percentage,maintenance_status,rental_price,seating_capcity)
        elif Vehicle_name=="scotter":
            max_speed = int(input("enter the max_speed"))
            Vehicl=ElectricScotter(Vehicle_id,model,battery_percentage,maintenance_status,rental_price,max_speed)
        else:
           print("Invaild value")
           return
        

        self.dic_hub[hub_name].append(Vehicl)

    def  display_hub(self):
        for hub_name, vehicles in self.dic_hub.items():
            print(f"Hub: {hub_name}")
            for v in vehicles:
              print(v.vehicle_id, v.model)

    def  search_hub_name(self, hub_name):
        if hub_name in self.dic_hub:
           print(f"vehicles in hub{hub_name}")
           for v in self.dic_hub[hub_name]:
               print(v.vehicle_id, v.model)  
        else:
            print("Invaild hub name")
    def search_battery_percentage(self) :  
         all_battery_percentage=[v.get_battery_percentage() for hub in self.dic_hub.values() for v in hub]
         all_battery_list=list(filter(lambda x:  x>80,all_battery_percentage))
         print(all_battery_list)

    def search_vehicle_type(self):
        category={}
        for hub in self.dic_hub.values():
            for v in hub:
                vehicle_type =v.get_type()
                if vehicle_type not in category:
                    category[vehicle_type] =[]
                category[vehicle_type].append(v)
    
        for vehicle_type, vehicles in category.items(): 
            print(f"\n{vehicle_type}s:")
            for v in vehicles:
              print(v.vehicle_id, v.model)
    def fleetcount(self):
        status_count={
           "Available" : 0,
           "On Trip" :0,
           "Under Maintenance" :0
        }
        for vehicle in self.dic_hub.values():
            for v in vehicle:
                status= v.get_maintenance_status()
                if status in status_count:
                    status_count[status] +=1
        
        print("\n--- Fleet Analytics Summary ---")
        print(f"Available Vehicles        : {status_count['Available']}")
        print(f"On Trip Vehicles          : {status_count['On Trip']}")
        print(f"Under Maintenance Vehicles: {status_count['Under Maintenance']}")

    def sort_by_model(self):
        for vehicle in self.dic_hub.values():
            vehicle.sort(key= lambda v: v.model.lower())
        for hub, vehicles in self.dic_hub.items():
            print(f"{hub}")
            for v in vehicles:
                print(f"{v}")   
    def sort_by_battery_level(self):
        for vehicles in self.dic_hub.values():
           vehicles.sort(key=lambda v: v.get_battery_percentage(), reverse=True)

        print("\n--- Vehicles Sorted by Battery Level (High → Low) ---")
        for hub, vehicles in self.dic_hub.items():
            print(f"\nHub: {hub}")
            for v in vehicles:
                 print(v)
    def sort_by_fare_price(self):
        for vehicles in self.dic_hub.values():
          vehicles.sort(key=lambda v: v.get_rental_price(), reverse=True)
        print("\n--- Vehicles Sorted by Fare Price (High → Low) ---")
        for hub, vehicles in self.dic_hub.items():
          print(f"\nHub: {hub}")
          for v in vehicles:
             print(v)
        

    def load_from_csv(self, filename="fleet_data.csv"):
        try:
           self.dic_hub.clear()
           with open(filename, mode="r", newline="") as file:
             reader = csv.DictReader(file)

             for row in reader:
                hub_name = row["hub_name"]

                if hub_name not in self.dic_hub:
                    self.dic_hub[hub_name] = []

                vehicle_type = row["vehicle_type"]

                if vehicle_type == "ElectricCar":
                    vehicle = ElectricCar(
                        row["vehicle_id"],
                        row["model"],
                        int(row["battery_percentage"]),
                        row["maintenance_status"],
                        int(row["rental_price"]),
                        int(row["seating_capacity"])
                    )

                elif vehicle_type == "ElectricScotter":
                    vehicle = ElectricScotter(
                        row["vehicle_id"],
                        row["model"],
                        int(row["battery_percentage"]),
                        row["maintenance_status"],
                        int(row["rental_price"]),
                        int(row["max_speed_limit"])
                    )
                else:
                    continue

                self.dic_hub[hub_name].append(vehicle)

           print("Fleet data loaded successfully from CSV")

        except FileNotFoundError:
           print("CSV file not found. No data loaded.")

    def save_to_csv(self, filename="fleet_data.csv"):
        with open(filename, mode="w", newline="") as file:
          fieldnames = [
            "hub_name",
            "vehicle_type",
            "vehicle_id",
            "model",
            "battery_percentage",
            "maintenance_status",
            "rental_price",
            "seating_capacity",
            "max_speed_limit"
         ]
        
          writer = csv.DictWriter(file, fieldnames=fieldnames)
          writer.writeheader()

          for hub_name, vehicles in self.dic_hub.items():
            for v in vehicles:
                row = {
                    "hub_name": hub_name,
                    "vehicle_type": v.get_type(),
                    "vehicle_id": v.vehicle_id,
                    "model": v.model,
                    "battery_percentage": v.get_battery_percentage(),
                    "maintenance_status": v.get_maintenance_status(),
                    "rental_price": v.get_rental_price(),
                    "seating_capacity": "",
                    "max_speed_limit": ""
                }

                if v.get_type() == "ElectricCar":
                    row["seating_capacity"] = v.seating_capacity

                elif v.get_type() == "ElectricScotter":
                    row["max_speed_limit"] = v.max_speed_limit

                writer.writerow(row)

        print("Fleet data saved successfully to CSV")
    def save_to_json(self, filename="fleet_data.json"):
      data = {}

      for hub_name, vehicles in self.dic_hub.items():
        data[hub_name] = []

        for v in vehicles:
            vehicle_data = {
                "vehicle_type": v.get_type(),
                "vehicle_id": v.vehicle_id,
                "model": v.model,
                "battery_percentage": v.get_battery_percentage(),
                "maintenance_status": v.get_maintenance_status(),
                "rental_price": v.get_rental_price()
            }

            if v.get_type() == "ElectricCar":
                vehicle_data["seating_capacity"] = v.seating_capacity

            elif v.get_type() == "ElectricScotter":
                vehicle_data["max_speed_limit"] = v.max_speed_limit

            data[hub_name].append(vehicle_data)

      with open(filename, "w") as file:
         json.dump(data, file, indent=4)

      print("Fleet data saved successfully to JSON")

    def load_from_json(self, filename="fleet_data.json"):
       try:
          with open(filename, "r") as file:
            data = json.load(file)

          self.dic_hub.clear()

          for hub_name, vehicles in data.items():
            self.dic_hub[hub_name] = []

            for v in vehicles:
                if v["vehicle_type"] == "ElectricCar":
                    vehicle = ElectricCar(
                        v["vehicle_id"],
                        v["model"],
                        v["battery_percentage"],
                        v["maintenance_status"],
                        v["rental_price"],
                        v["seating_capacity"]
                    )

                elif v["vehicle_type"] == "ElectricScotter":
                    vehicle = ElectricScotter(
                        v["vehicle_id"],
                        v["model"],
                        v["battery_percentage"],
                        v["maintenance_status"],
                        v["rental_price"],
                        v["max_speed_limit"]
                    )
                else:
                   continue

                self.dic_hub[hub_name].append(vehicle)

          print("Fleet data loaded successfully from JSON")

       except FileNotFoundError:
          print("JSON file not found. No data loaded.")
           
        

vehicles = [
    ElectricCar("C1", "Tesla", 80, "OK", 500, 5),
    ElectricScotter("S1", "Ola", 70, "OK", 200, 40)
]

for v in vehicles:
    print(v.calculate_trip_cost(10))
fleet= fleethub()
while True:
    print("Select any one option:")
    print("1.add a hub")
    print("2.add a Vehicle")
    print("3.display hub")
    print("4.search vehicle by hub name")
    print("5.search by vehicle bettery")
    print("6.fleet count")
    print("7.sort_by_model")
    print("8.sort_by_battery_level")
    print("9.sort_by_fare_price")
    print("10.load_from_csv")
    print("11.save_to_csv")
    print("12.load_from_json")
    print("13.save_to_json")
    print("exit")

    a=input("enter the choice ")
    if a=="1":
        fleet.add_hub()
    elif a=="2":
        hub_name = input("enter the hub_name")
        fleet.add_vehicle(hub_name)
    elif a=="3":
        fleet.display_hub()
    elif a=="4":
        hub_name = input("enter the hub_name")
        fleet.search_hub_name(hub_name)
    elif a=="5":
        fleet.search_battery_percentage()
    elif a=="6":
        fleet.fleetcount()    
    elif a=="7":
        fleet.sort_by_model()   
    elif a=="8":
        fleet.sort_by_battery_level()   
    elif a=="9":
        fleet.sort_by_fare_price()
    elif a=="10":
        fleet.load_from_csv()  
    elif a=="11":
        fleet.save_to_csv() 
    elif a=="12":
        fleet.load_from_json()  
    elif a=="13":
        fleet.save_to_json()                        
    else:
        print("Invalid choice")
        break
