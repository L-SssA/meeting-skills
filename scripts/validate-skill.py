#!/usr/bin/env python3
"""
Skill Validator - 技能验证脚本
检查技能是否符合官方规范
"""

import sys
import os
import re
from pathlib import Path


def validate_skill(skill_path: str) -> bool:
    """验证技能目录是否符合规范"""

    skill_dir = Path(skill_path)

    if not skill_dir.exists():
        print(f"❌ 错误: 目录不存在: {skill_path}")
        return False

    if not skill_dir.is_dir():
        print(f"❌ 错误: 路径不是目录: {skill_path}")
        return False

    # 检查目录名
    dir_name = skill_dir.name
    if not re.match(r'^[a-z0-9][a-z0-9-]{0,62}[a-z0-9]$', dir_name):
        print(f"❌ 错误: 目录名不符合规范: {dir_name}")
        print("   要求: 小写字母、数字、连字符,长度1-64,不能以连字符开头或结尾")
        return False

    print(f"✅ 目录名验证通过: {dir_name}")

    # 检查 SKILL.md 是否存在
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        print(f"❌ 错误: 缺少 SKILL.md 文件")
        return False

    print(f"✅ SKILL.md 文件存在")

    # 读取 SKILL.md
    with open(skill_file, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')

    # 检查行数
    if len(lines) > 500:
        print(f"❌ 错误: SKILL.md 行数过多 ({len(lines)}行),应保持在500行以内")
        print("   建议: 将详细内容移至 references/ 目录")
        return False

    print(f"✅ SKILL.md 行数合理: {len(lines)}行")

    # 检查 frontmatter
    if not content.startswith('---'):
        print(f"❌ 错误: 缺少 frontmatter (应以 --- 开头)")
        return False

    # 提取 frontmatter
    frontmatter_end = content.find('---', 3)
    if frontmatter_end == -1:
        print(f"❌ 错误: frontmatter 未正确闭合")
        return False

    frontmatter = content[3:frontmatter_end]

    # 检查 name 字段
    name_match = re.search(r'name:\s*(.+)', frontmatter)
    if not name_match:
        print(f"❌ 错误: frontmatter 中缺少 name 字段")
        return False

    name = name_match.group(1).strip()
    if name != dir_name:
        print(f"❌ 错误: frontmatter 中的 name ({name}) 与目录名 ({dir_name}) 不一致")
        return False

    print(f"✅ name 字段验证通过: {name}")

    # 检查 description 字段
    desc_match = re.search(
        r'description:\s*>?\s*\n?\s*(.+?)(?=\n[a-z]|\n---|$)', frontmatter, re.DOTALL)
    if not desc_match:
        print(f"❌ 错误: frontmatter 中缺少 description 字段")
        return False

    description = desc_match.group(1).strip()
    description = re.sub(r'\s+', ' ', description)  # 合并多行

    if len(description) < 1:
        print(f"❌ 错误: description 为空")
        return False

    if len(description) > 1024:
        print(f"❌ 错误: description 过长 ({len(description)}字符),应不超过1024字符")
        return False

    print(f"✅ description 长度合理: {len(description)}字符")

    # 检查 description 是否包含"做什么"和"何时使用"
    if not any(keyword in description for keyword in ['当', '用于', '适用', '帮助']):
        print(f"⚠️  警告: description 可能缺少'何时使用'的说明")

    # 检查 references 目录
    references_dir = skill_dir / "references"
    if references_dir.exists() and references_dir.is_dir():
        ref_files = list(references_dir.glob('*.md'))
        if ref_files:
            print(f"✅ references 目录存在,包含 {len(ref_files)} 个文档")

            # 检查 SKILL.md 中是否引用了 references
            if 'references/' in content or 'references\\\\' in content:
                print(f"✅ SKILL.md 中引用了 references 文档")
            else:
                print(f"⚠️  警告: SKILL.md 中未引用 references 文档")
        else:
            print(f"⚠️  警告: references 目录为空")
    else:
        print(f"⚠️  警告: 缺少 references 目录 (建议使用渐进式披露)")

    # 检查是否有 scripts 目录(可选)
    scripts_dir = skill_dir / "scripts"
    if scripts_dir.exists():
        print(f"ℹ️  scripts 目录存在")

    print(f"\n{'='*60}")
    print(f"✅ 验证通过! 技能 '{name}' 符合官方规范")
    print(f"{'='*60}")

    return True


def main():
    if len(sys.argv) < 2:
        print("用法: python validate-skill.py <skill_directory>")
        print("示例: python validate-skill.py skills/job-greeting-generator")
        sys.exit(1)

    skill_path = sys.argv[1]

    if validate_skill(skill_path):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
