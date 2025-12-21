#ASS 逻辑文件

import os
import re
import pysubs2
from utils import clean_subtitle_text_ass

def run_ass_task(target_dir, styles, log_func, progress_bar, root):
    """
     styles: {"kor": "Style string...", "chn": "Style string..."}
    """
    l_k = styles["kor"]
    l_c = styles["chn"]
    
    hdr = f"[Script Info]\nScriptType: v4.00+\nWrapStyle: 0\nScaledBorderAndShadow: yes\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n{l_k}\n{l_c}\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
    
    all_f = os.listdir(target_dir)
    duals = [f for f in all_f if f.lower().endswith('.dual.srt')]
    srts = [f for f in all_f if f.lower().endswith('.srt') and '.dual.' not in f.lower()]
    tasks = []
    done = set()
    
    for f in duals: 
        tasks.append({"type": "convert", "path": os.path.join(target_dir, f), "name": f})
        m = re.search(r'[Ss]\d{2}[Ee]\d{2}', f)
        if m: done.add(m.group().upper())
        
    gps = {}
    for f in srts:
        m = re.search(r'[Ss]\d{2}[Ee]\d{2}', f)
        if m:
            ep = m.group().upper()
            if ep not in done: gps.setdefault(ep, []).append(f)
            
    for ep, fl in gps.items():
        chi = [f for f in fl if any(x in f.lower() for x in ['chi', 'chs', 'cht'])]
        oth = [f for f in fl if f not in chi]
        if chi and oth: 
            tasks.append({"type": "merge", "ep": ep, "chi": os.path.join(target_dir, chi[0]), "other": os.path.join(target_dir, oth[0]), "base": oth[0]})
    
    progress_bar["maximum"] = len(tasks)
    
    for i, t in enumerate(tasks):
        evs = []
        if t["type"] == "convert":
            subs = pysubs2.load(t["path"])
            split = 0
            for j in range(1, len(subs)):
                if subs[j].start < subs[j-1].start: split = j; break
            for j, l in enumerate(subs):
                sty = "KOR - Noto Serif KR" if j < split else "CHN - Drama"
                st, et = pysubs2.time.ms_to_str(l.start, fractions=True).replace(',','.')[:-1], pysubs2.time.ms_to_str(l.end, fractions=True).replace(',','.')[:-1]
                evs.append(f"Dialogue: 0,{st},{et},{sty},,0,0,0,,{l.text.replace('\\N', ' ').strip()}")
            out = t["name"].replace('.dual.srt', '.ass')
        else:
            s1, s2 = pysubs2.load(t["other"]), pysubs2.load(t["chi"])
            for l in s1:
                c = clean_subtitle_text_ass(l.text)
                if c:
                    st, et = pysubs2.time.ms_to_str(l.start, fractions=True).replace(',','.')[:-1], pysubs2.time.ms_to_str(l.end, fractions=True).replace(',','.')[:-1]
                    evs.append(f"Dialogue: 0,{st},{et},KOR - Noto Serif KR,,0,0,0,,{c}")
            for l in s2:
                c = clean_subtitle_text_ass(l.text)
                if c:
                    st, et = pysubs2.time.ms_to_str(l.start, fractions=True).replace(',','.')[:-1], pysubs2.time.ms_to_str(l.end, fractions=True).replace(',','.')[:-1]
                    evs.append(f"Dialogue: 0,{st},{et},CHN - Drama,,0,0,0,,{c}")
            out = re.split(r'_track\d+', t["base"], flags=re.IGNORECASE)[0].rstrip('._ ') + ".ass"
        
        with open(os.path.join(target_dir, out), 'w', encoding='utf-8-sig') as f: 
            f.write(hdr + "\n".join(evs))
        
        progress_bar["value"] = i + 1
        root.update_idletasks()