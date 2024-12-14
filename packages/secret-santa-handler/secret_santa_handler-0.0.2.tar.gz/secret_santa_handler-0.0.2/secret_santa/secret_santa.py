import random


def shuffle(names):
    # Shuffle the list to randomize the order
    random.shuffle(names)

    # Create the Santa list with wrapped-around pairs
    santaList = [(names[i], names[i + 1]) for i in range(len(names) - 1)]
    santaList.append((names[-1], names[0]))  # Wrap the last person to the first

    return santaList

