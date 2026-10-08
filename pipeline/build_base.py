import json,re,csv,glob,collections as C
B='/home/claude/teot/'
REN={'Manguito rotador':'Manguito rotador e impacto','Fratura de Monteggia (adulto)':'Fratura de Monteggia','Lesões por arma de fogo':'Lesões por arma de fogo e explosivos','Tumores benignos de células gigantes e condroblastoma':'Condroblastoma e lesões com células gigantes'}
TEMA={'BAS':'Ortopedia básica/geral','TA':'Trauma adulto','TP':'Trauma pediátrico','OP':'Ortopedia pediátrica','OC':'Ombro e cotovelo','MAO':'Mão e microcirurgia','COL':'Coluna','QUA':'Quadril','JOE':'Joelho','PE':'Pé e tornozelo','ONC':'Oncologia ortopédica','ANUL':'Anulada'}
REG={'OC':'Ombro e cotovelo','MAO':'Mão e punho','COL':'Coluna','QUA':'Quadril, pelve e coxa','JOE':'Joelho e perna','PE':'Pé e tornozelo','GER':'Geral / sistêmico'}
TIPO={'CLA':'Classificação','CON':'Conduta / técnica','DIA':'Diagnóstico (clínico/imagem)','ANA':'Anatomia / via de acesso','FIS':'Fisiopatologia / biomecânica / ciência básica','EPI':'Epidemiologia / frequência','CPX':'Complicação / prognóstico'}
teot=json.load(open(B+'base.json'))
stem_teot={r['id']:r['enunciado'] for r in teot}
ref_teot={r['id']:(r['livro'],r['cap'],r['ref_origem']) for r in teot}
traw=json.load(open(B+'taro/raw.json')); tref=json.load(open(B+'taro/refs.json'))
def short(s):
    s=re.sub(r'\s+',' ',s)
    s=re.sub(r'^\s*0?\d{1,3}\s*[\.\)\-,]?\s*','',s)
    m=re.search(r'^(.*?)(?=\s[Aa]\s?[\.\)])',s)
    st=m.group(1) if m else s[:250]
    st=re.sub(r'(AZAR|HERRING|TORNET+A|MOTTA|NETTER|WEINSTEIN|LEITE|WATERS|Fonte|MCKEE|Rockwood|Williams|Campbell|Capítulo|Humana|ed\. Rio|\] Anatomia|2018\.|Traumatologia: Princípios|Ortopédica e Traum|Winter|Elsevier|\d+\. ed\.|orthopaedics\.).*$','',st).strip()
    return st[:300]
rows=[]
def add(exame,ano,caderno,q,t,r,i,sub,tp,det,stem,ref):
    sub=REN.get(sub,sub)
    livro,cap,orig=ref
    rows.append(dict(exame=exame,ano=ano,caderno=caderno,q=q,id=f'{exame} {ano}{" anat." if caderno=="Anatomia" else ""}-{q}',tema=TEMA[t],regiao=REG[r],idade='Pediátrico' if i=='P' else 'Adulto',
        subtema=sub,tipo=TIPO[tp],detalhe=int(det),livro=livro,cap=cap,ref_origem=orig,anulada=int(t=='ANUL'),enunciado=stem,periodo='2021–2026' if ano>=2021 else '2014–2020'))
for fn,ex in [('2021','2021'),('2023','2023'),('2023A','2023A'),('2024','2024'),('2025','2025'),('2026','2026')]:
    for ln in open(B+f'class/{fn}.tsv'):
        q,t,r,i,sub,tp,det=ln.strip().split('|')
        oid=f'{ex}-{q}'
        add('TEOT',int(ex[:4]),'Anatomia' if ex.endswith('A') else 'Teórica',int(q),t,r,i,sub,tp,det,stem_teot[oid],ref_teot[oid])
for f in sorted(glob.glob(B+'taro/class/T*.tsv')):
    y=re.search(r'T(\d{4})',f).group(1)
    for ln in open(f):
        q,t,r,i,sub,tp,det=ln.strip().split('|')
        rf=tref.get(y,{}).get(q)
        ref=(rf['livro'],rf.get('cap',''),'Tabela oficial da prova' if rf['origem'].startswith('Lista') else rf['origem']) if rf else ('Não informada','','Não informada')
        if y=='2023': ref=('Não informada','','Não informada')
        add('TARO',int(y),'Teórica',int(q),t,r,i,sub,tp,det,short(traw[y][q]),ref)
json.dump(rows,open(B+'base2.json','w'),ensure_ascii=False)
with open(B+'base_questoes_TARO_TEOT.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys()),delimiter=';'); w.writeheader(); w.writerows(rows)
v=[x for x in rows if not x['anulada']]
print(len(rows),len(v),C.Counter((x['exame'],x['periodo']) for x in v))
