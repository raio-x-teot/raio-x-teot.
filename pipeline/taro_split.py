import re,json,sys
sys.path.insert(0,'/home/claude/teot/scripts')
T='/home/claude/teot/taro/txt/'
FILES={'2014':'a9780cc6-TARO_2014','2016':'2e343e36-TARO_2016','2017':'b0a3332b-TARO_2017','2018':'2c7ef90c-TARO_2018','2019':'2c993ec0-TARO_2019','2020':'54e74ac5-TARO_2020','2021':'a7d47d58-TARO_2021','2022':'95ffd5be-TARO_2022','2023':'947d7064-TARO_OFICIAL_2023','2024':'b60b4b40-TARO_2024_corrigido_e_com_refer_ncias','2025':'79b44fc0-TARO_2025_-_corrigido_e_com_refer_ncias','2026':'63667948-TARO_2026_-_CORRIGIDO_E_COM_REFERENCIAS_BIBLIOGR_FICAS'}
NQ={y:(120 if y=='2024' else 100) for y in FILES}
def book(s):
    u=s.upper()
    for k,v in [('SKELETAL TRAUMA','Skeletal Trauma'),('AND WILKINS','Rockwood Infantil'),('CHILDREN','Rockwood Infantil'),('RWP','Rockwood Infantil'),('ROCKWOOD PED','Rockwood Infantil'),('SKELETAL TRAUMA IN CHILDREN','Rockwood Infantil'),
                ('ROCKWOOD','Rockwood Adulto'),('ADULTS','Rockwood Adulto'),('TORNET','Rockwood Adulto'),('RWA','Rockwood Adulto'),('BUCHOLZ','Rockwood Adulto'),
                ('CAMPBELL','Campbell'),('CAMPBEL','Campbell'),('CMP','Campbell'),('AZAR','Campbell'),('CANALE','Campbell'),
                ('TACHDJIAN','Tachdjian'),('TACHDJAN','Tachdjian'),('HERRING','Tachdjian'),('TAC ','Tachdjian'),
                ('LOVELL','Lovell & Winter'),('LOWELL','Lovell & Winter'),('LOWEL','Lovell & Winter'),('WEINSTEIN','Lovell & Winter'),('LOW ','Lovell & Winter'),
                ('MOTTA','Motta (Ortop. e Traumat.)'),('GERALDO','Motta (Ortop. e Traumat.)'),('GMO','Motta (Ortop. e Traumat.)'),
                ('NETTER','Netter'),('NET ','Netter'),('SIZ','Hebert/Sizínio'),('HEBERT','Hebert/Sizínio'),
                ('FALOP','Propedêutica (Faloppa)'),('FALLOP','Propedêutica (Faloppa)'),('PROPEDÊUTICA','Propedêutica (Faloppa)'),('LEITE','Propedêutica (Faloppa)'),
                ('TARC','Exame físico (Tarcísio)'),('EXAME F','Exame físico (Tarcísio)'),
                ('SKELETAL TRAUMA','Skeletal Trauma'),('JUPITER','Skeletal Trauma'),('BROWNER','Skeletal Trauma'),
                ('EFORT','EFORT Textbook'),('AO ','Manual AO'),('PARDINI','Pardini (Mão)'),('INSALL','Insall & Scott'),('GREEN','Green (Mão)'),('ROCKWOOD AND MATSEN','Rockwood & Matsen (Ombro)'),
                ('CLIN ORTHOP','Artigo de periódico'),('J BONE','Artigo de periódico'),('JBJS','Artigo de periódico'),('ARQUIVO CET','Arquivo CET (imagem própria)')]:
        if k in u: return v
    return None
def split(y):
    t=open(T+FILES[y]+'.txt').read()
    lines=t.split('\n'); starts={}; exp=1
    for i,ln in enumerate(lines):
        m=re.match(r'^\s{0,12}0?(\d{1,3})\s*[\.\)\-,]?\s+([A-Za-zÀ-ú\"“].*)$',ln) or re.match(r'^\s{0,12}0?(\d{1,3})\s*[\.\)\-]\s*(\S.*)?$',ln)
        if m and int(m.group(1))==exp and exp<=NQ[y]:
            rest=(m.group(2) or '')
            if re.match(r'^(Ed|ed|Pg|p\.|Cap)',rest): continue
            # need some letters
            if exp>1 and rest and not re.search(r'[A-Za-zÀ-ú]',rest): continue
            starts[exp]=i; exp+=1
    qs={}; ks=sorted(starts)
    for j,n in enumerate(ks):
        end=starts[ks[j+1]] if j+1<len(ks) else None
        if end is None:
            # last question: cut at first line after 'D)' option block
            seg=lines[starts[n]:starts[n]+60]
            cut=len(seg)
            for k,l in enumerate(seg):
                if re.match(r'^\s*[Dd][\)\.]',l): cut=k+1; 
                if cut<len(seg) and k>cut+25: break
            q='\n'.join(seg[:max(cut,1)+ (30 if y in('2024','2025','2026') else 0)]); tail_from=starts[n]+cut
        else: q='\n'.join(lines[starts[n]:end])
        qs[n]=q
    tail='\n'.join(lines[(starts[ks[-1]]+1):]) 
    return qs,tail
def refs_from_tail(y,tail):
    # official list after questions
    L=[l for l in tail.split('\n')]
    # find ref section start
    st=0
    for i,l in enumerate(L):
        if re.search(r'Bibliografia|REFER[EÊ]NCIAS BIBLIO',l): st=i; break
    else:
        for i,l in enumerate(L):
            if book(l) and re.match(r'^\s*1\b',l): st=i; break
    L=L[st:]
    nums=[];bks=[]
    for i,l in enumerate(L):
        m=re.match(r'^\s{0,12}(\d{1,3})\s*[\.\)]?(\s|$)',l)
        if m and 1<=int(m.group(1))<=NQ[y]: nums.append((i,int(m.group(1))))
        b=book(l)
        if b: bks.append((i,b,l.strip()))
    out={}
    prev=-1
    nums=[x for x in nums]
    seen=set(); clean=[]
    for i,n in nums:
        if n in seen: continue
        seen.add(n); clean.append((i,n))
    for k,(i,n) in enumerate(clean):
        lo=prev+1
        seg=[b for b in bks if lo<=b[0]<=i]
        if not seg:
            seg=[b for b in bks if b[0]==i+1]
        prev=i
        if seg:
            b=seg[-1] if any(x[0]==i for x in seg)==False else [x for x in seg if x[0]==i][0]
            capm=re.search(r'(?:Cap\.?|cap|Capítulo)\s*([\d\.]+)',b[2]+' '+L[i])
            out[n]={'livro':b[1],'cap':capm.group(1).strip('.') if capm else '', 'origem':'Lista oficial da prova'}
    return out
def refs_inline(qs):
    out={}
    for n,q in qs.items():
        m=re.findall(r'(?:FONTE OFICIAL|Fonte oficial|Fonte Oficial|Fonte)\s*:?\s*([^\n]+)',q)
        m=[x for x in m if book(x) and not x.strip().upper().startswith('NETTER, F. H. ATLAS DE ANATOMIA HUMANA. 7. ED. RIO')] or [x for x in m if book(x)]
        if m:
            s=m[-1]; capm=re.search(r'cap\.?\s*([\d\.]+)',s,re.I)
            out[n]={'livro':book(s),'cap':capm.group(1).strip('.') if capm else '','origem':'Correção comentada (referência oficial)'}
    return out
if __name__=='__main__':
    allq={};allr={}
    for y in FILES:
        qs,tail=split(y)
        if y in('2024','2025','2026'): r=refs_inline(qs)
        elif y=='2023': r={}
        else: r=refs_from_tail(y,tail)
        miss=[n for n in range(1,NQ[y]+1) if n not in qs]
        bad=[n for n,q in qs.items() if not re.search(r'(^|\n)\s*[Dd]\s*[\)\.]',q)]
        print(y,len(qs),'miss',miss[:10],'noD',bad[:15],'refs',len(r))
        allq[y]={n:q for n,q in qs.items()}; allr[y]=r
    json.dump(allq,open('/home/claude/teot/taro/raw.json','w'),ensure_ascii=False)
    json.dump(allr,open('/home/claude/teot/taro/refs.json','w'),ensure_ascii=False,indent=0)
