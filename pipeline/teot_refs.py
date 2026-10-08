import re,json
D='/home/claude/teot/txt/'
def book(s):
    s=s.upper()
    for k,v in [('ROCKWOOD AND WILKINS','Rockwood Infantil'),('FRACTURES IN CHILDREN','Rockwood Infantil'),('ROCKWOOD AND GREEN','Rockwood Adulto'),('TORNETT','Rockwood Adulto'),('ARQUIVO CET','Arquivo CET (imagem própria)'),('CAMPBEL','Campbell'),('FRACTURES IN ADULTS','Rockwood Adulto'),('CAMPBELL','Campbell'),('TACHDJIAN','Tachdjian'),('LOVELL','Lovell & Winter'),('PROPEDÊUTICA','Propedêutica (Faloppa)'),('FALOPPA','Propedêutica (Faloppa)'),('FALLOPA','Propedêutica (Faloppa)'),('MOTTA','Motta (Ortop. e Traumat.)'),('GERALDO','Motta (Ortop. e Traumat.)'),('SIZÍNIO','Hebert/Sizínio'),('HEBERT','Hebert/Sizínio'),('NETTER','Netter'),('INSALL','Insall & Scott'),('TARC','Exame físico (Tarcísio)'),('EXAME F','Exame físico (Tarcísio)')]:
        if k in s: return v
    return s[:40]
refs={}
# 2021
t=open(D+'0a36f328-TEOT-Prova-Te_rica_2021.txt').read().split('Bibliografia',1)[1]
lines=t.split('\n'); r={}; buf=''; 
# entries: number may be at line start or on its own line between wrapped lines
ent=[]; cur=None
for ln in lines:
    m=re.match(r'^\s{0,4}(\d{1,2})\s{2,}(\S.*)$',ln)
    m2=re.match(r'^\s*(\d{1,2})\s*$',ln)
    if m: ent.append([int(m.group(1)),m.group(2)])
    elif m2: ent.append([int(m2.group(1)),''])
    elif ln.strip() and ent is not None:
        ent.append([None,ln.strip()])
# merge: an entry with number; text lines before (if number alone) or after belong
q={}
i=0
txt=[e for e in ent]
# simple approach: group text between successive 'Cap' terminators
blocks=[]; cur_n=None; cur=''
pending=[]
for n,s in txt:
    if n is not None and s=='' : cur_n=n; 
    if n is not None and s: cur_n=n
    cur+=' '+s
    if re.search(r'(Cap|cap|seção)[^.]*\d',s) and cur_n is not None:
        q[cur_n]=cur.strip(); cur=''; cur_n=None
refs['2021']={k:{'livro':book(v),'cap':(re.findall(r'(?:Cap\.?|cap|seção)\s*([\w\.\d]+)',v) or [''])[-1].strip('.'),'origem':'Tabela oficial da prova'} for k,v in q.items()}
# 2024
t=open(D+'2024_reftab.txt').read()
q={}; cur=''
for ln in t.split('\n'):
    m=re.match(r'^\s*(\d{1,3})\s+(.*?)\s{2,}([\d\.]+)\s+([A-D])\s*$',ln)
    if m:
        q[int(m.group(1))]={'livro':book(cur+' '+m.group(2)),'cap':m.group(3),'origem':'Tabela oficial da prova','gab':m.group(4)}; cur=''
    else: cur+=' '+ln
refs['2024']=q
# 2025
d=json.load(open('/home/claude/teot/raw_questions.json'))
q={}
for n,s in d['2025'].items():
    m=re.search(r'([A-ZÀ-Ú][A-ZÀ-Ú\-]+,[^\n]{0,30}\.[^\n]*?(?:\n[^\n]*?){0,2}?(?:Cap[ií]tulo|Cap\.?)\s*:?\s*([\w\.]+))',s)
    if m: q[int(n)]={'livro':book(m.group(1)),'cap':m.group(2).strip('.'),'origem':'Tabela oficial (via correção comentada)'}
    else:
        m=re.search(r'Fonte Oficial:?\s*([^\n]+)',s)
        if m: q[int(n)]={'livro':book(m.group(1)),'cap':(re.findall(r'cap\.?\s*(\d+)',m.group(1),re.I) or [''])[0],'origem':'Correção comentada'}
refs['2025']=q
json.dump(refs,open('/home/claude/teot/refs.json','w'),ensure_ascii=False,indent=1)
for k,v in refs.items():
    print(k,len(v),[x for x in range(1,{'2021':81,'2024':101,'2025':121}[k]) if x not in v])
    from collections import Counter; print(Counter(x['livro'] for x in v.values()).most_common())
