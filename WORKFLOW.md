# Ver05 - הוראות עבודה מלאות

גרסה זו מיועדת לעבודה דרך Render.

את השינויים הבאים עושים ב-`VerNN`, בודקים מקומית, ואז מעלים ל-GitHub כדי ש-Render יעדכן את האתר.

## הלינקים הקבועים

מסך מנחה:

```text
https://kahoot-bat-mitzva.onrender.com/host
```

מסך שחקנים:

```text
https://kahoot-bat-mitzva.onrender.com/player
```

את הלינק של השחקנים שולחים ב-WhatsApp / מייל / הודעה:

```text
https://kahoot-bat-mitzva.onrender.com/player
```

## בדיקה מקומית אחרי שינוי קוד

פותחים Terminal בתיקיית `VerNN`.

אם זו הפעם הראשונה שמריצים את `VerNN` מקומית, יוצרים סביבה ומתקינים חבילות:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

אחרי זה מריצים:

```powershell
.\.venv\Scripts\python.exe app.py
```

## עצירת שרת מקומי

אם `Ctrl+C` לא עובד ב-Terminal, או אם המקלדת עוברת לעברית, לא צריך להשתמש בקיצור הזה.

פותחים Terminal חדש ומריצים:

```powershell
Stop-Process -Id (Get-NetTCPConnection -LocalPort 5000 -State Listen).OwningProcess -Force
```

אם הפקודה לא כותבת כלום, זה תקין.

כדי לוודא שהשרת באמת נסגר:

```powershell
Get-NetTCPConnection -LocalPort 5000 -State Listen
```

אם לא מופיע תהליך, פורט `5000` פנוי ואפשר להפעיל מחדש:

```powershell
.\.venv\Scripts\python.exe app.py
```

פותחים בדפדפן במחשב:

```text
http://localhost:5000/host
```

ולבדיקת שחקן במחשב:

```text
http://localhost:5000/player
```

אם הכל עובד מקומית, אפשר לעבור לעדכון GitHub.

## עדכון הפרויקט ב-GitHub

ב-GitHub נכנסים ל-repository:

```text
kahoot-bat-mitzva
```

מעדכנים את הקבצים ששונו מתוך `Ver04`.

בדרך כלל הקבצים החשובים יהיו:

```text
app.py
DataQuestions.py
Config.py
requirements.txt
Procfile
templates/
static/
images/
```

לא מעלים:

```text
.venv/
__pycache__/
*.pyc
server.out.log
server.err.log
```

אחרי העלאת הקבצים או עריכה ב-GitHub, לוחצים:

```text
Commit changes
```

## איך לוודא ש-Render מכיר את העדכון

אחרי `Commit changes` ב-GitHub, Render אמור לזהות את השינוי לבד ולהתחיל deploy חדש.

ב-Render נכנסים לשירות:

```text
kahoot-bat-mitzva
```

בודקים בלשונית `Events` או `Logs` שהתחיל deploy חדש.

מחכים עד שרואים הודעה בסגנון:

```text
Deploy live
```

או שהאתר חוזר לעבוד כרגיל.

אם Render לא התחיל לבד, אפשר ללחוץ ידנית:

```text
Manual Deploy
```

ואז:

```text
Deploy latest commit
```

## בדיקת האתר אחרי Render

פותחים את מסך המנחה:

```text
https://kahoot-bat-mitzva.onrender.com/host
```

בודקים שמופיע קוד משחק.

פותחים בטלפון או בדפדפן אחר:

```text
https://kahoot-bat-mitzva.onrender.com/player
```

מכניסים שם וקוד משחק, ובודקים שאפשר להצטרף.

## הערות חשובות

במסלול החינמי של Render האתר יכול להירדם אחרי זמן בלי פעילות.  
לפני משחק אמיתי, לפתוח את מסך המנחה 5-10 דקות מראש כדי להעיר את האתר:

```text
https://kahoot-bat-mitzva.onrender.com/host
```

לא לעדכן קוד בזמן משחק פעיל.  
כל deploy חדש מאפס את מצב המשחק, כי המצב נשמר בזיכרון של השרת.
