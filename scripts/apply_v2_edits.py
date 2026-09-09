#!/usr/bin/env python3
# apply_v2_edits.py — 在 D 开发副本上落地两处增强，再整体同步云端/镜像。
# 目标文件通过命令行参数传入（默认 D 版 prompt-builder.js）。
import sys, io

PB_DEFAULT = r"D:\code test\睡前故事\scripts\prompt-builder.js"
GS_DEFAULT = r"D:\code test\睡前故事\scripts\generate-story.js"

def edit(path, replacements):
    with io.open(path, encoding='utf-8') as f:
        s = f.read()
    for item in replacements:
        if len(item) == 3:
            old, new, label = item
        else:
            old, new = item
            label = old[:18].replace('\n', ' ')
        cnt = s.count(old)
        if cnt != 1:
            raise SystemExit(f"[FAIL] {label}: 期望匹配 1 次，实际 {cnt} 次\n---OLD---\n{old}\n---")
        s = s.replace(old, new, 1)
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(s)
    print(f"[OK] {path}: 应用 {len(replacements)} 处替换")

# ============ prompt-builder.js ============
PB = sys.argv[1] if len(sys.argv) > 1 else PB_DEFAULT

pb_repl = [
    # --- (1) 胎教期结尾放宽：不再只写「晚安」 ---
    (
        "→ 用「小宝宝，你听到了吗？」式对话与肚里宝宝说话 → 以温柔守候收尾（如「等你准备好了，外面的世界有软软的风和圆圆的月亮等你」）。`;",
        "→ 用「小宝宝，你听到了吗？」式对话与肚里宝宝说话 → 以温柔守候收尾（结尾不必每次都是「晚安」：可按本篇情境用「等你准备好了，外面的世界有软软的风和圆圆的月亮等你」「早安，小宝宝，今天的世界亮晶晶的」或「晚安，小宝宝，月亮陪着你」等，自然选择）。`;"
    ),
    (
        '→ talk to the unborn baby with "little one, can you hear?" → end with tender waiting (e.g. "when you are ready, the soft wind and round moon will be waiting").`;',
        '→ talk to the unborn baby with "little one, can you hear?" → end with tender waiting (not always "good night": per this story\'s occasion, use "when you are ready, the soft wind and round moon will be waiting", "good morning, little one, the world is sparkly today", or "good night, little one, the moon is with you" — choose naturally).`;'
    ),
    # --- (2) 在 pickTheme 之后新增 OCCASIONS + pickOccasion ---
    (
        "function pickTheme(dateStr, lang) {\n"
        "  const pool = lang === 'zh' ? THEME_POOL_ALL_CN : THEME_POOL_ALL_EN;\n"
        "  // Offset EN by half the pool so CN and EN differ on the same day.\n"
        "  const offset = lang === 'en' ? Math.floor(pool.length / 2) : 0;\n"
        "  const idx = (hashDate(dateStr) + offset) % pool.length;\n"
        "  return pool[idx];\n"
        "}",
        "function pickTheme(dateStr, lang) {\n"
        "  const pool = lang === 'zh' ? THEME_POOL_ALL_CN : THEME_POOL_ALL_EN;\n"
        "  // Offset EN by half the pool so CN and EN differ on the same day.\n"
        "  const offset = lang === 'en' ? Math.floor(pool.length / 2) : 0;\n"
        "  const idx = (hashDate(dateStr) + offset) % pool.length;\n"
        "  return pool[idx];\n"
        "}\n\n"
        "// ===== 情境/场合轮换（让每日故事不局限于「晚安」哄睡） =====\n"
        "const OCCASIONS_CN = [\n"
        "  { key: '早安', hint: '以温柔的晨光与苏醒开场，结尾用「早安」式清晨问候收束' },\n"
        "  { key: '白天', hint: '以安静白天的探索与发现为主，结尾是小主角在暖阳里满足地舒口气' },\n"
        "  { key: '晚安', hint: '以哄睡摇篮与星光为主，结尾用「晚安」温柔道别' },\n"
        "  { key: '奇妙发现', hint: '以一次温柔的好奇探险为主，结尾停留在「原来世界这么奇妙」的惊喜' },\n"
        "  { key: '暖心陪伴', hint: '以好朋友/家人的陪伴为主，结尾是依依不舍又安心的「明天见」' }\n"
        "];\n"
        "const OCCASIONS_EN = [\n"
        "  { key: 'Good morning', hint: 'open with gentle dawn light; end with a \"good morning\" greeting' },\n"
        "  { key: 'Daytime', hint: 'a calm daytime discovery; end with the little hero breathing satisfied in warm sun' },\n"
        "  { key: 'Good night', hint: 'a lullaby under starlight; end with a tender \"good night\"' },\n"
        "  { key: 'Wonder', hint: 'a gentle curious adventure; end on the surprise \"the world is so wonderful\"' },\n"
        "  { key: 'Warm company', hint: 'companionship of a friend/family; end with a reluctant but safe \"see you tomorrow\"' }\n"
        "];\n"
        "function pickOccasion(dateStr, lang) {\n"
        "  const list = lang === 'zh' ? OCCASIONS_CN : OCCASIONS_EN;\n"
        "  const idx = hashDate(dateStr + '-occ-' + lang) % list.length;\n"
        "  return list[idx];\n"
        "}"
    ),
    # --- (3) buildChinesePrompt：加入 occasion 变量 + 注入情境说明 ---
    (
        "function buildChinesePrompt(dateStr, ageInfo) {\n"
        "  const ageStyle = AGE_STYLE_CN[ageInfo.group];\n"
        "  const theme = pickTheme(dateStr, 'zh');\n"
        "  const prenatalBlock = ageInfo.group === 'prenatal' ? buildPrenatalBlock(dateStr, 'zh') : '';",
        "function buildChinesePrompt(dateStr, ageInfo) {\n"
        "  const ageStyle = AGE_STYLE_CN[ageInfo.group];\n"
        "  const theme = pickTheme(dateStr, 'zh');\n"
        "  const prenatalBlock = ageInfo.group === 'prenatal' ? buildPrenatalBlock(dateStr, 'zh') : '';\n"
        "  const occasion = pickOccasion(dateStr, 'zh');"
    ),
    (
        "**本篇灵感选题库（任选其一或受其启发展开，避免与已写过的故事重复）：**\n"
        "${pickSeeds(dateStr, 'zh').map(s => '- ' + s).join('\\n')}",
        "**本篇灵感选题库（任选其一或受其启发展开，避免与已写过的故事重复）：**\n"
        "${pickSeeds(dateStr, 'zh').map(s => '- ' + s).join('\\n')}\n\n"
        "**本篇情境/场合（每日故事不要局限于「晚安」哄睡，按情境自然变化）：「${occasion.key}」——${occasion.hint}。结尾请与情境呼应，不要千篇一律以「晚安」收束。**"
    ),
    # --- (4) buildEnglishPrompt：加入 occasion 变量 + 注入情境说明 ---
    (
        "function buildEnglishPrompt(dateStr, ageInfo) {\n"
        "  const ageStyle = AGE_STYLE_EN[ageInfo.group];\n"
        "  const theme = pickTheme(dateStr, 'en');\n"
        "  const prenatalBlock = ageInfo.group === 'prenatal' ? buildPrenatalBlock(dateStr, 'en') : '';",
        "function buildEnglishPrompt(dateStr, ageInfo) {\n"
        "  const ageStyle = AGE_STYLE_EN[ageInfo.group];\n"
        "  const theme = pickTheme(dateStr, 'en');\n"
        "  const prenatalBlock = ageInfo.group === 'prenatal' ? buildPrenatalBlock(dateStr, 'en') : '';\n"
        "  const occasion = pickOccasion(dateStr, 'en');"
    ),
    (
        "**Inspiration seed library for this story (pick one or be inspired by it; avoid repeating stories already written):**\n"
        "${pickSeeds(dateStr, 'en').map(s => '- ' + s).join('\\n')}",
        "**Inspiration seed library for this story (pick one or be inspired by it; avoid repeating stories already written):**\n"
        "${pickSeeds(dateStr, 'en').map(s => '- ' + s).join('\\n')}\n\n"
        "**Occasion for this story (daily stories need not all be \"good night\" — vary by occasion): \"${occasion.key}\" — ${occasion.hint}. End the story to match the occasion; don't default to \"good night\" every time.**"
    ),
    # --- (5) 科学故事（中文）：来源 + 儿童可理解的科学知识 ---
    (
        "    : '（未能抓取到当期杂志内容，请围绕这个科普主题创作）';",
        "    : '（未能抓取到指定杂志内容，请基于公认的儿童科普常识，围绕上述科普主题创作，并在文末点明知识来自儿童科普常识，不得编造。）';"
    ),
    (
        "    : `一个科普主题：「${scienceFallbackTopic(dateStr, 'zh')}」`;",
        "    : `一个科普主题：「${scienceFallbackTopic(dateStr, 'zh')}」（来源：儿童科普常识）`;"
    ),
    (
        "- 把真实科学内容改编成孩子爱听的故事，保留科学内核（如现象、原理的童趣化解释），但用拟声词、温柔节奏和\"守护/好奇/惊喜\"的情绪包装。\n"
        "- 适合胎教/哄睡朗读，句子有自然停顿，家长读着顺口。\n"
        "- 故事标题必须以「🔬科学故事」开头，并注明适合的年龄段。\n"
        "- 结尾用一两句话点出这个科学小知识，让孩子带着好奇入睡。",
        "- 把真实科学内容改编成孩子爱听的故事，保留科学内核（如现象、原理的童趣化解释），但用拟声词、温柔节奏和\"守护/好奇/惊喜\"的情绪包装。\n"
        "- 适合胎教/哄睡朗读，句子有自然停顿，家长读着顺口。\n"
        "- 故事标题必须以「🔬科学故事」开头，并注明适合的年龄段。\n"
        "- 本篇科普素材必须取自上方列出的指定来源（如《${article ? article.source : '儿童科普常识'}》），绝不可凭空编造科学结论；若取自杂志，请忠于其报道的科学内核。\n"
        "- 故事必须包含一段清楚、准确、适合该年龄段孩子理解的「科学知识讲解」（可由主角好奇提问「为什么会这样呢？」再自然解答），让孩子真的学到一点科学。\n"
        "- 结尾用一两句话点出这个科学小知识，让孩子带着好奇入睡；moral 必须是这条科学知识的准确、简洁小结，不得写「不知道」或含糊带过。"
    ),
    # --- (6) 科学故事（英文）：来源 + 儿童可理解的科学知识 ---
    (
        "    : '(Could not fetch the magazine; please write about this science topic.)';",
        "    : \"(Could not fetch the designated magazine; please base the story on widely accepted children's science facts for the topic above, note the source as general children's science, and do not invent.)\";"
    ),
    (
        "    : `a science topic: \"${scienceFallbackTopic(dateStr, 'en')}\"`;",
        "    : `a science topic: \"${scienceFallbackTopic(dateStr, 'en')}\" (source: children's science general)`;"
    ),
    (
        "- Adapt the real science into a story kids love: keep the science kernel but wrap it in onomatopoeia, a soft rhythm, and feelings of wonder, safety and curiosity.\n"
        "- Suitable for prenatal/soothing read-aloud; natural pauses; parent-friendly.\n"
        "- Title must start with \"🔬 Science Story\" and note the age range.\n"
        "- End with one or two lines revealing the little science fact, so the child falls asleep curious.",
        "- Adapt the real science into a story kids love: keep the science kernel but wrap it in onomatopoeia, a soft rhythm, and feelings of wonder, safety and curiosity.\n"
        "- Suitable for prenatal/soothing read-aloud; natural pauses; parent-friendly.\n"
        "- Title must start with \"🔬 Science Story\" and note the age range.\n"
        "- This story's science material MUST come from the designated source listed above (e.g. ${article ? article.source : \"children's science general\"}); never invent fake science. If from a magazine, stay true to its reported science kernel.\n"
        "- The story must contain a clear, accurate, age-appropriate \"science explanation\" (e.g. a character wonders \"why does this happen?\" then finds out), so the child truly learns something.\n"
        "- End with one or two lines revealing the little science fact, so the child falls asleep curious; moral must be the accurate, concise summary of that science fact — never \"I don't know\" or vague."
    ),
]

# ============ generate-story.js ============
GS = sys.argv[2] if len(sys.argv) > 2 else GS_DEFAULT
gs_repl = [
    (
        "        if (article && article.source) raw.source = article.source; // 标记来源杂志",
        "        raw.source = article ? article.source : (language === 'zh' ? '儿童科普常识' : \"Children's science (general)\"); // 标记来源（始终有值）"
    ),
]

if __name__ == '__main__':
    edit(PB, pb_repl)
    edit(GS, gs_repl)
