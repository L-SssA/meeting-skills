#!/usr/bin/env python3
"""
Agent Skills 管理工具 - 跨平台统一脚本
支持安装、卸载和验证技能功能
"""

import os
import sys
import shutil
import argparse
from pathlib import Path


def get_script_dir():
    """获取脚本所在目录"""
    return Path(__file__).parent.parent.resolve()


def setup_directories(script_dir, target_dir=None):
    """设置源目录和目标目录"""
    source_dir = script_dir / "skills"
    if target_dir:
        target_dir = Path(target_dir).resolve()
    else:
        target_dir = script_dir / ".agents" / "skills"
    return source_dir, target_dir


def create_link(source_path, target_path):
    """
    创建链接（跨平台兼容）
    - Linux/Mac: 使用符号链接
    - Windows: 优先使用目录联接，失败时复制
    """
    # 如果目标已存在，先删除
    if target_path.exists() or target_path.is_symlink():
        try:
            if sys.platform == 'win32':
                # Windows: 使用 rmdir 命令删除 junction 或符号链接
                import subprocess
                subprocess.run(
                    ['cmd', '/c', 'rmdir', str(target_path)],
                    capture_output=True,
                    text=True
                )
            else:
                # Unix-like 系统
                if target_path.is_dir() and not target_path.is_symlink():
                    shutil.rmtree(target_path)
                else:
                    target_path.unlink()
        except Exception:
            # 如果删除失败，尝试其他方法
            if target_path.is_dir():
                shutil.rmtree(target_path, ignore_errors=True)
            else:
                target_path.unlink(missing_ok=True)

    try:
        if sys.platform == 'win32':
            # Windows: 尝试创建目录联接
            import subprocess
            result = subprocess.run(
                ['cmd', '/c', 'mklink', '/J',
                    str(target_path), str(source_path)],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                # 如果目录联接失败，尝试符号链接
                result = subprocess.run(
                    ['cmd', '/c', 'mklink', '/D',
                        str(target_path), str(source_path)],
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    # 如果都失败，则复制目录
                    print(f"警告: 无法为 {target_path.name} 创建链接，正在复制...")
                    shutil.copytree(source_path, target_path)
                    return False
            return True
        else:
            # Unix-like 系统: 创建符号链接
            target_path.symlink_to(source_path.resolve())
            return True
    except Exception as e:
        print(f"警告: 无法为 {target_path.name} 创建链接 ({e})，正在复制...")
        shutil.copytree(source_path, target_path)
        return False


def install_skills(script_dir, target_dir=None, skills=None):
    """
    安装技能

    Args:
        script_dir: 脚本所在目录
        target_dir: 目标目录（可选，默认为 .agents/skills）
        skills: 要安装的技能列表（可选，默认为所有技能）
    """
    source_dir, target_dir = setup_directories(script_dir, target_dir)

    # 检查源目录是否存在
    if not source_dir.exists():
        print(f"错误: 源目录 {source_dir} 不存在")
        sys.exit(1)

    # 创建目标目录（如果不存在）
    target_dir.mkdir(parents=True, exist_ok=True)

    print("开始安装技能...")
    if target_dir:
        print(f"目标目录: {target_dir}")
    if skills:
        print(f"指定技能: {', '.join(skills)}")
    print()

    skill_count = 0
    # 遍历源目录中的技能
    for skill_dir in sorted(source_dir.iterdir()):
        if not skill_dir.is_dir():
            continue

        skill_name = skill_dir.name

        # 如果指定了技能列表，只安装指定的技能
        if skills and skill_name not in skills:
            continue

        target_path = target_dir / skill_name

        print(f"处理技能: {skill_name}")

        # 创建链接
        success = create_link(skill_dir, target_path)
        if success:
            print(f"✓ 已创建链接: {skill_name}")
        else:
            print(f"✓ 已复制: {skill_name}")

        skill_count += 1

    print()
    print("=" * 40)
    print("  安装完成！")
    print("=" * 40)
    print()
    print(f"技能已安装到: {target_dir}")
    print(f"共安装 {skill_count} 个技能")
    print()
    print("可用的技能:")
    for skill_dir in sorted(target_dir.iterdir()):
        if skill_dir.is_dir():
            print(f"  - {skill_dir.name}")
    print()


def uninstall_skills(script_dir, target_dir=None, skills=None):
    """
    卸载技能

    Args:
        script_dir: 脚本所在目录
        target_dir: 目标目录（可选，默认为 .agents/skills）
        skills: 要卸载的技能列表（可选，默认为所有技能）
    """
    _, target_dir = setup_directories(script_dir, target_dir)

    # 检查目标目录是否存在
    if not target_dir.exists():
        print("信息: 技能目录不存在，无需卸载")
        return

    print("开始卸载技能...")
    if target_dir:
        print(f"目标目录: {target_dir}")
    if skills:
        print(f"指定技能: {', '.join(skills)}")
    print()

    uninstall_count = 0
    # 遍历并删除技能
    for skill_dir in sorted(target_dir.iterdir()):
        if not skill_dir.is_dir():
            continue

        skill_name = skill_dir.name

        # 如果指定了技能列表，只卸载指定的技能
        if skills and skill_name not in skills:
            continue

        try:
            # 在 Windows 上，需要特殊处理 junction 和符号链接
            if sys.platform == 'win32':
                import subprocess
                # 使用 Windows 命令删除 junction 或符号链接
                result = subprocess.run(
                    ['cmd', '/c', 'rmdir', str(skill_dir)],
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    # 如果 rmdir 失败，尝试其他方法
                    raise Exception(result.stderr)
            else:
                # Unix-like 系统
                if skill_dir.is_symlink():
                    skill_dir.unlink()
                else:
                    shutil.rmtree(skill_dir)

            print(f"✓ 已卸载: {skill_name}")
            uninstall_count += 1
        except Exception as e:
            print(f"✗ 无法卸载 {skill_name}: {e}")

    print()
    print("=" * 40)
    print("  卸载完成！")
    print("=" * 40)
    print()
    print(f"共卸载 {uninstall_count} 个技能")
    print()


def verify_installation(script_dir, target_dir=None):
    """
    验证技能安装

    Args:
        script_dir: 脚本所在目录
        target_dir: 目标目录（可选，默认为 .agents/skills）
    """
    source_dir, target_dir = setup_directories(script_dir, target_dir)

    print("=" * 40)
    print("  Agent Skills 安装验证")
    print("=" * 40)
    print()

    if target_dir:
        print(f"目标目录: {target_dir}")
        print()

    # 检查目标目录是否存在
    if not target_dir.exists():
        print("[错误] 技能目录不存在！")
        print("请先运行 install 命令安装技能。")
        sys.exit(1)

    print("[信息] 检查已安装的技能...")
    print()

    # 统计源目录中的技能总数
    total_count = 0
    if source_dir.exists():
        total_count = len([d for d in source_dir.iterdir() if d.is_dir()])

    # 统计已安装的技能数量
    installed_count = 0
    installed_skills = []
    for skill_dir in sorted(target_dir.iterdir()):
        if skill_dir.is_dir():
            installed_skills.append(skill_dir.name)
            installed_count += 1

    # 显示已安装的技能
    for skill_name in installed_skills:
        print(f"[✓] {skill_name} - 已安装")

    print()
    print("=" * 40)
    print("  验证结果")
    print("=" * 40)
    print(f"已安装技能数: {installed_count}/{total_count}")
    print()

    if installed_count == total_count:
        print("[成功] 所有技能已正确安装！")
        print()
        print("你可以在代理会话中使用 /skills 命令来查看可用技能。")
    elif installed_count > 0:
        print("[警告] 部分技能未安装，请运行 install 命令重新安装。")
    else:
        print("[错误] 没有安装任何技能，请运行 install 命令进行安装。")

    print()


def main():
    parser = argparse.ArgumentParser(
        description="Agent Skills 管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 安装所有技能到默认目录
  python manage-skills.py install
  
  # 安装指定技能
  python manage-skills.py install --skills create-skill optimize-skill
  
  # 安装到指定目录
  python manage-skills.py install --target /path/to/skills
  
  # 卸载指定技能
  python manage-skills.py uninstall --skills feedback-skill
  
  # 验证指定目录的安装状态
  python manage-skills.py verify --target /path/to/skills
        """
    )

    parser.add_argument(
        'command',
        choices=['install', 'uninstall', 'verify'],
        help='要执行的操作'
    )

    parser.add_argument(
        '--target', '-t',
        type=str,
        default=None,
        help='目标目录路径（默认: .agents/skills）'
    )

    parser.add_argument(
        '--skills', '-s',
        type=str,
        nargs='+',
        default=None,
        help='要操作的技能名称列表（默认: 所有技能）'
    )

    args = parser.parse_args()

    # 获取脚本所在目录（项目根目录）
    script_dir = get_script_dir()

    # 根据命令执行相应操作
    if args.command == 'install':
        install_skills(script_dir, target_dir=args.target, skills=args.skills)
    elif args.command == 'uninstall':
        uninstall_skills(script_dir, target_dir=args.target,
                         skills=args.skills)
    elif args.command == 'verify':
        verify_installation(script_dir, target_dir=args.target)


if __name__ == "__main__":
    main()
