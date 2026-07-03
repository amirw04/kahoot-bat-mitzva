import Config


class clsAnswer:
    def __init__(
        self,
        Text,
        IsCrct=None,
        MandatoryPosition=None,
        Color=None,
        Image=None,
        IsCorrect=None,
        mandatoryPosition=None,
        color=None,
        image=None,
    ):
        self.Text = Text
        if IsCrct is None:
            IsCrct = IsCorrect
        self.IsCrct = bool(IsCrct)
        self.IsCorrect = self.IsCrct
        if MandatoryPosition is None:
            MandatoryPosition = mandatoryPosition
        if Color is None:
            Color = color
        if Image is None:
            Image = image
        self.MandatoryPosition = MandatoryPosition
        self.Color = normalize_rgb(Color) if Color is not None else None
        self.Image = Image


class clsQstn:
    def __init__(
        self,
        Qstn,
        AnsT=None,
        AnsF=None,
        Answers=None,
        prevQstn=None,
        Image=None,
        QuestionImages=None,
        CorrectImages=None,
        Timer=None,
        AnswerImages=None,
        AnswerColors=None,
        MandatoryPosition=None,
    ):
        self.Qstn = Qstn
        self.prevQstn = prevQstn
        self.Image = Image
        if QuestionImages is None:
            self.QuestionImages = []
        elif isinstance(QuestionImages, (list, tuple, set)):
            self.QuestionImages = list(QuestionImages)
        else:
            self.QuestionImages = [QuestionImages]
        if CorrectImages is None:
            self.CorrectImages = []
        elif isinstance(CorrectImages, (list, tuple, set)):
            self.CorrectImages = list(CorrectImages)
        else:
            self.CorrectImages = [CorrectImages]
        self.Timer = Timer if Timer is not None else Config.TimerDuration
        self.Answers = normalize_answers(
            Answers=Answers,
            AnsT=AnsT,
            AnsF=AnsF,
            AnswerImages=AnswerImages or {},
            AnswerColors=AnswerColors or {},
            MandatoryPosition=MandatoryPosition or {},
        )
        validate_unique_answer_texts(self.Qstn, self.Answers)
        self.AnsT = [answer.Text for answer in self.Answers if answer.IsCrct]
        if len(self.AnsT) == 1:
            self.AnsT = self.AnsT[0]
        self.AnsF = [answer.Text for answer in self.Answers if not answer.IsCrct]
        self.AnswerImages = {
            answer.Text: answer.Image for answer in self.Answers if answer.Image is not None
        }
        self.AnswerColors = {
            answer.Text: answer.Color for answer in self.Answers if answer.Color is not None
        }
        self.MandatoryPosition = {
            answer.Text: answer.MandatoryPosition
            for answer in self.Answers
            if answer.MandatoryPosition is not None
        }

class clsQstnList:
    def __init__(self, name, questions):
        self.questions = list(questions)
        self.name = name
        validate_questions_order(self.questions)


def normalize_answers(Answers, AnsT, AnsF, AnswerImages, AnswerColors, MandatoryPosition):
    if Answers is not None:
        return [
            answer
            if isinstance(answer, clsAnswer)
            else clsAnswer(**answer)
            for answer in Answers
        ]

    correct_answers = as_list(AnsT)
    false_answers = list(AnsF or [])
    answers = []

    for text in correct_answers:
        answers.append(
            clsAnswer(
                Text=text,
                IsCrct=True,
                MandatoryPosition=MandatoryPosition.get(text),
                Color=AnswerColors.get(text),
                Image=AnswerImages.get(text),
            )
        )

    for text in false_answers:
        answers.append(
            clsAnswer(
                Text=text,
                IsCrct=False,
                MandatoryPosition=MandatoryPosition.get(text),
                Color=AnswerColors.get(text),
                Image=AnswerImages.get(text),
            )
        )

    return answers


def validate_unique_answer_texts(question_text, answers):
    seen = set()
    for answer in answers:
        if answer.Text in seen:
            raise ValueError(
                f"Duplicate answer text in question '{question_text}': '{answer.Text}'. "
                "Each answer must have unique text so images, colors, and scoring can be matched."
            )
        seen.add(answer.Text)


def as_list(value):
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return list(value)
    return [value]


def normalize_rgb(color):
    if len(color) != 3:
        raise ValueError("Answer color must have exactly 3 RGB values.")

    rgb = []
    for value in color:
        number = float(value)
        if number < 0 or number > 1:
            raise ValueError("Answer color must use values between 0 and 1.")
        rgb.append(number)

    return rgb

        
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
