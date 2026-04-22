# Meeting Skills - 面试技能集合

## 项目简介

Meeting Skills 是一个专注于收集和整理面试相关技能的 Agent Skills 项目。该项目旨在为求职者和技术从业者提供一套完整的面试准备工具集，涵盖简历优化、面试问题模拟、技能评估等多个方面，帮助用户在技术面试中脱颖而出。

## 主要功能

### Tech Resume Optimizer (技术简历优化器)

这是一个专门针对工程技术岗位简历优化的智能助手，具有以下核心能力：

1. **深度简历分析** - 识别技术问题点，提供精细化修改建议
2. **灵活风格HTML报告生成** - 根据候选人特点选择合适的视觉风格（极简科技风/活力创新风/杂志编辑风），避免模板化
3. **面试问题模拟** - 基于简历内容生成针对性面试问题
4. **行业对标分析** - 评估简历竞争力并提供改进方向

该工具特别适用于前端、后端、运维和AI应用工程师岗位的简历优化和面试准备。

**设计理念**：

- 提供设计原则而非固化样式，保持灵活性
- 三种风格方向可选，适应不同候选人特点
- 纯CSS实现，无JavaScript依赖，确保兼容性
- 响应式设计，移动端和打印友好

## 项目结构

```
meeting-skills/
├── .agents/skills/          # 已安装的Agent Skills
├── scripts/                 # 管理脚本
│   └── manage-skills.py     # 跨平台技能管理工具
├── skills/                  # 可用技能目录
│   └── tech-resume-optimizer/  # 技术简历优化技能
│       ├── references/      # 参考资料
│       │   ├── html-style-guide.md            # HTML报告风格指导原则
│       │   ├── interview-questions.md         # 面试问题生成指南
│       │   ├── star-quantification.md         # STAR法则与量化指南
│       │   ├── tech-keywords.md               # 技术关键词库
│       │   ├── resume-best-practices.md       # 简历优化最佳实践
│       │   ├── conciseness-guide.md           # 内容精简指南
│       │   └── writing-logic.md               # 简历编写逻辑指南
│       └── SKILL.md         # 技能定义文件
└── .gitignore
```

## 安装和使用

### 安装技能

使用提供的管理脚本来安装技能：

```bash
# 安装所有技能到默认目录
python scripts/manage-skills.py install

# 安装指定技能
python scripts/manage-skills.py install --skills tech-resume-optimizer

# 安装到指定目录
python scripts/manage-skills.py install --target /path/to/skills
```

### 卸载技能

```bash
# 卸载所有技能
python scripts/manage-skills.py uninstall

# 卸载指定技能
python scripts/manage-skills.py uninstall --skills tech-resume-optimizer
```

### 验证安装

```bash
# 验证技能安装状态
python scripts/manage-skills.py verify
```

## 许可证

本项目采用 MIT 许可证。
