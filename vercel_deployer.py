# vercel_deployer.py

import requests
import json
from config import VERCEL_API_TOKEN, GITHUB_USERNAME
import time

class VercelDeployer:
    def __init__(self):
        self.base_url = "https://api.vercel.com/v10/projects"
        self.headers = {
            "Authorization": f"Bearer {VERCEL_API_TOKEN}",
            "Content-Type": "application/json"
        }

    def deploy(self, repo_url: str, project_name: str, env_vars: dict) -> str:
        """
        ينشئ مشروعًا جديدًا على Vercel، يربطه بمستودع GitHub، ويبدأ النشر.
        """
        repo_name = repo_url.split('/')[-1] 

        payload = {
            "name": project_name,
            "gitRepository": {
                "type": "github",
                "repo": f"{GITHUB_USERNAME}/{repo_name}"
            },
            # تعيين متغيرات البيئة
            "environmentVariables": [
                {"key": k, "value": v, "type": "encrypted", "target": ["production", "development"]}
                for k, v in env_vars.items()
            ],
            # قد تحتاج لتعيين الإطار (framework) بشكل صريح هنا إذا لم يتعرف عليه Vercel تلقائيًا
        }
        
        # 1. إنشاء المشروع على Vercel
        response = requests.post(self.base_url, headers=self.headers, data=json.dumps(payload))
        
        if response.status_code not in [200, 201]:
            raise Exception(f"فشل إنشاء مشروع Vercel: {response.text}")
        
        project_id = response.json().get('id')

        # 2. التحقق من حالة النشر (Polling) - (مبسط)
        # Vercel يبدأ النشر تلقائيًا عند إنشاء المشروع وربطه بـ GitHub.
        # تحتاج هنا إلى إضافة حلقة تكرارية للتحقق من حالة النشر عبر /v13/deployments
        # حتى تصل الحالة إلى "READY".

        # رابط افتراضي (لغرض العرض)
        deployed_url = f"https://{project_name.lower().replace('_', '-')}.vercel.app"
        return deployed_url
