# srt2ass.py 逻辑文件
import os
import re
import pysubs2
import configparser
import shutil  # 导入用于移动文件的库
from function.cleaners import clean_subtitle_text_ass
from function.paths import get_organized_path

# ==========================================
# 1. 预设硬编码默认样式
# ==========================================
DEFAULT_KOR_STYLE = "Style: KOR - Noto Serif KR,Noto Serif KR SemiBold,20,&H0026FCFF,&H000000FF,&H50000000,&H00000000,-1,0,0,0,100,100,0.1,0,1,0.6,0,2,10,10,34,1"
DEFAULT_CHN_STYLE = "Style: CHN - Drama,小米兰亭,17,&H28FFFFFF,&H000000FF,&H64000000,&H00000000,-1,0,0,0,100,100,0,0,1,0.5,0,2,10,10,15,1"

def get_config_styles(log_func=None):
    config_path = os.path.join(os.getcwd(), "SubtitleToolbox.ini")
    styles = {"kor": DEFAULT_KOR_STYLE, "chn": DEFAULT_CHN_STYLE}
    if not os.path.exists(config_path):
        try:
            config = configparser.ConfigParser(interpolation=None)
            config["ASS_Styles"] = {"kor_style": DEFAULT_KOR_STYLE, "chn_style": DEFAULT_CHN_STYLE}
            with open(config_path, 'w', encoding='utf-8-sig') as cf: config.write(cf)
        except: pass
    else:
        try:
            config = configparser.ConfigParser(interpolation=None)
            config.read(config_path, encoding='utf-8-sig')
            if "ASS_Styles" in config:
                styles["kor"] = config["ASS_Styles"].get("kor_style", DEFAULT_KOR_STYLE)
                styles["chn"] = config["ASS_Styles"].get("chn_style", DEFAULT_CHN_STYLE)
        except: pass
    return styles

def run_ass_task(target_dir, styles, log_func, progress_bar, root, output_dir=None):
    # --- 1. 路径自动纠偏 ---
    if log_func: log_func(f"🔍 初始选择路径: {target_dir}")
    current_dir_name = os.path.basename(target_dir).lower()
    if current_dir_name in ['script', 'srt']:
        if not any(f.lower().endswith('.srt') for f in os.listdir(target_dir)):
            target_dir = os.path.dirname(target_dir)

    # --- 2. 样式与头信息准备 ---
    ini_styles = get_config_styles(log_func)
    l_k = styles.get("kor") if styles and styles.get("kor") else ini_styles["kor"]
    l_c = styles.get("chn") if styles and styles.get("chn") else ini_styles["chn"]
    style_name_k = l_k.split(',')[0].replace("Style:", "").strip()
    style_name_c = l_c.split(',')[0].replace("Style:", "").strip()
    
    hdr = (f"[Script Info]\nScriptType: v4.00+\nWrapStyle: 0\nScaledBorderAndShadow: yes\n\n"
           f"[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
           f"OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, "
           f"Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
           f"{l_k}\n{l_c}\n\n"
           f"[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text")

    # --- 3. 扫描任务 ---
    all_f = os.listdir(target_dir)
    # 排除视频自带的 .DUAL. 干扰，只认真正的 .dual.srt 后缀
    duals = [f for f in all_f if f.lower().endswith('.dual.srt')]
    srts = [f for f in all_f if f.lower().endswith('.srt') and f not in duals]
    
    tasks = []
    EP_PATTERN = re.compile(r'[Ss](\d{2})[Ee](\d{2})')
    gps = {}
    for f in srts:
        m = EP_PATTERN.search(f)
        if m:
            ep = f"S{m.group(1)}E{m.group(2)}"
            gps.setdefault(ep, []).append(f)
            
    for ep, fl in gps.items():
        chi = [f for f in fl if '[chi]' in f.lower()]
        kor = [f for f in fl if '[kor]' in f.lower()]
        if not chi: chi = [f for f in fl if any(x in f.lower() for x in ['chi', 'chs', 'cht'])]
        if not kor: kor = [f for f in fl if f not in chi]

        if chi and kor: 
            tasks.append({
                "type": "merge", "ep": ep, 
                "chi_name": chi[0], "chi_path": os.path.join(target_dir, chi[0]), 
                "oth_name": kor[0], "oth_path": os.path.join(target_dir, kor[0])
            })
            if log_func: log_func(f"✅ 集数 {ep} 成功匹配")

    total = len(tasks)
    if total == 0:
        log_func("⚠️ 未找到可配对的字幕。")
        return

    # --- 4. 执行处理 ---
    base_output = output_dir if output_dir else target_dir
    
    for i, t in enumerate(tasks):
        try:
            # 加载与清洗
            s1, s2 = pysubs2.load(t["oth_path"]), pysubs2.load(t["chi_path"])
            evs = []
            for l in s1:
                c = clean_subtitle_text_ass(l.text)
                if c:
                    st = pysubs2.time.ms_to_str(l.start, fractions=True).replace(',','.')[:-1]
                    et = pysubs2.time.ms_to_str(l.end, fractions=True).replace(',','.')[:-1]
                    evs.append(f"Dialogue: 0,{st},{et},{style_name_k},,0,0,0,,{c}")
            for l in s2:
                c = clean_subtitle_text_ass(l.text)
                if c:
                    st = pysubs2.time.ms_to_str(l.start, fractions=True).replace(',','.')[:-1]
                    et = pysubs2.time.ms_to_str(l.end, fractions=True).replace(',','.')[:-1]
                    evs.append(f"Dialogue: 0,{st},{et},{style_name_c},,0,0,0,,{c}")

            # 1. 生成 .ass (利用 paths.py 直接放根目录)
            clean_name = re.split(r'_track\d+', t["oth_name"], flags=re.IGNORECASE)[0].rstrip('._ ') + ".ass"
            save_path_ass = get_organized_path(base_output, clean_name)
            
            with open(save_path_ass, 'w', encoding='utf-8-sig') as f: 
                f.write(hdr + "\n" + "\n".join(evs))
            
            log_func(f"📝 已生成: {os.path.basename(save_path_ass)}")

            # 2. 归档 .srt (利用 paths.py 移动到 srt 子目录)
            archive_dir_chi = get_organized_path(base_output, t["chi_name"])
            archive_dir_oth = get_organized_path(base_output, t["oth_name"])
            
            shutil.move(t["chi_path"], archive_dir_chi)
            shutil.move(t["oth_path"], archive_dir_oth)

        except Exception as e:
            log_func(f"❌ 处理 {t.get('ep')} 时出错: {e}")

        progress_bar.set((i + 1) / total)
        root.update_idletasks()
    
    log_func("📂 任务完成：.ass 已生成在根目录，原始 .srt 已归档至 srt/ 文件夹。")