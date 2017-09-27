a = [(2, "qw"), (5, "aqe"), (1, "cv"), (3, "yui")]
b = [i[0] for i in a]
print [a[b.index(i)][1] for i in sorted(b)]
