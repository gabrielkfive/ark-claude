// Cliente do ark-publisher (fila que publica pelo Composio). Sem segredo aqui:
// o acesso vem de private/client.json do publisher ou de ~/.ark/publisher.json.
// Uso: node publisher.mjs status | schedule job.json | prepare JOB_ID | hash <arquivo ou URL https>
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';

const CANDIDATOS = [
  path.join(os.homedir(), 'Documents', 'ARK CONTENT', 'SOFTWARE', 'ark-publisher', 'private', 'client.json'),
  path.join(os.homedir(), '.ark', 'publisher.json'),
];

async function acesso() {
  for (const p of CANDIDATOS) {
    try { const c = JSON.parse(await fs.readFile(p, 'utf8')); if (c.url && c.token) return c; } catch {}
  }
  throw new Error('Sem acesso ao publisher. Peça ao Gabriel o arquivo de acesso e salve em ' + CANDIDATOS[1]);
}

async function hash(alvo) {
  const h = crypto.createHash('sha256');
  if (/^https:\/\//.test(alvo)) {
    const r = await fetch(alvo, { redirect: 'follow', signal: AbortSignal.timeout(300000) });
    const tipo = r.headers.get('content-type') || '';
    if (!r.ok || tipo.includes('text/html')) throw new Error(`Link não serve o arquivo (HTTP ${r.status}, ${tipo}). Libere "qualquer pessoa com o link".`);
    let bytes = 0;
    for await (const parte of r.body) { h.update(parte); bytes += parte.length; }
    return { sha256: h.digest('hex'), bytes, tipo };
  }
  const buf = await fs.readFile(alvo);
  h.update(buf);
  return { sha256: h.digest('hex'), bytes: buf.length };
}

const [cmd, arg] = process.argv.slice(2);
if (cmd === 'hash') {
  console.log(JSON.stringify(await hash(arg), null, 2));
} else {
  let rota = '/jobs', metodo = 'GET', corpo;
  if (cmd === 'schedule') { metodo = 'POST'; corpo = await fs.readFile(path.resolve(arg), 'utf8'); }
  else if (cmd === 'prepare') { rota = `/jobs/${encodeURIComponent(arg)}/prepare`; metodo = 'POST'; }
  else if (cmd !== 'status') throw new Error('Use: node publisher.mjs status | schedule job.json | prepare JOB_ID | hash <arquivo ou URL>');
  const c = await acesso();
  const r = await fetch(c.url + rota, { method: metodo, headers: { authorization: `Bearer ${c.token}`, 'content-type': 'application/json' }, body: corpo, signal: AbortSignal.timeout(55000) });
  console.log(JSON.stringify(await r.json(), null, 2));
  if (!r.ok) process.exitCode = 1;
}
