import Config


class clsQstn:
    def __init__(
        self,
        Qstn,
        AnsT,
        AnsF,
        prevQstn=None,
        Image=None,
        QuestionImages=None,
        Timer=None,
        AnswerImages=None,
        MandatoryPosition=None,
    ):
        self.Qstn = Qstn
        self.AnsT = AnsT
        self.AnsF = list(AnsF)
        self.prevQstn = prevQstn
        self.Image = Image
        if QuestionImages is None:
            self.QuestionImages = []
        elif isinstance(QuestionImages, (list, tuple, set)):
            self.QuestionImages = list(QuestionImages)
        else:
            self.QuestionImages = [QuestionImages]
        self.Timer = Timer if Timer is not None else Config.TimerDuration
        self.AnswerImages = AnswerImages or {}
        self.MandatoryPosition = MandatoryPosition or {}

class clsQstnList:
    def __init__(self, name, questions):
        self.questions = list(questions)
        self.name = name
        validate_questions_order(self.questions)

def validate_questions_order(questions):
    active_questions = set(questions)

    for index, question in enumerate(questions):
        if question.prevQstn is None:
            continue

        # Ignore constraints that point to questions outside the active game list.
        if question.prevQstn not in active_questions:
            continue

        previous_question = questions[index - 1] if index > 0 else None
        if previous_question is question.prevQstn:
            continue

        raise ValueError(
            "Question order error: "
            f"'{question.Qstn}' must appear immediately after "
            f"'{question.prevQstn.Qstn}'."
        )

# Queastions Definitions

First_Prime_Minister = clsQstn(
    Qstn="מי היה ראש הממשלה הראשון של מדינת ישראל?",
    AnsT="דוד בן גוריון",
    AnsF=["יצחק רבין", "בנימין נתניהו", "מנחם בגין"],)

Where_Ben_Gurion_Have_Lived = clsQstn(
    Qstn="באיזה יישוב חי דוד בן גוריון בשנותיו האחרונות?",
    AnsT="קיבוץ שדה בוקר",
    AnsF=["תל אביב", "ירושלים", "חיפה"],
    prevQstn=First_Prime_Minister)

Year_Of_Independence = clsQstn(
    Qstn="באיזו שנה הכריזה מדינת ישראל על עצמאותה?",
    AnsT="1948",
    AnsF=["1945", "1967", "1999"],)

Wars_Years = clsQstn(
    Qstn="באיזו שנה היתה מלחמה בישראל?",
    AnsT="כל התשובות נכונות",
    AnsF=["1948", "1967", "1973", "1982", "2006"],
    MandatoryPosition={
        "1948": 1,
        "1967": 2,
        "1973": 3,
        "1982": 4,
        "2006": 5,
        "כל התשובות נכונות": 6,
    },)

YomKipurWar = clsQstn(
    Qstn="מתי פרצה מלחמת יום הכיפורים?",
    AnsT="אוקטובר 1973",
    AnsF=["יוני 1967", "מאי 1948", "יוני 1982"],
    MandatoryPosition={
        "מאי 1948": 1,
        "יוני 1967": 2,
        "אוקטובר 1973": 3,
        "יוני 1982": 4,
    },    
)

SixDaysWar = clsQstn(
    Qstn="ומלחמת ששת הימים?",
    AnsT="יוני 1967",
    AnsF=["אוקטובר 1973", "מאי 1948", "יוני 1982"],
    prevQstn=YomKipurWar,
    MandatoryPosition={
        "מאי 1948": 1,
        "יוני 1967": 2,
        "אוקטובר 1973": 3,
        "יוני 1982": 4,
    },    
)

GolanOcupation = clsQstn(
    Qstn="באיזו מלחמה נכבשה רמת הגולן",
    AnsT="מלחמת ששת הימים",
    AnsF=["מבצע סיני", "מלחמת יום הכיפורים", "מלחמת לבנון הראשונה"],
)

Israeli_Prime_Ministers = clsQstn(
    Qstn= "מי מהבאים לא היה ראש ממשלה של מדינת ישראל?",
    AnsT="משה דיין",
    AnsF=["לוי אשכול", "דוד בן גוריון", "אהוד אולמרט"],
    AnswerImages={
        "משה דיין": "Dayan.png",
        "לוי אשכול": "Eshcol.jpeg",
        "דוד בן גוריון": "BenGurion.jpeg",
        "אהוד אולמרט": "Olmert.jpeg",
    },
)

Capital_Of_Israel = clsQstn(
    Qstn="מהי עיר הבירה של מדינת ישראל?",
    AnsT="ירושלים",
    AnsF=["תל אביב", "חיפה", "באר שבע"],
)

Israeli_Flag_Colors = clsQstn(
    Qstn="איזה צבעים מופיעים בדגל ישראל?",
    AnsT=["כחול", "לבן"],
    AnsF=["ירוק", "אדום", "שחור"],
)

National_Anthem = clsQstn(
    Qstn="מה שם ההמנון הלאומי של מדינת ישראל?",
    AnsT="התקווה",
    AnsF=["ירושלים של זהב", "הבאנו שלום עליכם", "תותים"], 
    prevQstn=Israeli_Flag_Colors,
)

Sea_Near_Tel_Aviv = clsQstn(
    Qstn="איזה ים נמצא ליד תל אביב?",
    AnsT="הים התיכון",
    AnsF=["ים סוף", "ים המלח", "הכנרת"],
)

Lowest_Place = clsQstn(
    Qstn="איזה מקום בישראל ידוע כאחד המקומות הנמוכים בעולם?",
    AnsT="ים המלח",
    AnsF=["הכנרת", "הר חרמון", "מצפה רמון"],
)

Highest_Mountain = clsQstn(
    Qstn="מהו ההר הגבוה בישראל?",
    AnsT="הר חרמון",
    AnsF=["הר תבור", "הר הכרמל", "הר מירון"],
    prevQstn=Lowest_Place,
    QuestionImages=["Hermon1.jpeg", "Hermon2.jpeg"],
)

Knesset_City = clsQstn(
    Qstn="באיזו עיר נמצאת הכנסת?",
    AnsT="ירושלים",
    AnsF=["תל אביב", "חיפה", "ראשון לציון"],
)


# Qustions Lists

Prime_Ministers = clsQstnList(
    name="ראשי ממשלה",
    questions=[
        First_Prime_Minister,
        Where_Ben_Gurion_Have_Lived,
        Israeli_Prime_Ministers,
    ])

Wars_Quiz = clsQstnList(
    name="מלחמות",
    questions=[
        Wars_Years,
        GolanOcupation,
        YomKipurWar,
        SixDaysWar,
    ])

National_Symbols = clsQstnList(
    name="סמלים לאומיים",
    questions=[
        Capital_Of_Israel,
        Israeli_Flag_Colors,
        National_Anthem,
        Knesset_City,
    ])

Israeli_Geography = clsQstnList(
    name="גאוגרפיה",
    questions=[
        Capital_Of_Israel,
        Sea_Near_Tel_Aviv,
        Lowest_Place,
        Highest_Mountain,
    ])  

questions_lists = {
    "prime_ministers": Prime_Ministers,
    "wars": Wars_Quiz,
    "national_symbols": National_Symbols,
    "geography": Israeli_Geography,
}

questionnaires = questions_lists
questions_list = next(iter(questions_lists.values())).questions
