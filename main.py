import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)

case = "b"


def moveSweet(state, start, end):
    state[0, start] -= 1
    state[0, end] += 1

    # If a player is out of sweets, we want to remove them from the game
    if state[0, start] == 0:
        return False
    return True


def caseA(numChildren, numSweets):

    # Set up initial state
    if isinstance(numSweets, np.ndarray):
        sweets = np.copy(numSweets)
    else:
        sweets = np.zeros([1, numChildren], dtype=np.int8)
        sweets.fill(numSweets)

    # "players" holds the players who are still in the game
    players = []
    players[:] = range(0, numChildren)

    rounds = 0
    results = np.zeros([1, numChildren])
    results[0, :] = sweets

    while len(players) != 1:
        rounds += 1
        for i in players:
            # Make a probability distribution for the opponents
            prob = [1 / (len(players) - 1)] * len(players)
            prob[players.index(i)] = 0

            # Choose an opponent at random
            j = np.random.choice(players, p=prob)

            # Choose a game outcome at random
            outcome = np.random.choice(["win", "lose", "draw"])

            if outcome == "win":
                if (not moveSweet(sweets, i, j)):
                    players.remove(i)
            elif outcome == "lose":
                if (not moveSweet(sweets, j, i)):
                    players.remove(j)
        #print(players, sweets)
        results = np.append(results, sweets, axis=0)

    winner = players[0]
    return rounds, results, winner


def caseB(numChildren, numSweets, numRounds, autoWin, verbose):
    # Set up initial state
    if isinstance(numSweets, np.ndarray):
        sweets = np.copy(numSweets)
    else:
        sweets = np.zeros([1, numChildren], dtype=np.int8)
        sweets.fill(numSweets)

    players = []
    players[:] = range(0, numChildren)

    results = np.zeros([1, numChildren])
    results[0, :] = sweets

    rounds = 0
    while rounds < numRounds:
        rounds += 1
        for i in players:
            # Make a probability distribution for the opponents
            prob = [1 / (len(players) - 1)] * len(players)
            prob[players.index(i)] = 0

            # Choose an opponent at random
            j = np.random.choice(players, p=prob)

            # If both players have no sweets, it's a draw (prevents any one from getting negative sweets)
            if sweets[0, i] == 0 and sweets[0, j] == 0:
                continue

            # If someone has no sweets, they automatically win
            if sweets[0, i] == 0 and autoWin:
                moveSweet(sweets, j, i)
                continue
            if sweets[0, j] == 0 and autoWin:
                moveSweet(sweets, i, j)
                continue

            # Choose a game outcome at random
            outcome = np.random.choice(["win", "lose", "draw"])

            if outcome == "win" and sweets[0, i] != 0:
                moveSweet(sweets, i, j)
            elif outcome == "lose" and sweets[0, j] != 0:
                moveSweet(sweets, j, i)

            if verbose:
                print(sweets)
            results = np.append(results, sweets, axis=0)

    return results


nameDict = {0: "A", 1: "B", 2: "C", 3: "D"}

### CASE A ANALYSIS/PLOTS ###
if case.lower() == "a":
    # Run the simulation once and plot results
    numChildren = 4
    numSweets = 10
    results = caseA(numChildren, numSweets)[1]
    for i in range(numChildren):
        plt.plot(results[:, i], label=f"Child {nameDict[i]}")
    plt.xlabel("Round")
    plt.ylabel("Number of sweets")
    plt.legend()
    plt.savefig("caseAPlots/fullGame.png", dpi=400)
    plt.close()
    '''
    # Run the simulation 1000 times and plot results
    rounds = []
    for i in range(10000):
        if i % 100 == 0:
            print(f"Game {i}")
        rounds.append(caseA(numChildren, numSweets)[0])

    print('Average number of rounds: ', np.mean(rounds))
    print('Minimum number of rounds: ', np.min(rounds))
    print('Maximum number of rounds: ', np.max(rounds))
    plt.hist(rounds, bins=40)
    plt.xlabel("Number of rounds")
    plt.ylabel("Number of games")
    plt.savefig("caseAPlots/hist.png", dpi=400)
    '''
    rounds = np.zeros([100, 13])
    for i in range(100):
        for j in range(2, 15):
            rounds[i, j - 2] = caseA(j, numSweets)[0]
    means = np.mean(rounds, axis=0)
    #stds = np.std(rounds,)
    plt.plot(range(2, 15), means)
    plt.boxplot(rounds, sym="", positions=range(2, 15))
    plt.xlabel("Number of children")
    plt.ylabel("Average number of rounds")
    plt.savefig("caseAPlots/means_numChildren.png", dpi=400)
    plt.close()
    rounds = np.zeros([100, 20])
    for i in range(100):
        for j in range(10, 30):
            rounds[i, j - 10] = caseA(numChildren, j)[0]
    means = np.mean(rounds, axis=0)
    #stds = np.std(rounds, axis=0)
    plt.plot(range(10, 30), means)
    plt.boxplot(rounds, sym="", positions=range(10, 30, 3))
    plt.xlabel("Initial number of sweets per child")
    plt.ylabel("Average number of rounds")
    plt.savefig("caseAPlots/means_numSweets.png", dpi=400)
    plt.close()
    '''
    games_won = []
    for i in range(10, 40, 3):
        sweets = np.array([[i, (40 - i) / 3, (40 - i) / 3, (40 - i) / 3]])
        print(sweets)
        count = 0
        for j in range(1000):
            winner = caseA(4, sweets)[2]
            if winner == 0:
                count += 1
        games_won.append(count/10)  #Percentage of games won by child 0
    '''
    plt.plot(range(10, 40, 3), games_won)
    plt.xlabel("Initial number of sweets for oldest child")
    plt.ylabel("Percentage of games won")
    plt.savefig("caseAPlots/child0_games_won.png", dpi=400)
### CASE B ANALYSIS/PLOTS ###
elif case.lower() == "b":
    numChildren = 4
    numSweets = 10
    numRounds = 1000

    results = caseB(numChildren, numSweets, numRounds, True, True)

    # Get some values
    oldNoSweets = results[results[:, 0] == 0].shape[0] / results.shape[0]
    oldAllSweets = results[results[:, 0] == numChildren * numSweets].shape[0] / results.shape[0]

    print(
        f"Proportion of time oldest child has no sweets: {oldNoSweets} ({results[results[:, 0] == 0].shape[0]} / {results.shape[0]})\nProportion of time oldest child has all the sweets: {oldAllSweets} ({results[results[:, 0] == numChildren * numSweets].shape[0]} / {results.shape[0]})"
    )

    # Make plots (Only used for a single run)
    for i in range(numChildren):
        plt.plot(results[:, i], label=f"Child {nameDict[i]}")
    plt.xlabel("Turn")
    plt.ylabel("Number of sweets")
    plt.legend()
    plt.savefig("caseBPlots/fullGameAutoWin.png", dpi=400)

    # Create polygon plot which better shows proportions
    cumulativeResults = np.zeros(results.shape)
    cumulativeResults[:] = results[:]
    cumulativeResults[:, 1] += cumulativeResults[:, 0]
    cumulativeResults[:, 2] += cumulativeResults[:, 1]
    cumulativeResults[:, 3] += cumulativeResults[:, 2]
    cumulativeResults = np.insert(cumulativeResults, 0,
                                  np.zeros(cumulativeResults.shape[0]), 1)

    fig, ax = plt.subplots()

    for i in range(4):
        ax.fill_between(range(cumulativeResults.shape[0]),
                        cumulativeResults[:, i],
                        cumulativeResults[:, i + 1],
                        label=f"Child {nameDict[i]}")
    plt.xlabel("Turn")
    plt.ylabel("Number of sweets")
    plt.legend()
    plt.savefig("caseBPlots/polygonAutoWin.png", dpi=400)
elif case.lower() == "bmany":
    # Run many simulations to get data
    numChildren = 4
    numSweets = 10
    autoWin = False
    
    minRound, maxRound, step = 100, 5000, 50
    
    numRuns = 10
    totalNumRoundLengths = len(range(minRound, maxRound, step))
    
    # Keep track of all the proportions for every run
    oldNoSweetsArr = np.zeros([numRuns, totalNumRoundLengths])
    oldAllSweetsArr = np.zeros([numRuns, totalNumRoundLengths])
    
    # Get proportion of time oldest player has all sweets, for many different game lengths
    for i, gameLength in enumerate(range(minRound, maxRound, step)):
        if gameLength % 100 == 0:
            print(gameLength)
    
        for j in range(numRuns):  # Run it a number of times per game length
            results = caseB(numChildren, numSweets, gameLength, autoWin, False)
    
            # Get some values
            oldNoSweets = results[results[:, 0] == 0].shape[0] / results.shape[0]
            oldAllSweets = results[results[:, 0] == numChildren * numSweets].shape[0] / results.shape[0]
    
            oldNoSweetsArr[j, i] = oldNoSweets
            oldAllSweetsArr[j, i] = oldAllSweets
    
    avgOldNoSweets = np.mean(oldNoSweetsArr, 0)
    avgOldAllSweets = np.mean(oldAllSweetsArr, 0)
    plt.figure(figsize = [6.4 * 2, 4.8])
    plt.subplot(1, 2, 1)
    plt.plot(range(minRound, maxRound, step),
             avgOldNoSweets,
             label="Proportion oldest has no sweets")
    plt.xlabel("Length of game")
    plt.ylabel("Proportion of time")
    plt.subplot(1, 2, 2)
    plt.plot(range(minRound, maxRound, step),
             avgOldAllSweets,
             label="Proportion oldest has all sweets")
    plt.xlabel("Length of game")
    plt.ylabel("Proportion of time")
    if autoWin:
        print(f"With auto win, oldest child has all sweets {np.mean(oldAllSweetsArr) * 100}% of the time, on average.")
        print(f"With auto win, oldest child has no sweets {np.mean(oldNoSweetsArr) * 100}% of the time, on average.")
        plt.savefig("caseBPlots/oldestPlayerProportionsAutoWin.png", dpi = 400)
    else:
        print(f"With no auto win, oldest child has all sweets {np.mean(oldAllSweetsArr) * 100}% of the time, on average.")
        print(f"With no auto win, oldest child has no sweets {np.mean(oldNoSweetsArr) * 100}% of the time, on average.")
        plt.savefig("caseBPlots/oldestPlayerProportionsNoAutoWin.png", dpi = 400)
    
elif case.lower() == "scaling":
    # Run the simulation for a long time
    numChildren = 4
    numSweets = 10
    numRounds = 1000
    results = scalingProbs(numChildren, numSweets, numRounds)

    # Get some values
    oldNoSweets = results[results[:, 0] == 0].shape[0] / results.shape[0]
    oldAllSweets = results[results[:, 0] == numChildren *
                           numSweets].shape[0] / results.shape[0]
    print(
        f"Proportion of time oldest child has no sweets: {oldNoSweets} ({results[results[:, 0] == 0].shape[0]} / {results.shape[0]})\nProportion of time oldest child has all the sweets: {oldAllSweets} ({results[results[:, 0] == numChildren * numSweets].shape[0]} / {results.shape[0]})"
    )

    # Make plots
    for i in range(numChildren):
        plt.plot(results[:, i], label=f"Child {nameDict[i]}")
    plt.xlabel("Turn")
    plt.ylabel("Number of sweets")
    plt.legend()
    plt.savefig("scalingPlots/fullGame.png", dpi=400)

    # Create polygon plot which better shows proportions
    cumulativeResults = np.zeros(results.shape)
    cumulativeResults[:] = results[:]
    cumulativeResults[:, 1] += cumulativeResults[:, 0]
    cumulativeResults[:, 2] += cumulativeResults[:, 1]
    cumulativeResults[:, 3] += cumulativeResults[:, 2]
    cumulativeResults = np.insert(cumulativeResults, 0,
                                  np.zeros(cumulativeResults.shape[0]), 1)

    fig, ax = plt.subplots()

    for i in range(4):
        ax.fill_between(range(cumulativeResults.shape[0]),
                        cumulativeResults[:, i],
                        cumulativeResults[:, i + 1],
                        label=f"Child {nameDict[i]}")
    plt.xlabel("Turn")
    plt.ylabel("Number of sweets")
    plt.legend()
    plt.savefig("scalingPlots/polygon.png", dpi=400)
