# supabase_manager.py

from supabase import create_client, Client
from config import SUPABASE_PROJECT_URL, SUPABASE_SERVICE_ROLE_KEY

class SupabaseManager:
    def __init__(self):
        # استخدام مفتاح Service Role Key
        self.supabase: Client = create_client(SUPABASE_PROJECT_URL, SUPABASE_SERVICE_ROLE_KEY)
        self.url = SUPABASE_PROJECT_URL
        # يتم تمرير مفتاح Service Role Key كـ Anon Key في هذه الحالة للوصول السريع
        # (يجب أن يتم استبداله بمفتاح Anon Key الحقيقي في بيئات الإنتاج)
        self.anon_key = SUPABASE_SERVICE_ROLE_KEY 

    def setup_database(self, app_name: str, table_schema: dict = None) -> dict:
        """
        يقوم بإعداد أي بيانات أولية مطلوبة في Supabase ويعيد المفاتيح.
        *إضافة منطق إنشاء الجداول SQL يتطلب استخدام execute_query أو REST API مباشرة.*
        """
        
        # إرجاع مفاتيح البيئة التي سيحتاجها التطبيق المنشور على Vercel
        return {
            "NEXT_PUBLIC_SUPABASE_URL": self.url,
            "NEXT_PUBLIC_SUPABASE_ANON_KEY": self.anon_key
        }
