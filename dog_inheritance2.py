class Dog:
     species = 'mammal'

class SomeBreed(Dog):
     pass

class SomeOtherBreed(Dog):
     species = 'reptile'

frank = SomeBreed()
frank.species

beans = SomeOtherBreed()
beans.species
