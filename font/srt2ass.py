"""
SRT转ASS字幕转换模块
负责将SRT字幕文件转换为ASS格式，并支持双语字幕合并功能。
"""

import os
import sys
import re
import pysubs2
import configparser
import shutil
from function.parsers import clean_subtitle_text_ass
from function.file_utils import get_organized_path

# 预设硬编码默认样式
DEFAULT_KOR_STYLE = "Style: KOR - Noto Serif KR,Noto Serif KR SemiBold,20,&H0026FCFF,&H000000FF,&H50000000,&H00000000,-1,0,0,0,100,100,0.1,0,1,0.6,0,2,10,10,34,1"
DEFAULT_CHN_STYLE = "Style: CHN - Drama,小米兰亭,17,&H28FFFFFF,&H000000FF,&H64000000,&H00000000,-1,0,0,0,100,100,0,0,1,0.5,0,2,10,10,15,1"
DEFAULT_JPN_STYLE = "Style: JPN - EPSON 太明朝体,EPSON 太明朝体Ｂ,14,&H00FFFFFF,&H000000FF,&H50000000,&H00000000,0,0,0,0,100,100,1,0,1,0.6,0,2,10,10,15,1"

def get_config_path():
    """获取配置文件路径，使用 exe 所在的目录"""
    # 获取 exe 所在的目录或脚本所在目录
    if getattr(sys, 'frozen', False):
        # 如果是打包后的 exe
        base_dir = os.path.dirname(sys.executable)
    else:
        # 如果是开发环境
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(base_dir, "SubtitleToolbox.ini")

def fix_srt_format(srt_path):
    """
    修复SRT文件格式，将序号、时间戳和文本分离到不同行

    Args:
        srt_path: SRT文件路径

    Returns:
        bool: 是否进行了修复
    """
    try:
        with open(srt_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查是否需要修复（查找序号、时间戳和文本在同一行的情况）
        # 格式示例：1 00:00:00,000 --> 00:00:06,260 こんにちは。
        import re
        pattern = r'^(\d+)\s+(\d{2}:\d{2}:\d{2},\d{3}\s*-->\s*\d{2}:\d{2}:\d{2},\d{3})\s+(.+)$'

        needs_fix = False
        for line in content.split('\n'):
            if re.match(pattern, line.strip()):
                needs_fix = True
                break

        if not needs_fix:
            return False

        # 修复格式
        fixed_lines = []
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                fixed_lines.append('')
                continue

            # 检查是否是序号、时间戳和文本在同一行的格式
            match = re.match(pattern, line)
            if match:
                seq_num = match.group(1)
                timestamp = match.group(2)
                text = match.group(3)

                # 分离到不同行
                fixed_lines.append(seq_num)
                fixed_lines.append(timestamp)
                fixed_lines.append(text)
                fixed_lines.append('')  # 空行分隔
            else:
                # 如果不是要修复的格式，保持原样
                fixed_lines.append(line)

        # 写回文件
        with open(srt_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(fixed_lines))

        return True
    except Exception as e:
        print(f"修复SRT格式时出错: {e}")
        return False

def get_config_styles(log_func=None):
    """获取ASS样式配置

    从配置文件中读取ASS字幕样式，如果配置文件不存在则创建默认配置。

    Args:
        log_func: 日志记录函数（可选）

    Returns:
        dict: 包含kor、chn、jpn样式的字典
    """
    config_path = get_config_path()
    styles = {"kor": DEFAULT_KOR_STYLE, "chn": DEFAULT_CHN_STYLE, "jpn": DEFAULT_JPN_STYLE}

    if not os.path.exists(config_path):
        try:
            config = configparser.ConfigParser(interpolation=None)
            # 创建各种语言组合的配置节
            config["Srt2Ass_kor_chn"] = {
                "kor": DEFAULT_KOR_STYLE,
                "chn": DEFAULT_CHN_STYLE
            }
            config["Srt2Ass_jpn_chn"] = {
                "jpn": DEFAULT_JPN_STYLE,
                "chn": DEFAULT_CHN_STYLE
            }
            config["Srt2Ass_eng_chn"] = {
                "eng": DEFAULT_KOR_STYLE,  # 使用kor样式作为eng的默认
                "chn": DEFAULT_CHN_STYLE
            }
            config["Srt2Ass_kor_jpn"] = {
                "kor": DEFAULT_KOR_STYLE,
                "jpn": DEFAULT_JPN_STYLE
            }
            with open(config_path, 'w', encoding='utf-8-sig') as cf:
                config.write(cf)
        except:
            pass
    else:
        try:
            config = configparser.ConfigParser(interpolation=None)
            config.read(config_path, encoding='utf-8-sig')

            # 从各个配置节读取样式
            if "Srt2Ass_kor_chn" in config:
                styles["kor"] = config["Srt2Ass_kor_chn"].get("kor", DEFAULT_KOR_STYLE)
                styles["chn"] = config["Srt2Ass_kor_chn"].get("chn", DEFAULT_CHN_STYLE)
            if "Srt2Ass_jpn_chn" in config:
                styles["jpn"] = config["Srt2Ass_jpn_chn"].get("jpn", DEFAULT_JPN_STYLE)
            if "Srt2Ass_kor_jpn" in config:
                # 优先使用 kor_jpn 配置节中的样式
                styles["kor"] = config["Srt2Ass_kor_jpn"].get("kor", styles.get("kor", DEFAULT_KOR_STYLE))
                styles["jpn"] = config["Srt2Ass_kor_jpn"].get("jpn", styles.get("jpn", DEFAULT_JPN_STYLE))

            # 确保 [Srt2Ass_kor_jpn] 配置节存在
            if "Srt2Ass_kor_jpn" not in config:
                config["Srt2Ass_kor_jpn"] = {
                    "kor": DEFAULT_KOR_STYLE,
                    "jpn": DEFAULT_JPN_STYLE
                }
                # 保存更新后的配置
                with open(config_path, 'w', encoding='utf-8-sig') as cf:
                    config.write(cf)
        except:
            pass

    return styles

def run_ass_task(target_dir, styles, log_func, progress_bar, root, output_dir=None, stop_flag=[False]):
    """
    运行SRT转ASS转换任务
    
    扫描目标目录，匹配双语字幕文件，转换为ASS格式，并归档原始SRT文件。
    
    Args:
        target_dir: 目标目录
        styles: 样式配置字典
        log_func: 日志记录函数
        progress_bar: 进度条信号
        root: 根窗口
        output_dir: 输出目录（可选）
        stop_flag: 停止标志
    """
    # 路径自动纠偏
    if log_func: 
        log_func(f"🔍 初始选择路径: {target_dir.replace('/', '\\')}")
    
    current_dir_name = os.path.basename(target_dir).lower()
    if current_dir_name in ['script', 'srt']:
        if not any(f.lower().endswith('.srt') for f in os.listdir(target_dir)):
            target_dir = os.path.dirname(target_dir)

    # 样式与头信息准备
    ini_styles = get_config_styles(log_func)

    # 根据传入的 styles 参数确定当前字体方案
    # 可能的方案：
    # - kor_chn: 韩上中下（styles 包含 kor 和 chn）
    # - kor_jpn: 韩上日下（styles 包含 kor 和 jpn）
    # - jpn_chn: 日上中下（styles 包含 jpn 和 chn）
    # - eng_chn: 英上中下（styles 包含 eng 和 chn）
    style_keys = list(styles.keys())
    
    # 确定字体方案
    if "kor" in styles and "jpn" in styles:
        merge_mode = "kor_jpn"
        lang_key = "kor"
    elif "kor" in styles and "chn" in styles:
        merge_mode = "kor_chn"
        lang_key = "kor"
    elif "jpn" in styles and "chn" in styles:
        merge_mode = "jpn_chn"
        lang_key = "jpn"
    elif "eng" in styles and "chn" in styles:
        merge_mode = "eng_chn"
        lang_key = "eng"
    else:
        # 默认使用 kor_chn
        merge_mode = "kor_chn"
        lang_key = "kor"

    # 准备各种样式
    l_k = styles.get(lang_key) if styles and styles.get(lang_key) else ini_styles.get(lang_key, ini_styles.get("kor", ""))
    l_c = styles.get("chn") if styles and styles.get("chn") else ini_styles["chn"]
    l_j = styles.get("jpn") if styles and styles.get("jpn") else ini_styles["jpn"]

    # 提取样式名称
    style_name_k = l_k.split(',')[0].replace("Style:", "").strip()
    style_name_c = l_c.split(',')[0].replace("Style:", "").strip()
    style_name_j = l_j.split(',')[0].replace("Style:", "").strip()

    # 生成ASS头信息（包含所有可能的样式）
    hdr = (f"[Script Info]\nScriptType: v4.00+\nWrapStyle: 0\nScaledBorderAndShadow: yes\n\n"
           f"[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
           f"OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, "
           f"Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
           f"{l_k}\n{l_c}\n{l_j}\n\n"
           f"[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text")

    # 扫描任务
    all_f = os.listdir(target_dir)
    # 排除视频自带的 .DUAL. 干扰，只认真正的 .dual.srt 后缀
    duals = [f for f in all_f if f.lower().endswith('.dual.srt')]
    srts = [f for f in all_f if f.lower().endswith('.srt') and f not in duals]

    tasks = []
    EP_PATTERN = re.compile(r'[Ss](\d{2})[Ee](\d{2})')
    gps = {}

    # 先按集数分组
    for f in srts:
        m = EP_PATTERN.search(f)
        if m:
            ep = f"S{m.group(1)}E{m.group(2)}"
            gps.setdefault(ep, []).append(f)

    # 处理有集数标记的文件
    for ep, fl in gps.items():
        kor = [f for f in fl if '[kor]' in f.lower() or '[ko]' in f.lower()]
        jpn = [f for f in fl if '[jpn]' in f.lower() or '[jp]' in f.lower()]
        eng = [f for f in fl if '[eng]' in f.lower() or '[en]' in f.lower()]
        chi = [f for f in fl if '[chi]' in f.lower()]
        
        if not chi:
            chi = [f for f in fl if any(x in f.lower() for x in ['chn', 'chs', 'cht', 'chi'])]
        
        # 在严格匹配模式下，不自动推断语言标签
        # 只使用明确的语言标签进行匹配

        # 根据字体方案进行严格匹配
        if merge_mode == "kor_jpn":
            # 韩上日下：必须有 kor 和 jpn
            if not kor:
                if log_func:
                    log_func(f"❌ 集数 {ep} 缺少韩语字幕")
            if not jpn:
                if log_func:
                    log_func(f"❌ 集数 {ep} 缺少日语字幕")
            if kor and jpn:
                tasks.append({
                    "type": "merge", "ep": ep,
                    "chi_name": jpn[0], "chi_path": os.path.join(target_dir, jpn[0]),
                    "oth_name": kor[0], "oth_path": os.path.join(target_dir, kor[0]),
                    "lang_type": "kor_jpn"
                })
                if log_func:
                    log_func(f"✅ 集数 {ep} 成功匹配（韩日双语）")
        
        elif merge_mode == "kor_chn":
            # 韩上中下：必须有 kor 和 chn
            if not kor:
                if log_func:
                    log_func(f"❌ 集数 {ep} 缺少韩语字幕")
            if not chi:
                if log_func:
                    log_func(f"❌ 集数 {ep} 缺少中文字幕")
            if kor and chi:
                tasks.append({
                    "type": "merge", "ep": ep,
                    "chi_name": chi[0], "chi_path": os.path.join(target_dir, chi[0]),
                    "oth_name": kor[0], "oth_path": os.path.join(target_dir, kor[0])
                })
                if log_func:
                    log_func(f"✅ 集数 {ep} 成功匹配")
        
        elif merge_mode == "jpn_chn":
            # 日上中下：必须有 jpn 和 chn
            if not jpn:
                if log_func:
                    log_func(f"❌ 集数 {ep} 缺少日语字幕")
            if not chi:
                if log_func:
                    log_func(f"❌ 集数 {ep} 缺少中文字幕")
            if jpn and chi:
                tasks.append({
                    "type": "merge", "ep": ep,
                    "chi_name": chi[0], "chi_path": os.path.join(target_dir, chi[0]),
                    "oth_name": jpn[0], "oth_path": os.path.join(target_dir, jpn[0])
                })
                if log_func:
                    log_func(f"✅ 集数 {ep} 成功匹配")
        
        elif merge_mode == "eng_chn":
            # 英上中下：必须有 eng 和 chn
            if not eng:
                if log_func:
                    log_func(f"❌ 集数 {ep} 缺少英语字幕")
            if not chi:
                if log_func:
                    log_func(f"❌ 集数 {ep} 缺少中文字幕")
            if eng and chi:
                tasks.append({
                    "type": "merge", "ep": ep,
                    "chi_name": chi[0], "chi_path": os.path.join(target_dir, chi[0]),
                    "oth_name": eng[0], "oth_path": os.path.join(target_dir, eng[0])
                })
                if log_func:
                    log_func(f"✅ 集数 {ep} 成功匹配")

    # 处理没有集数标记的文件（直接按语言标签匹配）
    files_without_ep = [f for f in srts if not EP_PATTERN.search(f)]
    if files_without_ep:
        # 按基础文件名分组（去除语言标签和扩展名）
        name_groups = {}
        for f in files_without_ep:
            # 提取基础名称：去除 [chn]、[kor] 等语言标签
            base_name = re.sub(r'\[.*?\]', '', f, flags=re.IGNORECASE).strip()
            name_groups.setdefault(base_name, []).append(f)

        # 对每个基础名称组进行匹配
        for base_name, fl in name_groups.items():
            if len(fl) >= 2:  # 至少需要两个文件
                # 识别各种语言字幕文件
                kor = [f for f in fl if '[kor]' in f.lower() or '[ko]' in f.lower()]
                jpn = [f for f in fl if '[jpn]' in f.lower() or '[jp]' in f.lower()]
                eng = [f for f in fl if '[eng]' in f.lower() or '[en]' in f.lower()]
                chi_candidates = [f for f in fl if '[chn]' in f.lower() or '[chi]' in f.lower() or '[chs]' in f.lower() or '[cht]' in f.lower()]

                # 如果同时存在 [chs] 和 [cht]，优先选择 [chs]
                if chi_candidates:
                    has_chs = any('[chs]' in f.lower() for f in chi_candidates)
                    has_cht = any('[cht]' in f.lower() for f in chi_candidates)
                    if has_chs and has_cht:
                        chi = [f for f in chi_candidates if '[chs]' in f.lower()]
                    else:
                        chi = chi_candidates
                else:
                    chi = []

                # 根据字体方案进行严格匹配
                if merge_mode == "kor_jpn":
                    # 韩上日下：必须有 kor 和 jpn
                    if not kor:
                        if log_func:
                            log_func(f"❌ 文件 '{base_name}' 缺少韩语字幕")
                    if not jpn:
                        if log_func:
                            log_func(f"❌ 文件 '{base_name}' 缺少日语字幕")
                    if kor and jpn:
                        tasks.append({
                            "type": "merge", "ep": base_name,
                            "chi_name": jpn[0], "chi_path": os.path.join(target_dir, jpn[0]),
                            "oth_name": kor[0], "oth_path": os.path.join(target_dir, kor[0]),
                            "lang_type": "kor_jpn"
                        })
                        if log_func:
                            log_func(f"✅ 文件 '{base_name}' 成功匹配（韩日双语）")
                
                elif merge_mode == "kor_chn":
                    # 韩上中下：必须有 kor 和 chn
                    if not kor:
                        if log_func:
                            log_func(f"❌ 文件 '{base_name}' 缺少韩语字幕")
                    if not chi:
                        if log_func:
                            log_func(f"❌ 文件 '{base_name}' 缺少中文字幕")
                    if kor and chi:
                        tasks.append({
                            "type": "merge", "ep": base_name,
                            "chi_name": chi[0], "chi_path": os.path.join(target_dir, chi[0]),
                            "oth_name": kor[0], "oth_path": os.path.join(target_dir, kor[0])
                        })
                        if log_func:
                            log_func(f"✅ 文件 '{base_name}' 成功匹配")
                
                elif merge_mode == "jpn_chn":
                    # 日上中下：必须有 jpn 和 chn
                    if not jpn:
                        if log_func:
                            log_func(f"❌ 文件 '{base_name}' 缺少日语字幕")
                    if not chi:
                        if log_func:
                            log_func(f"❌ 文件 '{base_name}' 缺少中文字幕")
                    if jpn and chi:
                        tasks.append({
                            "type": "merge", "ep": base_name,
                            "chi_name": chi[0], "chi_path": os.path.join(target_dir, chi[0]),
                            "oth_name": jpn[0], "oth_path": os.path.join(target_dir, jpn[0])
                        })
                        if log_func:
                            log_func(f"✅ 文件 '{base_name}' 成功匹配")
                
                elif merge_mode == "eng_chn":
                    # 英上中下：必须有 eng 和 chn
                    if not eng:
                        if log_func:
                            log_func(f"❌ 文件 '{base_name}' 缺少英语字幕")
                    if not chi:
                        if log_func:
                            log_func(f"❌ 文件 '{base_name}' 缺少中文字幕")
                    if eng and chi:
                        tasks.append({
                            "type": "merge", "ep": base_name,
                            "chi_name": chi[0], "chi_path": os.path.join(target_dir, chi[0]),
                            "oth_name": eng[0], "oth_path": os.path.join(target_dir, eng[0])
                        })
                        if log_func:
                            log_func(f"✅ 文件 '{base_name}' 成功匹配")

    total = len(tasks)
    if total == 0:
        log_func("⚠️ 未找到可配对的字幕。")
        return

    # 执行处理
    base_output = output_dir if output_dir else target_dir
    
    for i, t in enumerate(tasks):
        # 检查停止标志
        if stop_flag[0]:
            return

        try:
            # 修复SRT文件格式（如果需要）
            fix_srt_format(t["oth_path"])
            fix_srt_format(t["chi_path"])

            # 加载与清洗字幕文件
            s1, s2 = pysubs2.load(t["oth_path"]), pysubs2.load(t["chi_path"])
            evs = []

            # 根据任务类型选择样式
            lang_type = t.get("lang_type", "normal")  # 默认为正常的中外字幕

            # 根据字体方案确定文件名后缀
            if lang_type == "kor_jpn":
                file_suffix = "[kor_jpn]"
            elif merge_mode == "kor_chn":
                file_suffix = "[kor_chn]"
            elif merge_mode == "jpn_chn":
                file_suffix = "[jpn_chn]"
            elif merge_mode == "eng_chn":
                file_suffix = "[eng_chn]"
            else:
                file_suffix = ""

            if lang_type == "kor_jpn":
                # 韩日字幕：韩语在上（oth_path），日语在下（chi_path）
                for l in s1:  # 韩语字幕
                    if stop_flag[0]:
                        return

                    c = clean_subtitle_text_ass(l.text)
                    if c:
                        st = pysubs2.time.ms_to_str(l.start, fractions=True).replace(',','.')[:-1]
                        et = pysubs2.time.ms_to_str(l.end, fractions=True).replace(',','.')[:-1]
                        evs.append(f"Dialogue: 0,{st},{et},{style_name_k},,0,0,0,,{c}")

                for l in s2:  # 日语字幕
                    if stop_flag[0]:
                        return

                    c = clean_subtitle_text_ass(l.text)
                    if c:
                        st = pysubs2.time.ms_to_str(l.start, fractions=True).replace(',','.')[:-1]
                        et = pysubs2.time.ms_to_str(l.end, fractions=True).replace(',','.')[:-1]
                        evs.append(f"Dialogue: 0,{st},{et},{style_name_j},,0,0,0,,{c}")
            else:
                # 正常的中外字幕：外语在上（oth_path），中文在下（chi_path）
                for l in s1:  # 外语字幕
                    if stop_flag[0]:
                        return

                    c = clean_subtitle_text_ass(l.text)
                    if c:
                        st = pysubs2.time.ms_to_str(l.start, fractions=True).replace(',','.')[:-1]
                        et = pysubs2.time.ms_to_str(l.end, fractions=True).replace(',','.')[:-1]
                        evs.append(f"Dialogue: 0,{st},{et},{style_name_k},,0,0,0,,{c}")

                for l in s2:  # 中文字幕
                    if stop_flag[0]:
                        return

                    c = clean_subtitle_text_ass(l.text)
                    if c:
                        st = pysubs2.time.ms_to_str(l.start, fractions=True).replace(',','.')[:-1]
                        et = pysubs2.time.ms_to_str(l.end, fractions=True).replace(',','.')[:-1]
                        evs.append(f"Dialogue: 0,{st},{et},{style_name_c},,0,0,0,,{c}")

            # 生成ASS文件
            clean_name = re.split(r'_track\d+', t["oth_name"], flags=re.IGNORECASE)[0].rstrip('._ ')
            # 去除原有的语言标签（如 [kor]、[jpn]、[chn] 等）和 .srt 后缀
            clean_name = re.sub(r'\[.*?\]', '', clean_name, flags=re.IGNORECASE)
            clean_name = re.sub(r'\.srt$', '', clean_name, flags=re.IGNORECASE)
            # 去除末尾的点和空格
            clean_name = clean_name.rstrip('. ')
            # 添加新的语言标签后缀（前面加点）
            clean_name = clean_name + "." + file_suffix + ".ass"
            save_path_ass = get_organized_path(base_output, clean_name)

            with open(save_path_ass, 'w', encoding='utf-8-sig') as f:
                f.write(hdr + "\n" + "\n".join(evs))

            log_func(f"📝 已生成: {os.path.basename(save_path_ass)}")

            # 归档原始SRT文件
            archive_dir_chi = get_organized_path(base_output, t["chi_name"])
            archive_dir_oth = get_organized_path(base_output, t["oth_name"])
            
            shutil.move(t["chi_path"], archive_dir_chi)
            shutil.move(t["oth_path"], archive_dir_oth)

        except Exception as e:
            log_func(f"❌ 处理 {t.get('ep')} 时出错: {e}")

        # 更新进度，支持不同类型的进度回调
        try:
            # 尝试PyQt的信号方式（progress_bar是信号对象）
            progress_bar.emit(int((i + 1) / total * 100))
        except AttributeError:
            try:
                # 尝试直接调用方式（progress_bar是emit方法本身）
                progress_bar(int((i + 1) / total * 100))
            except Exception as e:
                pass
    
    log_func("📂 任务完成：.ass 已生成在根目录，原始 .srt 已归档至 srt/ 文件夹。")