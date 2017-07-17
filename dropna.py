class Importable:
    @staticmethod
    def event():
        pass

    @staticmethod
    def render(wf_module, table):
        cols = wf_module.get_param_string('colnames').split(',')
        cols = [c.strip() for c in cols]

        if cols == [] or cols == ['']:
            return table

        for c in cols:
            if not c in table.columns:
                wf_module.set_error('There is no column named %s' % c)
                return None

        wf_module.set_ready(notify=False)
        newtab = table.dropna(subset=cols, how='all', axis='index')
        return newtab