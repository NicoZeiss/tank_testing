from enum import Enum


class ArmorType(Enum):
    """Enum for different types of tank armor."""
    CHOBHAM = 'chobham', 100
    COMPOSITE = 'composite', 50
    CERAMIC = 'ceramic', 50

    @property
    def name(self):
        """Returns the name of the armor type."""
        return self.value[0]

    @property
    def armor_value(self):
        """Returns the armor value of the armor type."""
        return self.value[1]
    

class Tank:
    """Class representing a tank."""

    def __init__(self, armor: int, penetration: int, armor_type: ArmorType, name: str = None) -> None:
        if not armor_type in ArmorType:
            raise Exception(f'Invalid armor type {armor_type}')
            
        self.armor = armor
        self.penetration = penetration
        self.armor_type = armor_type
        self.name = name

    @property
    def name(self) -> str:
        """Name getter"""
        return self._name

    @name.setter
    def name(self, value) -> None:
        """Name setter, with default value generation."""
        self._name = value or self._gen_default_name()

    def _gen_default_name(self) -> str:
        """Generates a default name for the tank."""
        return f"Tank {self.armor_type.name} A{self.armor} P{self.penetration}"
    
    @property
    def real_armor(self) -> int:
        """Calculates the real armor value of the tank."""
        return self.armor + self.armor_type.armor_value

    def vulnerable(self, tank: 'Tank') -> bool:
        """Checks if the tank is vulnerable to another tank's penetration."""
        return self.real_armor <= tank.penetration

    def swap_armor(self, other_tank: 'Tank') -> 'Tank':
        """Swaps the armor of this tank with another tank."""
        self.armor, other_tank.armor = other_tank.armor, self.armor
        return other_tank

    def __str__(self) -> str:
        return self.name.lower().replace(' ', '-')

    def __repr__(self) -> str:
        return str(self)
    

m1_1 = Tank(600, 670, ArmorType.CHOBHAM)
m1_2 = Tank(620, 670, ArmorType.CHOBHAM)

if m1_1.vulnerable(m1_2):
    print('Vulnerable to self') 
    # Ce n'est pas vraiment le même tank, l'armure est différente
    # Si on veut vraiment le même tank : m1_1 = m1_2 = Tank(600, 670, ArmorType.CHOBHAM)

m1_1.swap_armor(m1_2)


tanks = [Tank(400, 400, ArmorType.CERAMIC)] * 5 
# On peut aussi ajouter le type steel si nécessaire (j'ai remplacé arbitrairement par ceramic), 
# manque de définition du besoin métier.

# On crée 5 fois le même tank, ça n'a pas trop de sens avec 
# la suite de l'exercice (on veut tester la resistance de plusieurs tank)

for i, tank in enumerate(tanks):
    tank.name = f"Tank{str(i)}_Small"

# Pour faire mieux, on peut également créer la liste de tank comme suit (initialisation avec un name en param) :
# tanks = [Tank(400, 400, ArmorType.CERAMIC, f"Tank{str(i)}_Small") for i in range(5)]

# Si on veut une liste de tanks avec des armures différentes, on peut faire par exemple :
# tanks = [Tank(400 + i * 10, 400, ArmorType.CERAMIC, f"Tank{str(i)}_Small") for i in range(5)]

test = [tank.vulnerable(m1_1) for tank in tanks] # Je redéfinis test ici pour montrer le refactor de la boucle, 
# mais non nécessaire pour la suite du script

def test_tank_safe(shooter_tank: Tank, test_tanks: list[Tank] = None) -> str:
    """Tests if at least one tank is safe from the shooter's penetration."""
    at_least_one_safe = not all(tank.vulnerable(shooter_tank) for tank in test_tanks or [])
    return f"{'A' if at_least_one_safe else 'No'} tank is safe"

test_tank_safe(m1_1, tanks)
