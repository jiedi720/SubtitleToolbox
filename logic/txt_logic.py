import os
# [修改] 导入 get_organized_path
from utils import generate_output_name, get_save_path, get_organized_path, smart_group_files, find_files_recursively, parse_subtitle_to_list, clean_filename_title

def run_txt_creation_task(target_dir, log_func, progress_bar, root, batch_size=0, output_dir=None):
    log_func(f"[TXT] 扫描: {target_dir}")
    files = find_files_recursively(target_dir, ('.srt', '.vtt', '.ass', '.smi'))
    
    if not files: return log_func(f"❌ 未找到字幕文件")
    if batch_size > 0: log_func(f"分组: {batch_size} 集/组")

    file_groups = smart_group_files(files, batch_size)
    progress_bar["maximum"] = len(files)
    count = 0

    # 确定基础输出目录 (script 或 自定义)
    base_output_dir = output_dir if output_dir else os.path.join(target_dir, "script")

    for group in file_groups:
        if not group: continue
        
        out_name = generate_output_name([os.path.basename(f) for f in group], ".txt")
        
        # [修改] 使用自动分类路径 (存入 txt 子文件夹)
        out_path = get_organized_path(base_output_dir, out_name)
        
        log_func(f"生成: {out_name}")

        try:
            with open(out_path, 'w', encoding='utf-8') as outfile:
                for fp in group:
                    title = clean_filename_title(os.path.basename(fp))
                    outfile.write(f"{'='*50}\n【{title}】\n{'='*50}\n\n")
                    
                    content_list = parse_subtitle_to_list(fp)
                    if not content_list:
                        outfile.write("[内容为空或解析失败]\n\n")
                    else:
                        for time_str, text in content_list:
                            outfile.write(f"[{time_str}]  {text}\n")
                    outfile.write("\n\n")
                    
                    count += 1
                    progress_bar["value"] = count
                    root.update_idletasks()
        except Exception as e:
            log_func(f"❌ 失败: {e}")

    log_func(f"✅ TXT 任务完成！保存目录: {base_output_dir}\\txt")
    progress_bar["value"] = 0

def run_txt_merge_task(target_dir, log_func, progress_bar, root, output_dir=None):
    # [修改] 合并时去 txt 子目录找
    base_dir = output_dir if (output_dir and os.path.exists(output_dir)) else os.path.join(target_dir, "script")
    search_dir = os.path.join(base_dir, "txt")
    
    if not os.path.exists(search_dir):
        # 兼容性: 如果 txt 文件夹不存在，回退到 base_dir 找找看
        search_dir = base_dir
    
    log_func(f"正在搜索 TXT 文件: {search_dir}")
    files = [os.path.join(search_dir, f) for f in os.listdir(search_dir) if f.lower().endswith('.txt') and "全剧本" not in f]
    files.sort()
    
    if not files: return log_func("未找到 .txt 文件")
    
    out_path = os.path.join(search_dir, "全剧本.txt")
    
    try:
        with open(out_path, 'w', encoding='utf-8') as outfile:
            for i, f in enumerate(files):
                outfile.write(f"{'='*30}\n{os.path.basename(f)}\n{'='*30}\n\n")
                try:
                    with open(f, 'r', encoding='utf-8') as infile: outfile.write(infile.read() + "\n\n")
                except: pass
                progress_bar["value"] = i+1
                root.update_idletasks()
        log_func(f"✅ 合并完成: {out_path}")
    except Exception as e: log_func(f"❌ 错误: {e}")
    finally: progress_bar["value"] = 0