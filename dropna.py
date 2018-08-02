def render(table, params):
		import pandas as pd

		cols = params['colnames'].split(',')
		cols = [c.strip() for c in cols]
		if cols == [] or cols == ['']:
			return table

    # convert empty strings to none, because dropna says '' is not na
		for c in cols:
			if table[c].dtype.name == 'object' or table[c].dtype.name == 'category':  # object -> can have strings in it
				table[table[c] == ''] = None
			if table[c].dtype.name == 'category':
				table[c].cat.remove_unused_categories(inplace=True)

		newtab = table.dropna(subset=cols, how='all', axis='index')
		return newtab
