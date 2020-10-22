# -*- coding: utf-8 -*-
from __future__ import unicode_literals

status_codes = {
    '200':'درخواست تایید شد',
    '400':'پارامترها ناقص هستند',
    '401':'حساب کاربری غیرفعال شده است',
    '402':'عملیات ناموفق بود',
    '403':'کد شناسائی API-Key معتبر نمی‌باشد',
    '404':'متد نامشخص است',
    '405':'متد Get/Post اشتباه است',
    '406':'پارامترهای اجباری خالی ارسال شده اند',
    '407':'دسترسی به اطلاعات مورد نظر برای شما امکان پذیر نیست',
    '409':'سرور قادر به پاسخگوئی نیست بعدا تلاش کنید',
    '411':'دریافت کننده نامعتبر است',
    '412':'ارسال کننده نامعتبر است',
    '413':'پیام خالی است و یا طول پیام بیش از حد مجاز می‌باشد. لاتین  ﻛﺎراﻛﺘﺮ و ﻓﺎرﺳﻲ 268 ﻛﺎراﻛﺘﺮ',
    '414':'حجم درخواست بیشتر از حد مجاز است ،ارسال پیامک :هر فراخوانی حداکثر 200 رکوردو کنترل وضعیت :هر فراخوانی 500 رکورد',
    '415':'اندیس شروع بزرگ تر از کل تعداد شماره های مورد نظر است',
    '416':'IP سرویس مبدا با تنظیمات مطابقت ندارد',
    '417':'تاریخ ارسال اشتباه است و فرمت آن صحیح نمی باشد.',
    '418':'اعتبار شما کافی نمی‌باشد',
    '419':'طول آرایه متن و گیرنده و فرستنده هم اندازه نیست',
    '420':'استفاده از لینک در متن پیام برای شما محدود شده است',
    '422':'داده ها به دلیل وجود کاراکتر نامناسب قابل پردازش نیست',
    '424':'الگوی مورد نظر پیدا نشد',
    '426':'استفاده از این متد نیازمند سرویس پیشرفته می‌باشد',
    '427':'استفاده از این خط نیازمند ایجاد سطح دسترسی می باشد',
    '428':'ارسال کد از طریق تماس تلفنی امکان پذیر نیست',
    '429':'IP محدود شده است',
    '431':'ساختار کد صحیح نمی‌باشد',
    '432':'پارامتر کد در متن پیام پیدا نشد',
    '451':'فراخوانی بیش از حد در بازه زمانی مشخص IP محدود شده',
    '501':'فقط امکان ارسال پیام تست به شماره صاحب حساب کاربری وجود دارد',
}
	
status_choices = (
        ('0', 'بررسی نشده'),
        ('1', 'در صف ارسال قرار دارد'),
        ('2', 'زمان بندی شده (ارسال در تاریخ معین)'),
        ('4', 'ارسال شده به مخابرات'),
        ('5', 'ارسال شده به مخابرات'), 
        ('6', 'خطا در ارسال پیام که توسط سر شماره پیش می آید و به معنی عدم رسیدن پیامک می‌باشد'),
        ('10', 'رسیده به گیرنده'),
        ('11', 'نرسیده به گیرنده ، این وضعیت به دلایلی از جمله خاموش یا خارج از دسترس بودن گیرنده اتفاق می افتد'),
        ('13', 'ارسال پیام از سمت کاربر لغو شده یا در ارسال آن مشکلی پیش آمده که هزینه آن به حساب برگشت داده می‌شود'),
        ('14', 'بلاک شده است، عدم تمایل گیرنده به دریافت پیامک از خطوط تبلیغاتی که هزینه آن به حساب برگشت داده می‌شود'),
        ('100', 'شناسه پیامک نامعتبر است'),
    )