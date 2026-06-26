# Ver03 - גרסה לפריסה באינטרנט

זו אותה אפליקציית חידון, אבל מוכנה יותר לפריסה לשירות hosting.

## כתובות אחרי פריסה

מנחה:

```text
https://YOUR-SITE/host
```

שחקנים:

```text
https://YOUR-SITE/player
```

## קבצים חשובים לפריסה

- `app.py`
- `requirements.txt`
- `Procfile`
- `templates/`
- `static/`
- `images/`
- `DataQuestions.py`
- `Config.py`

## פקודת הרצה בשרת

```text
gunicorn app:app
```

## הערה חשובה

כרגע מצב המשחק נשמר בזיכרון של השרת. זה טוב ל-MVP, אבל אם שירות ה-hosting מרדים או מאתחל את השרת, המשחק יתאפס.
