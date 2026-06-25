# Markdown 题单格式

主题库文件是 `data/_题单.md`。

使用专题标题和清单行：

```md
## 哈希

- [ ] 1. 两数之和 `简单` `哈希` `two-sum`
- [ ] 49. 字母异位词分组 `中等` `哈希` `group-anagrams`
```

支持的行格式：

```md
- [ ] 1. 两数之和 `简单` `哈希` `two-sum`
- [ ] 1. 两数之和 `哈希`
- [x] 1. 两数之和 `简单` `哈希` `two-sum`
```

字段规则：

- 复选框控制完成进度。
- 题号必填。
- 中文题名必填。
- 反引号标签可以表示难度、专题或英文 slug。
- slug 可选。缺失时，脚本会优先使用内置 Hot100 slug 映射；如果不是 Hot100 题目，建议在题单中补充 slug。
- 如果题目行没有专题标签，默认使用最近的 `##` 标题作为专题。

导入规则：

- 导入时追加新题，并避免重复题号。
- 保留已有题目的完成状态。
- 保留已有笔记和复习记录。
- 优先使用可读 Markdown，不使用隐藏数据库。

## 题目链接

脚本会根据 slug 生成 `url` 字段。当前默认链接格式为：

```text
https://leetcode.cn/problems/<slug>/description/
```

例如：

```text
1. 两数之和 -> https://leetcode.cn/problems/two-sum/description/
```

导入非 Hot100 题单时，最好在题目行最后补充英文 slug：

```md
- [ ] 300. 最长递增子序列 `中等` `DP` `longest-increasing-subsequence`
```
