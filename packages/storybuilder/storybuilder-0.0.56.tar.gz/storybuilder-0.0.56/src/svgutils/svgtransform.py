import xml.etree.ElementTree as ET
import re
import sys
import os
import argparse
import glob

def extract_translate_values(transform_str):
    """
    只提取 translate 变换值，忽略其他变换
    
    Args:
        transform_str (str): Transform 属性字符串
        
    Returns:
        tuple: (tx, ty) 平移值 或 None
    """
    if not transform_str:
        return None
    
    # 只匹配 translate(x y) 或 translate(x,y)
    translate_pattern = r'translate\(([-\d.]+)(?:,|\s+)([-\d.]+)\)'
    translate_match = re.search(translate_pattern, transform_str)
    
    if translate_match:
        return float(translate_match.group(1)), float(translate_match.group(2))
    
    return None

def find_g_element(root):
    """
    Find g element with or without namespace.
    
    Args:
        root: Root element of the SVG
        
    Returns:
        element: First g element found or None
    """
    # Try with SVG namespace
    g_element = root.find('.//{http://www.w3.org/2000/svg}g')
    if g_element is not None:
        return g_element
        
    # Try without namespace
    g_element = root.find('.//g')
    return g_element

def remove_namespace_prefix(root):
    """
    Remove namespace prefixes from all elements and attributes.
    
    Args:
        root: Root element of the XML tree
    """
    # Remove namespace prefix from element tags
    for elem in root.iter():
        if '}' in elem.tag:
            elem.tag = elem.tag.split('}', 1)[1]
    
    # Store the original SVG namespace
    svg_ns = {'xmlns': 'http://www.w3.org/2000/svg'}
    
    # Clear other namespaces but keep the SVG namespace
    if root.tag.lower() == 'svg':
        # Remove all namespaces
        for key in list(root.attrib.keys()):
            if key.startswith('xmlns:'):
                del root.attrib[key]
        # Ensure SVG namespace is present
        root.attrib.update(svg_ns)

def format_number(num):
    """
    格式化数字，保留两位小数并移除尾随的零
    
    Args:
        num (float): 要格式化的数字
        
    Returns:
        str: 格式化后的数字字符串
    """
    # 先格式化为两位小数
    formatted = f"{num:.2f}"
    # 如果有小数点
    if '.' in formatted:
        # 移除尾随的零
        formatted = formatted.rstrip('0')
        # 如果只剩小数点，移除它
        formatted = formatted.rstrip('.')
    return formatted

def format_path_data(path_data):
    """
    格式化路径数据，移除命令字母周围的空格
    
    Args:
        path_data (str): 原始路径数据
        
    Returns:
        str: 格式化后的路径数据
    """
    # 将命令字母和数字分开
    parts = []
    current_number = ''
    
    for char in path_data:
        if char.isalpha():
            if current_number:
                parts.append(current_number.strip())
                current_number = ''
            parts.append(char)
        elif char.isspace() or char == ',':
            if current_number:
                parts.append(current_number.strip())
                current_number = ''
        else:
            current_number += char
    
    if current_number:
        parts.append(current_number.strip())
    
    # 重新组合路径数据，移除命令字母周围的空格
    formatted = ''
    i = 0
    while i < len(parts):
        if parts[i] in 'MmLlCcZzHhVvSsQqTtAa':
            # 添加命令字母，不加空格
            formatted += parts[i]
            i += 1
            # 添加该命令的参数，用空格分隔
            while i < len(parts) and not parts[i].isalpha():
                formatted += parts[i]
                if i + 1 < len(parts) and not parts[i + 1].isalpha():
                    formatted += ' '
                i += 1
        else:
            formatted += parts[i]
            if i + 1 < len(parts):
                formatted += ' '
            i += 1
    
    return formatted

def process_element(element, tx, ty):
    """处理单个元素的变换"""
    if element.tag.endswith('}path') or element.tag == 'path':
        d_attr = element.get('d')
        if not d_attr:
            return
            
        # 获取元素自身的transform
        element_transform = element.get('transform')
        if element_transform:
            # 提取元素自身的平移值
            element_translation = extract_translate_values(element_transform)
            if element_translation:
                # 合并平移值
                tx += element_translation[0]
                ty += element_translation[1]
            # 移除元素的transform属性
            element.attrib.pop('transform')

        # 将路径数据分割成命令和数字
        parts = []
        current_number = ''
        
        for char in d_attr:
            if char.isalpha():
                if current_number:
                    parts.append(('N', float(current_number)))
                    current_number = ''
                parts.append(('C', char))
            elif char.isspace() or char == ',':
                if current_number:
                    parts.append(('N', float(current_number)))
                    current_number = ''
            else:
                current_number += char
        
        if current_number:
            parts.append(('N', float(current_number)))

        # 应用变换
        new_path = []
        i = 0
        current_command = ''
        
        while i < len(parts):
            type_, value = parts[i]
            
            if type_ == 'C':  # 命令
                new_path.append(value)
                current_command = value
            elif type_ == 'N':  # 数字
                if current_command in 'mMlL':  # 移动和直线命令
                    if i + 1 < len(parts) and parts[i+1][0] == 'N':
                        x = value + tx
                        y = parts[i+1][1] + ty
                        new_path.extend([format_number(x), format_number(y)])
                        i += 1
                elif current_command in 'hH':  # 水平线命令
                    x = value + tx
                    new_path.append(format_number(x))
                elif current_command in 'vV':  # 垂直线命令
                    y = value + ty
                    new_path.append(format_number(y))
                elif current_command in 'cC':  # 三次贝塞尔曲线
                    if i + 5 < len(parts) and all(p[0] == 'N' for p in parts[i:i+6]):
                        x1 = value + tx
                        y1 = parts[i+1][1] + ty
                        x2 = parts[i+2][1] + tx
                        y2 = parts[i+3][1] + ty
                        x = parts[i+4][1] + tx
                        y = parts[i+5][1] + ty
                        new_path.extend([format_number(x1), format_number(y1),
                                       format_number(x2), format_number(y2),
                                       format_number(x), format_number(y)])
                        i += 5
                elif current_command in 'sSqQ':  # 平滑曲线和二次贝塞尔
                    if i + 3 < len(parts) and all(p[0] == 'N' for p in parts[i:i+4]):
                        x1 = value + tx
                        y1 = parts[i+1][1] + ty
                        x = parts[i+2][1] + tx
                        y = parts[i+3][1] + ty
                        new_path.extend([format_number(x1), format_number(y1),
                                       format_number(x), format_number(y)])
                        i += 3
                elif current_command in 'aA':  # 圆弧命令
                    if i + 6 < len(parts) and all(p[0] == 'N' for p in parts[i:i+7]):
                        rx = value
                        ry = parts[i+1][1]
                        angle = parts[i+2][1]
                        large_arc = parts[i+3][1]
                        sweep = parts[i+4][1]
                        x = parts[i+5][1] + tx
                        y = parts[i+6][1] + ty
                        new_path.extend([format_number(rx), format_number(ry),
                                       format_number(angle),
                                       str(int(large_arc)), str(int(sweep)),
                                       format_number(x), format_number(y)])
                        i += 6
                elif current_command in 'zZ':  # 闭合路径
                    pass
                else:
                    # 如果没有当前命令，假设它是一个隐式的线命令
                    if i + 1 < len(parts) and parts[i+1][0] == 'N':
                        x = value + tx
                        y = parts[i+1][1] + ty
                        new_path.extend([format_number(x), format_number(y)])
                        i += 1
            i += 1

        # 更新路径数据
        element.set('d', ' '.join(str(x) for x in new_path))

def remove_duplicate_paths(root):
    """
    移除重复的路径元素，保留最上层的路径
    
    Args:
        root: SVG的根元素
    """
    # 收集所有路径及其数据
    all_paths = []  # 所有路径的列表，保持顺序
    path_data = {}  # key: 路径元素, value: 标准化的路径数据
    
    # 遍历所有路径元素
    for path in root.findall('.//path') + root.findall('.//{http://www.w3.org/2000/svg}path'):
        d = path.get('d')
        if d:
            # 标准化路径数据（移除多余空格和格式化数字）
            if isinstance(d, dict):
                normalized_d = format_path_data(' '.join(d['d'].split()))
            else:
                normalized_d = format_path_data(' '.join(d.split()))
            all_paths.append(path)
            path_data[path] = normalized_d
    
    print(f"Initial path count: {len(all_paths)}")
    
    # 找出要保留的路径（每个相同数据只保留最后一个）
    paths_to_keep = {}  # key: 标准化的路径数据, value: 要保留的路径元素
    for path in reversed(all_paths):  # 从后向前遍历，这样自动保留最后出现的路径
        normalized_d = path_data[path]
        if normalized_d not in paths_to_keep:
            paths_to_keep[normalized_d] = path
    
    # 移除不需要保留的路径
    removed_count = 0
    for path in all_paths:
        normalized_d = path_data[path]
        if paths_to_keep[normalized_d] != path:  # 如果不是要保留的那个路径
            # 找到父元素
            for parent in root.iter():
                if path in list(parent):
                    try:
                        parent.remove(path)
                        removed_count += 1
                        print(f"Removed duplicate path: {normalized_d[:50]}...")
                        break
                    except:
                        print(f"Warning: Failed to remove path")
    
    if removed_count > 0:
        print(f"Total removed duplicate paths: {removed_count}")

def process_g_elements(root):
    """处理SVG中的g元素

    Args:
        root: SVG根元素
    """
    # 查找所有g元素
    for g in root.findall('.//g'):
        transform = g.get('transform', '')
        
        # 处理translate变换
        translate_match = re.search(r'translate\(([-\d.]+)[,\s]+([-\d.]+)\)', transform)
        if translate_match:
            tx = float(translate_match.group(1))
            ty = float(translate_match.group(2))
            
            # 更新子元素
            for child in g:
                child_transform = child.get('transform', '')
                
                # 如果子元素已有matrix变换
                matrix_match = re.search(r'matrix\(([-\d.\s,]+)\)', child_transform)
                if matrix_match:
                    values = [float(x) for x in matrix_match.group(1).split()]
                    # 应用平移到matrix的最后两个值
                    values[4] += tx
                    values[5] += ty
                    new_transform = f"matrix({' '.join(str(v) for v in values)})"
                    child.set('transform', new_transform)
                else:
                    # 如果子元素没有transform，添加translate
                    child.set('transform', f"translate({tx},{ty})")
            
            # 移除g元素的transform
            g.attrib.pop('transform')

        # 处理scale变换
        scale_match = re.search(r'scale\(([-\d.]+)(?:[,\s]+([-\d.]+))?\)', transform)
        if scale_match:
            sx = float(scale_match.group(1))
            sy = float(scale_match.group(2)) if scale_match.group(2) else sx
            
            # 更新子元素
            for child in g:
                child_transform = child.get('transform', '')
                
                # 如果子元素已有matrix变换
                matrix_match = re.search(r'matrix\(([-\d.\s,]+)\)', child_transform)
                if matrix_match:
                    values = [float(x) for x in matrix_match.group(1).split()]
                    # 应用缩放到matrix的值
                    values[0] *= sx
                    values[1] *= sy
                    values[2] *= sx
                    values[3] *= sy
                    values[4] *= sx
                    values[5] *= sy
                    new_transform = f"matrix({' '.join(str(v) for v in values)})"
                    child.set('transform', new_transform)
                else:
                    # 如果子元素没有transform，添加scale
                    child.set('transform', f"scale({sx},{sy})")
            
            # 移除g元素的transform
            g.attrib.pop('transform')

def apply_translate_from_g(svg_path, output_path):
    """
    Extracts translate transform from all <g> elements and applies them to child elements.
    Handles SVG files with or without namespace.
    
    Args:
        svg_path (str): Path to input SVG file
        output_path (str): Path where modified SVG will be saved
    """
    # Parse the SVG file
    tree = ET.parse(svg_path)
    root = tree.getroot()
    
    # 记录原始内容
    original_content = ET.tostring(root, encoding='unicode')
    
    # 处理所有g元素的变换
    process_g_elements(root)
    
    # Remove namespace prefixes
    remove_namespace_prefix(root)
    
    # 在写入文件前添加最终路径计数
    final_path_count = len(root.findall('.//path')) + len(root.findall('.//{http://www.w3.org/2000/svg}path'))
    print(f"Final path count: {final_path_count}")
    
    # 获取处理后的内容
    processed_content = ET.tostring(root, encoding='unicode')
    processed_content = processed_content.replace('ns0:', '').replace(':ns0', '')
    
    # 只有当内容真正发生变化时才写入文件
    if processed_content != original_content:
        # Custom write function to output clean XML
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(processed_content)
        print(f"File modified: {output_path}")
    else:
        print(f"No changes needed for: {output_path}")

def process_folder(input_folder, output_folder=None, recursive=True):
    """
    Process all SVG files in a folder.
    
    Args:
        input_folder (str): Input folder path
        output_folder (str, optional): Output folder path. If not provided, will overwrite input files
        recursive (bool): Whether to process subfolders recursively
    
    Returns:
        dict: Processing statistics
    """
    stats = {
        'total_files': 0,
        'successful': 0,
        'failed': 0,
        'failed_files': []
    }
    
    # ���指定了输文���夹，确保它存在
    if output_folder:
        os.makedirs(output_folder, exist_ok=True)
    
    def process_file(file_path):
        if not file_path.lower().endswith('.svg'):
            return
            
        stats['total_files'] += 1
        
        # 确定输出路径
        if output_folder:
            rel_path = os.path.relpath(file_path, input_folder)
            out_path = os.path.join(output_folder, rel_path)
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
        else:
            out_path = file_path
        
        try:
            apply_translate_from_g(file_path, out_path)
            stats['successful'] += 1
            print(f"Successfully processed: {file_path}")
        except Exception as e:
            stats['failed'] += 1
            stats['failed_files'].append(file_path)
            print(f"Failed to process {file_path}: {str(e)}")
    
    # 遍历文件夹
    if recursive:
        for root, _, files in os.walk(input_folder):
            for file in files:
                process_file(os.path.join(root, file))
    else:
        for file in os.listdir(input_folder):
            process_file(os.path.join(input_folder, file))
    
    return stats

def process_folder_with_action(input_folder, output_folder, recursive, action_func):
    """
    通用的文件夹处理函数
    
    Args:
        input_folder (str): 输入文件夹路径
        output_folder (str): 输出文件夹路径
        recursive (bool): 是否递归处理子文件夹
        action_func (callable): 处理单个文件的函数
    """
    stats = {
        'total_files': 0,
        'successful': 0,
        'failed': 0,
        'failed_files': []
    }
    
    if output_folder:
        os.makedirs(output_folder, exist_ok=True)
    
    def process_file(file_path):
        if not file_path.lower().endswith('.svg'):
            return
            
        stats['total_files'] += 1
        
        if output_folder:
            rel_path = os.path.relpath(file_path, input_folder)
            out_path = os.path.join(output_folder, rel_path)
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
        else:
            out_path = file_path
        
        try:
            action_func(file_path, out_path)
            stats['successful'] += 1
            print(f"Successfully processed: {file_path}")
        except Exception as e:
            stats['failed'] += 1
            stats['failed_files'].append(file_path)
            print(f"Failed to process {file_path}: {str(e)}")
    
    if recursive:
        for root, _, files in os.walk(input_folder):
            for file in files:
                process_file(os.path.join(root, file))
    else:
        for file in os.listdir(input_folder):
            process_file(os.path.join(input_folder, file))
    
    return stats

def print_stats(stats):
    """打印处理统计信息"""
    print("\nProcessing Summary:")
    print(f"Total files: {stats['total_files']}")
    print(f"Successful: {stats['successful']}")
    print(f"Failed: {stats['failed']}")
    
    if stats['failed'] > 0:
        print("\nFailed files:")
        for file in stats['failed_files']:
            print(f"- {file}")

def circle_to_path(cx, cy, r):
    """
    将圆形转换为SVG路径命令
    
    Args:
        cx (float): 圆心x坐标
        cy (float): 圆心y坐标
        r (float): 半径
        
    Returns:
        str: SVG路径数据
    """
    # 使用四个贝塞尔曲线来近似一个圆
    # 魔术数字 0.552284749831 是为了使贝塞尔曲线最大程度接近圆形
    c = 0.552284749831
    cr = r * c
    
    return (
        f"M{cx-r},{cy} "  # 起点：左中
        f"C{cx-r},{cy-cr} {cx-cr},{cy-r} {cx},{cy-r} "  # 第一段：到上中
        f"C{cx+cr},{cy-r} {cx+r},{cy-cr} {cx+r},{cy} "  # 第二：到右中
        f"C{cx+r},{cy+cr} {cx+cr},{cy+r} {cx},{cy+r} "  # 第三段：到下中
        f"C{cx-cr},{cy+r} {cx-r},{cy+cr} {cx-r},{cy} "  # 第四段：回到起点
        f"Z"  # 闭合路径
    )

def convert_circle_to_path(element):
    """
    将circle元素转换为等效的path元素
    
    Args:
        element: circle元素
        
    Returns:
        element: 新的path元素
    """
    # 获取circle的属性
    cx = float(element.get('cx', '0').rstrip('px'))
    cy = float(element.get('cy', '0').rstrip('px'))
    r = float(element.get('r', '0').rstrip('px'))
    
    # 创建新的path元素
    path = ET.Element('path')
    
    # 复制所有属性
    for key, value in element.attrib.items():
        if key not in ['cx', 'cy', 'r']:
            path.set(key, value)
    
    # 设置路径数据
    path.set('d', circle_to_path(cx, cy, r))
    
    return path

def convert_circles(root):
    """
    换SVG中的所有circle元素为path元素
    
    Args:
        root: SVG的根元素
    """
    # 计数转换的圆形数量
    converted_count = 0
    
    # 查找所有circle元素（包含命名空间的和不包含的）
    circles = root.findall('.//circle') + root.findall('.//{http://www.w3.org/2000/svg}circle')
    
    if circles:
        print(f"Found {len(circles)} circle elements")
    
    for circle in circles:
        # 创建新的path元素
        path = convert_circle_to_path(circle)
        
        # 找到circle的父元素
        for parent in root.iter():
            if circle in list(parent):
                # 在相同位置插入新的path元素
                index = list(parent).index(circle)
                parent.insert(index, path)
                # 移除原始的circle元素
                parent.remove(circle)
                converted_count += 1
                break
    
    if converted_count > 0:
        print(f"Converted {converted_count} circle elements to paths")

def find_parent_and_index(root, element):
    """
    找元素的父元素和它在父元素中的索引
    
    Args:
        root: XML树的根元素
        element: 要查找的元素
        
    Returns:
        tuple: (parent_element, index) 或 (None, -1)
    """
    for parent in root.iter():
        if element in list(parent):
            return parent, list(parent).index(element)
    return None, -1

def flatten_nested_g(element, root, parent_tx=0, parent_ty=0):
    """
    递归处理嵌套的g元素，合并变换并移除不必要的g元素
    
    Args:
        element: 当前处理的元��
        root: SVG的根元素
        parent_tx: 父元素的x变换值
        parent_ty: 父元素的y变换值
    """
    # 处理当前元素的变换
    current_tx, current_ty = parent_tx, parent_ty
    
    # 处理g元素的变换
    if element.tag.endswith('}g') or element.tag == 'g':
        transform = element.get('transform')
        if transform:
            translation = extract_translate_values(transform)
            if translation:
                tx, ty = translation
                current_tx += tx
                current_ty += ty
                # 移除transform属性
                element.attrib.pop('transform')
    
    # 如果是路径元素，应用累积的变换
    if element.tag.endswith('}path') or element.tag == 'path':
        process_element(element, current_tx, current_ty)
    
    # 处理所有子元素
    for child in list(element):
        # 递归处理子元素，传递累积的变换值
        flatten_nested_g(child, root, current_tx, current_ty)

def extract_paths(root):
    """
    提取SVG中的所有路径元素
    
    Args:
        root: SVG的根元素
        
    Returns:
        list: 路径元素列表的深拷贝
    """
    paths = []
    for path in root.findall('.//path') + root.findall('.//{http://www.w3.org/2000/svg}path'):
        # 创建新的path元素
        new_path = ET.Element('path')
        # 复制所有属性
        for key, value in path.attrib.items():
            new_path.set(key, value)
        paths.append(new_path)
    return paths

def apply_paths(source_path, pattern, layer_position='top'):
    """
    将源SVG文件中的路径应用到匹配模式的所有文件上
    
    Args:
        source_path (str): 源SVG文件路径
        pattern (str): 目标文件匹配模
        layer_position (str): 'top' 或 'bottom'，决定新路径添加的位置
    """
    # 解析源文件
    source_tree = ET.parse(source_path)
    source_root = source_tree.getroot()
    
    # 提取路径
    paths = extract_paths(source_root)
    print(f"Extracted {len(paths)} paths from {source_path}")
    
    # 获取目标文件列表
    if isinstance(pattern, list):  # 如果pattern是文件列表
        target_files = pattern
    else:  # 如果pattern是通配符模式
        target_files = glob.glob(pattern)
        
    if not target_files:
        print(f"No files found matching pattern: {pattern}")
        return
    
    print(f"Found {len(target_files)} matching files")
    print(f"Applying paths at {layer_position} layer")
    
    # 处理每个目标文件
    for target_file in target_files:
        try:
            # 跳过源文件
            if os.path.abspath(target_file) == os.path.abspath(source_path):
                print(f"Skipping source file: {target_file}")
                continue
                
            print(f"Processing {target_file}...")
            
            # 解析目标文件
            tree = ET.parse(target_file)
            root = tree.getroot()
            
            # 找到SVG元素可能有命名空间）
            svg = root
            if not (svg.tag.endswith('svg') or svg.tag == 'svg'):
                svg = root.find('.//{http://www.w3.org/2000/svg}svg') or root.find('.//svg')
                if svg is None:
                    print(f"Warning: No SVG element found in {target_file}")
                    continue
            
            # 添加新路径到目标文件
            for path in paths:
                if layer_position == 'bottom':
                    # 在开头插入路
                    svg.insert(0, ET.fromstring(ET.tostring(path)))
                else:  # 'top'
                    # 在末尾添加路径
                    svg.append(ET.fromstring(ET.tostring(path)))
            
            # 保存修改后的文件
            with open(target_file, 'w', encoding='utf-8') as f:
                xml_str = ET.tostring(root, encoding='unicode')
                xml_str = xml_str.replace('ns0:', '').replace(':ns0', '')
                f.write(xml_str)
            
            print(f"Successfully processed: {target_file}")
            
        except Exception as e:
            print(f"Failed to process {target_file}: {str(e)}")

def convert_circles_to_paths(input_path, output_path):
    """将SVG文件中的圆形转换为路径"""
    tree = ET.parse(input_path)
    root = tree.getroot()
    convert_circles(root)  # 使用已有的convert_circles函数
    
    with open(output_path, 'w', encoding='utf-8') as f:
        xml_str = ET.tostring(root, encoding='unicode')
        xml_str = xml_str.replace('ns0:', '').replace(':ns0', '')
        f.write(xml_str)

def get_transform_matrix(transform_str):
    """Extract matrix values from transform string
    
    Args:
        transform_str: Transform attribute string
        
    Returns:
        list: Matrix values [a, b, c, d, e, f] or None
    """
    if not transform_str:
        return None
        
    # Check for matrix transform
    matrix_match = re.match(r'matrix\(([-\d.\s,]+)\)', transform_str)
    if matrix_match:
        matrix_str = matrix_match.group(1)
        matrix_values = re.findall(r'[-+]?\d*\.?\d+', matrix_str)
        return [float(x) for x in matrix_values]
    
    # Check for translate transform
    translate_match = re.match(r'translate\(([-\d.]+)(?:[,\s]+([-\d.]+))?\)', transform_str)
    if translate_match:
        tx = float(translate_match.group(1))
        ty = float(translate_match.group(2)) if translate_match.group(2) else 0
        # Convert translate to matrix [1 0 0 1 tx ty]
        return [1, 0, 0, 1, tx, ty]
    
    return None

def combine_matrices(matrix1, matrix2):
    """Combine two transformation matrices
    
    Args:
        matrix1: First matrix [a1, b1, c1, d1, e1, f1]
        matrix2: Second matrix [a2, b2, c2, d2, e2, f2]
        
    Returns:
        list: Combined matrix [a, b, c, d, e, f]
    """
    a1, b1, c1, d1, e1, f1 = matrix1
    a2, b2, c2, d2, e2, f2 = matrix2
    
    return [
        a1 * a2 + b1 * c2,        # a
        a1 * b2 + b1 * d2,        # b
        c1 * a2 + d1 * c2,        # c
        c1 * b2 + d1 * d2,        # d
        e1 * a2 + f1 * c2 + e2,   # e
        e1 * b2 + f1 * d2 + f2    # f
    ]

def get_accumulated_transform(element):
    """Get accumulated transform matrix from element and all its ancestors
    
    Args:
        element: XML element
        
    Returns:
        list: Accumulated matrix [a, b, c, d, e, f] or None
    """
    # Default identity matrix
    accumulated_matrix = [1, 0, 0, 1, 0, 0]
    
    # Collect all transforms from bottom to top
    transforms = []
    current = element
    while current is not None:
        transform = current.get('transform', '')
        if transform:
            matrix = get_transform_matrix(transform)
            if matrix:
                transforms.append(matrix)
        current = current.getparent()  # Get parent element
    
    # Apply transforms from top to bottom
    for matrix in reversed(transforms):
        accumulated_matrix = combine_matrices(matrix, accumulated_matrix)
    
    return accumulated_matrix

def apply_transform_to_path(svg_path, output_path=None):
    """Apply transform attributes to path data and remove transforms"""
    try:
        # Use lxml for better parent tracking
        from lxml import etree as ET
        tree = ET.parse(svg_path)
        root = tree.getroot()
        made_changes = False

        # Process all path elements
        for path in root.findall('.//path') + root.findall('.//{http://www.w3.org/2000/svg}path'):
            # Get accumulated transform from all ancestor g elements
            matrix = get_accumulated_transform(path)
            if matrix == [1, 0, 0, 1, 0, 0]:  # Skip if no real transform
                continue

            # Get path data
            d = path.get('d', '')
            if not d:
                continue

            # Parse path data
            new_d = []
            current_pos = [0, 0]
            parts = re.findall(r'([A-Za-z])([^A-Za-z]*)', d)
            
            for cmd, params in parts:
                params = re.findall(r'[-+]?\d*\.?\d+', params)
                params = [float(p) for p in params]
                
                if cmd in 'mM':
                    for i in range(0, len(params), 2):
                        x, y = params[i:i+2]
                        new_x = matrix[0] * x + matrix[2] * y + matrix[4]
                        new_y = matrix[1] * x + matrix[3] * y + matrix[5]
                        new_d.append(f"{cmd}{new_x:.2f},{new_y:.2f}")
                        current_pos = [x, y] if cmd.isupper() else [current_pos[0] + x, current_pos[1] + y]
                        cmd = cmd.lower()
                        
                elif cmd in 'lL':
                    for i in range(0, len(params), 2):
                        x, y = params[i:i+2]
                        new_x = matrix[0] * x + matrix[2] * y + matrix[4]
                        new_y = matrix[1] * x + matrix[3] * y + matrix[5]
                        new_d.append(f"{cmd}{new_x:.2f},{new_y:.2f}")
                        
                elif cmd in 'hH':
                    for x in params:
                        new_x = matrix[0] * x + matrix[4]
                        new_y = matrix[5]
                        new_d.append(f"L{new_x:.2f},{new_y:.2f}")
                        
                elif cmd in 'vV':
                    for y in params:
                        new_x = matrix[4]
                        new_y = matrix[1] * y + matrix[5]
                        new_d.append(f"L{new_x:.2f},{new_y:.2f}")
                        
                elif cmd in 'cC':
                    for i in range(0, len(params), 6):
                        x1, y1, x2, y2, x, y = params[i:i+6]
                        new_x1 = matrix[0] * x1 + matrix[2] * y1 + matrix[4]
                        new_y1 = matrix[1] * x1 + matrix[3] * y1 + matrix[5]
                        new_x2 = matrix[0] * x2 + matrix[2] * y2 + matrix[4]
                        new_y2 = matrix[1] * x2 + matrix[3] * y2 + matrix[5]
                        new_x = matrix[0] * x + matrix[2] * y + matrix[4]
                        new_y = matrix[1] * x + matrix[3] * y + matrix[5]
                        new_d.append(f"{cmd}{new_x1:.2f},{new_y1:.2f} {new_x2:.2f},{new_y2:.2f} {new_x:.2f},{new_y:.2f}")
                        
                elif cmd in 'zZ':
                    new_d.append(cmd)
        
            # Update path with new data
            path.set('d', ' '.join(new_d))
            # Remove transform from path itself
            if 'transform' in path.attrib:
                path.attrib.pop('transform')
            made_changes = True

        # Remove all transform attributes from g elements
        for g in root.findall('.//g') + root.findall('.//{http://www.w3.org/2000/svg}g'):
            if 'transform' in g.attrib:
                g.attrib.pop('transform')
                made_changes = True

        if made_changes:
            output_path = output_path or svg_path
            with open(output_path, 'w', encoding='utf-8') as f:
                xml_str = ET.tostring(root, encoding='unicode')
                xml_str = xml_str.replace('ns0:', '').replace(':ns0', '')
                f.write(xml_str)
            print(f"Applied transforms in: {output_path}")
            return True
        else:
            print(f"No transforms to apply in: {svg_path}")
            return False
            
    except Exception as e:
        print(f"Error applying transforms in {svg_path}: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='SVG transformation tools',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # transform 命令
    transform_parser = subparsers.add_parser('transform',
        help='Transform SVG file by applying g element translations')
    transform_parser.add_argument('files', nargs='+',
                               help='Input SVG files to process')
    transform_parser.add_argument('-o', '--output',
                               help='Output folder path. If not provided, will overwrite input files')
    
    # dedup 命令
    dedup_parser = subparsers.add_parser('dedup', 
        help='Remove duplicate paths from SVG files')
    dedup_parser.add_argument('files', nargs='+',
                            help='Input SVG files to process')
    dedup_parser.add_argument('-o', '--output',
                            help='Output folder path. If not provided, will overwrite input files')
    
    # circle2path 命令
    circle2path_parser = subparsers.add_parser('circle2path',
        help='Convert circles to paths in SVG files')
    circle2path_parser.add_argument('files', nargs='+',
                                 help='Input SVG files to process')
    circle2path_parser.add_argument('-o', '--output',
                                 help='Output folder path. If not provided, will overwrite input files')
    
    # applytransformtopath command
    transform_parser = subparsers.add_parser('applytransformtopath', 
        help='Apply transform attributes to path data',
        description='Calculate path values with transform attributes and remove transforms')
    transform_parser.add_argument('files', nargs='+', help='SVG files to process')
    transform_parser.add_argument('-o', '--output', help='Output directory')

    args = parser.parse_args()
    
    try:
        if args.command == 'transform':
            for file_path in args.files:
                try:
                    print(f"\nProcessing {file_path}...")
                    output_path = os.path.join(args.output, os.path.basename(file_path)) if args.output else file_path
                    if args.output:
                        os.makedirs(args.output, exist_ok=True)
                    apply_translate_from_g(file_path, output_path)
                except Exception as e:
                    print(f"Failed to process {file_path}: {str(e)}")
                    
        elif args.command == 'dedup':
            for file_path in args.files:
                try:
                    print(f"\nProcessing {file_path}...")
                    output_path = os.path.join(args.output, os.path.basename(file_path)) if args.output else file_path
                    if args.output:
                        os.makedirs(args.output, exist_ok=True)
                    tree = ET.parse(file_path)
                    root = tree.getroot()
                    remove_duplicate_paths(root)
                    with open(output_path, 'w', encoding='utf-8') as f:
                        xml_str = ET.tostring(root, encoding='unicode')
                        xml_str = xml_str.replace('ns0:', '').replace(':ns0', '')
                        f.write(xml_str)
                except Exception as e:
                    print(f"Failed to process {file_path}: {str(e)}")
                    
        elif args.command == 'circle2path':
            for file_path in args.files:
                try:
                    print(f"\nProcessing {file_path}...")
                    output_path = os.path.join(args.output, os.path.basename(file_path)) if args.output else file_path
                    if args.output:
                        os.makedirs(args.output, exist_ok=True)
                    convert_circles_to_paths(file_path, output_path)
                except Exception as e:
                    print(f"Failed to process {file_path}: {str(e)}")
            
        elif args.command == 'applytransformtopath':
            for file_path in args.files:
                try:
                    print(f"\nProcessing {file_path}...")
                    output_path = os.path.join(args.output, os.path.basename(file_path)) if args.output else file_path
                    if args.output:
                        os.makedirs(args.output, exist_ok=True)
                    apply_transform_to_path(file_path, output_path)
                except Exception as e:
                    print(f"Failed to process {file_path}: {str(e)}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()