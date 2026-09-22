"""Build the two-page Humantech extended abstract (v1/paper/abs_paper.docx) from audited fps-text-v2 results.

Numbers in the table, figure and key sentences are read from the audited
summaries so the document cannot drift from the artifacts. Formatting is
copied from the official template (v1/paper/33rd_notitle.docx): full-width
title/abstract frames, then the two-column body.

Usage: python scripts/build_abs_paper_v2.py
Then run Word Inspect Document > Remove All (RemoveDocumentInformation) before submission.
"""
from copy import deepcopy
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, Cm

from rttdist.experiment_io import read_json, write_json, digest, timestamp

ROOT=Path(__file__).resolve().parents[1]
TEMPLATE=ROOT/'v1/paper/33rd_notitle.docx'
TARGET=ROOT/'v1/paper/abs_paper.docx'
H2=ROOT/'artifacts-commandcode/fps-v2/main'
H1=ROOT/'artifacts-commandcode/fps-v2-control/main'
FIGURE=ROOT/'v1/paper/abs_figure.png'
LABEL={'cpp':'C++','haskell':'Haskell','prolog':'Prolog','python':'Python','java':'Java'}
SHORT={'cpp':'C','haskell':'H','prolog':'P','python':'Py','java':'J'}
BATANG='바탕체'

def route_label(route):
    a,b=route.split('-via-');return f'{SHORT[a]}→{SHORT[b]}→{SHORT[a]}'

def set_font(run,size=10,bold=False,italic=False,latin='Times New Roman'):
    run.font.size=Pt(size);run.bold=bold;run.italic=italic
    fonts=run._element.get_or_add_rPr().get_or_add_rFonts()
    fonts.set(qn('w:ascii'),latin);fonts.set(qn('w:hAnsi'),latin);fonts.set(qn('w:eastAsia'),BATANG)

def add_runs(p,parts,size,bold=False):
    """parts: str or list of (text, {'b':..,'i':..}) segments."""
    if isinstance(parts,str):parts=[(parts,{})]
    for text,style in parts:
        set_font(p.add_run(text),size,style.get('b',bold),style.get('i',False))

def para(doc,parts,size=10,bold=False,align='both',indent=True,before=3,after=0,keep=False):
    p=doc.add_paragraph()
    p.alignment={'both':WD_ALIGN_PARAGRAPH.JUSTIFY,'left':WD_ALIGN_PARAGRAPH.LEFT,'center':WD_ALIGN_PARAGRAPH.CENTER}[align]
    f=p.paragraph_format;f.space_before=Pt(before);f.space_after=Pt(after);f.line_spacing=1.0
    f.first_line_indent=Pt(size) if indent else Pt(0);f.keep_with_next=keep;f.widow_control=True
    add_runs(p,parts,size,bold)
    return p

def heading(doc,text,before=6):
    return para(doc,text,11,True,'left',False,before,2,True)

def framed(doc,prototype,parts,size,bold):
    """Copy a full-width frame paragraph from the template and replace its text."""
    p=deepcopy(prototype)
    for r in p.findall(qn('w:r')):p.remove(r)
    body=doc.element.body
    body.insert(len(body)-1,p)  # the section properties must stay the last body child
    from docx.text.paragraph import Paragraph
    para_obj=Paragraph(p,doc._body)
    add_runs(para_obj,parts,size,bold)
    return para_obj

def table(doc,header,rows,widths):
    t=doc.add_table(rows=1+len(rows),cols=len(header));t.autofit=False
    tbl=t._tbl;pr=tbl.tblPr
    borders=OxmlElement('w:tblBorders')
    for edge,sz in [('top',8),('bottom',8),('insideH',0),('left',0),('right',0),('insideV',0)]:
        e=OxmlElement(f'w:{edge}');e.set(qn('w:val'),'single' if sz else 'nil')
        if sz:e.set(qn('w:sz'),str(sz));e.set(qn('w:space'),'0');e.set(qn('w:color'),'000000')
        borders.append(e)
    pr.append(borders)
    layout=OxmlElement('w:tblLayout');layout.set(qn('w:type'),'fixed');pr.append(layout)
    for r,values in enumerate([header]+rows):
        row=t.rows[r]
        row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
        for c,(cell,value,w) in enumerate(zip(row.cells,values,widths)):
            cell.width=Cm(w)
            if r==0:
                tcpr=cell._tc.get_or_add_tcPr();b=OxmlElement('w:tcBorders');e=OxmlElement('w:bottom')
                e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:space'),'0');e.set(qn('w:color'),'000000')
                b.append(e);tcpr.append(b)
            p=cell.paragraphs[0];p.alignment=WD_ALIGN_PARAGRAPH.LEFT if c==0 else WD_ALIGN_PARAGRAPH.CENTER
            f=p.paragraph_format;f.space_before=Pt(1);f.space_after=Pt(1);f.line_spacing=1.0;f.first_line_indent=Pt(0)
            f.keep_with_next=r<len(rows)
            set_font(p.add_run(value),8,r==0)
    for col,w in zip(t.columns,widths):col.width=Cm(w)
    return t

def fmt(x,digits=2):
    return 'NA' if x is None else f'{x:.{digits}f}'

def make_figure(h1,h2,diag1,path):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family':'Times New Roman','font.size':8})
    fig,axs=plt.subplots(2,1,figsize=(3.3,3.55),gridspec_kw={'height_ratios':[1.55,1]})
    order=[('cpp-via-python',h1,'#2a6f97'),('cpp-via-java',h1,'#2a6f97'),('cpp-via-haskell',h1,'#c8553d'),('cpp-via-prolog',h1,'#c8553d'),
           ('haskell-via-cpp',h2,'#7a7a7a'),('haskell-via-prolog',h2,'#7a7a7a'),('prolog-via-cpp',h2,'#7a7a7a'),('prolog-via-haskell',h2,'#7a7a7a')]
    for i,(route,s,color) in enumerate(order):
        r=s['routes'][route];p=r['p_sf'];lo,hi=r['bootstrap95']
        axs[0].errorbar(p,i,xerr=[[p-lo],[hi-p]],fmt='o',color=color,capsize=2.5,ms=4,lw=1)
        axs[0].text(1.04,i,f'{r["success"]}/{r["valid"]}',va='center',fontsize=7)
    axs[0].set_yticks(range(len(order)),[route_label(r) for r,_,_ in order]);axs[0].invert_yaxis()
    axs[0].set_xlim(-.03,1.0);axs[0].set_xlabel('$P_{sf}$ (problem bootstrap 95% CI)');axs[0].grid(axis='x',alpha=.25)
    axs[0].axhline(3.5,color='black',lw=.5,ls=':')
    import json
    routes=['cpp-via-python','cpp-via-java','cpp-via-haskell','cpp-via-prolog']
    values=[]
    for route in routes:
        vals=[]
        for obs in sorted(H1.glob(f'*/{route}/attempt-*/observation.json')):
            vals+=[s['sym_adj'] for s in read_json(obs)['steps'] if s.get('sym_adj') is not None]
        values.append(vals)
    box=axs[1].boxplot(values,vert=False,widths=.55,patch_artist=True,medianprops={'color':'black'},flierprops={'ms':2})
    for patch,color in zip(box['boxes'],['#2a6f97','#2a6f97','#c8553d','#c8553d']):patch.set_facecolor(color);patch.set_alpha(.45)
    axs[1].set_yticks(range(1,5),[f'{route_label(r)} (n={len(v)})' for r,v in zip(routes,values)]);axs[1].invert_yaxis()
    axs[1].axvline(.85,color='black',lw=.8,ls='--');axs[1].set_xlim(-.03,1.03)
    axs[1].set_xlabel('Adjacent restored similarity $Sym(x_{t-1},x_t)$')
    for ax in axs:ax.spines[['top','right']].set_visible(False)
    fig.tight_layout(h_pad=.8);fig.savefig(path,dpi=300,bbox_inches='tight');plt.close(fig)

def main():
    h1=read_json(H1/'summary.json');h2=read_json(H2/'summary.json')
    assert h1['complete'] and h2['complete'] and h1['recorded']==300 and h2['recorded']==450
    d1=read_json(H1/'diagnostics.json');d2=read_json(H2/'diagnostics.json');mb=read_json(H2/'diagnostics_multiblock.json')
    R1=h1['routes'];R2=h2['routes']
    pairs={(c['left'],c['right'],c['metric']):c for c in h1['paired_comparisons']}
    pp=lambda a,b,m='p_sf':pairs[(a,b,m)]
    bon_low=min(pp(a,b)['bonferroni95'][0] for a in ['cpp-via-python','cpp-via-java'] for b in ['cpp-via-haskell','cpp-via-prolog'])
    dn_diffs=[pp(a,b,'d_n')['mean_difference'] for a in ['cpp-via-python','cpp-via-java'] for b in ['cpp-via-haskell','cpp-via-prolog']]
    sym={r:d1['routes'][r]['sym_adj']['median'] for r in ['cpp-via-python','cpp-via-java','cpp-via-haskell','cpp-via-prolog']}
    rates={}
    for diag in (d1,d2):
        for v in diag['routes'].values():
            for k,x in v['step_pass_rate'].items():rates.setdefault(k.split('->')[1],[]).append(x['rate'])
    rng=lambda l:(min(rates[l])*100,max(rates[l])*100)
    nf={r:(R1[r]['categories']['success'],R1[r]['categories']['success']+R1[r]['categories']['fps_limit']+R1[r]['categories']['budget']) for r in R1}
    mb_rows=mb['rows'];mb_pass=sum(1 for x in mb_rows if x['last_block_status']=='success')
    mb_prolog=sum(1 for x in mb_rows if x['language']=='prolog')
    total_calls=h1['cost']['calls']+h2['cost']['calls']+read_json(ROOT/'artifacts-commandcode/fps-v2/main_design.json')['pilot_calls']

    doc=Document(TEMPLATE)
    body=doc.element.body;children=list(body)
    title_proto,blank_proto,abstract_proto=children[0],children[1],children[3]
    first_sect=deepcopy(children[47].find(qn('w:pPr')).find(qn('w:sectPr')))
    for child in children:body.remove(child)
    body.append(first_sect)  # section 1 of the template: first-page and even-page headers/footers

    framed(doc,title_proto,'왕복 번역의 근사 고정점으로 측정한 프로그래밍 패러다임 간 코드 번역 거리',20,True)
    framed(doc,blank_proto,'',10,False)
    framed(doc,abstract_proto,
        '(Abstract) 대규모 언어 모델(Large Language Model, LLM)의 코드 번역에서 패러다임 차이가 번역 안정성에 주는 영향을 '
        '왕복 번역(Round-Trip Translation, RTT)의 근사 고정점으로 측정하였다. 편도 번역마다 생성된 서로 다른 (언어, 소스) 상태의 수를 '
        '거리 dₙ으로, 모든 생성 코드가 기능 검사를 통과하고 상태 상한 안에서 인접 복원 코드의 유사도가 0.85에 도달한 시도의 비율을 '
        'P_sf로 정의하였다. C++, Haskell, Prolog로 검증한 15개 문제에 GLM-5.3 Flash를 적용하여, 사전 등록한 규칙으로 8개 경로 '
        f'690회 시도를 수행하였다. C++에서 같은 명령형인 Python과 Java를 거친 경로의 P_sf는 {R1["cpp-via-python"]["p_sf"]:.2f}와 '
        f'{R1["cpp-via-java"]["p_sf"]:.2f}로, 함수형 Haskell({R1["cpp-via-haskell"]["p_sf"]:.2f})과 논리형 Prolog({R1["cpp-via-prolog"]["p_sf"]:.2f})를 '
        '거친 경로보다 높았고, 네 비교의 Bonferroni 구간은 모두 0을 포함하지 않았다. 성공 시도의 dₙ은 대조 경로가 약 1 작았으나 구간이 0을 포함하였다. '
        f'실패의 대부분은 중간 언어의 생성 오류였으며 편도 기능 통과율은 Haskell {rng("haskell")[0]:.0f}~{rng("haskell")[1]:.0f}%, '
        f'Prolog {rng("prolog")[0]:.0f}~{rng("prolog")[1]:.0f}%였다. 결과는 패러다임 가설과 같은 방향이지만, '
        '그 차이가 모델의 언어별 생성 능력과 분리되지 않음을 보인다.',10,True)
    framed(doc,blank_proto,'',10,False)

    heading(doc,'1. 서론',0)
    para(doc,'LLM의 코드 번역은 문법 변환을 넘어 자료 구조, 제어 흐름과 입출력 동작의 보존을 요구한다. 번역 품질은 흔히 참조 번역이나 '
         '단위 테스트로 평가되지만[3], 패러다임이 다른 언어 사이에서 모델의 번역이 얼마나 안정적인지를 하나의 척도로 비교하기는 어렵다. '
         '자연어에서는 RTT를 고정점에 도달할 때까지 반복하고 그 과정의 고정점 집합(Fixed-Point Set, FPS) 크기를 언어 간 거리로 쓰는 방법이 제안되었다[1,2].')
    para(doc,'본 연구는 이 방법을 실행 가능한 코드로 옮겨 "패러다임이 다른 언어를 거칠수록 거리가 길어진다"는 가설을 검증한다. '
         '기여는 세 가지다. 첫째, 기능 검사와 결합한 코드 상태 기반 FPS 거리와 정지 기준을 정의한다. 둘째, 반복 시도와 사전 등록된 종료 규칙으로 '
         '도달률과 거리를 분리해 보고한다. 셋째, 같은 패러다임의 대조 경로를 두어 관찰된 차이의 원인을 진단한다.')

    heading(doc,'2. 방법')
    heading(doc,'2.1. 거리와 정지 기준',2)
    para(doc,'출발 언어 A의 원본을 x₀, t번째 중간 코드를 yₜ, A로 복원한 코드를 xₜ라 하면 경로는 x₀ → y₁ → x₁ → y₂ → x₂ → …이다. '
         'j번째 편도 번역이 만든 언어와 소스를 (Lⱼ, zⱼ), 줄바꿈만 LF로 통일한 소스의 SHA-256 해시를 h라 할 때 상태 집합과 크기는 다음과 같다.')
    para(doc,'S₀ = {(A, h(x₀))},  Sⱼ = Sⱼ₋₁ ∪ {(Lⱼ, h(zⱼ))},  Dⱼ = |Sⱼ|',10,False,'center',False,3,3)
    para(doc,'복원 단계에서 인접 복원 코드의 유사도 Sym(xₜ₋₁, xₜ)가 처음 θ = 0.85 이상이 되면 근사 고정점에 도달한 것으로 보고 '
         'dₙ = Dⱼ를 기록한다. Sym은 JPlag[4] text 모드의 평균 유사도(최소 일치 9토큰)이며 정지 기준으로만 쓴다. '
         '모든 생성 코드는 13개 평가 입력으로 검사하고, 코드 추출·컴파일·실행 실패, 오답, 시간 초과가 나오면 기능 실패로 종료한다. '
         'Dⱼ > 10이면 상한 초과, 편도 20회에 이르면 예산 소진으로 종료한다. 성공 판정은 θ 기준이며, 민감도 분석을 위해 0.90에 도달할 때까지 번역을 이어간다.')
    para(doc,'경로·문제마다 독립 시도를 5회 수행하고, P_sf는 문제별 성공 비율의 동일 가중 평균으로 집계한다. '
         'dₙ은 성공 시도에서만 정의되므로 P_sf와 함께 읽는다. 신뢰구간은 문제를 재표집하는 부트스트랩(2,000회)으로 구하고, 비교 쌍 수로 Bonferroni 보정한다.')
    heading(doc,'2.2. 실험 설정',2)
    para(doc,'IPOP 6문제와 LeetCode 9문제에 대해 C++, Haskell, Prolog 기준 코드 45개가 13개 입력을 모두 통과함을 확인하였다. '
         'H2는 세 언어 사이의 6개 방향 경로, H1은 C++에서 Python·Java를 거치는 대조 경로와 Haskell·Prolog를 거치는 처리 경로의 비교이다. '
         '모델은 GLM-5.3 Flash(temperature 0.6, top_p 0.95, 추론 강도 low, 시도별 seed)이며 도구는 GCC 14.2, GHC 9.10.3, SWI-Prolog 10.0.2, JPlag 6.3.0이다. '
         f'3문제 예비 실험 후 규칙을 동결했고, 총 {total_calls:,}회 호출에 비용은 약 0.43달러였다. 무효 시도는 없었다.')
    para(doc,'사전 점검에서 같은 편집을 세 언어 기준 코드에 적용했을 때 공백·주석·연산자·한 줄 삭제에 대한 Sym 변화는 언어 간 0.05 이내였다. '
         '다만 식별자 개명은 짧은 Haskell 코드에서 더 크게 떨어졌고(평균 0.62, C++ 0.79), 연산자 변경에는 거의 반응하지 않았다. '
         '따라서 Sym은 텍스트 안정성의 조작적 기준이며, 의미 보존은 기능 검사가 담당한다.')

    heading(doc,'3. 결과 및 고찰')
    para(doc,'표 1은 8개 경로의 주 결과이며, 모든 경로는 계획한 75회 시도를 완료하고 사후 감사를 통과하였다. '
         'H1의 판정 규칙은 실험 전에 정하였다. 대조 경로의 P_sf가 높고 dₙ이 작으며 문제 단위 구간이 0을 포함하지 않으면 지지, '
         '두 지표 중 하나만 만족하면 부분 지지, 방향이 반대이거나 구간이 0을 포함하면 기각으로 본다.')
    heading(doc,'3.1. H1: 같은 패러다임 대조 경로와의 비교',2)
    para(doc,f'대조 경로의 P_sf는 처리 경로보다 {min(pp(a,b)["mean_difference"] for a in ["cpp-via-python","cpp-via-java"] for b in ["cpp-via-haskell","cpp-via-prolog"]):.2f}~'
         f'{max(pp(a,b)["mean_difference"] for a in ["cpp-via-python","cpp-via-java"] for b in ["cpp-via-haskell","cpp-via-prolog"]):.2f} 높았고, '
         f'네 비교의 Bonferroni 95% 구간 하한은 모두 {bon_low:.2f} 이상이었다. 임계값을 0.80이나 0.90으로 바꾸거나 예비 실험 문제를 빼도 결론은 같았다. '
         f'성공 시도의 dₙ 차이는 {min(dn_diffs):.1f}~{max(dn_diffs):.1f}로 대조 경로가 작은 방향이었으나, 두 경로가 함께 성공한 문제가 2~6개뿐이라 구간이 0을 포함하였다. '
         '사전 규칙에 따라 H1은 P_sf에서 지지, dₙ에서 방향만 일치하는 부분 지지로 판정한다.')
    para(doc,'표 1. 경로별 도달률과 성공 조건부 거리 (θ = 0.85, 경로당 75회)',9,True,'left',False,3,2,True)
    rows=[]
    for route,s in [(r,R1[r]) for r in ['cpp-via-python','cpp-via-java','cpp-via-haskell','cpp-via-prolog']]+[(r,R2[r]) for r in ['haskell-via-cpp','haskell-via-prolog','prolog-via-cpp','prolog-via-haskell']]:
        lo,hi=s['bootstrap95'];d=s['d_n']
        rows.append([route_label(route),f'{s["success"]}/{s["valid"]}',f'{s["p_sf"]:.2f} [{lo:.2f}, {hi:.2f}]',
                     'NA' if not d['n'] else f'{d["mean"]:.1f} ({d["n"]})',str(s['categories']['functional_failure']),str(s['categories']['fps_limit'])])
    table(doc,['경로','성공','P_sf [95% CI]','dₙ 평균 (n)','기능실패','상한'],rows,[1.75,1.1,2.3,1.3,1.0,1.1])
    para(doc,'C=C++, H=Haskell, P=Prolog, Py=Python, J=Java. 위 네 경로가 H1, 아래 네 경로와 C→H→C, C→P→C가 H2이다. '
         '예산 소진과 무효는 모든 경로에서 0이다.',8.5,False,'left',False,2,4)
    heading(doc,'3.2. H2: 세 패러다임 사이의 방향 경로',2)
    c=h2['paired_comparisons'][0]
    para(doc,f'C→H→C가 {R2["cpp-via-haskell"]["p_sf"]:.2f}로 가장 높았고 H→C→H {R2["haskell-via-cpp"]["p_sf"]:.2f}, C→P→C {R2["cpp-via-prolog"]["p_sf"]:.2f} 순이었으며, '
         f'Prolog가 포함된 나머지 세 경로는 성공이 없었다. C++와 Haskell의 방향 차이는 {c["mean_difference"]:.2f} [{c["bonferroni95"][0]:.2f}, {c["bonferroni95"][1]:.2f}]로 '
         '비대칭을 확정할 수 없었고, 경로 순위는 세 임계값에서 같았다.')
    heading(doc,'3.3. 차이는 어디에서 왔는가',2)
    para(doc,f'편도 번역의 기능 통과율은 생성 언어에 따라 C++ {rng("cpp")[0]:.0f}~{rng("cpp")[1]:.0f}%, Python {rng("python")[0]:.0f}%, Java {rng("java")[0]:.0f}%, '
         f'Haskell {rng("haskell")[0]:.0f}~{rng("haskell")[1]:.0f}%, Prolog {rng("prolog")[0]:.0f}~{rng("prolog")[1]:.0f}%였다. '
         '성공에는 중간 언어 생성이 여러 번 연속으로 통과해야 하므로, 처리 경로의 낮은 P_sf는 대부분 이 생성 실패에서 나온다. '
         f'기능 실패가 없던 시도만 보면 도달 비율은 Python {nf["cpp-via-python"][0]}/{nf["cpp-via-python"][1]}, Java {nf["cpp-via-java"][0]}/{nf["cpp-via-java"][1]}, '
         f'Haskell {nf["cpp-via-haskell"][0]}/{nf["cpp-via-haskell"][1]}, Prolog {nf["cpp-via-prolog"][0]}/{nf["cpp-via-prolog"][1]}로 차이가 줄었다.')
    para(doc,f'그럼에도 기능이 보존된 복원 코드끼리의 인접 Sym 중앙값은 Python {sym["cpp-via-python"]:.2f}, Java {sym["cpp-via-java"]:.2f}, '
         f'Haskell {sym["cpp-via-haskell"]:.2f}, Prolog {sym["cpp-via-prolog"]:.2f}로(Fig. 1 아래), 다른 패러다임을 거친 C++는 왕복마다 더 크게 다시 쓰였다. '
         f'또한 H2의 코드 추출 실패 {len(mb_rows)}건은 모두 한 응답에 초안과 수정본 등 여러 코드 블록을 낸 경우였고 {mb_prolog}건이 Prolog 생성이었다. '
         f'사후 진단으로 마지막 블록만 평가하면 {mb_pass}건이 통과했으나, 이는 주 결과에 반영하지 않았다.')
    make_figure(h1,h2,d1,FIGURE)
    p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before=Pt(0);p.paragraph_format.space_after=Pt(2)
    p.add_run().add_picture(str(FIGURE),width=Cm(8.6))
    para(doc,'Fig. 1. 경로별 P_sf와 문제 단위 부트스트랩 95% 구간(위, 점선 위는 H1 네 경로), H1 경로의 인접 복원 유사도 분포(아래, 점선은 θ = 0.85). '
         '파란색은 같은 패러다임 대조, 빨간색은 처리 경로이다.',9,True,'left',False,2,4)

    heading(doc,'4. 결론')
    para(doc,'코드 RTT에서 도달률 P_sf와 성공 조건부 거리 dₙ을 분리하여 측정하고, 같은 패러다임 대조 경로와 비교하였다. '
         '이 모델과 설정에서 C++는 Python·Java를 거칠 때 근사 고정점에 훨씬 자주 도달하였고, 이는 패러다임이 다를수록 거리가 길어진다는 가설과 같은 방향이다. '
         '그러나 주된 기제는 중간 언어의 생성 실패였으며, Python·Java는 명령형이면서 학습 자료가 가장 많은 언어이기도 하다. '
         '따라서 결과를 패러다임 자체의 거리로 해석하지 않고, 모델의 언어별 능력과 결합된 관찰로 한정한다. '
         'dₙ은 공통 성공 문제가 적어 비교력이 낮았고, JPlag text 유사도는 짧은 코드와 연산자 변경에 한계가 있다. '
         '후속 연구로 상위 모델에서의 재실행, 기능 실패와 수렴을 분리한 조건부 지표의 사전 등록, 문제 수 확대를 수행할 계획이다.')

    heading(doc,'참고문헌')
    refs=[
        [('[1] Cho, C. et al. Computing the Distance Between Languages Based on Round Trip Translation and Fixed Points. ',{}),
         ('Proc. Korea Software Congress',{'i':True}),(' ',{}),('2025',{'b':True}),(', 1467–1469 (2025)',{})],
        [('[2] Crone, N. et al. Quality Estimation Using Round-Trip Translation with Sentence Embeddings. ',{}),
         ('arXiv',{'i':True}),(': 2111.00554 (2021)',{})],
        [('[3] Roziere, B. et al. Unsupervised Translation of Programming Languages. ',{}),
         ('Adv. Neural Inf. Process. Syst.',{'i':True}),(' ',{}),('33',{'b':True}),(', 20601–20611 (2020)',{})],
        [('[4] Prechelt, L. et al. Finding Plagiarisms among a Set of Programs with JPlag. ',{}),
         ('J. Univers. Comput. Sci.',{'i':True}),(' ',{}),('8',{'b':True}),(', 1016–1038 (2002)',{})]]
    for ref in refs:
        p=para(doc,ref,9,False,'both',False,1,0)
        p.paragraph_format.left_indent=Pt(13);p.paragraph_format.first_line_indent=Pt(-13)

    props=doc.core_properties
    for attr in ['author','last_modified_by','comments','keywords','subject','category']:setattr(props,attr,'')
    props.title='왕복 번역의 근사 고정점으로 측정한 프로그래밍 패러다임 간 코드 번역 거리'
    props.revision=1
    doc.save(TARGET)
    write_json(ROOT/'v1/paper/abs_paper_provenance.json',{'at':timestamp(),'document_sha256':digest(TARGET.read_bytes()),
        'h1_summary_sha256':digest((H1/'summary.json').read_bytes()),'h2_summary_sha256':digest((H2/'summary.json').read_bytes()),
        'builder_sha256':digest(Path(__file__).read_bytes())})
    print(TARGET)

if __name__=='__main__':main()
