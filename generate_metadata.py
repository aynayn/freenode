import os
import json
import subprocess
from datetime import datetime

# GitHub Actions ရဲ့ Local Git မှတစ်ဆင့် ဖိုင်တစ်ခုချင်းစီ၏ နောက်ဆုံးပြင်ဆင်ခဲ့သော အချိန်ကို ရယူခြင်း
def get_file_last_modified_date(filepath):
    try:
        # Local Git command သုံး၍ ဖိုင်တစ်ခုချင်းစီ၏ Commit အချိန်ကို ဆွဲယူခြင်း (API Rate Limit မရှိပါ)
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%ci', filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        date_str = result.stdout.strip()
        if date_str:
            # ရရှိလာသော အချိန်ကို '18.6.2026 5:16' ပုံစံသို့ ပြောင်းလဲခြင်း
            dt = datetime.fromisoformat(date_str)
            return f"{dt.day}.{dt.month}.{dt.year} {dt.hour}:{dt.minute:02d}"
    except Exception as e:
        print(f"ရက်စွဲရယူရာတွင် ချို့ယွင်းချက်ရှိပါသည် {filepath}: {e}")
    
    # အကယ်၍ Git မှ မရရှိပါက လက်ရှိအချိန်ကိုသာ ပြသပေးပါမည်
    now = datetime.now()
    return f"{now.day}.{now.month}.{now.year} {now.hour}:{now.minute:02d}"

def main():
    metadata = {}
    
    # လက်ရှိ Directory ထဲရှိ 'sub_part*.txt' ဖိုင်အားလုံးကို ရှာဖွေခြင်း
    files = [f for f in os.listdir('.') if f.startswith('sub_part') and f.endswith('.txt')]
    files.sort() # ဖိုင်အမည်များကို အစဉ်လိုက်စီခြင်း

    for file in files:
        # ဖိုင်တစ်ခုချင်းစီ၏ အမည်နှင့် ရက်စွဲကို သိမ်းဆည်းခြင်း
        metadata[file] = get_file_last_modified_date(file)

    # စုစည်းထားသော ဒေတာများကို 'metadata.json' အဖြစ် သိမ်းဆည်းခြင်း
    with open('metadata.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print("metadata.json ဖိုင်ကို အောင်မြင်စွာ ဖန်တီးပြီးပါပြီ။")

if __name__ == '__main__':
    main()
