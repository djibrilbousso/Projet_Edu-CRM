# Edu.CRM — Système de Gestion Scolaire

Application Flask modulaire de gestion d'une école, développée en groupe avec Blueprints.

---

## 👥 Membres du groupe et tâches

- 1 — Djibril Bousso
- 2 — Thiane Gueye
- 3 — Seynabou Gueye
- 4 — Fily Thiaw
- 5 — Halima Léna Camara
- 6 — Mame Coumba Sall

### Étudiant 1 — Djibril Bousso (`etudiant1`) — AUTH & Sécurité
- Création du blueprint `auth`
- Implémentation de `/login` et `/logout`
- Gestion des sessions
- Implémentation du décorateur `login_required`
- Protection des blueprints students, teachers, courses
- Gestion des flash messages

### Étudiant 2 — Thiane Gueye (`etudiant2`) — Gestion Étudiants
- Création du blueprint `students`
- Implémentation des routes : `/students`, `/students/create`, `/students/delete/<id>`
- Création de `student_service.py` :
  - `add_student()`
  - `delete_student()`
  - `list_students()`
  - `get_student_by_id()`
- **Ajout par Halima Léna Camara** :
  - Service : vérification d'unicité d'email, `update_student()`, `search_students()`
  - Route : `/students/edit/<id>`, recherche par nom/niveau/filière, validation du format email

### Étudiant 3 — Seynabou Gueye(`etudiant3`) — Gestion Enseignants
- Création du blueprint `teachers`
- Création de `teacher_service.py` :
  - `add_teacher()`
  - `list_teachers()`
  - `delete_teacher()`
- **Ajout par Halima Léna Camara** :
  - Service : vérification d'unicité d'email, `update_teacher()`, `search_teachers()`, `get_teacher_by_id()`, protection suppression si cours actifs, protection modification spécialité si cours actifs
  - Route : `/teachers/edit/<id>`, recherche par nom, validation du format email

### Étudiant 4 — Fily Thiaw et Halima Léna Camara (`etudiant4`) — Gestion Cours
- Création de `course_service.py` :
  - `add_course()`
  - `list_courses()`
  - `delete_course()`
- **Ajout par Halima Léna Camara** :
  - Service : `assign_student_to_course()`, `get_course_by_id()`
  - Route : `courses/route.py` complet, filtrage enseignants par spécialité, inscription étudiants avec filtres niveau/filière, page détail du cours

### Étudiant 5 — Mame Coumba (`etudiant5`) — Dashboard & UI
- Création du blueprint `dashboard`
- Création de `base.html` et navbar commune
- Templates cohérents pour toutes les pages
- Affichage des flash messages
- Intégration du travail des autres
- Pagination des listes

---

##  Comment lancer le projet

### 1. Cloner le repo
```bash
git clone https://github.com/djibrilbousso/Projet_Edu-CRM.git
cd Projet_Edu-CRM
```

### 2. Créer l'environnement virtuel
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install flask
```

### 4. Lancer l'application
```bash
python3 run.py
```

### 5. Ouvrir dans le navigateur
```
http://127.0.0.1:5000
```

### 6. Compte de test
| Username | Mot de passe |
|----------|-------------|
| mame | mame123 |

---

## 🏗️ Architecture du projet
```
Projet_Edu-CRM/
├── app/
│   ├── auth/           → Blueprint AUTH (etudiant1)
│   ├── students/       → Blueprint Students (etudiant2)
│   ├── teachers/       → Blueprint Teachers (etudiant3)
│   ├── courses/        → Blueprint Courses (etudiant4)
│   ├── dashboard/      → Blueprint Dashboard (etudiant5)
│   ├── services/       → Logique métier
│   │   ├── student_service.py
│   │   ├── teacher_service.py
│   │   └── course_service.py
│   ├── templates/      → Templates HTML (héritage base.html)
│   ├── static/
│   │   └── css/        → Fichiers CSS séparés par page
│   ├── __init__.py     → Application Factory (create_app)
│   └── utils.py        → Décorateurs réutilisables
├── config.py
├── run.py
└── README.md
```

---

## ✅ Fonctionnalités

### Auth
- Login / Logout
- Protection des routes avec `@login_required`
- Gestion des sessions et flash messages

### Étudiants
- Liste, ajout, modification, suppression
- Recherche par nom, niveau ou filière
- Caractérisés par : nom, email, niveau (L1-M2), filière (GLRS/CPD/CDSD)

### Enseignants
- Liste, ajout, modification, suppression
- Recherche par nom
- Protection suppression et modification spécialité si cours actifs
- Caractérisés par : nom, email, spécialité

### Cours
- Liste, ajout, suppression
- Filtrage enseignants par spécialité
- Inscription étudiants avec filtres niveau/filière
- Voir liste des étudiants inscrits
- Caractérisés par : titre, enseignant, spécialité, étudiants inscrits

### Dashboard
- Statistiques : nombre d'étudiants, enseignants, cours
- Actions rapides
- Pagination

---

## ❓ Réponses aux questions

**Pourquoi utiliser Application Factory ?**
Sans Application Factory, l'application Flask est créée directement au démarrage — on ne peut pas la reconfigurer.
Avec Application Factory, on appelle `create_app()` pour créer l'application, ce qui permet de passer différentes configurations selon le contexte (développement, test, production) sans modifier le code source.

**Pourquoi séparer routes et services ?**
Si on met toute la logique dans les routes, le code devient difficile à lire et à maintenir.
En séparant, si on veut changer comment on ajoute un étudiant, on modifie uniquement `student_service.py` sans toucher à `route.py`. Chaque fichier a une seule responsabilité claire.

**Que se passe-t-il si un blueprint n'est pas enregistré ?**
Flask ne connaît pas les routes de ce blueprint.
Exemple : si on oublie d'enregistrer le blueprint `dashboard`, accéder à `/` retourne une erreur 404. Et utiliser `url_for('dashboard.index')` dans un template provoque une `BuildError` et fait planter l'application.

**Pourquoi utiliser url_prefix ?**
Sans url_prefix, deux blueprints peuvent avoir la même route `/` et Flask ne sait pas laquelle utiliser.
Exemple : students et teachers ont tous les deux une route `/` — grâce au prefix, Flask sait que `/students/` appartient au blueprint students et `/teachers/` appartient au blueprint teachers.

**Où doit se trouver la logique métier ?**
Dans les services uniquement. Les routes ne doivent pas manipuler les données directement.
Exemple : vérifier si un email existe déjà se fait dans `student_service.py`, pas dans `route.py`. Ainsi si plusieurs routes ont besoin de cette vérification, elles appellent toutes le même service.