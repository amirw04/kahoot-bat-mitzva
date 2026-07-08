from Question_Classes import clsAnswer, clsQstn, clsQstnList


Kama_Netas_Best_Freind = clsQstn(
    Qstn='איך קוראים לחברה הטובה ביותר של נטע',
    Answers=[
        clsAnswer(
            Text='קמה',
            IsCrct=True,
        ),
        clsAnswer(
            Text='מורן',
            IsCrct=False,
        ),
        clsAnswer(
            Text='נטלי',
            IsCrct=False,
        ),
        clsAnswer(
            Text='עלמה',
            IsCrct=False,
        ),
    ],
)

ShuinGruin_Imaginary_Freind = clsQstn(
    Qstn='מה היה שמה של החברה הדמיונית של איילה?',
    Answers=[
        clsAnswer(
            Text='שואין גרואין',
            IsCrct=True,
        ),
        clsAnswer(
            Text='אלזה',
            IsCrct=False,
        ),
        clsAnswer(
            Text='לבבית',
            IsCrct=False,
        ),
        clsAnswer(
            Text="מיראבלה ג'יגלברוקס",
            IsCrct=False,
        ),
    ],
    prevQstn=Kama_Netas_Best_Freind,
)

ShuinGruins_Family = clsQstn(
    Qstn='ומי מהבאים לא היה בן משפחתה של שואין גרואין?',
    Answers=[
        clsAnswer(
            Text='פלוטו כלבלב מקיבוץ מגידו',
            IsCrct=True,
        ),
        clsAnswer(
            Text='לבבית',
            IsCrct=False,
        ),
        clsAnswer(
            Text='כוכבית',
            IsCrct=False,
        ),
        clsAnswer(
            Text='אלוהים',
            IsCrct=False,
        ),
    ],
    prevQstn=ShuinGruin_Imaginary_Freind,
)

ShuinGruins_House = clsQstn(
    Qstn='ואיך נראה הבית שלה?',
    CorrectImages=["Shuin_Gruins_House.jpg"],
    Answers=[
        clsAnswer(
            Text='על עץ, עם מדרגות מסתובבות',
            IsCrct=True,
            Color = [0.0, 0.7, 0.0], 
        ),
        clsAnswer(
            Text='כמו תחנת הרכבת בפרדס חנה',
            IsCrct=False,
            Color = [0.7, 0.7, 0.7],
        ),
        clsAnswer(
            Text='ארמון גדול הבנוי בקרח',
            IsCrct=False,
            Color = [0.2, 0.7, 1.0],
        ),
        clsAnswer(
            Text='מערת נטיפים שבתוכה טירה ענקית',
            IsCrct=False,
            Color = [0.2, 0.2, 0.3],
        ),
    ],
    prevQstn=ShuinGruins_Family,
)

Persi_Jackson = clsQstn(
    Qstn='מה הקשר בין איילה לפרסאוס',
    CorrectImages=["Persi_Jackson.jpg"],
    Answers=[
        clsAnswer(
            Text="פרסאוס הוא 'פרסי ג'קסון' - גיבור סדרת ספרים שאיילה אוהבת לקרוא.",
            IsCrct=True,
        ),
        clsAnswer(
            Text='פרסאוס הוא שמו של החתול של מאיה קראסיק.',
            IsCrct=False,
        ),
        clsAnswer(
            Text='פרסאוס הוא שמו של הרובוט שאיילה בנתה בחוג הרובטיקה.',
            IsCrct=False,
        ),
        clsAnswer(
            Text='פרסאוס הוא גיבור סרט מצוייר, שאיילה רואה שוב... ושוב... ושוב....',
            IsCrct=False,
        ),
    ],
)

Who_is_Green_Monster = clsQstn(
    Qstn='מי מהבאות היא "מפלצת ירוקה"',
    Answers=[
        clsAnswer(
            MandatoryPosition=1,
            Color=[0.4, 0.6, 0.7],
            Image=["Hau_Hau.jpg"],
            Text='תמונה 1',
            IsCrct=False,
        ),
        clsAnswer(
            MandatoryPosition=2,
            Color=[0.4, 0.6, 0.7],
            Image=["Green_Monster_True.jpg"],
            Text='תמונה 2',
            IsCrct=True,
        ),
        clsAnswer(
            MandatoryPosition=3,
            Color=[0.4, 0.6, 0.7],
            Image=["Green_Monster_False.jpg"],
            Text='תמונה 3',
            IsCrct=False,
        ),
        clsAnswer(
            MandatoryPosition=4,
            Color=[0.4, 0.6, 0.7],
            Image=["GaGa.jpg"],
            Text='תמונה 4',
            IsCrct=False,
        ),
    ],
)

Adi_GreenMonsters_Freind = clsQstn(
    Qstn='ומה שמה של חברתה הקרובה ביותר',
    Answers=[
        clsAnswer(
            Image=["Adi.jpg"],
            Text='עדי',
            IsCrct=True,
        ),
        clsAnswer(
            Image=["Zelig.jpg"],
            Text='זליג',
            IsCrct=False,
        ),
        clsAnswer(
            Image=["Rikko.jpg"],
            Text='עכברונת',
            IsCrct=False,
        ),
        clsAnswer(
            Image=["Muff_Muff.jpg"],
            Text='מוף-מופונת',
            IsCrct=False,
        ),
    ],
    prevQstn=Who_is_Green_Monster,
)

Ayalas_Long_Lived_Dress = clsQstn(
    Qstn='במה מפורסמת השמלה הבאה',
    QuestionImages=["AyalaDressA.JPG"],
    Answers=[
        clsAnswer(
            Text='השמלה שימשה את איילה משך שנים רבות - הרבה מעבר למה שמתאים.....',
            IsCrct=True,
        ),
        clsAnswer(
            Text='שמלה שסבתא רותי תפרה בשביל איילה ליום ההולדת 3.',
            IsCrct=False,
        ),
        clsAnswer(
            Text='שמלה שאיילה, קיבלה במתנה מעלמה, החברה מגן יקינטון, כשעברנו להר חלוץ.',
            IsCrct=False,
        ),
        clsAnswer(
            Text='"שמלת המריבות" - שנטע ואיילה נלחמו עליה בכל פעם שיצאה מהכביסה.',
            IsCrct=False,
        ),
    ],
)

What_Neta_Dress_Age_4 = clsQstn(
    Qstn='נטע בת שלוש - מה הגיוני שתלבש',
    CorrectImages=["Neta_Yellow.jpg"],
    Answers=[
        clsAnswer(
            Text='שמלה צהובה, המון סיכות ראש וגרביים שחור לבן.',
            IsCrct=True,
            Color=[1.0, 0.9, 0.0],
        ),
        clsAnswer(
            Text='שמלת תכלת מתנפנפת וקשת עם צבעי קשת בענן.',
            IsCrct=False,
            Color=[0.0, 0.5, 1.0],
        ),
        clsAnswer(
            Text='חולצה ורודה, סווטשירט ורוד גרביים ורודים ונעליים ורודות מבריקות.',
            IsCrct=False,
            Color=[1.0, 0.4, 0.8],
        ),
        clsAnswer(
            Text="פיג'מה של דינוזאור",
            IsCrct=False,
            Color=[0.3, 0.5, 0.2],
        ),
    ],
    prevQstn=Ayalas_Long_Lived_Dress,
)

Ayalas_Favors_Cats = clsQstn(
    Qstn='מה החיה האהובה ביותר על איילה?',
    Answers=[
        clsAnswer(
            Text='חתולים.',
            IsCrct=True,
        ),
        clsAnswer(
            Text='שועלים.',
            IsCrct=False,
        ),
        clsAnswer(
            Text='קפיבארות.',
            IsCrct=False,
        ),
        clsAnswer(
            Text='ציפורי שיר.',
            IsCrct=False,
        ),
    ],
)

Ayala_was_a_Cat = clsQstn(
    Qstn='בעברה הייתה איילה חתול - איזה חתול?',
    CorrectImages=["GingerCat.jpg"],
    Answers=[
        clsAnswer(
            Text= "תשובות 1 ו-3 (ג'ינג'י וסגול) נכונות",
            IsCrct=True,
            MandatoryPosition=4,
            Color=[1.0, 0.0, 0.0],
        ),
        clsAnswer(
            Text='סגול יותר ממה שחושבים....',
            IsCrct=False,
            MandatoryPosition=1,
            Color=[0.7, 0.0, 1.0],
        ),
        clsAnswer(
            Text="ג'ינג'י",
            IsCrct=False,
            MandatoryPosition=3,
            Color=[1.0, 0.5, 0.0],
        ),
        clsAnswer(
            Text='אפור מפוספס',
            IsCrct=False,
            MandatoryPosition=2,
            Color=[0.7, 0.72, 0.75],
        ),
    ],
    prevQstn=Ayalas_Favors_Cats,
)

Achbary_Place_to_Sit = clsQstn(
    Qstn='מה עכברי (כלומר נטע עד גיל מסויים) יודע לעשות?',
    Answers=[
        clsAnswer(
            Text='למצוא פינות להפסקה בזמן טיולים.',
            IsCrct=True,
            Color=[0.0, 0.7, 0.2],
        ),
        clsAnswer(
            Text='להריח אוכל מהמקרר ולוודא שהוא לא מקולקל.',
            IsCrct=False,
            Color=[0.6, 0.6, 0.5],
        ),
        clsAnswer(
            Text='לאכול כמויות גדולות של גבינה צהובה.',
            IsCrct=False,
            Color=[1.0, 1.0, 0.0],
        ),
        clsAnswer(
            Text='להתחבא בפינות מוזרות בבית.',
            IsCrct=False,
            Color=[0.2, 0.2, 0.2],
        ),
    ],
)

Ayala_Corona_Mask = clsQstn(
    Qstn='איך לדעתה של איילה ראוי לחבוש מסכת קורונה',
    Answers=[
        clsAnswer(
            Text='על הסנטר, כך קל יותר לנשום!',
            IsCrct=True,
        ),
        clsAnswer(
            Text='בהתאם להנחיות המורה ומשרד הבריאות!',
            IsCrct=False,
        ),
        clsAnswer(
            Text='לא צריך ללבוש מסכת קורונה - זה לא נעים...',
            IsCrct=False,
        ),
        clsAnswer(
            Text='בכיס של הילקוט',
            IsCrct=False,
        ),
    ],
)

Gaga_Dipers = clsQstn(
    Qstn='?מה זה גגה',
    CorrectImages=["Gaga_Dipper.jpg", "GaGa.jpg"],
    Answers=[
        clsAnswer(
            Text='חיתול עם ציור של דג.',
            IsCrct=True,
        ),
        clsAnswer(
            Text='הדרך בה נטע ביקשה לשמוע שיר של ליידי גגה.',
            IsCrct=False,
        ),
        clsAnswer(
            Text='חברה מגן גלגול (גאיה לדעתם של ההורים שלה).',
            IsCrct=False,
        ),
        clsAnswer(
            Text='ארנב (אל תשאלו אותנו...)',
            IsCrct=False,
        ),
    ],
)

Six_on_the_Dice = clsQstn(
    Qstn='לאיילה יש מצב שמכונה "שש בקוביה" - מה מהדברים הבאים לא קרה במסגרתו?',
    Answers=[
        clsAnswer(
            Text="ניסתה להרים מדוזה",
            IsCrct=True,
            Color=[0.9, 0.9, 0.8]
        ),    
        clsAnswer(
            Text="ליטפה זברה דרך חלון האוטו בספארי",
            IsCrct=False,
            Color=[0.4, 0.4, 0.4]
        ),
        clsAnswer(
            Text='הקפיצה את כיתת הכוננות של הישוב.',
            IsCrct=False,
            Color=[0.3, 0.5, 0.2]
        ),
        clsAnswer(
            Text='נגעה בסרפד כי "הפרח נראה נעים".',
            IsCrct=False,
            Color=[0.0, 1.0, 0.0]
        ),
        clsAnswer(
            Text='גזרה לעצמה את הגבה.',
            IsCrct=False,
            Color=[0.3, 0.3, 0.1]
        ),
        clsAnswer(
            Text='פינתה שולחן באמצעות השלכת צלחת לכיור.',
            IsCrct=False,
            Color=[0.8, 0.8, 0.8]
        ),
        clsAnswer(
            Text='נגעה בבועה של דבק חם וקיבלה כוויה.',
            IsCrct=False,
            Color=[1.0, 1.0, 0.6]
        ),
        clsAnswer(
            Text='הלכה לאיבוד בגיל שנתיים, ובנונשלנטיות, מצאה מישהי שתעזור לה.',
            IsCrct=False,
            Color=[0.0, 0.0, 0.0]
        ),
        clsAnswer(
            Text="הפרידה את האוכל בקערה של יסמין (החתולה)  לפי הצבעים השונים.",
            IsCrct=False,
            Color=[1.0, 0.4, 0.0]
        ),        
        clsAnswer(
            Text='קפצה לבריכת מים כי "הדגים קראו לה".',
            IsCrct=False,
            Color=[0.4, 0.6, 0.7]
        ),
    ],
)

Neta_Hard_Life_Sivling = clsQstn(
    Qstn='מה קשה בלהיות אחות של איילה ועומר?',
    Answers=[
        clsAnswer(
            Text='כל התשובות נכונות',
            IsCrct=True,
            MandatoryPosition=4,
        ),
        clsAnswer(
            Text='לא אוהבים סרטים מפחידים, ודברים שהם לא מכירים, ודברים שהם לא מצויירים!',
            IsCrct=False,
            MandatoryPosition=1,
        ),
        clsAnswer(
            Text='תמיד צריך לסדר הכל לבד - לא כי הם לא רוצים - אלא כי הם לא יעילים!',
            IsCrct=False,
            MandatoryPosition=2,
        ),
        clsAnswer(
            Text='בגלל שעומר קטן ואיילה עייפה - אי אפשר לראות תוכניות עד מאוחר',
            IsCrct=False,
            MandatoryPosition=3,
        ),
    ],
)

Neta_and_Granma_Cook = clsQstn(
    Qstn='מה נטע הכי אוהבת לעשות עם הסבתות',
    Answers=[
        clsAnswer(
            Text='לבשל',
            IsCrct=True,
        ),
        clsAnswer(
            Text='לעבוד בגינה.',
            IsCrct=False,
        ),
        clsAnswer(
            Text='לשחק במחשב.',
            IsCrct=False,
        ),
        clsAnswer(
            Text='לרכל ולקשקש.',
            IsCrct=False,
        ),
    ],
)

Favorate_Podcast_Is = clsQstn(
    Qstn='מה הפודקאסט האהוב על נטע ואיילה (ועומר)?',
    Answers=[
        clsAnswer(
            Text='התשובה - דורון פישלר',
            IsCrct=True,
        ),
        clsAnswer(
            Text='המעבדה לילדות וילדים - כאן',
            IsCrct=False,
        ),
        clsAnswer(
            Text='היסטוריה עם יובל מלחי - יובל מלחי',
            IsCrct=False,
        ),
        clsAnswer(
            Text='עושים חלל - רשת "עושים היסטוריה"',
            IsCrct=False,
        ),
    ],
)

Gragamel_Menora = clsQstn(
    CorrectImages=["Gargamel.jpg"],
    Qstn='באיזה הקשר נטע, איילה ועומר אוזכרו בפודקאסט',
    Answers=[
        clsAnswer(
            Text='הן שמצאו את החנוכיה של גרגמל.',
            IsCrct=True,
            MandatoryPosition=3,
        ),
        clsAnswer(
            Text='בפרק על הדרקונים, הם אוזכרו כשואלות.',
            IsCrct=False,
            MandatoryPosition=2,
        ),
        clsAnswer(
            Text='בפרק מוקלט עם ילדים, הם שוחחו עם דורון פישלר.',
            IsCrct=False,
            MandatoryPosition=1,
        ),
        clsAnswer(
            Text='הן לא אוזכרו בו עדיין - אבל - עוד יבוא היום....',
            IsCrct=False,
            MandatoryPosition=4,
        ),
    ],
    prevQstn=Favorate_Podcast_Is,
)

Amaris_and_Lili = clsQstn(
    Qstn='מיהן "אמאריס ולילי"?',
    CorrectImages=["DnD_Party_Fix.png"],
    Answers=[
        clsAnswer(
            Text='דמויות ה-D&D של נטע ואיילה.',
            IsCrct=True,
        ),
        clsAnswer(
            Text='דמויות מסדרה מצויירת טיפשית שנטע ואיילה ראו שוב.... ושוב.... ושוב....',
            IsCrct=False,
        ),
        clsAnswer(
            Text='שמות של שתיים מהבובות המיתולוגיות שלהן.',
            IsCrct=False,
        ),
        clsAnswer(
            Text='חברות מגן יקינטון (כן - הייתה ילדה בשם אמאריס!)',
            IsCrct=False,
        ),
    ],
)

Ain_and_Kleps = clsQstn(
    Qstn='ומיהם "עין וקלפס"',
    CorrectImages=["AinKleps3.JPG"],
    Answers=[
        clsAnswer(
            Text='נטע ואיילה בנות 4, רק כשהן רוכבות על אופני איזון!',
            IsCrct=True,
            MandatoryPosition=3,
        ),
        clsAnswer(
            Text='שני הנבלים הגדולים מהקמפיין....',
            IsCrct=False,
            MandatoryPosition=1,
        ),
        clsAnswer(
            Text='שוב, בובות - אף אחד כבר לא זוכר מי.',
            IsCrct=False,
            MandatoryPosition=2,
        ),
        clsAnswer(
            Text='כינוי בעלי בורקסייה בכרמיאל (נקראת על שמם) בה קונים בכל שישי בבוקר.',
            IsCrct=False,
            MandatoryPosition=4,
        ),
    ],
    prevQstn=Amaris_and_Lili,
)

Neta_Prays_to_God = clsQstn(
    Qstn='למה התפללה נטע אל האלים....',
    Answers=[
        clsAnswer(
            Text='"תעשו שאני אהיה מלצרית..."',
            IsCrct=True,
            mandatoryPosition=1,
        ),
        clsAnswer(
            Text='"אני רוצה אופניים בכל צבעי הקשת!"',
            IsCrct=False,
            mandatoryPosition=2,
        ),
        clsAnswer(
            Text='"תעשו שאני אמלוך על כל העולם וכולם יעשו מה שאני רוצה"',
            IsCrct=False,
            mandatoryPosition=3,
        ),
        clsAnswer(
            Text='כל התשובות נכונות',
            IsCrct=False,
            mandatoryPosition=4,
        ),
    ],
)

Neta_Sport_Hoogs = clsQstn(
    Qstn='מה מהבאים אינו חוג של נטע',
    Answers=[
        clsAnswer(
            Text='כדורסל',
            IsCrct=True,
        ),
        clsAnswer(
            Text='טניס',
            IsCrct=False,
        ),
        clsAnswer(
            Text='קפוארה',
            IsCrct=False,
        ),
        clsAnswer(
            Text='ציור',
            IsCrct=False,
        ),
    ],
)

Generated_Quiz = clsQstnList(
    name='חידון יום ההולדת של הבנות',
    questions=[
        Neta_and_Granma_Cook,           
        Neta_Sport_Hoogs,        
        Kama_Netas_Best_Freind,     
        ShuinGruin_Imaginary_Freind,
        ShuinGruins_Family,
        ShuinGruins_House,        
        Who_is_Green_Monster,
        Adi_GreenMonsters_Freind,
        Persi_Jackson,        
        Neta_Hard_Life_Sivling,
        Ayalas_Long_Lived_Dress,
        What_Neta_Dress_Age_4,
        Ayalas_Favors_Cats,
        Ayala_was_a_Cat,
        Achbary_Place_to_Sit,
        Neta_Prays_to_God,
        Ayala_Corona_Mask,
        Gaga_Dipers,
        Six_on_the_Dice,
        Favorate_Podcast_Is,
        Gragamel_Menora,
        Amaris_and_Lili,
        Ain_and_Kleps,
    ],
)

questions_lists = {
    'Questions_Bat_Mitzva': Generated_Quiz,
}

questionnaires = questions_lists
questions_list = next(iter(questions_lists.values())).questions
