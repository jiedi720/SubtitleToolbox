# ASS 逻辑文件
import os
import re
import pysubs2
from function.utils import clean_subtitle_text_ass

# 预设默认 ASS 样式常量 (供外部导入或内部默认使用)
DEFAULT_KOR_STYLE = "Style: KOR - Noto Serif KR,Noto Serif KR SemiBold,20,&H0026FCFF,&H000000FF,&H50000000,&H00000000,-1,0,0,0,100,100,0.1,0,1,0.6,0,2,10,10,34,1"
DEFAULT_CHN_STYLE = "Style: CHN - Drama,小米兰亭,17,&H28FFFFFF,&H000000FF,&H64000000,&H00000000,-1,0,0,0,100,100,0,0,1,0.5,0,2,10,10,15,1"

def run_ass_task(target_dir, styles, log_func, progress_bar, root, output_dir=None):
    """
    styles: {"kor": "Style string...", "chn": "Style string..."}
    output_dir: 如果不提供，默认保存在 target_dir
    """
    l_k = styles.get("kor", DEFAULT_KOR_STYLE)
    l_c = styles.get("chn", DEFAULT_CHN_STYLE)
    
    # 获取样式名称用于后续 Dialogue 分派 (假设格式为 Style: Name, ...)
    style_name_k = l_k.split(',')[0].replace("Style:", "").strip()
    style_name_c = l_c.split(',')[0].replace("Style:", "").strip()
    
    final_out_path = output_dir if output_dir else target_dir
    
    hdr = (f"[Script Info]\nScriptType: v4.00+\nWrapStyle: 0\nScaledBorderAndShadow: yes\n\n"
           f"[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
           f"OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, "
           f"Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
           f"{l_k}\n{l_c}\n\n"
           f"[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text")
    
    all_f = os.listdir(target_dir)
    duals = [f for f in all_f if f.lower().endswith('.dual.srt')]
    srts = [f for f in all_f if f.lower().endswith('.srt') and '.dual.' not in f.lower()]
    
    tasks = []
    done = set()
    
    # 处理已有的双语 SRT
    for f in duals: 
        tasks.append({"type": "convert", "path": os.path.join(target_dir, f), "name": f})
        m = re.search(r'[Ss]\d{2}[Ee]\d{2}', f)
        if m: done.add(m.group().upper())
        
    # 处理需要合并的单语 SRT
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
            tasks.append({"type": "merge", "ep": ep, "chi": os.path.join(target_dir, chi[0]), 
                          "other": os.path.join(target_dir, oth[0]), "base": oth[0]})
    
    total_tasks = len(tasks)
    if total_tasks == 0:
        log_func("⚠️ 未找到可处理的字幕文件。")
        return

    for i, t in enumerate(tasks):
        evs = []
        try:
            if t["type"] == "convert":
                subs = pysubs2.load(t["path"])
                split = 0
                for j in range(1, len(subs)):
                    if subs[j].start < subs[j-1].start: split = j; break
                for j, l in enumerate(subs):
                    sty = style_name_k if j < split else style_name_c
                    st, et = pysubs2.time.ms_to_str(l.start, fractions=True).replace(',','.'), pysubs2.time.ms_to_str(l.end, fractions=True).replace(',','.')
                    evs.append(f"Dialogue: 0,{st[:-1]},{et[:-1]},{sty},,0,0,0,,{l.text.replace('\\N', ' ').strip()}")
                out = t["name"].replace('.dual.srt', '.ass')
            else:
                s1, s2 = pysubs2.load(t["other"]), pysubs2.load(t["chi"])
                for l in s1:
                    c = clean_subtitle_text_ass(l.text)
                    if c:
                        st, et = pysubs2.time.ms_to_str(l.start, fractions=True).replace(',','.'), pysubs2.time.ms_to_str(l.end, fractions=True).replace(',','.')
                        evs.append(f"Dialogue: 0,{st[:-1]},{et[:-1]},{style_name_k},,0,0,0,,{c}")
                for l in s2:
                    c = clean_subtitle_text_ass(l.text)
                    if c:
                        st, et = pysubs2.time.ms_to_str(l.start, fractions=True).replace(',','.'), pysubs2.time.ms_to_str(l.end, fractions=True).replace(',','.')
                        evs.append(f"Dialogue: 0,{st[:-1]},{et[:-1]},{style_name_c},,0,0,0,,{c}")
                out = re.split(r'_track\d+', t["base"], flags=re.IGNORECASE)[0].rstrip('._ ') + ".ass"
            
            # 写入文件
            save_path = os.path.join(final_out_path, out)
            with open(save_path, 'w', encoding='utf-8-sig') as f: 
                f.write(hdr + "\n" + "\n".join(evs))
            log_func(f"✅ 已生成: {out}")
            
        except Exception as e:
            log_func(f"❌ 处理 {t.get('name', '任务')} 时出错: {e}")

        # 更新 CustomTkinter 进度条 (0.0 ~ 1.0)
        progress_bar.set((i + 1) / total_tasks)
        root.update_idletasks()