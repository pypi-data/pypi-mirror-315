from python_dependency_resolver import DependencyResolver

tree = {
    'Buying food': ['Learning a new recipe'],
    'Cooking': ['Buying food', 'Learning a new recipe'],
    'Feeding kitties': [],
    'Feeding my self': ['Cooking'],
    'Doing the dishes': ['Feeding my self', 'Feeding kitties'],
    'Learning a new recipe': ['Buying a cookbook'],
    'Buying a cookbook': []
}

dependency_resolver = DependencyResolver()
result, unsolved = dependency_resolver.resolve(tree)

print('My sorted list depending on the requirements :')
for idx in range(0, len(result)):
    r = result[idx]
    print('  %s - %s' % (idx+1, r))
