# ASCII pattern matching simulation

Space invaders are upon us!
We have to track them down.

This Python application takes a file(this readme file)
and accuracy as an argument, 
extract the radar sample and known invader samples, 
and reveal possible locations of those pesky invaders.
Prints the cleaned radar sample in the same directory of the input file. 

### Known invaders:
~~~~
--o-----o--
---o---o---
--ooooooo--
-oo-ooo-oo-
ooooooooooo
o-ooooooo-o
o-o-----o-o
---oo-oo---
~~~~

~~~~
---oo---
--oooo--
-oooooo-
oo-oo-oo
oooooooo
--o--o--
-o-oo-o-
o-o--o-o
~~~~

### Example radar sample:
~~~~
----o--oo----o--ooo--ooo--o------o---oo-o----oo---o--o---------o----o------o-------------o--o--o--o-
--o-o-----oooooooo-oooooo---o---o----o------ooo-o---o--o----o------o--o---ooo-----o--oo-o------o----
--o--------oo-ooo-oo-oo-oo-----O------------ooooo-----oo----o------o---o--o--o-o-o------o----o-o-o--
-------o--oooooo--o-oo-o--o-o-----oo--o-o-oo--o-oo-oo-o--------o-----o------o-ooooo---o--o--o-------
------o---o-ooo-ooo----o-----oo-------o---oo-ooooo-o------o----o--------o-oo--ooo-oo-------------o-o
-o--o-----o-o---o-ooooo-o-------oo---o---------o-----o-oo-----------oo----ooooooo-ooo-oo------------
o-------------ooooo-o--o--o--o-------o--o-oo-oo-o-o-o----oo------------o--oooo--ooo-o----o-----o--o-
--o-------------------------oo---------oo-o-o--ooo----oo----o--o--o----o--o-o-----o-o------o-o------
-------------------o----------o------o--o------o--------o--------o--oo-o-----oo-oo---o--o---o-----oo
----------o----------o---o--------------o--o----o--o-o------------oo------o--o-o---o-----o----------
------o----o-o---o-----o-o---o-----oo-o--------o---------------------------------o-o-o--o-----------
---------------o-------o-----o-------o-------------------o-----o---------o-o-------------o-------oo-
-o--o-------------o-o-----o--o--o--oo-------------o----ooo----o-------------o----------oo----o---o-o
-o--o-------------o----oo------o--o-------o--o-----o-----o----o-----o--o----o--oo-----------o-------
-o-----oo-------o------o----o----------o--o----o-----o-----o-------o-----------o---o-o--oooooo-----o
-o--------o-----o-----o---------oo----oo---o-o---------o---o--oooo-oo--o-------o------oo--oo--o-----
------------o---------o---------o----oooo-------------oo-oo-----ooo-oo-----o-------o-oo-oooooooo---o
----------------------o------------oooooooo---o-----o-------o--oooooo-o------------o-o-ooooooo-o----
------------o------o---o---o-------oo-oo--o--o---------o--o-o-o-ooooo-o--------------oo-o----o-oo-o-
---o-o----------oo-------oo----o----oooooooo-------o----o-o-o-o-----o-o-----o----------ooo-oo--o---o
-o-o---------o-o---------------o--o--o--ooo---ooo-------o------oo-oo------------o--------o--o-o--o--
-------oo---------------------------o-oo----------o------o-o-------o-----o----o-----o-oo-o-----o---o
---o--------o-----o-------o-oo-----oo--oo-o----oo----------o--o---oo------oo----o-----o-------o-----
---o--ooo-o---------o-o----o------------o---------o----o--o-------o----o--------o----------------oo-
---o------o----------------o----o------o------o---oo-----------o-------------o----------oo---------o
--oo---------------o--o------o---o-----o--o-------------o------o-------o-----o-----o----o------o--o-
-o-------o----------o-o-o-------o-----o--o-o-----------o-oo-----------o------o---------o-----o-o----
----------o----o-------o----o--o------o------------o---o---------------oo----o-----ooo--------------
----o--------oo----o-o----o--o------ooo----o-oooo---o--o-oo--------o-oo-----o-o---o-o--o-----oo-----
------o--------o-ooooo----o---o--o-----o---------------o-o-------o-----o----------------------------
o-------oo----o--oooooo-o---o--o------oooo----------o-oo-------o---o----------o------oo-------------
-o---o----------o--oo-oo-o---o-----o-o-----------------------oo--o------o------o--------------------
-----oo-o-o-o---ooooooooo----o----o--------o--o---oo---o------------o----------o-o---o------o-o--oo-
------o------o---ooo-o---------------------------o--o---o---o----o--o-------o-----o------o----o----o
-------o----------ooo-o-----o----o---o--o-oo--o--o-o--o------o--o-oo---ooo------------------------o-
-o-------o------o-o--ooo--o---o---oo-----o----o-------------o----o-ooo-o------o--o-o------o-o-------
---oo--o---o-o---------o---o--------------o--o-----o-------o-----o--o---o-oo--------o----o----o-----
o------o----oo-o-----------oo--o---o--------o-o------o-------o-o------o-oo---------o-----oo---------
----o--o---o-o-----------o---o------------o-------o----o--o--o--o-o---------------o-----------------
-------oo--o-o-----o-----o----o-o--o----------------------o-------o------o----oo----ooo---------o---
o-----oo-------------------o--o-----o-----------o------o-------o----o-----------o----------------o--
--o---o-------o------------o--------------------o----o--o-------------oo---o---------oo--------o----
--o--------o---------o------------o------o-------o------------o-------o---o---------ooooo-----------
------o--------------o-o-o---------o---o-------o--o-----o-------o-o----------o-----oo-ooo----------o
--o---------------o----o--oo-------------o---------o-------------------oo---------oo-o-ooo----------
-o-----------o------ooo----o----------------ooo-----o--------o--o---o-----------o-o-oooooo--------oo
-o---o-------o---o-oooo-----o-------------------o----oo-----------------o--o--------o--o------o--o--
-------o---o------oooooo--o----ooo--o--------o-------o----------------------------oo-oo-o--o--------
o--oo------o-----oo--o-oo------------oo--o------o--o-------------oo----o------------oooo-o------oo--
-----o----------ooooooooo--------------oo--------------oo-----o-----o-o--o------o----------o----o---
~~~~