import keyword
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from pprint import pformat


MD_FILE = "Questions_Bat_Mitzva.md"
OUTPUT_FILE = None
QUESTIONNAIRE_NAME = "חידון יום ההולדת של הבנות"

QUESTION_NAME_OVERRIDES = {
    "איך קוראים לחברה הטובה ביותר של נטע": "Kama_Netas_Best_Freind",
    "מה היה שמה של החברה הדמיונית של איילה?": "ShuinGruin_Imaginary_Freind",
    "ומי מהבאים לא היה בן משפחתה של שואין גרואין?": "ShuinGruins_Family",
    "ואיך נראה הבית שלה?": "ShuinGruins_House",
    "מה הקשר בין איילה לפרסאוס": "Persi_Jackson",
    'מי מהבאות היא "מפלצת ירוקה"': "Who_is_Green_Monster",
    "ומה שמה של חברתה הקרובה ביותר": "Adi_GreenMonsters_Freind",
    "במה מפורסמת השמלה הבאה": "Ayalas_Long_Lived_Dress",
    "נטע בת שלוש - מה הגיוני שתלבש": "What_Neta_Dress_Age_4",
    "מה החיה האהובה ביותר על איילה?": "Ayalas_Favors_Cats",
    "בעברה הייתה איילה חתול - איזה חתול?": "Ayala_was_a_Cat",
    "מה עכברי (כלומר נטע עד גיל מסויים) יודע לעשות?": "Achbary_Place_to_Sit",
    "איך לדעתה של איילה ראוי לחבוש מסכת קורונה": "Ayala_Corona_Mask",
    "מה זה גגה": "Gaga_Dipers",
}


@dataclass
class ParsedQuestion:
    title: str
    correct_answers: list[str] = field(default_factory=list)
    false_answers: list[str] = field(default_factory=list)
    prev_title: str | None = None
    question_images: list[str] = field(default_factory=list)
    correct_images: list[str] = field(default_factory=list)
    answer_images: dict[str, str] = field(default_factory=dict)
    answer_colors: dict[str, list[float]] = field(default_factory=dict)
    mandatory_position: dict[str, int] = field(default_factory=dict)
    timer: int | None = None


SECTION_ALIASES = {
    "correct": ("תשובות נכונות", "תשובה נכונה"),
    "false": ("תשובות שגויות", "תשובה שגויה", "מסיחים"),
    "prev": ("חייב לבוא אחרי", "חייבת לבוא אחרי", "אחרי"),
    "question_images": ("תמונות שאלה", "תמונת שאלה", "תמונה לשאלה"),
    "correct_images": (
        "תמונות תשובה נכונה",
        "תמונת תשובה נכונה",
        "תמונות בסוף",
        "תמונה בסוף",
        "תמונות אחרי תשובה נכונה",
        "תמונה אחרי תשובה נכונה",
    ),
    "answer_images": ("תמונות תשובות", "תמונות לתשובות", "תמונת תשובה"),
    "answer_colors": ("צבעי תשובות", "צבעים לתשובות", "צבע תשובה"),
    "timer": ("טיימר", "זמן", "זמן לשאלה"),
}


def normalize_heading(value):
    value = value.strip()
    value = value.rstrip(":")
    return re.sub(r"\s+", " ", value)


def section_key(heading):
    normalized = normalize_heading(heading)
    for key, aliases in SECTION_ALIASES.items():
        if any(normalized.startswith(alias) for alias in aliases):
            return key
    return None


def clean_bullet(line):
    return re.sub(r"^\s*[-*]\s+", "", line).strip()


def split_inline_metadata(value):
    metadata = []

    def collect(match):
        item = match.group(1).strip()
        if is_inline_metadata(item):
            metadata.append(item)
            return ""
        return match.group(0)

    text = re.sub(r"\(([^()]*)\)", collect, value).strip()
    text = re.sub(r"\s+", " ", text)
    return text, metadata


def is_inline_metadata(value):
    return bool(
        re.search(r"סדר\s+כפוי\s*-\s*\d+", value)
        or re.search(r"צבע\s*[-:=]\s*", value)
    )


def extract_mandatory_position(metadata):
    for item in metadata:
        match = re.search(r"סדר\s+כפוי\s*-\s*(\d+)", item)
        if match:
            return int(match.group(1))
    return None


def extract_answer_color(metadata):
    for item in metadata:
        match = re.search(r"צבע\s*[-:=]\s*(.+)$", item)
        if match:
            return parse_rgb(match.group(1))
    return None


def extract_prev_title(value):
    match = re.search(r"\[\[#([^\]]+)\]\]", value)
    if match:
        return normalize_heading(match.group(1))
    return normalize_heading(value) if value else None


def parse_answer_image(value):
    if ":" in value:
        answer, image_name = value.split(":", 1)
    elif "=" in value:
        answer, image_name = value.split("=", 1)
    else:
        return None, value.strip()
    return answer.strip(), image_name.strip()


def parse_answer_color(value):
    if ":" in value:
        answer, color = value.split(":", 1)
    elif "=" in value:
        answer, color = value.split("=", 1)
    else:
        return None, parse_rgb(value)
    return answer.strip(), parse_rgb(color)


def parse_rgb(value):
    numbers = re.findall(r"\d+(?:\.\d+)?", value)
    if len(numbers) != 3:
        raise ValueError(f"RGB color must have exactly 3 values: {value}")

    rgb = [float(number) for number in numbers]
    if any(number < 0 or number > 1 for number in rgb):
        raise ValueError(f"RGB color values must be between 0 and 1: {value}")
    return rgb


def parse_timer(value):
    match = re.search(r"\d+", value)
    return int(match.group(0)) if match else None


def parse_md(md_path):
    questions = []
    current = None
    current_section = None
    pending_prev = False

    for raw_line in md_path.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line:
            continue

        question_match = re.match(r"^###\s+(?!#)(.+)$", line)
        if question_match:
            current = ParsedQuestion(title=normalize_heading(question_match.group(1)))
            questions.append(current)
            current_section = None
            pending_prev = False
            continue

        if current is None:
            continue

        section_match = re.match(r"^####\s+(.+)$", line)
        if section_match:
            current_section = section_key(section_match.group(1))
            pending_prev = current_section == "prev"
            inline_value = section_match.group(1).split(":", 1)[1].strip() if ":" in section_match.group(1) else ""
            if inline_value:
                apply_section_value(current, current_section, inline_value)
                pending_prev = False
            continue

        if pending_prev and line.startswith("[[#"):
            current.prev_title = extract_prev_title(line)
            pending_prev = False
            continue

        if not line.startswith(("-", "*")):
            continue

        value = clean_bullet(line)
        apply_section_value(current, current_section, value)

    return questions


def apply_section_value(question, section, value):
    if not section:
        return

    if section == "prev":
        question.prev_title = extract_prev_title(value)
        return

    if section == "timer":
        timer = parse_timer(value)
        if timer is not None:
            question.timer = timer
        return

    if section == "question_images":
        question.question_images.append(value)
        return

    if section == "correct_images":
        question.correct_images.append(value)
        return

    if section == "answer_images":
        answer, image_name = parse_answer_image(value)
        if answer:
            question.answer_images[answer] = image_name
        return

    if section == "answer_colors":
        answer, color = parse_answer_color(value)
        if answer:
            question.answer_colors[answer] = color
        return

    answer_text, metadata = split_inline_metadata(value)
    if not answer_text:
        return

    position = extract_mandatory_position(metadata)
    if position is not None:
        question.mandatory_position[answer_text] = position

    color = extract_answer_color(metadata)
    if color is not None:
        question.answer_colors[answer_text] = color

    if section == "correct":
        question.correct_answers.append(answer_text)
    elif section == "false":
        question.false_answers.append(answer_text)


def make_identifier(text, used):
    override = QUESTION_NAME_OVERRIDES.get(text)
    if override and override not in used:
        used.add(override)
        return override

    words = re.findall(r"[A-Za-z0-9]+", text)
    if words:
        base = "_".join(words)
    else:
        base = "Q_" + str(len(used) + 1)
    base = re.sub(r"\W+", "_", base).strip("_") or "Question"
    if base[0].isdigit():
        base = "Q_" + base
    if keyword.iskeyword(base):
        base += "_"

    candidate = base
    suffix = 2
    while candidate in used:
        candidate = f"{base}_{suffix}"
        suffix += 1
    used.add(candidate)
    return candidate


def py_value(value):
    return pformat(value, width=100, sort_dicts=False)


def write_question(out, name, question, title_to_name, warnings):
    out.append(f"{name} = clsQstn(")
    out.append(f"    Qstn={py_value(question.title)},")
    out.append("    Answers=[")
    for answer_text in question.correct_answers:
        write_answer(out, answer_text, True, question)
    for answer_text in question.false_answers:
        write_answer(out, answer_text, False, question)
    out.append("    ],")

    if question.prev_title:
        prev_name = title_to_name.get(question.prev_title)
        if prev_name:
            out.append(f"    prevQstn={prev_name},")
        else:
            warnings.append(f"Previous question was not found: {question.title} -> {question.prev_title}")

    if question.question_images:
        out.append(f"    QuestionImages={py_value(question.question_images)},")
    if question.correct_images:
        out.append(f"    CorrectImages={py_value(question.correct_images)},")
    if question.timer is not None:
        out.append(f"    Timer={question.timer},")
    out.append(")")
    out.append("")

    if not question.correct_answers:
        warnings.append(f"Question has no correct answers: {question.title}")


def write_answer(out, answer_text, is_correct, question):
    out.append("        clsAnswer(")
    out.append(f"            Text={py_value(answer_text)},")
    out.append(f"            IsCrct={is_correct},")
    if answer_text in question.mandatory_position:
        out.append(f"            MandatoryPosition={question.mandatory_position[answer_text]},")
    if answer_text in question.answer_colors:
        out.append(f"            Color={py_value(question.answer_colors[answer_text])},")
    if answer_text in question.answer_images:
        out.append(f"            Image={py_value(question.answer_images[answer_text])},")
    out.append("        ),")


def default_output_path(md_path):
    stem = md_path.stem
    ascii_stem = re.sub(r"[^A-Za-z0-9]+", "_", stem).strip("_")
    if not ascii_stem:
        ascii_stem = "Generated"
    return md_path.with_name(f"DataQ_{ascii_stem}.py")


def default_quiz_name(md_path):
    return md_path.stem.replace("_", " ")


def generate_dataq(md_file, output_file=None, questionnaire_name=None):
    md_path = Path(md_file)
    output_path = Path(output_file) if output_file else default_output_path(md_path)
    quiz_name = questionnaire_name or default_quiz_name(md_path)

    questions = parse_md(md_path)
    if not questions:
        raise ValueError(f"No questions were found in {md_path}")

    used_names = set()
    title_to_name = {}
    question_names = []
    for question in questions:
        name = make_identifier(question.title, used_names)
        title_to_name[question.title] = name
        question_names.append(name)

    warnings = []
    out = [
        "from Question_Classes import clsAnswer, clsQstn, clsQstnList",
        "",
        "",
    ]

    for name, question in zip(question_names, questions):
        write_question(out, name, question, title_to_name, warnings)

    out.extend(
        [
            "Generated_Quiz = clsQstnList(",
            f"    name={py_value(quiz_name)},",
            "    questions=[",
        ]
    )
    out.extend(f"        {name}," for name in question_names)
    out.extend(
        [
            "    ],",
            ")",
            "",
            "questions_lists = {",
            f"    {py_value(md_path.stem)}: Generated_Quiz,",
            "}",
            "",
            "questionnaires = questions_lists",
            "questions_list = next(iter(questions_lists.values())).questions",
            "",
        ]
    )

    output_path.write_text("\n".join(out), encoding="utf-8")
    return output_path, warnings


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

    output_path, warnings = generate_dataq(
        md_file=MD_FILE,
        output_file=OUTPUT_FILE,
        questionnaire_name=QUESTIONNAIRE_NAME,
    )
    print(f"Created {output_path}")
    for warning in warnings:
        print(f"WARNING: {warning}")


if __name__ == "__main__":
    main()
