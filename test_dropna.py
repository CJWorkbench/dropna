import unittest
import pandas as pd
import numpy as np
from dropna import render

class TestDropNA(unittest.TestCase):

	def setUp(self):
		# Test data includes:
		#  - rows of numeric and string types
		#  - zero entries (which should not be removed)
		#  - some partially and some completely empty rows
		self.table = pd.DataFrame([
			['fred',			2,			3.14,		'2018-1-12', '',1],
			['frederson',	5,			None,		'2018-1-12 08:15', 'a',None],
			['', 					-10, 		None, 	'', 'b',2],
			['',					-2,			10,			'','',None],
			['maggie',		8,			0,			'1984-7-11','c',3]],
			columns=['stringcol','intcol','floatcol','datecol','catcol','floatcatcol'])

		# Pandas should infer these types anyway, but leave nothing to chance
		self.table['stringcol'] = self.table['stringcol'].astype(str)
		self.table['intcol'] = self.table['intcol'].astype(np.int64)
		self.table['floatcol'] = self.table['floatcol'].astype(np.float64)
		self.table['datecol'] = self.table['datecol'].astype(str)
		self.table['catcol'] = self.table['catcol'].astype('category')
		self.table['floatcatcol'] = self.table['floatcatcol'].astype('category')

	def test_NOP(self):
		params = { 'colnames': ''}
		out = render(self.table, params)
		self.assertTrue(out.equals(self.table)) # should NOP when first applied

	def test_numeric(self):
		params = { 'colnames': 'intcol'}
		out = render(self.table, params)
		ref = self.table[[True, True, True, True, True]]  # also tests no missing
		self.assertTrue(out.equals(ref))

		params = { 'colnames': 'floatcol'}
		out = render(self.table, params)
		ref = self.table[[True, False, False, True, True]]
		self.assertTrue(out.equals(ref))

	def test_string(self):
		params = { 'colnames': 'stringcol'}
		out = render(self.table, params)
		ref = self.table[[True, True, False, False, True]]
		self.assertTrue(out.equals(ref))

	def test_cat(self):
		params = { 'colnames': 'catcol'}
		out = render(self.table, params)
		ref = self.table[[False, True, True, False, True]]
		cat_ref = set(['a', 'b', 'c'])
		self.assertTrue(out.equals(ref))
		self.assertTrue(set(out['catcol'].cat.categories) == cat_ref)

	def test_cat_num(self):
		params = {'colnames': 'floatcatcol'}
		out = render(self.table, params)
		ref = self.table[[True, False, True, False, True]]
		cat_ref = set([1.0, 2.0, 3.0])
		self.assertTrue(out.equals(ref))
		self.assertTrue(set(out['floatcatcol'].cat.categories) == cat_ref)

	def test_multiple_colnames(self):
		params = { 'colnames': 'intcol,floatcol'}
		out = render(self.table, params)
		self.assertTrue(out.equals(self.table))  # no drop b/c int has no empty vals

if __name__ == '__main__':
    unittest.main()


