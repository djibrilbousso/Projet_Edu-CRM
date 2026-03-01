# Edu.CRM — Étudiant 1 : AUTH & Sécurité

## Architecture respectée

```
edu.crm/
├── app/
│   ├── auth/
│   │   └── route.py              ← Blueprint auth (login, logout)
│   ├── courses/
│   │   └── route.py              ← Placeholder étudiant 4
│   ├── dashboard/
│   │   └── route.py              ← Placeholder étudiant 5
│   ├── services/
│   │   ├── course_service.py     ← Placeholder étudiant 4
│   │   ├── student_service.py    ← Placeholder étudiant 2
│   │   └── teacher_service.py    ← Placeholder étudiant 3
│   ├── students/
│   │   └── route.py              ← Placeholder étudiant 2
│   ├── teachers/
│   │   └── route.py              ← Placeholder étudiant 3
│   ├── templates/
│   │   ├── base.html             ← Template de base commun
│   │   └── auth/
│   │       ├── login.html
│   │       └── home.html
│   ├── __init__.py               ← Application Factory
│   └── utils.py                  ← Décorateur login_required
├── config.py
└── run.py
```

## Installation & lancement

```bash
pip install flask
python run.py
```

Ouvrir : http://127.0.0.1:5000/auth/login

## Comptes de test

| Utilisateur | Mot de passe |
|-------------|--------------|
| admin       | admin123     |
| prof        | prof456      |

---

## Guide d'intégration pour les autres étudiants

### Étape 1 — Décommenter le blueprint dans `app/__init__.py`

```python
from app.students.route import students
app.register_blueprint(students, url_prefix='/students')
```

### Étape 2 — Protéger vos routes avec `login_required`

```python
from app.utils import login_required

@students.route('/')
@login_required
def list():
    ...
```

### Étape 3 — Mettre à jour la navbar dans `base.html`

Remplacer les `href="#"` par les vrais `url_for(...)` :

```html
<a class="nav-link" href="{{ url_for('students.list') }}">Étudiants</a>
```

---

## Réponses aux questions de la phase finale

**Pourquoi Application Factory ?**
Pour créer plusieurs instances de l'app avec des configs différentes (test, dev, prod) et éviter les imports circulaires.

**Pourquoi séparer routes et services ?**
Les routes gèrent uniquement le flux HTTP. Les services contiennent la logique métier. Code plus testable, lisible et réutilisable.

**Que se passe-t-il si un blueprint n'est pas enregistré ?**
Ses routes n'existent pas — Flask retourne 404. `url_for()` lève une `BuildError`.

**Pourquoi `url_prefix` ?**
Pour regrouper les routes par module (`/auth/login`, `/students/`) sans répéter le préfixe dans chaque route.

**Où doit se trouver la logique métier ?**
Dans `app/services/*_service.py` uniquement. Jamais dans les routes.
