# telegram_bot.py

import os
import logging
import shutil
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from config import TELEGRAM_BOT_TOKEN, TEMP_CODE_DIR
from gemini_generator import CodeGenerator
from github_manager import GitHubManager 
from vercel_deployer import VercelDeployer
from supabase_manager import SupabaseManager

# إعدادات التسجيل (Logging)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# تهيئة المُدراء
code_generator = CodeGenerator()
github_manager = GitHubManager()
vercel_deployer = VercelDeployer()
supabase_manager = SupabaseManager()

# *************************************************************
# الأوامر الرئيسية للبوت
# *************************************************************

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """يرسل رسالة ترحيب."""
    await update.message.reply_text(
        'مرحباً! أنا بوت إنشاء تطبيقات الويب. استخدم الأمر:\n'
        '/create_app "اسم التطبيق" "وصف مفصل"\n'
        'مثال: /create_app "Task App" "تطبيق قائمة مهام بسيط بلون داكن ويستخدم Supabase لحفظ المهام."'
    )

async def create_app_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """المنطق الأساسي لتوليد ونشر التطبيق بالكامل."""
    
    chat_id = update.effective_chat.id
    args = context.args
    app_path = None # تعريف مبدئي للمسار

    if len(args) < 2:
        await update.message.reply_text(
            'خطأ: يرجى تقديم اسم ووصف.\n'
            'الصيغة: /create_app "اسم التطبيق" "الوصف"'
        )
        return

    # استخلاص الاسم والوصف
    app_name = args[0]
    app_description = " ".join(args[1:])
    # اسم نظيف وصالح للمجلدات وGitHub
    safe_app_name = app_name.replace(" ", "_").lower().replace('-', '_')

    await update.message.reply_text(f"🤖 جاري البدء في إنشاء تطبيق: **{app_name}**...", parse_mode='Markdown')

    try:
        # 1. توليد الكود باستخدام Gemini
        await update.message.reply_text("✨ 1/5: جاري توليد الكود باستخدام Gemini...")
        gemini_output = code_generator.generate_app_code(app_description, app_name)
        
        if not gemini_output:
            await update.message.reply_text("❌ فشل توليد الكود من Gemini. يرجى مراجعة إعدادات API.")
            return
            
        # 2. حفظ ملفات الكود
        app_path = code_generator.save_code_files(gemini_output, safe_app_name)
        await update.message.reply_text(f"📝 2/5: تم حفظ ملفات الكود مؤقتاً.")
        
        # 3. إعداد Supabase والحصول على المفاتيح
        await update.message.reply_text("🔑 3/5: جاري إعداد بيانات Supabase...")
        supabase_keys = supabase_manager.setup_database(safe_app_name) 
        
        # *ملاحظة: يجب أن يضيف الكود هنا منطق تعديل الملفات في app_path لتضمين المفاتيح*
        
        # 4. الرفع على GitHub
        await update.message.reply_text("🐙 4/5: جاري رفع الكود إلى GitHub...")
        repo_url = github_manager.create_and_push(app_path, safe_app_name) 
        await update.message.reply_text(f"✅ تم رفع الكود إلى GitHub بنجاح: {repo_url}")
        
        # 5. النشر على Vercel
        await update.message.reply_text("🚀 5/5: جاري النشر التلقائي عبر Vercel. قد يستغرق هذا دقيقة...")
        deployed_url = vercel_deployer.deploy(repo_url, safe_app_name, supabase_keys) 
        
        # النهاية والنجاح
        await update.message.reply_text(
            f"🎉 **تم بنجاح! تطبيقك جاهز:**\n"
            f"🌐 رابط التطبيق المنشور: [اضغط هنا]({deployed_url})\n"
            f"🔗 مستودع GitHub: [اضغط هنا]({repo_url})",
            parse_mode='Markdown'
        )

    except Exception as e:
        logger.error(f"خطأ غير متوقع في عملية create_app: {e}", exc_info=True)
        await update.message.reply_text(f"❌ حدث خطأ غير متوقع أثناء العملية: {e}")
        
    finally:
        # خطوة تنظيف (حذف المجلد المؤقت)
        if app_path and os.path.exists(app_path):
            shutil.rmtree(app_path)
            logger.info(f"تم حذف المجلد المؤقت: {app_path}")


def main() -> None:
    """نقطة الدخول الرئيسية لتشغيل البوت."""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("create_app", create_app_command))
    
    # التأكد من وجود مسار حفظ الكود
    os.makedirs(TEMP_CODE_DIR, exist_ok=True)
    
    print("البوت يعمل...")
    application.run_polling(poll_interval=3)

if __name__ == '__main__':
    main()
