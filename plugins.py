""" A set of plugins that may be useful for processing csv data
"""

def cleaner(items):
    for struct in items.values():
        for k,v in struct.items():
            if k == '':
                del struct[k]

def build_relations(*args):
    """ A partial for relating sibling items based on columns denoted by `*args`

        usage. ``build_relations('col1', 'col2')``
    """
    def build(items):
        # initialise the catalog
        catalog = {}
        for arg in args:
            catalog[arg] = {}
        
        # build the catalog
        for uid,struct in items.items():
            for arg in args:
                val = struct.get(arg)
                if val:
                    catalog[arg].setdefault(val, []).append(uid)
            
        for uid,struct in items.items():
            # query the rest of the items to see if they match one or more of
            # the columns
            children = struct.setdefault('children', [])
            for arg in args:
                index = catalog[arg]
                key = struct.get(arg)
                if key:
                    children += index.get(key)

            # append a unique list of children to the parent item
            struct['children'] = list(set(children))

    return build

def expand_child_data(items):
    """ For each `item`, expands the `uids` in `item['children']` into a
        dictionary with more data
    """
    def format_child(struct):
        child = {}
        child['uid'] = struct['uid']
        child['title'] = struct['title']
        return child

    for struct in items.values():
        struct['children'] = [format_child(items[uid]) for uid in struct.get('children', [])]
