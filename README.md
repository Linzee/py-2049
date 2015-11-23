## py-2049
Program is analysing data about train delays.

###Statistics of delays
It displays statistics about particular train or group of trains.

```python 2049.py -h```

Specific train
```python 2049.py -t "Os 9206"```

Group of trains
```python 2049.py -t "EC"```

All trains
```python 2049.py```

###Probability I'll be able to change train
It calculate probability you'll be able to change your train based on past delays.

Input is list of train names with time (in minutes) you have between each to transfer.

```python 2049.py -p "EC 277 Slovan" 40 "R 1601 Chopok" 10 "Os 9119" 20 "Os 9219"```

```python 2049.py -p "Os 4171" 32 "Zr 1847 Rozsutec" 20 "R 811 Gemeran"```

Data have to by obtained by [py-2049-data](https://github.com/Linzee/py-2049-data) or [downloaded from my website](http://ienze.me/media/delays.json)

## py-2049
Program analyzuje dáta o meškaní vlakov.

###Štatistika meškania
Zobrazenie štatistík o vlaku alebo vlakoch.

```python 2049.py -h```

Konkrétny vlak
```python 2049.py -t "Os 9206"```

Skupina vlakov
```python 2049.py -t "EC"```

Všetky vlaky
```python 2049.py```

###Pravdepodobnosť, že stihnem prestúpiť
Výpočet pravdepodobnosti, že stihnem prestúpiť na základe predošlích údajov.

Program najprv vyhľadá stanice v ktorých sa bude prestupovať. Pre každý vlak zistí koľko krát stihol prísť z menším ako zadaným meškaním a vypočíta pravepodobnoť prestupu.

Zadáva sa zoznam mien vlakov z časom na prestup medzi nimi.

```python 2049.py -p "EC 277 Slovan" 40 "R 1601 Chopok" 10 "Os 9119" 20 "Os 9219"```

```python 2049.py -p "Os 4171" 32 "Zr 1847 Rozsutec" 20 "R 811 Gemeran" 10```

Dáta musia byť získané pomocou [py-2049-data](https://github.com/Linzee/py-2049-data) alebo [stiahnuté z mojej stránky](http://ienze.me/media/delays.json)