"""Run the prespecified text-similarity diagnostics before model translation."""
from pathlib import Path
from rttdist.experiment_io import digest, read_json, write_json, timestamp
from rttdist.jplag_similarity import measure

ROOT=Path(__file__).resolve().parents[1]

def config():
    jar=ROOT/'jplag-6.3.0-jar-with-dependencies.jar'
    return {'java':'C:/Users/sigma/scoop/apps/openjdk/current/bin/java.exe',
            'jar':str(jar),'jar_sha256':digest(jar.read_bytes()),'language':'text',
            'minimum_tokens':9,'normalize':False,'similarity_field':'averageSimilarity',
            'scale':[0,1],'threshold':0,'cluster':False,'match_merging':False}

def main():
    root=ROOT/'artifacts-lmstudio/fps-v1/calibration'
    results=[]
    for lang,ext in [('cpp','cpp'),('haskell','hs'),('prolog','pl')]:
        source=(ROOT/f'data/fps-v1/IPOP_2609/reference.{ext}').read_text(encoding='utf-8')
        comment={'cpp':'// diagnostic comment\n','haskell':'-- diagnostic comment\n','prolog':'% diagnostic comment\n'}[lang]
        changes={'identical':source,'repeat':source,'whitespace':source.replace(' ','  '),
                 'comment':comment+source, 'identifier':source.replace('gcd','greatest_common_divisor').replace('euclid','greatest_common_divisor'),
                 'operator':source.replace('*','+'),'short':'x',
                 'wrapper':source[:source.find('main')] if 'main' in source else ''}
        # Supplementary after main began; this never retunes its frozen threshold.
        changes['branch_supplementary']={
            'cpp':source.replace('b != 0','b == 0'),
            'haskell':source.replace('euclid a 0 = a','euclid a 0 = 0'),
            'prolog':source.replace('gcd_value(A, 0, A)','gcd_value(A, 0, 0)')}[lang]
        for variant,candidate in changes.items():
            m=measure(source,candidate,root/lang/variant,config=config())
            results.append({'language':lang,'variant':variant,'status':m['status'],'value':m['value'],'reason':m['reason']})
            print(lang,variant,m['status'],m['value'],flush=True)
    write_json(root/'diagnostics.json',{'created_at':timestamp(),'config':config(),'results':results})

if __name__=='__main__':main()
