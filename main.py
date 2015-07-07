from elph import ELPHStream

s = ELPHStream(1, 2)
s.record('A')
s.record('B')
s.record('A')
s.record('C')
s.record('A')
s.record('B')
s.record('A')
s.record('D')

print(s.predict())

