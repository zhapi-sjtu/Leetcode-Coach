# LeetCode 刷题教练 Skill

这是一个面向 Codex 的 LeetCode 刷题 Skill。它用于规划刷题、严格复盘、记录题解笔记、安排间隔复习，并支持导入 Hot100 以外的自定义题单。

## 一、目录结构

```text
leetcode-coach/
├── SKILL.md                    # Codex Skill 主入口
├── agents/openai.yaml          # Codex UI 元数据
├── data/
│   ├── _题单.md                # 题单和完成进度
│   ├── _复习表.md              # 复习台账
│   └── 题解/                   # 每题一篇题解笔记
├── references/                 # Codex 按需读取的工作说明
└── scripts/                    # 稳定更新题单和复习表的脚本
```

## 二、如何让 Codex 使用这个 Skill

当前目录已经是一个完整 Skill。你可以在当前工作区里显式调用：

```text
使用 $leetcode-coach 开始刷题
```

如果希望 Codex 全局自动发现这个 Skill，可以把整个目录复制到：

```text
C:/Users/78460/.codex/skills/leetcode-coach
```

目录名应保持为 `leetcode-coach`，与 `SKILL.md` 中的 `name: leetcode-coach` 一致。

## 三、日常使用方式

### 1. 开始刷题

对 Codex 说：

```text
使用 $leetcode-coach 开始刷题，告诉我今天该做什么。
```

Codex 会读取：

```text
data/_题单.md
data/_复习表.md
```

然后给出：

- 今天到期的复习题；
- 下一道未完成的新题；
- 题目的力扣链接；
- 当前进度。

底层脚本是：

```bash
python -B scripts/pick_next.py
```

### 2. 做完一题后复盘

做完题后，对 Codex 说：

```text
使用 $leetcode-coach 复盘这题。我做完了 1. 两数之和，下面是我的 Python 代码：...
```

Codex 不会直接写笔记，而会先严格追问你：

- 暴力解是什么；
- 为什么要优化；
- 最优解的关键观察是什么；
- 正确性如何保证；
- 边界条件有哪些；
- Python 实现里有什么语法和数据结构细节。

如果你回答不清楚，它会继续追问。只有当你能讲明白后，才会生成题解笔记。

复盘完成后，Codex 会记录进度：

```bash
python -B scripts/record_done.py --number 1 --title "两数之和" --topic "哈希"
```

这会：

- 在 `data/_题单.md` 中把题目标记为完成；
- 在 `data/_复习表.md` 中登记 3 天后复习；
- 在 `data/题解/` 下创建题解笔记。

### 3. 复习旧题

对 Codex 说：

```text
使用 $leetcode-coach 复习今天到期的旧题。
```

Codex 会先让你主动回忆，不会直接展示答案。

复习后根据结果更新阶段：

```bash
python -B scripts/record_review.py --number 1 --result pass
python -B scripts/record_review.py --number 1 --result fail
```

复习间隔规则：

```text
阶段 0：做完 3 天后复习
阶段 1：通过后 7 天复习
阶段 2：通过后 15 天复习
阶段 3：毕业
```

复习失败会回到阶段 0。

### 4. 设置定时提醒

你可以对 Codex 说：

```text
每天晚上 9 点提醒我复习 LeetCode 到期题。
```

Skill 会使用 `data/_复习表.md` 中的复习日期作为依据。提醒本身需要 Codex automation 支持，Skill 只负责提供检查逻辑。

## 四、如何自行补充题单

默认题单是 Hot100，存放在：

```text
data/_题单.md
```

你可以直接编辑这个文件，也可以准备一个新的 Markdown 题单再导入。

### 1. 推荐题单格式

使用专题标题 + Markdown checklist：

```md
## 动态规划专题

- [ ] 300. 最长递增子序列 `中等` `DP` `longest-increasing-subsequence`
- [ ] 72. 编辑距离 `困难` `DP` `edit-distance`
```

每一行含义：

```text
- [ ] 题号. 中文题名 `难度` `专题` `英文-slug`
```

其中：

- `[ ]` 表示未完成；
- `[x]` 表示已完成；
- 题号必填；
- 中文题名必填；
- 难度可选；
- 专题可选；
- 英文 slug 推荐填写。

### 2. 为什么需要英文 slug

力扣题目链接使用英文 slug 生成，例如：

```text
https://leetcode.cn/problems/two-sum/description/
```

这里的 `two-sum` 就是 slug。

如果题目在 Hot100 内，脚本内置了题号到 slug 的映射。  
如果是 Hot100 以外的题，建议你在题单行最后补充 slug：

```md
- [ ] 912. 排序数组 `中等` `排序` `sort-an-array`
```

这样 Skill 就能自动生成：

```text
https://leetcode.cn/problems/sort-an-array/description/
```

你不需要手动输入完整网址，只需要补 slug。

### 3. 如何找到 slug

打开任意力扣题目页面，网址通常是：

```text
https://leetcode.cn/problems/sort-an-array/description/
```

其中：

```text
sort-an-array
```

就是 slug。

### 4. 手动追加题目

可以直接在 `data/_题单.md` 末尾添加：

```md
## 排序专题

- [ ] 912. 排序数组 `中等` `排序` `sort-an-array`
- [ ] 215. 数组中的第 K 个最大元素 `中等` `堆/快排` `kth-largest-element-in-an-array`
```

添加后再对 Codex 说：

```text
使用 $leetcode-coach 开始刷题。
```

### 5. 从外部 Markdown 文件导入题单

假设你有一个文件：

```text
my-questions.md
```

内容类似：

```md
## 二分专题

- [ ] 704. 二分查找 `简单` `二分` `binary-search`
- [ ] 35. 搜索插入位置 `简单` `二分` `search-insert-position`
```

可以让 Codex 导入：

```text
使用 $leetcode-coach 导入 my-questions.md 这个题单。
```

底层脚本是：

```bash
python -B scripts/import_markdown_questions.py my-questions.md
```

导入规则：

- 新题会追加到 `data/_题单.md`；
- 已存在的题号会跳过；
- 不会覆盖已有完成进度；
- 不会覆盖已有复习记录。

## 五、常用命令速查

在 `leetcode-coach/` 目录下可以直接运行：

```bash
# 查看今天该做什么
python -B scripts/pick_next.py

# 只查看到期复习题
python -B scripts/due_reviews.py

# 标记题目完成
python -B scripts/record_done.py --number 1 --title "两数之和" --topic "哈希"

# 记录复习通过
python -B scripts/record_review.py --number 1 --result pass

# 记录复习未通过
python -B scripts/record_review.py --number 1 --result fail

# 导入外部 Markdown 题单
python -B scripts/import_markdown_questions.py path/to/questions.md
```

平时更推荐直接让 Codex 调用 `$leetcode-coach`，不需要自己手动运行脚本。

## 六、建议的刷题节奏

推荐每天流程：

1. 使用 `$leetcode-coach` 开始刷题。
2. 先复习到期旧题。
3. 再做今日新题。
4. 做完后用 `$leetcode-coach` 严格复盘。
5. 通过追问后再生成笔记。
6. 让 Skill 登记 3 天后的复习。

这个 Skill 的目标不是帮你“看懂答案”，而是逼你能讲清楚：

- 为什么这么做；
- 为什么这样是对的；
- Python 代码为什么这样写；
- 下次遇到类似题如何快速想起来。
