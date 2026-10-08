"""Monta index.html a partir de page/ e data/base.json.
Uso (na raiz do repositório): python3 pipeline/build_page.py
"""
import json, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
rows = json.load(open(R/'data'/'base.json'))
keys = ['id','exame','ano','periodo','tema','regiao','idade','subtema','tipo','detalhe','livro','ref_origem','anulada']
data = 'const K='+json.dumps(keys,ensure_ascii=False)+';\nconst RAW='+json.dumps([[x[k] for k in keys] for x in rows],ensure_ascii=False,separators=(',',':'))+';\n'
inner = (R/'page'/'head.html').read_text()+(R/'page'/'style.html').read_text()
body = (R/'page'/'body.html').read_text().replace('/*DATA*/',data)
# artifact.html: formato do artifact do Claude (o host adiciona <!doctype>, <head> e <body>)
(R/'artifact.html').write_text(inner+'\n'+body)
# index.html: documento completo para o GitHub Pages
reset = '<style>html{color-scheme:light}body{margin:0;font-size:14px}img{max-width:100%}[hidden]{display:none!important}</style>'
page = ('<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<meta name="description" content="Mapeamento questão a questão das provas TARO e TEOT da SBOT (2014–2026).">\n'
        + reset + '\n' + inner + '\n</head>\n<body>\n' + body + '\n</body>\n</html>\n')
(R/'index.html').write_text(page)
print('index.html gerado:', len(page), 'bytes,', len(rows), 'questões')
