# GTM 操盘手册 · AI Skill

> 基于2C业务GTM（Go-To-Market）实战方法论，帮助GTM经理、品类经理、国家经理系统性地操盘产品全生命周期。

---

## 📦 仓库结构

```
gtm-playbook-skill/
├── skill/
│   └── SKILL.md          # Claude Skills 核心文件（可直接安装到 Claude.ai）
├── cli/
│   ├── gtm_advisor.py    # CLI 工具：通过 API 接入 AI 解答执行问题
│   ├── requirements.txt  # Python 依赖
│   └── .env.example      # 环境变量示例
├── docs/
│   └── usage_examples.md # 使用场景与提问示例
└── README.md
```

---

## 🚀 快速开始

### 方式一：作为 Claude Skill 使用（推荐）

将 `skill/SKILL.md` 安装到你的 Claude 环境中。安装后，当你向 Claude 提问以下类型问题时，skill 会自动触发：

- "我这个产品该怎么定价？"
- "新品上市前8周要准备哪些东西？"
- "PSI表里库存周转天数偏高怎么处理？"
- "帮我做一个产品路标规划"

### 方式二：通过 CLI 工具接入 API

适合在 **Claude Code** 或 **Gemini CLI** 环境中使用，直接在终端提问并获得基于GTM手册的专业回答。

```bash
# 安装依赖
cd cli
pip install -r requirements.txt

# 配置 API Key（选择其一）
cp .env.example .env
# 编辑 .env，填入你的 API Key

# 使用 Claude API
python gtm_advisor.py --provider claude "我的产品库存DOS已经超过90天，该怎么处理？"

# 使用 Gemini API
python gtm_advisor.py --provider gemini "如何制定一个新品上市的促销地图？"

# 进入交互模式（连续对话）
python gtm_advisor.py --interactive
```

---

## 🧠 Skill 覆盖内容

| 模块 | 内容 |
|------|------|
| GTM 角色认知 | 大脑/协同/执行三大定位，KPI框架 |
| IPMS SOP | 从TTM-12周到退市的全生命周期标准动作 |
| 新品上市管理表 | 产品路标、竞争力分析、Checklist、GTM标准动作管理表、首销复盘 |
| PSI 管理表 | 进销存三层视角、销售预测、库存周转管理 |
| 产品经营表 | 成本层级、损益测算、三种定价策略、经营四比 |
| 市场洞察框架 | 看市场/竞争/用户/自己，渠道洞察模板，月度SOP |
| 会议运作机制 | GTM会议/SMR/MMR/要货计划会/BP会/复盘会 |
| 词汇速查 | 30+ 跨境商务专业术语中英对照 |

---

## 💡 典型使用场景

```
场景1：新品选型
"我们准备进入德国市场，想推一款3000元档位的TWS耳机，竞品是Sony WH系列，
请帮我梳理竞争力分析表的填写框架"

场景2：定价决策
"产品BOM成本150元，目标售价RRP 599元，增值税20%，渠道前向15%，
帮我算一下销售毛利率和净利润"

场景3：库存预警
"我的FBA库存还有2000台，日均销量30台，大促还有6周，该发多少货？"

场景4：上市推进
"距离TTM还有4周，GTM会议上需要确认哪些关键交付件没有Ready？"
```

更多示例见 [`docs/usage_examples.md`](docs/usage_examples.md)

---

## 🔧 CLI 工具支持的 AI 提供商

| 提供商 | 模型 | 环境变量 |
|--------|------|----------|
| Anthropic Claude | claude-sonnet-4-5 | `ANTHROPIC_API_KEY` |
| Google Gemini | gemini-2.0-flash | `GEMINI_API_KEY` |

---

## 📄 License

MIT License — 欢迎 Fork、改造和贡献。

---