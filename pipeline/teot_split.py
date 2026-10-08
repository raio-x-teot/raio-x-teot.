import re, json, sys
def clean(t):
    t = re.sub(r'[ \t]+', ' ', t)
    t = re.sub(r'\n\s*\n+', '\n', t)
    return t.strip()
out = {}
D='/home/claude/teot/txt/'
# 2021
t = open(D+'0a36f328-TEOT-Prova-Te_rica_2021.txt').read()
body, refs = t.split('REFER',1) if 'REFER' in t else (t,'')
qs = re.split(r'\n\s*(\d{1,2})\.\s+', '\n'+body)
q21={}
for i in range(1,len(qs),2):
    n=int(qs[i]); 
    if n not in q21: q21[n]=clean(qs[i+1])
out['2021']=q21
# 2023
t = open(D+'9344864f-TEOT_2023.txt').read()
t = re.sub(r'Prova Teórica: Verde – pág\. \d+','',t)
qs = re.split(r'\n\s*(\d{1,3})\)\s+', '\n'+t.split('Boa Prova!')[1])
out['2023']={int(qs[i]):clean(qs[i+1]) for i in range(1,len(qs),2)}
# 2023 anatomia
t = open(D+'348a7004-TEOT_2023-_Prova-de-Anatomia-1.txt').read()
qs = re.split(r'\n\s*(\d{1,3})\)\s+', '\n'+t)
out['2023A']={int(qs[i]):clean(qs[i+1]) for i in range(1,len(qs),2)}
# 2024
t = open(D+'d7aa0177-TEOT_2024-PROVA-BRANCA-ARQUIVO-FINAL-PARA-PUBLICA__O.txt').read()
t = re.sub(r'Prova Escrita: Branca – Pág\. \d+','',t)
body = t.split('Boa Prova!')[1]
idx = body.find('Bibliografia')
body, reftab = body[:idx], body[idx:]
qs = re.split(r'\n\s*(\d{1,3})\.\s+', '\n'+body)
q={}
for i in range(1,len(qs),2):
    n=int(qs[i])
    if n not in q and n<=100: q[n]=clean(qs[i+1])
out['2024']=q
open('/home/claude/teot/txt/2024_reftab.txt','w').write(reftab)
# 2025
t = open(D+'315e7d2f-TEOT_2025_-__corrigido_e_com_referencia_oficial.txt').read()
t = re.sub(r'ELABORADO POR.*\n.*INSTAGRAM.*\n.*TEOT 2025- Correção utilizando a referência oficial','',t)
qs = re.split(r'\n\s*(\d{1,3})-\s+', '\n'+t)
q={}
for i in range(1,len(qs),2):
    n=int(qs[i])
    if n not in q and n<=120: q[n]=clean(qs[i+1])
out['2025']=q
# 2026
t = open(D+'26cols.txt').read()
qs = re.split(r'\n\s*Item[: ]*(\d{1,3})\s*:?\s*', '\n'+t)
q={}
for i in range(1,len(qs),2):
    n=int(qs[i]); q.setdefault(n,clean(qs[i+1]))
out['2026']=q
json.dump(out, open('/home/claude/teot/raw_questions.json','w'), ensure_ascii=False, indent=1)
for k,v in out.items():
    ks=sorted(v); print(k, len(ks), 'max',max(ks), 'missing', [x for x in range(1,max(ks)+1) if x not in v])
