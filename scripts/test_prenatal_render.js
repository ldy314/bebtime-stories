// -*- coding: utf-8 -*-
const pb = require("C:/Users/Administrator/WorkBuddy/Claw/github-bedtime-stories/scripts/prompt-builder.js");

const PRE = "2026-08-05";   // before 2026-09-22 -> prenatal
const POST = "2026-10-01";  // after birthday -> 0-1 stage

function check(name, dateStr, fn) {
  const age = pb.getAgeInfo(dateStr);
  const out = fn(dateStr, age, dateStr);
  const hasCast = /小海螺·小旋旋|月亮妈妈|小星星·暖暖|小熊·安安|露珠邮递员·露露|云朵精灵·朵朵|小种子·芽芽|小鸟·啾啾|小闹钟·叮当/.test(out);
  const hasAnchors = /情感锚点|Emotional anchors/.test(out);
  // The crab PROHIBITION rule text itself mentions 螃蟹/crab — that is correct & desired for prenatal.
  // We assert the *rule* is present for prenatal and ABSENT for post-birth.
  const hasCrabRule = /螃蟹|大闸蟹|crab/i.test(out);
  const unborn = /绝不可把宝宝写成已经出生|never write the baby as already born/.test(out);
  console.log(`\n=== ${name} [${dateStr} / ${age.group}] ===`);
  console.log("  cast injected       :", hasCast);
  console.log("  emotional anchors   :", hasAnchors);
  console.log("  crab-rule injected  :", hasCrabRule);
  console.log("  unborn-baby rule    :", unborn);
  // show the protagonist chosen for determinism check
  const m = out.match(/(小海螺·小旋旋|月亮妈妈|小星星·暖暖|小熊·安安|露珠邮递员·露露|云朵精灵·朵朵|小种子·芽芽|小鸟·啾啾|小闹钟·叮当)/);
  if (m) console.log("  chosen protagonist :", m[1]);
  return { hasCast, hasAnchors, hasCrabRule, unborn };
}

console.log("getAgeInfo(2026-08-05) =", JSON.stringify(pb.getAgeInfo(PRE)));
console.log("getAgeInfo(2026-10-01) =", JSON.stringify(pb.getAgeInfo(POST)));

const cnPre = check("CN normal (prenatal)", PRE, (d, a) => pb.buildChinesePrompt(d, a));
const enPre = check("EN normal (prenatal)", PRE, (d, a) => pb.buildEnglishPrompt(d, a));
const sciCnPre = check("CN science (prenatal)", PRE, (d, a) => pb.buildScienceChinesePrompt(null, a, d));
const sciEnPre = check("EN science (prenatal)", PRE, (d, a) => pb.buildScienceEnglishPrompt(null, a, d));

const cnPost = check("CN normal (post-birth)", POST, (d, a) => pb.buildChinesePrompt(d, a));
const enPost = check("EN normal (post-birth)", POST, (d, a) => pb.buildEnglishPrompt(d, a));

// Assertions
let ok = true;
function assert(cond, msg) { if (!cond) { ok = false; console.log("ASSERT FAIL:", msg); } }
[cnPre, enPre, sciCnPre, sciEnPre].forEach((r, i) => {
  assert(r.hasCast, `prenatal prompt #${i} should inject cast`);
  assert(r.hasAnchors, `prenatal prompt #${i} should inject anchors`);
  assert(r.hasCrabRule, `prenatal prompt #${i} should inject the crab-prohibition rule`);
  assert(r.unborn, `prenatal prompt #${i} should contain unborn-baby rule`);
});
[cnPost, enPost].forEach((r, i) => {
  assert(!r.hasCast, `post-birth prompt #${i} must NOT inject cast`);
  assert(!r.hasAnchors, `post-birth prompt #${i} must NOT inject anchors`);
  assert(!r.hasCrabRule, `post-birth prompt #${i} must NOT inject the crab-prohibition rule`);
});

console.log("\nALL ASSERTIONS PASSED:", ok);
process.exit(ok ? 0 : 1);
