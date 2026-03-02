from abc import ABC, abstractmethod
class StarShip(ABC):
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
        # If value is below 0, just set it to 0
        if value < 0:
            self.__health = 0
            print(f"ALERT: {self.name} has been destroyed!")
        # If value is above 100, just set it to 100
        elif value > 100:
            self.__health = 100
            print(f"{self.name} is fully repaired.")
        # Otherwise, set it normally
        else:
            self.__health = value
            
    def take_damage(self,amount):
        self.health= self.__health - amount
    def repair(self,amount):
        self.health = self.__health + amount
        
    @abstractmethod
    def perform_maintenance(self):
        pass

# INHERITANCE - FighterShip inherits from StarShip
class FighterShip(StarShip):
    """Fighter ships have weapons and can attack"""
    def __init__(self, name, fuel, health, crew_count, weapon_power):
        # Call the parent class __init__ to set up common attributes
        super().__init__(name, fuel, health, crew_count)
        # Add fighter-specific attribute
        self.weapon_power = weapon_power
    
    # Fighter-specific method
    def fire_weapons(self, target):
        print(f"{self.name} fires weapons at {target.name}!")
        print(f"Weapon power: {self.weapon_power}")
        target.take_damage(self.weapon_power)
    def perform_maintenance(self):
        print(f"{self.name} can Calibrate weapons")
        

class CargoHauler(StarShip):
    def __init__(self,name,fuel,health,crew_count,cargo_capacity,current_cargo):
        super().__init__(name,fuel,health,crew_count)
        self.cargo_capacity=cargo_capacity
        self.current_cargo=current_cargo
    def load_cargo(self,amount):
        capacity=self.current_cargo+amount
        if amount<0:
            print("capacity cannot be negative")
        if capacity>self.cargo_capacity:
            print(f"Cargo has exceeded the capacity,left with {100-self.current_cargo} but {amount-self.current_cargo} tons could be loaded ")
            self.current_cargo=0
        else:
            self.current_cargo=capacity
    def status_report(self):
        base_status = super().status_report()  # Get parent's report
        return f"{base_status} | Cargo: {self.current_cargo}/{self.cargo_capacity} tons"

    def unload_cargo(self,amount):
        capacity=self.current_cargo-amount
        if amount<0:
            print("capacity cannot be negative")
        if capacity<0:
            print(f"The cargo cannot be unloaded because only this left {self.current_cargo} but {amount-self.current_cargo} tons remains unloaded")
            self.current_cargo=0
        else:
            self.current_cargo=capacity
    def perform_maintenance(self):
        print(f"{self.name} can Inspect cargo holds")

class ScienceVessel(StarShip):
    def __init__(self,name,fuel,health,crew_count,lab_level):
        super().__init__(name,fuel,health,crew_count)
        self.lab_level=lab_level
    def scan_planet(self,planet_name):
        print(f"The StarShip Lab {self.name} has lab level : {self.lab_level} and has printed {planet_name}")
        
    def perform_maintenance(self):
        print(f"{self.name} can Calibrate lab instruments")
        
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

# Create ships
print("=== Creating Ships ===")
generic_ship = StarShip("USS Generic", fuel=80, health=100, crew_count=50)
viper = FighterShip("Viper", fuel=100, health=90, crew_count=2, weapon_power=25)

print(generic_ship.status_report())
print(viper.status_report())

print("\n=== Fighter Attacking Generic Ship ===")
viper.fire_weapons(generic_ship)
print(generic_ship.status_report())

print("\n=== Can a generic ship fire weapons? ===")
try:
    generic_ship.fire_weapons(viper)
except AttributeError as e:
    print(f"Error: {e}")
    print("Generic StarShip doesn't have fire_weapons() method!")

#Testing all three ship types
print("=== Creating Fleet ===")
fighter = FighterShip("Viper", fuel=100, health=90, crew_count=2, weapon_power=25)
cargo = CargoHauler("Atlas", fuel=80, health=100, crew_count=20, cargo_capacity=100, current_cargo=0)
science = ScienceVessel("Discovery", fuel=90, health=95, crew_count=50, lab_level=4)

print(fighter.status_report())
print(cargo.status_report())
print(science.status_report())
print(f"Total fleet: {StarShip.fleet_size} ships")

print("\n=== Fighter Attack ===")
fighter.fire_weapons(cargo)
print(cargo.status_report())

print("\n=== Cargo Operations ===")
print(f"Starting cargo: {cargo.current_cargo}/{cargo.cargo_capacity}")
cargo.load_cargo(50)
print(f"After loading 50: {cargo.current_cargo}/{cargo.cargo_capacity}")
# cargo.load_cargo(60)  # Should exceed
# print(f"After trying to load 60: {cargo.current_cargo}/{cargo.cargo_capacity}")
cargo.unload_cargo(30)
print(f"After trying to unload 30: {cargo.current_cargo}/{cargo.cargo_capacity}")
cargo.unload_cargo(50)
print(f"After trying to unload 50: {cargo.current_cargo}/{cargo.cargo_capacity}")

print("\n=== Science Mission ===")
science.scan_planet("Mars")
science.scan_planet("Jupiter")
