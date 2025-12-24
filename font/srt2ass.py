# srt2ass.py 逻辑文件
import os
import re
import pysubs2
import configparser
from function.cleaners import clean_subtitle_text_ass
# 建议导入智能路径函数，确保逻辑统一
from function.paths import get_organized_path

# ==========================================
# 1. 预设硬编码默认样式 (作为最终兜底)
# ==========================================
DEFAULT_KOR_STYLE = "Style: KOR - Noto Serif KR,Noto Serif KR SemiBold,20,&H0026FCFF,&H000000FF,&H50000000,&H00000000,-1,0,0,0,100,100,0.1,0,1,0.6,0,2,10,10,34,1"
DEFAULT_CHN_STYLE = "Style: CHN - Drama,小米兰亭,17,&H28FFFFFF,&H000000FF,&H64000000,&H00000000,-1,0,0,0,100,100,0,0,1,0.5,0,2,10,10,15,1"

def get_config_styles(log_func=None):
    """
    从根目录下的 SubtitleToolbox.ini 读取样式，不存在则生成。
    """
    config_path = os.path.join(os.getcwd(), "SubtitleToolbox.ini")
    styles = {"kor": DEFAULT_KOR_STYLE, "chn": DEFAULT_CHN_STYLE}
    
    if not os.path.exists(config_path):
        try:
            config = configparser.ConfigParser(interpolation=None)
            config["ASS_Styles"] = {
                "kor_style": DEFAULT_KOR_STYLE,
                "chn_style": DEFAULT_CHN_STYLE
            }
            with open(config_path, 'w', encoding='utf-8-sig') as configfile:
                config.write(configfile)
            if log_func:
                log_func("ℹ️ 未发现配置文件，已在程序目录下自动生成默认 SubtitleToolbox.ini")
        except Exception as e:
            if log_func: log_func(f"⚠️ 尝试创建配置文件失败: {e}")
    else:
        try:
            config = configparser.ConfigParser(interpolation=None)
            config.read(config_path, encoding='utf-8-sig')
            if "ASS_Styles" in config:
                styles["kor"] = config["ASS_Styles"].get("kor_style", DEFAULT_KOR_STYLE)
                styles["chn"] = config["ASS_Styles"].get("chn_style", DEFAULT_CHN_STYLE)
        except Exception as e:
            if log_func: log_func(f"⚠️ 读取配置文件出错，使用默认样式: {e}")
                
    return styles

def run_ass_task(target_dir, styles, log_func, progress_bar, root, output_dir=None):
    """
    执行 ASS 任务
    """
    # --- 1. 路径自动纠偏 ---
    # 如果传入的 target_dir 指向了 script 文件夹，自动回退到父目录
    if os.path.basename(target_dir).lower() == 'script':
        target_dir = os.path.dirname(target_dir)

    # --- 2. 样式准备 ---
    if not styles or not styles.get("kor") or not styles.get("chn"):
        ini_styles = get_config_styles(log_func)
        styles = styles or {}
        if not styles.get("kor"): styles["kor"] = ini_styles["kor"]
        if not styles.get("chn"): styles["chn"] = ini_styles["chn"]

    l_k, l_c = styles.get("kor"), styles.get("chn")
    style_name_k = l_k.split(',')[0].replace("Style:", "").strip()
    style_name_c = l_c.split(',')[0].replace("Style:", "").strip()
    
    # --- 3. 确定基础输出路径 ---
    base_output = output_dir if output_dir else target_dir
    
    hdr = (f"[Script Info]\nScriptType: v4.00+\nWrapStyle: 0\nScaledBorderAndShadow: yes\n\n"
           f"[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
           f"OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, "
           f"Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
           f"{l_k}\n{l_c}\n\n"
           f"[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text")
    
    # --- 4. 扫描任务 ---
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
            tasks.append({"type": "merge", "ep": ep, "chi": os.path.join(target_dir, chi[0]), 
                          "other": os.path.join(target_dir, oth[0]), "base": oth[0]})
    
    total_tasks = len(tasks)
    if total_tasks == 0:
        log_func("⚠️ 未找到可处理的字幕文件。")
        return

    # --- 5. 处理任务 ---
    for i, t in enumerate(tasks):
        evs = []
        try:
            if t["type"] == "convert":
                subs = pysubs2.load(t["path"])
                split = 0
                for j in range(1, len(subs)):
                    if subs[j].start < subs[j-1].start:
                        split = j; break
                for j, l in enumerate(subs):
                    sty = style_name_k if j < split else style_name_c
                    c = clean_subtitle_text_ass(l.text)
                    if c:
                        st = pysubs2.time.ms_to_str(l.start, fractions=True).replace(',','.')
                        et = pysubs2.time.ms_to_str(l.end, fractions=True).replace(',','.')
                        evs.append(f"Dialogue: 0,{st[:-1]},{et[:-1]},{sty},,0,0,0,,{c}")
                out = t["name"].replace('.dual.srt', '.ass')
            else:
                s1, s2 = pysubs2.load(t["other"]), pysubs2.load(t["chi"])
                for l in s1:
                    c = clean_subtitle_text_ass(l.text)
                    if c:
                        st = pysubs2.time.ms_to_str(l.start, fractions=True).replace(',','.')
                        et = pysubs2.time.ms_to_str(l.end, fractions=True).replace(',','.')
                        evs.append(f"Dialogue: 0,{st[:-1]},{et[:-1]},{style_name_k},,0,0,0,,{c}")
                for l in s2:
                    c = clean_subtitle_text_ass(l.text)
                    if c:
                        st = pysubs2.time.ms_to_str(l.start, fractions=True).replace(',','.')
                        et = pysubs2.time.ms_to_str(l.end, fractions=True).replace(',','.')
                        evs.append(f"Dialogue: 0,{st[:-1]},{et[:-1]},{style_name_c},,0,0,0,,{c}")
                
                out = re.split(r'_track\d+', t["base"], flags=re.IGNORECASE)[0].rstrip('._ ') + ".ass"
            
            # --- 关键：统一使用 utils 的路径生成逻辑 ---
            save_path = get_organized_path(base_output, out)
            
            with open(save_path, 'w', encoding='utf-8-sig') as f: 
                f.write(hdr + "\n" + "\n".join(evs))
            
            log_func(f"✅ 已生成: ass/{os.path.basename(save_path)}")
            
        except Exception as e:
            log_func(f"❌ 处理 {t.get('name', '任务')} 时出错: {e}")

        progress_bar.set((i + 1) / total_tasks)
        root.update_idletasks()