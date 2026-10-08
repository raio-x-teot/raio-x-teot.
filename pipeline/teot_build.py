import json,re,csv
B='/home/claude/teot/'
raw=json.load(open(B+'raw_questions.json')); refs=json.load(open(B+'refs.json'))
exec(open(B+'scripts/refs.py').read().split('refs={}')[0].replace("D='/home/claude/teot/txt/'",""))
TEMA={'BAS':'Ortopedia básica/geral','TA':'Trauma adulto','TP':'Trauma pediátrico','OP':'Ortopedia pediátrica','OC':'Ombro e cotovelo','MAO':'Mão e microcirurgia','COL':'Coluna','QUA':'Quadril','JOE':'Joelho','PE':'Pé e tornozelo','ONC':'Oncologia ortopédica','ANUL':'Anulada'}
REG={'OC':'Ombro e cotovelo','MAO':'Mão e punho','COL':'Coluna','QUA':'Quadril, pelve e coxa','JOE':'Joelho e perna','PE':'Pé e tornozelo','GER':'Geral / sistêmico'}
TIPO={'CLA':'Classificação','CON':'Conduta / técnica','DIA':'Diagnóstico (clínico/imagem)','ANA':'Anatomia / via de acesso','FIS':'Fisiopatologia / biomecânica / ciência básica','EPI':'Epidemiologia / frequência','CPX':'Complicação / prognóstico'}
def short(s):
    s=re.sub(r'\s+',' ',s)
    m=re.search(r'^(.*?)(?=\s[A]\s?[\.\)])',s)
    st=(m.group(1) if m else s[:250])
    st=re.sub(r'(AZAR|HERRING|TORNET+A|MOTTA|NETTER|WEINSTEIN|LEITE|WATERS|Fonte|MCKEE|Rockwood|Williams|Campbell|Capítulo|Humana|ed\. Rio|\] Anatomia|2018\.|Traumatologia: Princípios|Ortopédica e Traum|Winter).*$','',st).strip()
    st=re.sub(r'\s\d{1,3}$','',st)
    return st[:300]
rows=[]
for ex,fn,prova in [('2021','2021','Teórica'),('2023','2023','Teórica'),('2023A','2023A','Anatomia (caderno separado)'),('2024','2024','Teórica'),('2025','2025','Teórica + anatomia'),('2026','2026','Teórica + anatomia')]:
    for ln in open(B+f'class/{fn}.tsv'):
        q,t,r,i,sub,tp,det=ln.strip().split('|')
        ano=ex[:4]; s=raw[ex][q]
        ref=refs.get(ex,{}).get(q)
        if ref: livro,cap,orig=ref['livro'],ref.get('cap',''),ref['origem']
        else:
            m=re.search(r'Fonte:?\s*([^\n]+(?:\n[^\n]+)?)',s)
            if m: livro,cap,orig=book(m.group(1)),'','Fonte da imagem (sem tabela oficial)'
            else: livro,cap,orig='Não informada','','Não informada'
        rows.append(dict(ano=int(ano),prova=prova,q=int(q),id=f'{ex}-{q}',tema_cod=t,tema=TEMA[t],regiao=REG[r],idade='Pediátrico' if i=='P' else 'Adulto',
            natureza=('Trauma' if t in('TA','TP') else 'Oncologia' if t=='ONC' else 'Ortopedia'),subtema=sub,tipo=TIPO[tp],detalhe=int(det),
            livro=livro,cap=cap,ref_origem=orig,anulada=int(t=='ANUL'),enunciado=short(s)))
json.dump(rows,open(B+'base.json','w'),ensure_ascii=False,indent=0)
with open(B+'base_questoes_TEOT.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys()),delimiter=';'); w.writeheader(); w.writerows(rows)
print(len(rows))
