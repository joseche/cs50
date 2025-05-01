from nim import train, play

ai = train(10000)
print(len(ai.q))
play(ai)
