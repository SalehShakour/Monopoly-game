# Monopoly Game

This project is a Monopoly game implementation for an Artificial Intelligence lesson. The game runs automatically with two players playing against each other. The implemented algorithm is Expectiminimax, and the game includes a utility function that evaluates the current state of the board.

## Algorithm

The algorithm used in this project is Expectiminimax, which is an extension of the Minimax algorithm that can handle uncertain events in the game. In Monopoly, the uncertainty comes from the chance and community chest cards, as well as the dice rolls. The Expectiminimax algorithm considers all possible events and their probabilities, and it chooses the best action that maximizes the expected utility.

## Strategies

The implemented strategies in this game are as follows:

- At the beginning of the game, each player buys a property until their cash is in the danger zone. By doing this, the player can take rent from their opponent for each property and bring them one step closer to failure.
- When the player's cash enters the danger zone, they must try to save their property by selling it. The risk range is the range in which the player may go bankrupt with the next move and lose the game. Determining this range depends on the level of risk tolerance of the players.
- The cost of renting properties in the game is designed from 50 to 340 dollars, and the average cost of renting each property is 195 dollars. If we define the risk range below $340, the game becomes very cautious. In a reasonable case, this range is considered to be less than 200 dollars so that both players have risk tolerance and don't go too far.
- When the player gets out of the danger zone and knows that they will not enter this zone by making a move, they start to land their assets so that they can get rent from their opponent.
- In this strategy, cash is given a different value. At the beginning of the game, when most of the houses are ownerless and the player has a lot of money, they prefer to add to their properties. But at the end of the game, when they feel threatened, they try to keep themselves in the game by selling the property.

Note that by increasing the level of intelligence, the agents can make better decisions, but it takes time.

## Usage

To run the game, simply run the `main.py` file.

That's all you need to know to start playing Monopoly with an AI twist. Have fun!


## Credits

This project is created by Saleh Shakour.
