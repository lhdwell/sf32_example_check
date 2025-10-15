import os
import sys
from pathlib import Path

def is_valid_example(directory_path):
    """
    检查一个目录是否是有效的example（不区分大小写）
    """
    directory = Path(directory_path)
    
    # 检查 src 目录是否存在
    src_dir = directory / "src"
    if not src_dir.exists() or not src_dir.is_dir():
        return False, "缺少 src 目录"
    
    # 检查 project 目录是否存在
    project_dir = directory / "project"
    if not project_dir.exists() or not project_dir.is_dir():
        return False, "缺少 project 目录"
    
    # 检查 project/SConstruct 文件是否存在
    sconstruct_file = project_dir / "SConstruct"
    if not sconstruct_file.exists() or not sconstruct_file.is_file():
        return False, "缺少 project/SConstruct 文件"
    
    return True, "有效的example"

def find_valid_examples(root_directory):
    """
    在指定根目录下递归查找所有有效的example目录
    """
    root_path = Path(root_directory)
    valid_examples = []
    
    print("正在扫描目录...")
    
    for current_dir, dirs, files in os.walk(root_path):
        current_path = Path(current_dir)
        
        is_valid, message = is_valid_example(current_path)
        if is_valid:
            valid_examples.append(str(current_path))
            print(f"✓ 找到有效example: {current_path}")
        else:
            # 可选：显示为什么不是有效example
            # print(f"  {current_path} - {message}")
            pass
    
    return valid_examples

def main():
    example_root = "example"  # 修改为你的实际路径
    
    if not os.path.exists(example_root):
        print(f"错误：目录 '{example_root}' 不存在")
        sys.exit(1)
    
    print(f"开始在 '{example_root}' 目录下查找有效的example...")
    print("有效条件：")
    print("  - 包含 src 目录")
    print("  - 包含 project 目录") 
    print("  - 包含 readme.md 文件")
    print("  - project 目录包含 SConstruct 文件")
    print("-" * 50)
    
    valid_examples = find_valid_examples(example_root)
    
    print("-" * 50)
    if valid_examples:
        print(f"\n找到 {len(valid_examples)} 个有效的example:")
        for i, example_path in enumerate(valid_examples, 1):
            print(f"{i}. {example_path}")
    else:
        print("\n没有找到任何有效的example")
    
    return valid_examples

if __name__ == "__main__":
    main()