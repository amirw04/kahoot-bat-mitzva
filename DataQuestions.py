import Config


class clsQstn:
    def __init__(self, Qstn, AnsT, AnsF, prevQstn=None, Image=None, Timer=None):
        self.Qstn = Qstn
        self.AnsT = AnsT
        self.AnsF = list(AnsF)
        self.prevQstn = prevQstn
        self.Image = Image
        self.Timer = Timer if Timer is not None else Config.TimerDuration


First_Prime_Minister = clsQstn(
    Qstn="מי היה ראש הממשלה הראשון של מדינת ישראל?",
    AnsT="דוד בן גוריון",
    AnsF=["יצחק רבין", "בנימין נתניהו", "אהוד ברק"])

Where_Ben_Gurion_Have_Lived = clsQstn(
    Qstn="באיזה יישוב חי דוד בן גוריון בשנותיו האחרונות?",
    AnsT="קיבוץ שדה בוקר",
    AnsF=["תל אביב", "ירושלים", "חיפה"],
    prevQstn=First_Prime_Minister)

Year_Of_Independence = clsQstn(
    Qstn="באיזו שנה הכריזה מדינת ישראל על עצמאותה?",
    AnsT="1948",
    AnsF=["1945", "1967", "1999"],
)

Capital_Of_Israel = clsQstn(
    Qstn="מהי עיר הבירה של מדינת ישראל?",
    AnsT="ירושלים",
    AnsF=["תל אביב", "חיפה", "באר שבע"],
    prevQstn=Year_Of_Independence,
)

Israeli_Flag_Colors = clsQstn(
    Qstn="מהם הצבעים המרכזיים בדגל ישראל?",
    AnsT="כחול ולבן",
    AnsF=["אדום ולבן", "ירוק ולבן", "שחור וזהב"],
    prevQstn=Capital_Of_Israel,
)

National_Anthem = clsQstn(
    Qstn="מה שם ההמנון הלאומי של מדינת ישראל?",
    AnsT="התקווה",
    AnsF=["ירושלים של זהב", "הבאנו שלום עליכם", "שיר לשלום"],
    prevQstn=Israeli_Flag_Colors,
)

Sea_Near_Tel_Aviv = clsQstn(
    Qstn="איזה ים נמצא ליד תל אביב?",
    AnsT="הים התיכון",
    AnsF=["ים סוף", "ים המלח", "הכנרת"],
    prevQstn=National_Anthem,
)

Lowest_Place = clsQstn(
    Qstn="איזה מקום בישראל ידוע כאחד המקומות הנמוכים בעולם?",
    AnsT="ים המלח",
    AnsF=["הכנרת", "הר חרמון", "מצפה רמון"],
    prevQstn=Sea_Near_Tel_Aviv,
)

Highest_Mountain = clsQstn(
    Qstn="מהו ההר הגבוה בישראל?",
    AnsT="הר חרמון",
    AnsF=["הר תבור", "הר הכרמל", "הר מירון"],
    prevQstn=Lowest_Place,
)

Knesset_City = clsQstn(
    Qstn="באיזו עיר נמצאת הכנסת?",
    AnsT="ירושלים",
    AnsF=["תל אביב", "חיפה", "ראשון לציון"],
    prevQstn=Highest_Mountain,
)

questions_list = [
    First_Prime_Minister,
    Where_Ben_Gurion_Have_Lived,
    Year_Of_Independence,
    Capital_Of_Israel,
    Israeli_Flag_Colors,
    National_Anthem,
    Sea_Near_Tel_Aviv,
    Lowest_Place,
    Highest_Mountain,
    Knesset_City,
]
