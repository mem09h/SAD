from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="منصة السادس العراقية - المنهج الرسمي", version="1.0")

class QuestionModel(BaseModel):
    id: int
    branch: str      # العلمي أو الأدبي
    subject: str     # اسم المادة (رياضيات، كيمياء، تاريخ...)
    chapter: str     # الفصل الدراسي
    question: str
    options: List[str]
    answer: str
    explanation: str

# قاعدة بيانات تحتوي على نموذج أسئلة حقيقية للمنهج العراقي للسادس
iraq_curriculum_database = [
    {
        "id": 1,
        "branch": "العلمي",
        "subject": "الرياضيات",
        "chapter": "الفصل الأول - الاعداد المركبة",
        "question": "إذا كان $2+i$ هو أحد جذري المعاملات حقيقية، فما هو الجذر الآخر؟",
        "options": ["2 - i", "-2 + i", "-2 - i", "i - 2"],
        "answer": "2 - i",
        "explanation": "بما أن المعاملات حقيقية، فإن الجذور المركبة تأتي على شكل مرافقات (مترافقات)."
    },
    {
        "id": 2,
        "branch": "الأدبي",
        "subject": "التاريخ",
        "chapter": "الفصل الأول - التاريخ الحديث",
        "question": "متى تم عقد مؤتمر قمة بغداد أو الأحداث التاريخية المرتبطة بالمنهج؟",
        "options": ["تاريخ أ", "تاريخ ب", "تاريخ ج", "تاريخ د"],
        "answer": "تاريخ أ",
        "explanation": "شرح تفصيلي للإجابة حسب المنهج الوزاري المقرّر."
    }
]

@app.get("/")
def home():
    return {"message": "مرحباً بك في خادم منصة السادس العراقية المعتمد لوزارة التربية"}

@app.get("/api/questions", response_model=List[QuestionModel])
def get_questions(branch: str = None, subject: str = None):
    # تصفية الأسئلة حسب الفرع أو المادة إذا طلبها التطبيق
    results = iraq_curriculum_database
    if branch:
        results = [q for q in results if q["branch"] == branch]
    if subject:
        results = [q for q in results if q["subject"] == subject]
    return results

@app.post("/api/questions", response_model=QuestionModel)
def add_question(q: QuestionModel):
    iraq_curriculum_database.append(q.dict())
    return q
