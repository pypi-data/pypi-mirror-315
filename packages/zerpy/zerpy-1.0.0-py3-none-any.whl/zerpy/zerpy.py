# zerpy.py
import json
import os
from dotenv import load_dotenv

class ZerPy:
    def __init__(self):
        self.data = {}

    def connect(self, db_name):
        """الاتصال بقاعدة البيانات (ملف JSON)"""
        self.db_name = db_name
        self.load()
        return self

    def load(self):
        """تحميل البيانات من ملف JSON"""
        if os.path.exists(self.db_name):
            with open(self.db_name, 'r') as f:
                self.data = json.load(f)
        else:
            self.save()

    def save(self):
        """حفظ البيانات في ملف JSON"""
        with open(self.db_name, 'w') as f:
            json.dump(self.data, f, indent=2)

    def get(self, key):
        """إرجاع بيانات باستخدام المفتاح"""
        return self.data.get(key, None)

    def register(self, **kwargs):
        """تسجيل عدة بيانات دفعة واحدة باستخدام المعاملات المسماة"""
        for key, value in kwargs.items():
            self.data[key] = value
        self.save()

    def delete(self, key):
        """حذف قاعدة بيانات باستخدام المفتاح"""
        if key in self.data:
            del self.data[key]
            self.save()
        else:
            print(f"Key '{key}' does not exist.")

# التعامل مع متغيرات البيئة
class Env:
    def __init__(self):
        self.envs = {}

    def load(self):
        """تحميل جميع متغيرات البيئة من ملف .env"""
        load_dotenv()  # تحميل المتغيرات البيئية من ملف .env
        self.envs = dict(os.environ)  # نسخ جميع المتغيرات البيئية إلى envs

    def set(self, key, value):
        """تعيين متغير بيئة جديد"""
        os.environ[key] = value
        self.envs[key] = value

    def get(self, key):
        """إرجاع قيمة متغير البيئة"""
        return os.getenv(key)

# استيراد الوظائف
db = ZerPy()
env = Env()

# وظيفة الاتصال بالمكتبة
def connect(db_name):
    return db.connect(db_name)
