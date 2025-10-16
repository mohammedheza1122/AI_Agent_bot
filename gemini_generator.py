# gemini_generator.py

import os
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, TEMP_CODE_DIR
import re

class CodeGenerator:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model = "gemini-2.5-pro" 

        self.system_prompt = (
            "أنت بوت ذكي متخصص في توليد تطبيقات الويب الكاملة. "
            "مهمتك هي إنشاء كود تطبيق ويب كامل وجاهز للنشر (مثل HTML/CSS/JS بسيط أو تطبيق Next.js صغير). "
            "يجب أن تكون المخرجات منظمة في صيغة ملفات، باستخدام فواصل واضحة لكل ملف:\n\n"
            "--- START FILE: index.html ---\n"
            "\n"
            "--- END FILE: index.html ---\n\n"
            "استخدم هذه الصيغة حصريًا. تأكد من أن الكود يعمل وقابل للنشر مباشرة."
        )

    def generate_app_code(self, app_description: str, app_name: str) -> str:
        """يولد الكود ويرجع النص كاملاً من Gemini."""
        prompt = f"قم بإنشاء تطبيق ويب بعنوان '{app_name}' بناءً على الوصف التالي: '{app_description}'."
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt
                )
            )
            return response.text
        except Exception as e:
            print(f"خطأ في توليد Gemini: {e}")
            return None

    def save_code_files(self, gemini_output: str, app_name: str) -> str:
        """يحلل مخرجات Gemini ويحفظها كملفات في مجلد جديد."""
        app_path = os.path.join(TEMP_CODE_DIR, app_name.replace(" ", "_"))
        
        os.makedirs(app_path, exist_ok=True)
        
        file_pattern = re.compile(
            r'--- START FILE: (.+?) ---\s*\n(.+?)\n\s*--- END FILE: \1 ---', 
            re.DOTALL
        )
        
        matches = file_pattern.findall(gemini_output)
        
        if not matches:
            raise ValueError("لم يتم العثور على صيغة ملفات صالحة في مخرجات Gemini.")

        for filename, content in matches:
            filename = filename.strip()
            content = content.strip() 
            
            file_path = os.path.join(app_path, filename)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
        
        return app_path
