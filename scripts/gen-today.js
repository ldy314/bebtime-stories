const https = require('https');
const fs = require('fs');
const { buildChinesePrompt, buildEnglishPrompt, getAgeInfo, getChineseWeekday, formatDateCn, formatDateShort } = require('./prompt-builder');
const age = getAgeInfo('2026-08-02');

function callAPI(prompt) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({
      model: 'deepseek-chat',
      messages: [
        { role: 'system', content: 'You are a creative children bedtime story writer. You always respond with valid JSON.' },
        { role: 'user', content: prompt }
      ],
      response_format: { type: 'json_object' },
      temperature: 0.85,
      max_tokens: 4096
    });
    const req = https.request({
      hostname: 'api.deepseek.com', path: '/v1/chat/completions', method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + process.env.DEEPSEEK_API_KEY, 'Content-Length': Buffer.byteLength(data) }
    }, res => { let b = ''; res.on('data', c => b += c); res.on('end', () => resolve(JSON.parse(b))); });
    req.on('error', reject);
    req.write(data); req.end();
  });
}

async function main() {
  const stories = JSON.parse(fs.readFileSync('stories.json', 'utf8'));

  console.log('=== 生成中文故事 ===');
  const zhPrompt = buildChinesePrompt('2026-08-02', age);
  const zhRes = await callAPI(zhPrompt);
  const zhStory = JSON.parse(zhRes.choices[0].message.content);

  console.log('=== 生成英文故事 ===');
  const enPrompt = buildEnglishPrompt('2026-08-02', age);
  const enRes = await callAPI(enPrompt);
  const enStory = JSON.parse(enRes.choices[0].message.content);

  const dateStr = '2026-08-02';
  const dateCn = formatDateCn(dateStr);
  const weekday = getChineseWeekday(dateStr);
  const dateShort = formatDateShort(dateStr);

  const zhObj = {
    id: '2026-08-02-cn', date: dateCn + ' · ' + weekday, dateShort,
    title: zhStory.title, language: 'zh', ageGroup: 'prenatal', ageLabel: '胎教期',
    preview: zhStory.preview, moral: zhStory.moral, content: zhStory.content
  };
  const enObj = {
    id: '2026-08-02-en', date: dateCn + ' · ' + weekday, dateShort,
    title: enStory.title, language: 'en', ageGroup: 'prenatal', ageLabel: 'Prenatal',
    preview: enStory.preview, moral: enStory.moral, content: enStory.content
  };

  const filtered = stories.filter(s => s.id !== '2026-08-02-cn' && s.id !== '2026-08-02-en');
  filtered.push(zhObj, enObj);
  fs.writeFileSync('stories.json', JSON.stringify(filtered, null, 2) + '\n', 'utf8');

  let html = fs.readFileSync('index.html', 'utf8');
  const jsonStr = JSON.stringify(filtered);
  const lines = html.split('\n');
  const idx = lines.findIndex(l => l.trim().startsWith('const EMBEDDED_STORIES = '));
  if (idx !== -1) { lines[idx] = 'const EMBEDDED_STORIES = ' + jsonStr + ';'; fs.writeFileSync('index.html', lines.join('\n'), 'utf8'); }

  console.log('\n=== 已保存 ===');
  console.log('中文:', zhObj.title, '| 预览:', zhObj.preview, '| 段落:', zhObj.content.length);
  console.log('英文:', enObj.title, '| 预览:', enObj.preview, '| 段落:', enObj.content.length);
  console.log('总故事数:', filtered.length);
}

main().catch(console.error);
