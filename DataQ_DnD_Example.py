from Question_Classes import clsAnswer, clsQstn, clsQstnList

# שאלה שבה צבעי התשובות קבועים מראש
DragonColors = clsQstn(
    Qstn="מי מהבאים אינו נחשב לרוב כצבע של דרקון?",
    Answers=[
        clsAnswer(
            Text='צהוב',
            IsCrct=True,
            Color= [0.9, 0.9, 0.1],
        ),
        clsAnswer(
            Text='ירוק',
            IsCrct=False,
            Color= [0.1, 0.8, 0.1],
        ),
        clsAnswer(
            Text='כחול',
            IsCrct=False,
            Color= [0.1, 0.1, 0.9],
        ),
        clsAnswer(
            Text='שחור',
            IsCrct=False,
            Color= [0.0, 0.0, 0.0],
        ),
        clsAnswer(
            Text='אדום',
            IsCrct=False,
            Color= [0.9, 0.1, 0.1],
        ),
        clsAnswer(
            Text='לבן',
            IsCrct=False,
            Color= [0.9, 0.9, 0.9],
        ),                
    ],
)

# שאלה שלה מספר תשובות נכונות
HumanoidTypes = clsQstn(
    Qstn="מי מהבאים נחשב ליצורים הומנואידים?",
    Answers=[
        clsAnswer(
            Text= "אלפים",
            IsCrct=True,
        ),
        clsAnswer(
            Text = "גמדים",
            IsCrct=True,
        ),
        clsAnswer(
            Text="אורקים",
            IsCrct=True,
        ),
        clsAnswer(
            Text= "זומבים",
            IsCrct=False,
        ),
        clsAnswer(
            Text= "טרולים",
            IsCrct=False,
        ),
        clsAnswer(
            Text= "שדים",
            IsCrct=False,
        ),                
    ],
)

# שאלה שסדר התשובות בה חשוב
WybrenDragonFamily = clsQstn(
    Qstn= "מי מהבאים הוא קרוב משפחה של הדרקון",
    Answers=[
        clsAnswer(
            Text="קובולד",
            IsCrct=False,
            MandatoryPosition=1,
        ),
        clsAnswer(
            Text="וויברן",
            IsCrct=False,
            MandatoryPosition=2,
        ),
        clsAnswer(
            Text="טאראסק",
            IsCrct=False,
            MandatoryPosition=3,
        ),
        clsAnswer(
            Text="תשובות א ו-ב נכונות (קובולד וויברן)",
            IsCrct=True,
            MandatoryPosition=4,            
        ),
        clsAnswer(
            Text="תשובות א ו-ג נכונות (קובולד וטראסק)",
            IsCrct=False,
            MandatoryPosition=5,            
        ),
        clsAnswer(
            Text= "כל התשובות נכונות",
            IsCrct=False,
            MandatoryPosition=6,            
        ),                
    ],
)

# שאלה שהתמונה מופיעה מיד
BeholderImgAtQ = clsQstn(
    Qstn="איזו מפלצת מופיעה בתמונה?",
    QuestionImages=["Beholder.jpeg"],
    Answers=[
        clsAnswer(
            Text="בהולדר",
            IsCrct=True,
        ),
        clsAnswer(
            Text="כימרה",
            IsCrct=False,
        ),
        clsAnswer(
            Text="גרגנטואן",
            IsCrct=False,
        ),
        clsAnswer(
            Text= "(דמונייז) שד עיניים",
            IsCrct=False,
        ),
    ],
)

# שאלה שבה כל תשובה כוללת תמונה
WizardQuestion = clsQstn(
    Qstn="מי מהדמויות הבאות עלולה להטיל עליך כדור אש?",
    Answers=[
        clsAnswer(
            Text="קוסם",
            IsCrct=True,
            Image="wizard.jpeg",
        ),
        clsAnswer(
            Text="לוחם",
            IsCrct=False,
            Image="fighter.jpeg",
        ),
        clsAnswer(
            Text="נוכל",
            IsCrct=False,
            Image="rogue.png",
        ),
        clsAnswer(
            Text="כוהן",
            IsCrct=False,
            Image="cleric.jpeg",
        ),
    ],
)

# שאלה שבה תמונה מופיעה בסוף (לאחר חשיפת התשובה)
MimicReveal = clsQstn(
    Qstn="איזה חפץ בחדר הכי מסוכן לפתוח?",
    CorrectImages=["mimic.png"],
    Answers=[
        clsAnswer(
            Text="תיבה שנראית רגילה לגמרי",
            IsCrct=True,
        ),
        clsAnswer(
            Text="דלת עץ פשוטה",
            IsCrct=False,
        ),
        clsAnswer(
            Text="ספר מאובק",
            IsCrct=False,
        ),
        clsAnswer(
            Text="לפיד כבוי",
            IsCrct=False,
        ),
    ],
)


DnD_Example_Quiz = clsQstnList(
    name="דוגמאות D&D",
    questions=[
        DragonColors,
        HumanoidTypes,
        WybrenDragonFamily,
        BeholderImgAtQ,
        WizardQuestion,
        MimicReveal,
    ],
)

questions_lists = {
    "dnd_example": DnD_Example_Quiz,
}

questionnaires = questions_lists
questions_list = next(iter(questions_lists.values())).questions
