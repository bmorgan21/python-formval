from formval21 import FormVal, types as tt

f = FormVal()
f.add_field('b', tt.Unicode(min_length=2, max_length=10))
f.add_field('c', tt.Integer(optional=True, default=tt.UNDEF))
result = f.process_strings({'b': 'brian', 'c': '10'})

print 'Success', result.success()
print '  Values', result.values
print '  Errors', result.errors

f2 = FormVal()
f2.add_field('d', tt.Unicode(min_length=2, max_length=10))
f2.add_field('e', tt.Integer(optional=True, default=tt.UNDEF))
result = f2.process_strings({'d': 'brian'})

print 'Success', result.success()
print '  Values', result.values
print '  Errors', result.errors
