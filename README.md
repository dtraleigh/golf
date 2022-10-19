# Golf - The Card Game
My intro to PyGame by building the card game Golf. This is only a two-player version.

The objective of the game is to have the lowest score. There are many variations of the game but we typically play with the first player reaching a score of 50 is the loser. You can also player 9 rounds, or more/less, and see who has the lower score after that.

This game is built to play one round, present each players score for that round, and then start over. Please keep your running score on your own. (future enhancement)

## How to Play
### Preparation to play

1. Golf with 2 players uses a 52-card deck + the two jokers for a total of 54 cards.
2. Each player's cards are placed in a 2-column, 3-row grid face down.
3. The remaining cards are face down in a pile.
4. Draw one card face up next to the pile.

Before the game starts, each player can turn two cards face up in their hand. Once this is done, the game can start.

### Game Play
With two players, players take turns making moves to lower the score of their hand. The round is over when a player has all their cards face up forcing the other player to make their last turn.

On their turn, a player can do one of the following moves:
1. Flip a face down card in their hand. (cannot do this if they have drawn from the pile already).
2. Exchange any hand card (face up or down) for something from the face up pile.
3. Draw a card from the pile and add it to the face up pile. Then can consider an exchange mentioned in scenario #2.
4. The player can pass at any time and do nothing.

Once the first player has all their cards in their hand face up, this forces the last round. On the last round, the other player will take their turn as normal but at the end, the game will flip over any face down cards remaining. The total score will then be shown.

How to navigate on your turn
- To flip a card, click on it twice.
- To exchange a card, select a hand card and the draw card. Press the Exchange button to perform the swap.
- To pass, you must at least draw a card from the pile. Press the Pass button.

### Scoring
Points for each card are as follows:
- Ace = 1
- 2 through 10 = card value
- Jack, Queen = 10
- King = 0
- Joker = -2

#### Row match scenario
To really lower your score, if the two cards in a row are the same value, they cancel each other out. For example, if a row has a 7 of Clubs and 7 of Hearts, the resulting score is a 0. (not 14)

I'll add some example images with a brief explanation of the score.

<img width="352" alt="image" src="https://user-images.githubusercontent.com/1951867/196714478-57e0645a-cfb3-463a-9247-2798097a592f.png">
Scenario #1
This player scores an 11. The 5s cancel each other out. Same with the Aces. Queen 10 + Ace 1 = 11.

<img width="311" alt="image" src="https://user-images.githubusercontent.com/1951867/196715697-690e7f85-abfb-4813-947c-c94e6fb407bc.png">
Scenario #2
This player scores an 18. Nothing cancels out here but the kings are zero so seven + three + ten = 20 and the joke is -2. Score is 18.

<img width="326" alt="image" src="https://user-images.githubusercontent.com/1951867/196716032-1475ccc7-4303-4144-969e-b4a0ef1bf450.png">
Scenario #3
This player has 16. Queens cancel. Four + Eight + Ace 1 + Three = 16
