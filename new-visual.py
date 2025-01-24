c = 3 sometimes it can be 4 v_dict = pulp.LpVariable.dicts( nm, ((j,c,t) for j, c, t in _combination), lowbound = lb cat = ct )

This entire above code is inside a function which takes nm, lb and ct as input The problem to solve is

1) ((j,c,t) for j, c, t in _combination), it can be ((v,j,c,t) for v,j,c,t in _combination) it depends on the c value if 3 or 4
2) lowbound = lb ==> lb is passed sometimes and is not passed to function at all when passed itself we need to have this tag lowbound = lb
3) nm is a string input, lb is a integer value ,ct is a string value
Can you get me a optimized fn
