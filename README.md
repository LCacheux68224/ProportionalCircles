Analyse en ronds/secteurs proportionnels<br>avec échelle et légende automatique
===================

###_(Extension pour Qgis 2.0.1 et +)_
L'analyse en ronds proportionnels est utilisée pour représenter des effectifs ou des évolutions en effectifs, par exemple la population de communes d'un pays ou d'une région.<br><br>
Dans l'exemple présenté ici, l'extension crée deux couches : l'une pour une analyse en ronds et une seconde pour sa légende. Ces deux couche peuvent ainsi être utilisée comme n'importe quel fond cartographique (analyse catégorisée/graduée, filtrage, déplacement d'entités notamment les ronds de la légende). Elles peuvent également être enregistrées et réutilisées dans n'importe quel logiciel de cartographie acceptant le format Shapefile.<BR>   
##Exemple d'analyse en ronds : <br>Nombre de ménages des communes du Morbihan en 2009
![](https://raw.githubusercontent.com/LCacheux68224/ImagesForDoc/master/ProportionalCircles/ProportionalCircles1.png)<br>
_Source : Insee, RP2009 au lieu de résidence_<br>
_Fonds de cartes : Chefs-lieux de communes créé à partir du Répertoire Géographique des Communes IGN-RGC® 2012, contours de département et régions IGN-GEOFLA® 2012_
## Fichiers nécessaires :
* Un fond d'analyse (points ou polygones) ;
* Une table de données contenant un identifiant géographique ainsi que la variable à représenter au cas où cette dernière ne serait pas déjà présente dans le fond d'analyse. ;<br>![](https://raw.githubusercontent.com/LCacheux68224/ImagesForDoc/master/ProportionalCircles/Table.png)
* Un fond de contour est nécessaire uniquement pour un calcul automatique de l'échelle.
 
## Utilisation :
L'analyse en rond se lance soit depuis le menu « **_Vecteur\Analyse en ronds_** »,
soit en cliquant sur l'icône 
![](https://raw.githubusercontent.com/LCacheux68224/ImagesForDoc/master/ProportionalCircles/iconRonds.png). Les données à analyser doivent soit être déjà présentes dans la table attributaire du fond d'analyse, soit y être ajoutées par une jointure<br><br>
Les paramètres à renseigner :
* **Fond cartographique**-> Fond d'analyse (points ou vecteurs) ;
* **Variables sélectionnées** -> La ou les Variable(s) à représenter. En cas de choix multiple l'analyse affichera des secteurs proportionnels d'angle fixe.;
* **Fond de référence** -> Contour utilisé pour le calcul de l'échelle automatique ;<br><br>
L'échelle automatique permet d'obtenir de manière à ce que l'aire des l'ensemble des ronds soit égale à 1/7 de la surface d'un contour de référence choisi par l'utilisateur.<br> <br>
L'échelle personnalisée permet quant à elle de faire correspondre une valeur particulière à un rayon déterminé par l'utilisateur pour pouvoir faire plusieures analyses comparables, par exemple.
* **Rayon** -> Rayon maximum de l'échelle personnalisée (attention le rayon s'exprime en mètres);
* **Valeur** -> Valeur maximum de l'échelle personnalisée ;<br>
La valeur maximale ainsi que le rayon maximum apparaissent automatiquement dans la barre de message en fin d'analyse au cas où l'on voudrait refaire une analyse sur un autre territoire en utilisant la même échelle.<br><br>
* **Valeurs à représenter…** -> Il est possible de définir ici une liste de valeurs que l'on souhaite voir apparaître dans la légende. Les valeurs sont à séparer par un point-virgule ou un espace. Si la case est laissée vide, trois valeurs seront automatiquement représentées (max, max/3, max/9)

Il est possible également de restreindre l'annalyse en ne sélectionnant qu'une partie des entités du fond de carte.<br>
![](https://raw.githubusercontent.com/LCacheux68224/ImagesForDoc/master/ProportionalCircles/ProportionalCircles2.png)<br>
_Fonds de cartes : Chefs-lieux de communes créé à partir du Répertoire Géographique des Communes IGN-RGC® 2012, contours de département et régions IGN-GEOFLA® 2012_<br><br>
En cochant la case **Analyse étendue**, l'échelle des ronds est calculée en fonction de la sélection du fond d'analyse et du contour, puis étendue au reste des entités.<br>
![](https://raw.githubusercontent.com/LCacheux68224/ImagesForDoc/master/ProportionalCircles/ProportionalCircles3.png)<br>
_Source : Insee, RP2009 au lieu de résidence_<br>
_Fonds de cartes : Chefs-lieux de communes créé à partir du Répertoire Géographique des Communes IGN-RGC® 2012, contours de département et régions IGN-GEOFLA® 2012_<br>

### Les deux types de sorties proposées : 
* Une sortie sous forme de deux cartes "mémoire" (analyse + légende). Ce type de sortie nécessite l'extension « **Memory Layer Saver** » pour que les fonds puisse être enregistrés en parallèle au projet dans un fichier _NomDuProjet.qgs.mldata_ ;
* Une sortie sous forme de deux fonds Shapefile classiques (analyse + légende).
