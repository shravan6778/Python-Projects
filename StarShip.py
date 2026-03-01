class StarShip:
    fleet_size = 0
    
    def __init__(self, name, fuel, health, crew_count):
        self.name = name
        self.__fuel = fuel  # Private variable
        self.__health = health
        self.crew_count = crew_count
        StarShip.fleet_size += 1
    
    # GETTER - allows reading with apollo.fuel
    @property
    def fuel(self):
        return self.__fuel
    
    # SETTER - allows controlled writing with apollo.fuel = value
    @fuel.setter
    def fuel(self, value):
        if value < 0:
            print("Error: Fuel cannot be negative!")
        elif value > 100:
            print("Error: Fuel cannot exceed 100!")
        else:
            self.__fuel = value
            print(f"Fuel set to {self.__fuel}")
    def add_crew(self,amount):
        self.crew_count+=amount
        
    def status_report(self):
        return f"{self.name}: Fuel:{self.__fuel} Health:{self.__health} Crew:{self.crew_count}"
    
    def refuel(self, amount):
        if amount < 0:
            print("Cannot refuel with negative amount!")
            return
        new_fuel = self.__fuel + amount
        if new_fuel > 100:
            print(f"Can only add {100 - self.__fuel} more fuel")
        else:
            self.__fuel = new_fuel
            print(f"Refueled! Current fuel: {self.__fuel}")
            
    @property
    def health(self):
        return self.__health
    
    @health.setter
    def health(self, value):
        if value < 0:
            print("Error: Health cannot be negative!")
        elif value > 100:
            print("Error: Health cannot exceed 100!")
        else:
            self.__health = value
            print(f"Health set to {self.__health}")
    def take_damage(self,amount):
        self.health= self.__health - amount
    def repair(self,amount):
        self.health = self.__health + amount
    
    
apollo = StarShip("Apollo", fuel=50, health=100,crew_count=10)
enterprise = StarShip("Enterprise", fuel=80, health=95,crew_count=8)
print(apollo.status_report())
print(enterprise.status_report())
print(f"Total fleet size: {StarShip.fleet_size}")
# Both ships can access the SAME fleet_size
print(apollo.fleet_size)      
print(enterprise.fleet_size)  
print(StarShip.fleet_size)    
apollo.add_crew(2)
apollo.refuel(50)
print(apollo.status_report())
# How do we check fuel without calling status_report()?
print(f"Apollo's fuel: {apollo.fuel}")  # What do we write here?

print("\n=== Testing damage and repair ===")
apollo.take_damage(20)
print(apollo.status_report())
apollo.repair(10)
print(apollo.status_report())

print("\n=== THE BUG - Watch this! ===")
apollo.take_damage(200)  # Taking 200 damage!
print(apollo.status_report())  # Health is now NEGATIVE!

print("\n=== Another problem ===")
apollo.repair(500)  # Repairing 500 health!
print(apollo.status_report())  # Health is now WAY over 100!