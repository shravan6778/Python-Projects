class StarShip:
     # Class attribute - shared by ALL starships
    fleet_size=0
    def __init__(self,name,fuel,health,crew_count):
        # Instance attributes - unique to EACH starship
        self.name=name
        self.fuel=fuel
        self.health= health
        self.crew_count=crew_count
        # Every time a ship is created, increment fleet_size
        StarShip.fleet_size += 1
    def status_report(self):
        return f"{self.name}: Fuel:{self.fuel} Health:{self.health} crew_count:{self.crew_count}"
    def add_crew(self,number:int):
        self.crew_count+=number
    
apollo = StarShip("Apollo", fuel=100, health=100,crew_count=10)
enterprise = StarShip("Enterprise", fuel=80, health=95,crew_count=8)
print(apollo.status_report())
print(enterprise.status_report())
print(f"Total fleet size: {StarShip.fleet_size}")
# Both ships can access the SAME fleet_size
print(apollo.fleet_size)      
print(enterprise.fleet_size)  
print(StarShip.fleet_size)    
apollo.add_crew(2)
print(apollo.status_report())
