// This adapter evaluates only reviewed files with the pinned per-file SHA-256.
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),crypto=require('node:crypto');
const root=path.resolve(__dirname,'..'),checkout=path.resolve(process.argv[2]);
const manifest=JSON.parse(fs.readFileSync(path.join(root,'manifest.json'),'utf8'));
const requests=JSON.parse(fs.readFileSync(0,'utf8'));
const results=[];
for(const request of requests) {
  const p=manifest.problems.find(p=>p.id===request.id);
  const bytes=fs.readFileSync(path.join(checkout,p.upstream_path));
  if(crypto.createHash('sha256').update(bytes).digest('hex')!==p.upstream_sha256) throw Error('Source hash mismatch: '+p.problem_id);
  const ctx=vm.createContext({args:request.args});
  new vm.Script(bytes.toString('utf8'),{filename:p.upstream_path}).runInContext(ctx,{timeout:5000});
  const expression=p.id===283 ? 'moveZeroes(...args); args[0]' : `${p.function}(...args)`;
  let result=new vm.Script(expression).runInContext(ctx,{timeout:5000});
  if(p.id===1)result=result.slice().sort((a,b)=>a-b);
  const equal=JSON.stringify(result)===JSON.stringify(request.expected);
  const row={problem_id:p.problem_id,case_id:request.case_id,status:equal?'pass':'fail'};
  if(!equal)Object.assign(row,{expected:request.expected,actual:result});
  results.push(row);
}
process.stdout.write(JSON.stringify({node_version:process.version,results}));
