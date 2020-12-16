
Intercept('malloc', ['set *__errno_location()=12', 'return (void*)0'])

Intercept('open', [['set *__errno_location()=13', 'return (int)-1'], #EACCESS
                   ['set *__errno_location()=2', 'return (int)-1'],  #ENOENT
                   ])
