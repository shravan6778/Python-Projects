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
    #POLYMORPHIC METHOD - Every ship moves, but HOW they move is different
    @abstractmethod
    def move(self,distance):
        pass
    
    @abstractmethod
    def emergency_protocol(self):
        pass

# INHERITANCE - FighterShip inherits from StarShip
class FighterShip(StarShip):
    """Fighter ships have weapons and can attack"""
    def __init__(self, name, fuel, health, crew_count, weapon_power):
        # Call the parent class __init__ to set up common attributes
        super().__init__(name, fuel, health, crew_count)
        # Add fighter-specific attribute
        self.weapon_power = weapon_power
        self.speed = 100  # Fast!
    
    # Fighter-specific method
    def fire_weapons(self, target):
        print(f"{self.name} fires weapons at {target.name}!")
        print(f"Weapon power: {self.weapon_power}")
        target.take_damage(self.weapon_power)
    def perform_maintenance(self):
        print(f"{self.name} can Calibrate weapons")
        
    # Fighter's version of move - FAST and AGILE
    def move(self, distance):
        fuel_used = distance * 0.5  # Fighters are fuel-efficient
        self.fuel = self.fuel - fuel_used
        print(f"{self.name} zips {distance} km at {self.speed} km/h (fuel:-{fuel_used})")
        
    def emergency_protocol(self):
        print("Activating combat shields and evasive maneuvers!")

class CargoHauler(StarShip):
    def __init__(self,name,fuel,health,crew_count,cargo_capacity,current_cargo):
        super().__init__(name,fuel,health,crew_count)
        self.cargo_capacity=cargo_capacity
        self.current_cargo=current_cargo
        self.speed = 30  # Slow!
        
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
    # Cargo's version of move - SLOW and HEAVY
    def move(self, distance):
        fuel_used = distance * 2.0  # Cargo ships guzzle fuel
        self.fuel = self.fuel - fuel_used
        print(f"🐢 {self.name} lumbers {distance} km at {self.speed} km/h (fuel: -{fuel_used})")

    def emergency_protocol(self):
        print("Jettisoning cargo and sealing hull breaches!")

class ScienceVessel(StarShip):
    def __init__(self,name,fuel,health,crew_count,lab_level):
        super().__init__(name,fuel,health,crew_count)
        self.lab_level=lab_level
        self.speed = 60  # Medium
        
    def scan_planet(self,planet_name):
        print(f"The StarShip Lab {self.name} has lab level : {self.lab_level} and has printed {planet_name}")
        
    def perform_maintenance(self):
        print(f"{self.name} can Calibrate lab instruments")
        
    # Science's version of move - STEADY
    def move(self, distance):
        fuel_used = distance * 1.0
        self.fuel = self.fuel - fuel_used
        print(f"🔬 {self.name} cruises {distance} km at {self.speed} km/h (fuel: -{fuel_used})")
        
    def emergency_protocol(self):
        print("Evacuating labs and securing research data!")
        
# MIXIN CLASS - adds cloaking ability
class CloakingDevice:
    """A mixin that adds stealth capabilities to any ship"""
    
    def __init__(self, *args, **kwargs):
        # CRITICAL: Must call super() to continue the chain!
        super().__init__(*args, **kwargs)
        self.cloaked = False
        print(f"CloakingDevice.__init__ called")
    
    def engage_cloak(self):
        self.cloaked = True
        print(f"🌫️ {self.name} vanishes into the void... [CLOAKED]")
    
    def disengage_cloak(self):
        self.cloaked = False
        print(f"✨ {self.name} decloaks and becomes visible!")
    
    def status(self):
        return "CLOAKED" if self.cloaked else "VISIBLE"


# MULTIPLE INHERITANCE - inherits from BOTH FighterShip AND CloakingDevice
class StealthBomber(FighterShip, CloakingDevice):
    """A fighter with cloaking technology - inherits from TWO classes!"""
    
    def __init__(self, name, fuel, health, crew_count, weapon_power):
        print(f"\nCreating StealthBomber '{name}':")
        # super() will call BOTH parent __init__ methods in the right order!
        super().__init__(name, fuel, health, crew_count, weapon_power)
        print(f"   StealthBomber.__init__ completed\n")
    
    def perform_maintenance(self):
        print(f"🔧 {self.name}: Calibrating weapons AND cloaking device")
    
    def stealth_attack(self, target):
        """Special ability - only StealthBomber has this!"""
        if self.cloaked:
            print(f"🥷 {self.name} strikes from the shadows!")
            self.fire_weapons(target)
            self.disengage_cloak()
        else:
            print(f"⚠️  Cannot stealth attack - not cloaked!")

# MIXIN CLASS - adds shield protection
class ShieldGenerator:
    """A mixin that adds energy shields to any ship"""
    
    def __init__(self, *args, **kwargs):
        # CRITICAL: Must call super() to continue the chain!
        super().__init__(*args, **kwargs)
        self.shield_strength = 0
        print(f"ShieldGenerator.__init__ called")
    
    def activate_shields(self):
        self.shield_strength = 100
        print(f"🛡️ {self.name} shields activated! [SHIELDS: 100]")
    
    def take_hit(self, damage):
        """Shields absorb damage before health is affected"""
        if self.shield_strength > 0:
            if damage <= self.shield_strength:
                # Shields absorb all damage
                self.shield_strength -= damage
                print(f"🛡️ Shields absorbed {damage} damage! [SHIELDS: {self.shield_strength}]")
            else:
                # Shields absorb partial damage, rest goes to health
                remaining_damage = damage - self.shield_strength
                print(f"🛡️ Shields absorbed {self.shield_strength} damage and collapsed!")
                self.shield_strength = 0
                self.take_damage(remaining_damage)
                print(f"💥 {remaining_damage} damage penetrated to hull!")
        else:
            # No shields, all damage to health
            print(f"⚠️ No shields active! Taking full damage...")
            self.take_damage(damage)

# MULTIPLE INHERITANCE - inherits from BOTH CargoHauler AND ShieldGenerator
class ShieldedCargoHauler(CargoHauler, ShieldGenerator):
    """A cargo hauler with shield technology - inherits from TWO classes!"""
    
    def __init__(self, name, fuel, health, crew_count, cargo_capacity, current_cargo):
        print(f"\nCreating ShieldedCargoHauler '{name}':")
        # super() will call BOTH parent __init__ methods in the right order!
        super().__init__(name, fuel, health, crew_count, cargo_capacity, current_cargo)
        print(f"   ShieldedCargoHauler.__init__ completed\n")
    
    def status_report(self):
        """Override to include shield status"""
        base_status = super().status_report()
        return f"{base_status} | Shields: {self.shield_strength}"
    
    def perform_maintenance(self):
        print(f"🔧 {self.name}: Inspecting cargo holds AND calibrating shield generators")

# apollo = StarShip("Apollo", fuel=50, health=100,crew_count=10)
# enterprise = StarShip("Enterprise", fuel=80, health=95,crew_count=8)
# print(apollo.status_report())
# print(enterprise.status_report())
# print(f"Total fleet size: {StarShip.fleet_size}")
# # Both ships can access the SAME fleet_size
# print(apollo.fleet_size)      
# print(enterprise.fleet_size)  
# print(StarShip.fleet_size)    
# apollo.add_crew(2)
# apollo.refuel(50)
# print(apollo.status_report())
# # How do we check fuel without calling status_report()?
# print(f"Apollo's fuel: {apollo.fuel}")  # What do we write here?

# print("\n=== Testing damage and repair ===")
# apollo.take_damage(20)
# print(apollo.status_report())
# apollo.repair(10)
# print(apollo.status_report())

# print("\n=== THE BUG - Watch this! ===")
# apollo.take_damage(200)  # Taking 200 damage!
# print(apollo.status_report())  # Health is now NEGATIVE!

# print("\n=== Another problem ===")
# apollo.repair(500)  # Repairing 500 health!
# print(apollo.status_report())  # Health is now WAY over 100!

# # Create ships
# print("=== Creating Ships ===")
# generic_ship = StarShip("USS Generic", fuel=80, health=100, crew_count=50)
# viper = FighterShip("Viper", fuel=100, health=90, crew_count=2, weapon_power=25)

# print(generic_ship.status_report())
# print(viper.status_report())

# print("\n=== Fighter Attacking Generic Ship ===")
# viper.fire_weapons(generic_ship)
# print(generic_ship.status_report())

# print("\n=== Can a generic ship fire weapons? ===")
# try:
#     generic_ship.fire_weapons(viper)
# except AttributeError as e:
#     print(f"Error: {e}")
#     print("Generic StarShip doesn't have fire_weapons() method!")

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

# THE MAGIC OF POLYMORPHISM
def fleet_movement(ships, distance):
    """This function works with ANY ship type!"""
    print(f"=== Moving fleet {distance} km ===")
    for ship in ships:
        ship.move(distance)  # Same method name, different behavior!

def fleet_emergency(ships):
    for ship in ships:
        ship.emergency_protocol()
      
fleet = [fighter, cargo, science]

# This ONE function works with ALL ship types
fleet_movement(fleet, 50)

print("\n=== Moving again ===")
fleet_movement(fleet, 100)

fleet_emergency(fleet)
# Testing Multiple Inheritance
print("=" * 60)
print("CREATING SHIPS")
print("=" * 60)

regular_fighter = FighterShip("Viper", 100, 90, 2, 25)
stealth_bomber = StealthBomber("Shadow", 100, 95, 3, 30)
print("\n" + "=" * 60)
print("METHOD RESOLUTION ORDER (MRO)")
print("=" * 60)
print("StealthBomber MRO:")
for cls in StealthBomber.__mro__:
    print(f"  → {cls.__name__}")

print("\n" + "=" * 60)
print("TESTING ABILITIES")
print("=" * 60)

print("\n--- Regular Fighter (no cloaking) ---")
regular_fighter.perform_maintenance()
regular_fighter.move(50)
# regular_fighter.engage_cloak()  # This would error - no cloaking!

print("\n--- Stealth Bomber (has BOTH fighter AND cloaking abilities) ---")
stealth_bomber.perform_maintenance()
stealth_bomber.move(50)
stealth_bomber.engage_cloak()
print(f"Status: {stealth_bomber.status()}")

print("\n--- Combat Scenario ---")
dummy_target = FighterShip("Target", 100, 100, 2, 10)
stealth_bomber.stealth_attack(dummy_target)

print("\n--- Checking what StealthBomber inherited ---")
print(f"Has fire_weapons? {hasattr(stealth_bomber, 'fire_weapons')}")
print(f"Has engage_cloak? {hasattr(stealth_bomber, 'engage_cloak')}")
print(f"Has weapon_power? {hasattr(stealth_bomber, 'weapon_power')}")
print(f"Has cloaked attribute? {hasattr(stealth_bomber, 'cloaked')}")

print("\n" + "=" * 60)
print("TESTING SHIELDED CARGO HAULER")
print("=" * 60)

print("\n--- Creating ShieldedCargoHauler ---")
armored_hauler = ShieldedCargoHauler("Fortress", fuel=80, health=100, crew_count=25, cargo_capacity=80, current_cargo=0)

print("\n--- Method Resolution Order (MRO) ---")
print("ShieldedCargoHauler MRO:")
for cls in ShieldedCargoHauler.__mro__:
    print(f"  → {cls.__name__}")

print("\n--- Initial Status ---")
print(armored_hauler.status_report())

print("\n--- Testing Cargo Abilities (from CargoHauler) ---")
armored_hauler.load_cargo(50)
print(armored_hauler.status_report())

print("\n--- Testing Shield Abilities (from ShieldGenerator) ---")
armored_hauler.activate_shields()
print(armored_hauler.status_report())

print("\n--- Combat Test: Taking damage WITH shields ---")
armored_hauler.take_hit(30)  # Shields should absorb this
print(armored_hauler.status_report())

armored_hauler.take_hit(50)  # Shields should absorb some, health takes rest
print(armored_hauler.status_report())

armored_hauler.take_hit(30)  # No shields left, all damage to health
print(armored_hauler.status_report())

print("\n--- Reactivating shields ---")
armored_hauler.activate_shields()
print(armored_hauler.status_report())

print("\n--- Testing Maintenance ---")
armored_hauler.perform_maintenance()

print("\n--- Checking inherited abilities ---")
print(f"Has load_cargo? {hasattr(armored_hauler, 'load_cargo')}")
print(f"Has activate_shields? {hasattr(armored_hauler, 'activate_shields')}")
print(f"Has cargo_capacity? {hasattr(armored_hauler, 'cargo_capacity')}")
print(f"Has shield_strength? {hasattr(armored_hauler, 'shield_strength')}")
