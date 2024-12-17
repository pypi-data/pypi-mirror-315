from depedit import DepEdit

d = DepEdit()

conllu = open("GUM_academic_art.conllu").read()

d.run_depedit(conllu, parse_entities=True)

print(d.mentions)