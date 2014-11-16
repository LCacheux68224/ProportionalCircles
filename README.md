Analyse en ronds proportionnels<br>avec échelle automatique
===================

###_(Extension pour Qgis 2.0.1 et +)_
L'analyse en ronds proportionnels est utilisée pour représenter des effectifs, par exemple la population de communes de pays.
##Exemple : Nombre de ménages des communes du Morbihan en 2009
![](https://raw.githubusercontent.com/LCacheux68224/ImagesForDoc/master/ProportionalCircles/ProportionalCircles1.png)<br>
_Source : Insee, RP2009 au lieu de résidence_<br>
_Fonds de cartes : Chefs-lieux de communes créé à partir du Répertoire Géographique des Communes IGN-RGC® 2012, contours de département et régions IGN-GEOFLA® 2012_
## Fichiers nécessaires :
* Un fond d'analyse (points ou polygones) ;
* Une table de données contenant un identifiant géographique et la variable à représenter ;<br>![](https://raw.githubusercontent.com/LCacheux68224/ImagesForDoc/master/ProportionalCircles/Table.png)
* Un fond correspondant au contour de l'analyse en cas de calcul automatique de l'échelle.
 
## Utilisation :
L'analyse en rond se lance soit depuis le menu « **_Vecteur\Analyse en ronds_** »,
soit en cliquant sur l'icône 
![](https://raw.githubusercontent.com/LCacheux68224/ImagesForDoc/master/ProportionalCircles/iconRonds.png) après avoir fait la jointure entre la table de données et le fond d'analyse<br><br>
Renseigner les paramètres suivants :
* **Fond cartographique**-> Fond d'analyse (points ou vecteurs) ;
* **Valeurs** -> Variable à représenter ;
* **Contour** -> Contour d'analyse pour le calcul de l'échelle automatique ;<br><br>
Pour une échelle personnalisée, pour permette d'obtenir plusieurs analyses comparables
* **Rayon** -> Rayon maximum de l'échelle personnalisée ;
* **Valeur** -> Valeur maximum de l'échelle personnalisée ;<br><br>
* **Valeurs à représenter…** -> Liste des valeurs à représenter dans la légende. Les valeurs sont à séparer par un point-virgule. Laisser vide pour obtenir une légende avec trois valeurs automatiques (max, max/3, max/9)

Il est possible également de ne sélectionner qu'une partie des entités du fond de carte pour limiter l'analyse à une zone restreinte.<br>
![](https://raw.githubusercontent.com/LCacheux68224/ImagesForDoc/master/ProportionalCircles/ProportionalCircles2.png)<br>
_Fonds de cartes : Chefs-lieux de communes créé à partir du Répertoire Géographique des Communes IGN-RGC® 2012, contours de département et régions IGN-GEOFLA® 2012_<br><br>
En cochant la case **Analyse étendue**, l'échelle des ronds est calculée en fonction des entités sélectionnées, puis étendue au reste de la carte.<br>
![](https://raw.githubusercontent.com/LCacheux68224/ImagesForDoc/master/ProportionalCircles/ProportionalCircles3.png)<br>
_Source : Insee, RP2009 au lieu de résidence_<br>
_Fonds de cartes : Chefs-lieux de communes créé à partir du Répertoire Géographique des Communes IGN-RGC® 2012, contours de département et régions IGN-GEOFLA® 2012_

### Deux sorties sont proposées : 
* Une sortie sous forme de carte mémoire qui nécessite l'extension « **Memory Layer Saver** » pour que le fond puisse être enregistré en parallèle au projet dans un fichier _NomDuProjet.qgs.mldata_ ;
* Une sortie sous forme de fond Shapefile classique.
