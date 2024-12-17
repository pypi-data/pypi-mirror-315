# Debate Environment

## Overview
**Debate** is a two-player game where each player is assigned a side on a given topic—either Affirmative or Negative. Players present arguments in turns to convince a panel of simulated judges. The winner is determined by the change in judges' opinions before and after the debate.

## Action Space
- **Format:** Actions are strings representing the player's arguments.
- **Example:** `"I believe that technology improves our lives because..."`, `"My opponent overlooks the fact that..."`

## Observation Space

### Observations
Each player receives messages exchanged during the debate, including their assigned topic and position.

**Reset Observation:**

On reset, each player receives a prompt containing the debate topic, their position, and game instructions. For example:
```plaintext
You are Player {player_id} in the Debate game.
Topic: {topic}
Your position: {'Affirmative'|'Negative'}
You will have {max_turns} turns to present your arguments.
On your turn, simply type your argument.
```

**Step Observation:**
After each step, players receive the latest argument. For example:
```plaintext
[Player 0]: While the idea of free education for all citizens sounds appealing, it is important to consider the economic implications and potential drawbacks. Implementing a system of free education would require substantial funding, which would likely result in increased taxes or budget cuts in other critical areas such as healthcare, infrastructure, or social services. This could place a strain on the economy and potentially lead to negative consequences for citizens in other aspects of their lives. Additionally, without the financial investment from students and their families, educational institutions may face challenges in maintaining the quality of education, as they may struggle to attract and retain qualified teachers, update their facilities, and provide necessary resources. Therefore, it is crucial to weigh the economic costs and potential impacts on educational quality before embracing free education for all.
```

## Gameplay
- **Players**: 2
- **Turns**: Players alternate presenting arguments.
- **Topic Assignment**: A debate topic is randomly selected at the start.
- **Position Assignment**: One player is randomly assigned the Affirmative side; the other is assigned the Negative side.
- **Objective**: Convince the judges to change their opinions in favor of your side.
- **Judges**: A panel of simulated judges evaluates the debate.
- **Turn Limit**: The number of back and forths before the judges make their decision.

## Key Rules
1. Debate Structure:
    - Each player has a set number of turns to present their arguments.
    - Players alternate turns.
2. Judge Evaluation:
    - **Pre-Debate Vote:** Judges vote based solely on the topic before the debate begins.
    - **Post-Debate Vote:** Judges vote again after the debate concludes; this time based on the topic and debate transcript.
    - **Winner Determination:** The player whose side gains the most votes compared to the pre-debate vote wins. If the votes remain unchanged, the game ends in a draw.
3. Winning Conditions:
    - **Win:** Achieve a higher increase in judge votes for your side compared to the opponent.
    - **Draw:** If both sides gain an equal number of votes, the game ends in a draw.
4. Game Termination:
    - The game ends after all turns are completed and the judges have re-evaluated their votes.

## Rewards
| Outcome          | Reward for Player | Reward for Opponent |
|------------------|:-----------------:|:-------------------:|
| **Win**          | `+1`              | `-1`                |
| **Lose**         | `-1`              | `+1`                |
| **Draw**         | `0`               | `0`                 |

## Parameters
- `max_turns` (`int`):
    - **Description**: Number of turns per player
    - **Impact**: Determines the length of the debate

- `num_judges` (`int`):
    - **Description**: Number of simulated judges evaluating the debate.
    - **Impact**: Affects the granularity of judge opinion changes.

- `judge_class` (`ta.JudgeVote`)
    - **Description**: The type of judges used. By default, the `ta.game_makers.GPTJudgeVote` object is used, which utilized a random mix of different openai models.
    - **Impact:** This will significantly impact what types of arguments work well when trying to convince the judges.

- `topics_path` (`str`)
    - **Description:** Path to the JSON file containing debate topics.
    - **Impact:** Allows customization of the topics used in the debates.

## Variants

| Env-id                   | max_turns | num_judges | judge_class    |
|--------------------------|:---------:|:----------:|:--------------:|
| `Debate-v0`              | `6`       | `7`        | `GPTJudgeVote` |
| `Debate-v0-long`         | `12`      | `11`       | `GPTJudgeVote` |
| `Debate-v0-super-long`   | `30`      | `15`       | `GPTJudgeVote` |


## Example Usage

```python
import textarena as ta

# Initialize the environment
env = ta.make(env_id="Debate-v0")

# Wrap the environment for easier observation handling
env = ta.wrappers.LLMObservationWrapper(env=env)

# initalize agents
agents = {
    0: ta.basic_agents.OpenRouter(model_name="gpt-4o"),
    1: ta.basic_agents.OpenRouter(model_name="gpt-4o-mini")
    }

# reset the environment to start a new game
observations = env.reset(seed=490)

# Game loop
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

# Finally, print the game results
for player_id, agent in agents.items():
    print(f"{agent.agent_identifier}: {rewards[player_id]}")
print(f"Reason: {info['reason']}")
```

## Troubleshooting
- **Uneven Arguments:**
    - **Issue:** One player provides significantly shorter or less substantive arguments.
    - **Solution:** Encourage players to provide well-thought-out arguments within their turn limits.

- **Tie in Judge Votes:**
    - **Issue:** Both players achieve the same gain in judge votes, resulting in a draw.
    - **Solution:** Adjust the num_judges parameter to reduce the likelihood of ties.

- **Missing Topics File:**
    - **Issue:** The topics JSON file is not found at the specified path.
    - **Solution:** Verify the topics_path and ensure the file exists and is properly formatted.

- **Unbalanced Pre-Debate Vote:**
    - **Issue:** All judges vote for one side in the pre-debate vote.
    - **Solution:** We tried filtering out all too polarizing topics. If this still happens, please reach out to Guertlerlo@cfar.a-star.edu.sg, or submit a pull request that removes or adjusts the affected topic.


## Version History
- **v0**
  - Initial release 



### Contact
If you have questions or face issues with this specific environment, please reach out directly to Guertlerlo@cfar.a-star.edu.sg
