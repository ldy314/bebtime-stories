#!/usr/bin/env node
/**
 * Inject a single locally-authored (prenatal) story into all 4 copies:
 *   - D:\code test\睡前故事
 *   - C:\Users\Administrator\WorkBuddy\Claw\bedtime-story-app
 *   - C:\Users\Administrator\WorkBuddy\Claw\github-bedtime-stories
 *   - D:\code test\睡前故事\github-pages
 * Rewrites each index.html's EMBEDDED_STORIES single line.
 */
const fs = require('fs');
const path = require('path');

const COPIES = [
  'D:\\code test\\睡前故事',
  'C:\\Users\\Administrator\\WorkBuddy\\Claw\\bedtime-story-app',
  'C:\\Users\\Administrator\\WorkBuddy\\Claw\\github-bedtime-stories',
  'D:\\code test\\睡前故事\\github-pages',
];

const story = {
  id: '2026-08-10-cn-5',
  date: '2026年8月10日 · 星期一',
  dateShort: '08/10',
  title: '「台风天的小船」（胎教期）',
  language: 'zh',
  ageGroup: 'prenatal',
  ageLabel: '胎教期',
  preview: '台风来了，外面的风呼呼地吹，雨哗啦哗啦落下来，把整座城市都洗成了亮晶晶的水世界。',
  moral: '无论外面的风有多大、雨有多急，爸爸妈妈的爱和家，永远是你温暖又安全的小港湾。',
  content: [
    '台风来了，外面的风呼呼地吹，雨哗啦哗啦落下来，把整座城市都洗成了亮晶晶的水世界。',
    '爸爸开着小车出门，车轮下面咕嘟咕嘟冒着小水花，小车好像变成了一艘圆圆的小船，在水面上轻轻摇啊摇。',
    '红绿灯的倒影在水洼里晃呀晃，像一串温柔的星星。小车船慢慢划过街道，遇见的小树、小房子都朝它轻轻点头。',
    '不一会儿，小车船稳稳停在家的门口。妈妈张开温暖的怀抱，把你——还在肚子里的小宝宝——轻轻护住。你听见了吗？咚咚、咚咚，那是妈妈的心跳，像小船靠岸时，轻轻拍着水面的声音。',
    '风还在外面吹，雨还在外面下，可我们的小家，永远是干干爽爽、暖暖和和的小港湾。晚安，我的小船长。'
  ]
};

function rewriteEmbedded(html, stories) {
  const marker = 'EMBEDDED_STORIES';
  const idx = html.indexOf(marker);
  if (idx === -1) throw new Error('EMBEDDED_STORIES not found');
  // find the '=' after marker
  const eq = html.indexOf('=', idx);
  // the value is a JSON array on one line ending with ';'
  const semi = html.indexOf(';', eq);
  if (semi === -1) throw new Error('semicolon not found');
  const newLine = ' '.repeat(eq - html.lastIndexOf('\n', idx) - 1) ; // keep simple
  const prefix = html.slice(0, eq + 1);
  const suffix = html.slice(semi);
  return prefix + ' ' + JSON.stringify(stories) + suffix;
}

let total = 0;
for (const dir of COPIES) {
  const sj = path.join(dir, 'stories.json');
  const ih = path.join(dir, 'index.html');
  if (!fs.existsSync(sj)) { console.log('SKIP (no stories.json):', dir); continue; }
  const stories = JSON.parse(fs.readFileSync(sj, 'utf8'));
  if (stories.some(s => s.id === story.id)) {
    console.log('ALREADY present:', story.id, 'in', dir);
  } else {
    stories.push(story);
    fs.writeFileSync(sj, JSON.stringify(stories, null, 2), 'utf8');
    console.log('+ added to stories.json:', dir, '-> total', stories.length);
    total++;
  }
  // rewrite index.html EMBEDDED_STORIES (keep single line)
  if (fs.existsSync(ih)) {
    const html = fs.readFileSync(ih, 'utf8');
    const updated = rewriteEmbedded(html, stories);
    fs.writeFileSync(ih, updated, 'utf8');
    console.log('  rewrote index.html EMBEDDED_STORIES:', dir);
  }
}
console.log('Done. copies updated:', total);
