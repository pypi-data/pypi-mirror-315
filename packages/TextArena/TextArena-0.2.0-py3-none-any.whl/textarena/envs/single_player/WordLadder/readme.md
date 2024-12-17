# Word Ladder Environment Documentation

## Overview

Word Ladder is a single-player puzzle game where the player aims to transform a starting word into a target word by changing one letter at a time. Each step must yield a valid word that differs by exactly one letter from the previous word, forming a chain from the start word to the target. The environment provides both a standard and a hardcore mode, impacting the word list difficulty. Players are guided by a prompt detailing the rules and gameplay, and their move history is displayed to track progress.

## Action Space
- **Format**: Actions are strings in the format [word], where:
- **Examples**:
    - To say that the next word after "sain" is "main": [main]
- **Notes**: Additional text may accompany the action, but it must contain the correct format for the action to be processed. Incorrectly formatted actions will be marked as invalid.

## Observation Space
**Reset Observation:**
On reset, the observation provides the initial prompt and the starting words and target words. For example:
```plaintext
[GAME] You are Player 0. You are playing Word Ladder (Hardcore).
The objective of the game is to convert the start word to the target word by changing one letter at a time.
The start word is: sain
The target word is: teal
To submit your word, you must wrap it in square brackets, e.g. [word].
As you play, the history of your choices will be appended below. Use the information to win the game.
```

** Step Observation: **
After each step, the environment returns the action and the updated Word Ladder text as the observation. For example:
```plaintext
[Player 0] To start, I'll change one letter in "sain" to get closer to "teal." 

I'll change the first letter 's' to 't' to form "tain."

My move: [tain]
[GAME] You've selected a valid word.
('Word Ladder History: sain -> tain. Target Word: teal\n',)
```

By default, the environment returns observations in the following format:
```python
{
  player_id: int : [
    (sender_id: int, message: str),
    (sender_id: int, message: str),
    ...
  ]
}
```

## Gameplay
**Word Length:** The length of the words is customizable, with a default setting of four-letter words. Both the starting and target words are of this length, with other words in the chain matching this requirement.

**Turns:** The player enters words by typing them in the format [word], where each word differs from the previous one by exactly one letter. Players continue to submit words in this format until they reach the target word or exhaust their turns. The game defaults to a maximum of 10 turns.

**Word Graph:** All words of the specified length are represented as nodes in a graph, with edges connecting words that differ by one letter. The start and target words are selected to ensure a valid path exists between them.

**Winning Condition: **The game is won when the player reaches the target word within the allowed number of turns, transforming the start word into the target word through a chain of valid single-letter changes.

## Key Rules
- **Valid Moves**:
    - The player must enter a word that:
        - Is exactly one letter different from the current word.
        - Exists within the game's word list and matches the length of the target word.

- **Invalid Moves**:
    - Entering a word that is not in the list of valid words.
    - Entering a word that does not match the target word length.

- **Incorrect Tries:**
    - Entering a word that differs by more than one letter from the current word.

## Rewards
| Outcome          | Reward for Player  |
|------------------|:------------------:|
| **Win**          |       `+1`         |
| **Lose**         |       `0`          |
| **Invalid Move** |       `-1`         |

## Parameters

- `hardcore` (`bool`):
    - **Description:** Determines the type of words to spot
    - **Impact:**
        - **False:** Hidden words follow basic english.
        - **True**: Hidden words would be uncommon and challenging words.

- `word_len` (`int`):
    - **Description:** Determines the length of the words used in the word graph.
    - **Impact:** Longer words are typically more challenging. 

## Variants

| Env-id                      | hardcore | word_len |
|-----------------------------|:--------:|:--------:|
| `WordLadder-v0-hardcore`    | `True`   | `5`      |
| `WordLadder-v0-hardcore-10` | `True`   | `10`     |

## Example Usage
```python
import textarena as ta

## initializa the environment
env = ta.make("WordLadder-v0-hardcore")

## Wrap the environment for easier observation handling
env = ta.wrappers.LLMObservationWrapper(env=env)

## Wrap the environment for pretty rendering
env = ta.wrappers.PrettyRenderWrapper(env=env)

## initalize agents
agents = {
    0: ta.basic_agents.OpenRouter(model_name="gpt-4o-mini")
    }

## reset the environment to start a new game
observations = env.reset(seed=490)

## Game loop
done = False
while not done:

    # Get the current player
    current_player_id = env.state.get("current_player")

    # Get the current observation for the player
    obs = observations[current_player_id]

    # Agent decides on an action based on the observation
    action = agents[current_player_id](obs)

    # Execute the action in the environment
    observations, rewards, truncated, terminated, info = env.step(current_player_id, action)

    # Check if the game has ended
    done = terminated or truncated

    # Optionally render the environment to see the current state
    env.render()

    if done:
        break

## Finally, print the game results
for player_id, agent in agents.items():
    print(f"{agent.agent_identifier}: {rewards[player_id]}")
print(f"Reason: {info['reason']}")
```

## Troubleshooting

**Incorrect Word Length**
- **Issue**: The player submits a word that does not match the required length.
- **Solution**: Ensure the chosen word matches the specified word length set for the environment (e.g., 4 letters by default).

**Invalid Move Format**
- **Issue**: The player’s word is not in the required [word] format.
- **Solution**: Prompt the player to submit their word inside square brackets, like [word], for correct processing.

**No Path Between Words**
- **Issue**: The generated start and target words do not have a valid path connecting them.
- **Solution**: Restart the game to regenerate words or preselect start and target pairs with known paths to reduce such occurrences.

**Isolated Nodes in Graph**
- **Issue**: Some words may be isolated (no one-letter connections) in the word graph, preventing path validation.
- **Solution**: Filter out isolated nodes during graph construction to ensure connectivity.


## Version History
- **v0**
  - Initial release 


### Contact
If you have questions or face issues with this specific environment, please reach out directly to bobby_cheng@i2r.a-star.edu.sg