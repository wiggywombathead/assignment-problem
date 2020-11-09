from collections import Counter
from fractions import Fraction
from itertools import permutations, product

def object_available(remaining):
    return any(remaining.values())

def print_assignment(assignment):
    if assignment is None:
        print("Error: invalid assingment")
        return

    for i in assignment.keys():
        for a in assignment[i].keys():
            print(assignment[i][a], end='\t')
        print()

def PS(preferences):

    players = [i for i in range(len(preferences))]
    objects = [a for a in preferences[0]]
    n = len(players)
    m = len(objects)

    if n != m:
        print("Error: input must be a square matrix")
        return

    # track how much remains of object a
    remaining = {a: 1 for a in objects}

    # track what object agent i is currently consuming
    consuming = {i: preferences[i][0] for i in players}

    # track the proportion of object a player i receives
    consumed = {i: {a: 0 for a in objects} for i in players}

    while True:
        # get the most consumed object
        c = Counter(consuming.values()).most_common()

        # the object being the most consumed
        most_consumed = c[0][0]

        # the number of agents consuming this object
        agents_consuming = c[0][1]

        # give each player delta more of their currently consumed object
        delta = Fraction(remaining[most_consumed], agents_consuming)

        for i in players:
            consumed[i][consuming[i]] += delta
            remaining[consuming[i]] -= delta

        # player i starts consuming their next most preferred
        # available object, if necessary
        for i in players:
            if remaining[consuming[i]] == 0:
                idx = 0
                while remaining[preferences[i][idx]] == 0:
                    idx += 1

                    # there are no objects left
                    if idx > n-1:
                        return consumed

                consuming[i] = preferences[i][idx]

def sd(P, Q, player, preferences):
    """ return TRUE if allocation P stochastically dominates allocation Q
    according to PREFERENCES for PLAYER """
    
    p = P[player]
    q = Q[player]

    for t in range(len(preferences)):
        t += 1
        best_items = preferences[:t]

        p_sum = sum([p[i] for i in best_items])
        q_sum = sum([q[i] for i in best_items])

        if q_sum > p_sum:
            return False

    return True

def prefers(P, Q, player, preferences):
    """ suppose P allocates PLAYER the objects, in order of most to least
    preferred), with probabilities (x,y,z,...) while Q allocates
    (x',y',z',...). Then PLAYER prefers P to Q if: (x > x') OR (x = x' AND y >
    y') OR ... according to the preference ordering for PLAYER (the list of
    length n PREFERENCES) """

    p = P[player]
    q = Q[player]

    for t in range(len(preferences)):
        t += 1
        best_items = preferences[:t]

        p_sum = sum([p[i] for i in best_items])
        q_sum = sum([q[i] for i in best_items])

        if p_sum > q_sum:
            return True
        elif q_sum > p_sum:
            return False

    # NOTE: if the allocations are equal, return False
    return False

def best(preferences, player, true):
    """ find an allocation that is the best case outcome from submitting the
    strategy in PREFERENCES[PLAYER], compared by the preference ordering TRUE
    of PLAYER (which may be different from the preference order they submit)
    """

    pi = preferences[player]
    p_i = preferences[:player] + preferences[player+1:]

    best = None

    # compute a permutation on each player's preferences other than PLAYER and
    # calculate the allocation

    # TODO: generalise to n-1 players
    combos = list(product(permutations(p_i[0]), permutations(p_i[1])))

    # for each profile p of player i
    for profile_i in combos:
        profile = list(profile_i[:player] + profile_i[player+1:])
        profile.insert(player, tuple(pi))
        outcome = PS(profile)

        if best is None:
            best = outcome
        elif prefers(outcome, best, player, true):
            best = outcome
    
    return best

def main():

    preferences = [
        [0,1,2],
        [0,2,1],
        [1,0,2]]

    # true preferences for player 3
    tp_3 = preferences[2]

    p = PS(preferences)
    q = PS(preferences[:2] + [list([0,1,2])])

    #print(sd(p, q, 2, preferences[2]))
    #print(prefers(p, q, 2, preferences[2]))

    truthful = PS(preferences)
    print_assignment(truthful)
    print()

    # test if player 3 has an incentive to deviate according to prefers(.)
    #for perm in permutations(preferences[2]):
    #    profile = preferences[:2] + [list(perm)]
    #    deviation = PS(profile)
    #    print("Preferences:", profile)
    #    print_assignment(deviation)
    #    print("Player 3 prefers {} to {}\n".format(
    #        "truthful" if prefers(truthful, deviation, 2, preferences[2]) else "deviation",
    #        "deviation" if prefers(truthful, deviation, 2, preferences[2]) else "truthful"))

    truthful_best = best(preferences, 2, tp_3)
    
    print_assignment(truthful_best)

if __name__=="__main__":
    main()
