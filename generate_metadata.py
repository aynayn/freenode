import os
import json
from datetime import datetime, timezone, timedelta

def get_file_actual_mtime(filepath):
    try:
        # ဖိုင်တကယ့် ပြင်ဆင်ခဲ့တဲ့ စနစ်အချိန် (Physical File Modification Time) ကို ရယူခြင်း
        mtime_timestamp = os.path.getmtime(filepath)
        
        # UTC standard အချိန်အဖြစ် ပြောင်းလဲခြင်း
        utc_dt = datetime.fromtimestamp(mtime_timestamp, tz=timezone.utc)
        
        # မြန်မာစံတော်ချိန် (UTC + 6:30) သို့ ပြောင်းလဲခြင်း
        mm_timezone = timezone(timedelta(hours=6, minutes=30))
        mm_dt = utc_dt.astimezone(mm_timezone)
        
        # ရက်စွဲနှင့် အချိန်ကို '18.6.2026 5:16' ပုံစံသို့ ပြောင်းလဲခြင်း
        return f"{mm_dt.day}.{mm_dt.month}.{mm_dt.year} {mm_dt.hour}:{mm_dt.minute:02d}"
    except Exception as e:
        print(f"ဖိုင်ပြင်ဆင်ချိန် ရယူရာတွင် ချို့ယွင်းချက်ရှိပါသည် {filepath}: {e}")
        
        # အမှားတစ်စုံတစ်ရာ ရှိခဲ့ပါက လက်ရှိ မြန်မာစံတော်ချိန်ကို သုံးပါမည်
        mm_timezone = timezone(timedelta(hours=6, minutes=30))
        now = datetime.now(mm_timezone)
        return f"{now.day}.{now.month}.{now.year} {now.hour}:{now.minute:02d}"

def main():
    metadata = {}
    
    # လက်ရှိ Directory ထဲရှိ 'sub_part*.txt' ဖိုင်အားလုံးကို ရှာဖွေခြင်း
    files = [f for f in os.listdir('.') if f.startswith('sub_part') and f.endswith('.txt')]
    files.sort() # ဖိုင်အမည်များကို အစဉ်လိုက်စီခြင်း

    for file in files:
        # ဖိုင်တစ်ခုချင်းစီ၏ တကယ့်အချိန်အစစ်အမှန်ကို ရယူသိမ်းဆည်းခြင်း
        metadata[file] = get_file_actual_mtime(file)

    # စုစည်းထားသော ဒေတာများကို 'metadata.json' အဖြစ် သိမ်းဆည်းခြင်း
    with open('metadata.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print("metadata.json ဖိုင်အသစ်ကို တကယ့်အချိန်အစစ်အမှန်များဖြင့် ဖန်တီးပြီးပါပြီ။")

if __name__ == '__main__':
    main()
