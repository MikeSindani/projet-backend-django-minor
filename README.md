# projet-django-minor-back-end
## Presentation 
c'est le projet minor :
qui contient 4 applications pour entreprise miniere.
- **minor dash**: application de dashbord. 
- **minor asset**: application de minatenance puis de gestion de l'inventaire.
- **`minor planned** : application de planification de team et de approvisionnement.
- **minor fleet** : chaine d'approsionnement.

## Demarrer 
installer docker 
pour installer toutes les dependences:
```
docker-compose build
```
pour demarrer le serveur de developpement.
```
docker-compose up
```
pour acceder au shell afin de faire des migrations ou cree un superuser pour django docker utilise cette commander:
```
docker exec -it <nom du contanaire> /bin/bash
```
chez moi le contenaire est : "projet-backend-django-minor-web-1"
Ce projet est liees a un frontend disponible a ce lien [Lien](https://github.com/MikeSindani/projet-frondend-react-minor "titre de lien optionnel").

