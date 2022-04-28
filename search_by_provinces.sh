#!/usr/bin/env bash

set -euo pipefail

pip install -r requirements.txt
python3 -m pip install --no-cache-dir --editable .

for province in "Achaia" "Aegyptus" "Africa proconsularis" "Alpes Cottiae" "Alpes Graiae" "Alpes Maritimae" "Alpes Poeninae" "Apulia et Calabria / Regio II" "Aquitani(c)a" "Arabia" "Armenia" "Asia" "Baetica" "Barbaricum" "Belgica" "Britannia" "Bruttium et Lucania / Regio III" "Cappadocia" "Cilicia" "Corsica" "Creta et Cyrenaica" "Cyprus" "Dacia" "Dalmatia" "Etruria / Regio VII" "Galatia" "Gallia Narbonensis" "Germania inferior" "Germania superior" "Hispania citerior" "Italia" "Latium et Campania / Regio I" "Liguria / Regio IX" "Lugudunensis" "Lusitania" "Lycia et Pamphylia" "Macedonia" "Mauretania Caesariensis" "Mauretania Tingitana" "Mesopotamia" "Moesia inferior" "Moesia superior" "Noricum" "Numidia" "Palaestina" "Pannonia inferior" "Pannonia superior" "Picenum / Regio V" "Pontus et Bithynia" "Provincia incerta" "Raetia" "Regnum Bospori" "Roma" "Aemilia / Regio VIII" "Samnium / Regio IV" "Sardinia" "Sicilia" "Syria" "Thracia" "Transpadana / Regio XI" "Umbria / Regio VI" "Venetia et Histria / Regio X"
	do
		echo "Currently scraping: $province"
		python3 src/lat_epig/parse.py "%" -v "$province" --debug
		
done
