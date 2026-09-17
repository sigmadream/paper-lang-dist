// Only the three reviewed, hash-pinned source files are evaluated by this adapter.
// vm provides a timeout, not a security sandbox for arbitrary upstream code.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');

const base = path.resolve(__dirname, '..');
const checkout = path.resolve(process.argv[2]);
const manifest = JSON.parse(fs.readFileSync(path.join(base, 'manifest.json'), 'utf8'));
const normalize = s => s.trim().split(/\s+/).join(' ');
const results = [];
for (const p of manifest.problems.filter(p => p.upstream_mapping)) {
  const mapping = p.upstream_mapping;
  const bytes = fs.readFileSync(path.join(checkout, mapping.path));
  if (crypto.createHash('sha256').update(bytes).digest('hex') !== mapping.sha256)
    throw new Error(`Upstream hash mismatch: ${mapping.path}`);
  for (const c of p.cases) {
    const tokens = fs.readFileSync(path.join(base, c.input), 'utf8').trim().split(/\s+/);
    const context = vm.createContext({tokens});
    let adapter;
    if (p.problem_id === 'IPOP_10988') {
      adapter = 'String(Number(isPalindrome(tokens[0])))';
    } else if (p.problem_id === 'IPOP_9012') {
      adapter = 'tokens.slice(1).map(s => isValid(s) ? "YES" : "NO").join("\\n")';
    } else {
      new vm.Script(`function Node(val,isLeaf,topLeft,topRight,bottomLeft,bottomRight) {
        Object.assign(this,{val,isLeaf,topLeft,topRight,bottomLeft,bottomRight});
      }
      function encode(n) {
        return n.isLeaf ? String(Number(n.val)) : "(" +
          [n.topLeft,n.topRight,n.bottomLeft,n.bottomRight].map(encode).join("") + ")";
      }`).runInContext(context, {timeout:5000});
      adapter = 'encode(construct(tokens.slice(1).map(row => [...row].map(Number))))';
    }
    new vm.Script(bytes.toString('utf8'), {filename:mapping.path}).runInContext(context,{timeout:5000});
    const actual = new vm.Script(adapter).runInContext(context,{timeout:5000});
    const expected = fs.readFileSync(path.join(base,c.output),'utf8');
    results.push({problem_id:p.problem_id, case_id:c.case_id,
      status:normalize(actual)===normalize(expected)?'pass':'fail'});
  }
}
process.stdout.write(JSON.stringify({node_version:process.version, cases:results}));
if (results.some(r=>r.status!=='pass')) process.exitCode=1;
