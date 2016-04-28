# jobscraper


## Un spider pour trouver un poste de développeur en France

Trouver un poste de développeur quand on ne fait pas C#, .NET, PHP, Java/JEE
mais du Python et du R peut être ardu. Les outils à disposition sont
principalement des interfaces Web qui peuvent vite devenir frustrantes en
fonction des fonctionnalités implémentées et de la multitude de données à parcourir.

En tant que développeur, j'aime trouver des solutions efficaces en utilisant
des outils existants ou en les créant moi-même. 

Ce projet allie donc l'utile à l'agréable en fournissant un spider qui va
extraire les offres d'emploi avec certains critères sur le site de [Pole Emploi][pole_emploi].
Les offres sont ensuite stockées en local dans une base SQLite (située dans
`data/jobs.db`).


## Limitations

* Actuellement **jobscraper** ne fonctionne qu'avec un seul site (Pole Emploi)
mais ajouter d'autres sites n'est pas difficile (cf [pyjobs/crawlers][crawlers])

* Le site de Pole Emploi ne permet d'afficher que 20 resultats maximum.


## Usage

* Extraire les données et créer/mettre à jour la base de données:

    make create_db

* Supprimer la base de données

    make remove_db


## Note

**jobscraper** n'a pas la prétention d'être la solution ultime mais est avant
tout un projet personnel commencé parce que

* j'étais frustré de parcourir des centaines d'offres dont la plupart ne
  correspondent pas à mon profil
* j'avais du temps en fin d'après-midi et **scrapy** m'avait l'air sympa


## Inspiration

Ce projet s'inspire en grande partie sur [pyjobs/crawlers][crawlers] qui est
utilisé pour le site [pyjobs][pyjobs]. Je vous conseille d'aller y jeter un
oeil. 


[crawlers]: https://github.com/pyjobs/crawlers
[pole_emploi]: http://www.pole-emploi.fr/accueil/
[pyjobs]: http://pyjobs.fr/
