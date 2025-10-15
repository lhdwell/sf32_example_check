import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from find import find_valid_examples

CPU_CORES = os.cpu_count() or 1
MAX_WORKERS = max(CPU_CORES*2/8, 1)

def compile_single_example(example: str):
    docker_command = [
        "bash", "-i", "-c",
        f"cd {example} && cd project && scons --board=sf32lb52-lcd_n16r8 -j8"
    ]
    try:
        subprocess.run(
            docker_command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        return (example, True, None)
    except subprocess.CalledProcessError:
        return (example, False, "编译失败")
    except Exception as e:
        return (example, False, str(e))

def compile_examples_parallel():
    valid_examples = find_valid_examples("example")
    total = len(valid_examples)
    success_count = 0
    failed_examples = []  # ⬅️ 新增：用于记录失败示例

    print(f"找到 {total} 个有效示例，开始多线程编译（{MAX_WORKERS} 并发）...\n")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(compile_single_example, ex): ex for ex in valid_examples}
        
        for future in as_completed(futures):
            example, ok, msg = future.result()
            if ok:
                print(f"✓ {example} - 成功")
                success_count += 1
            else:
                print(f"✗ {example} - {msg}")
                failed_examples.append(example)  # ⬅️ 记录失败项

    print(f"\n编译完成: {success_count}/{total} 成功")
    if success_count == total:
        print("🎉 所有示例编译成功！")
    else:
        print(f"❌ {total - success_count} 个示例编译失败")
        print("\n以下示例编译失败：")
        for ex in failed_examples:
            print(f" - {ex}")  # ⬅️ 输出所有失败示例

if __name__ == "__main__":
    compile_examples_parallel()
