# DISCover: DISC Behavioral Assessment Platform

A Django web application that lets users take a DISC behavioral-style questionnaire, see their dominant profile with a description and suggested work environments, and compare it against the profile distribution of other registered users. Built as a capstone project (TCC) for an Information Systems degree, with first-job interns in mind.

> The interface is in Brazilian Portuguese.

## Tech stack

| Area | Technology |
| --- | --- |
| Backend | Python, Django 4.2 |
| Authentication | `django-allauth` with a custom user model (`user_auth.CustomUser`) |
| Forms | `django-crispy-forms`, `django-widget-tweaks` |
| Frontend | Django templates, HTML, CSS, JavaScript, Bootstrap 5 and Bootstrap Icons (CDN) |
| Charts | Chart.js (CDN) |
| Database | SQLite (configured in `settings.py`) |

<!-- TODO: confirmar — o README original dizia que a produção usa MySQL e `mysqlclient` está no requirements.txt, mas o settings.py só configura SQLite. Confirmar se MySQL foi usado em produção e, se sim, documentar a configuração. -->

## Key features

- **Sign-up and login** with `django-allauth`, extended with profile fields: phone, occupation, education level and status, gender, date of birth, location and sector. E-mail verification is disabled.
- **DISC questionnaire** using a 5-point Likert scale (strongly disagree to strongly agree). Questions are randomly shuffled on every load. The committed database ships with 20 questions, 5 per profile (Dominant, Influential, Steady, Conscientious).
- **Scoring**: the answers for each profile are averaged, the result is stored, and the highest average determines the user's main profile.
- **Results page** with the main profile, a description, and suggested work environments for that profile. Signed-in users keep their latest result on a personal profile page.
- **Profile pages** describing each of the four DISC styles.
- **Live distribution chart** on the home page: a Chart.js bar chart that polls a JSON endpoint (`/disc/estatisticas/`) every 15 seconds and shows how many registered users fall into each profile.
- **Django admin** to manage the question bank.
- **Static pages**: home, about and contact.

## Getting started

### Prerequisites

- Python 3.10 or newer (the project targets Django 4.2; the setup below was verified on Python 3.13)

### Installation

```bash
git clone https://github.com/Daniiizita/disc_assessment
cd disc_assessment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

`requirements.txt` includes `mysqlclient`, which needs the MySQL client development libraries to compile and is **not used** by the default SQLite configuration. If it fails to install, remove that line and run `pip install` again.

### Run

```bash
python manage.py migrate
python manage.py runserver
```

Then open <http://localhost:8000>. The repository includes a `db.sqlite3` with the 20 questions already loaded; `migrate` applies any pending migrations. To start from an empty database instead, delete `db.sqlite3`, run `migrate`, create an admin with `python manage.py createsuperuser`, and add questions at <http://localhost:8000/admin/> (each question has a text and a DISC profile).

`ALLOWED_HOSTS` in `assessment_disc_project/settings.py` lists `localhost` and `127.0.0.1`; to serve the app from another address, set the `ALLOWED_HOSTS` environment variable (comma-separated) or edit the list.

### Configuration

For anything beyond local development, set these environment variables (the defaults are for local use only):

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | Django secret key. Always set your own in production. |
| `DEBUG` | `true` (default) or `false`. Use `false` in production. |
| `ALLOWED_HOSTS` | Extra allowed hosts, comma-separated. |

### Run the tests

```bash
python manage.py test
```

The tests cover anonymous questionnaire submission, per-profile score averaging and the results page.

## Technical highlight: a Likert-based DISC scoring model

Each `Pergunta` (question) belongs to one of the four DISC profiles. When the form is submitted, answers (1 to 5) are grouped by the profile of their question and averaged per profile, so the score stays comparable even if profiles have different numbers of questions. The averages are stored in a `ResultadoDISC` row, and its `perfil_mais_alto` property picks the highest-scoring profile. For signed-in users the result is linked to their `CustomUser` through a one-to-one relation, which is what feeds the distribution chart on the home page.

## Project structure

```
assessment_disc_project/   Django settings and root URLs
core/                      Home, about, contact and DISC profile pages
disc/                      Questions, questionnaire form, scoring, results, statistics endpoint
user_auth/                 Custom user model, user profile page
templates/account/         allauth login, signup and logout templates
```

## Roadmap

Ideas listed by the author as future work (none of them are implemented yet):

- Integration with recruitment APIs to suggest job openings based on the user's profile
- A custom admin dashboard with user-activity reports
- A more comprehensive automated test suite (a small one exists today: see [Run the tests](#run-the-tests))

## Contact

Questions or suggestions: <goncalvesdani54@gmail.com>

## License

Distributed under the MIT License. See [LICENSE](LICENSE).
