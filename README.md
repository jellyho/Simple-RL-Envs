# Python_RL_Envs

## 1. 그리드월드

그리드월드는 강화학습 알고리즘을 적용해보기에 아주 좋은 기초적인 환경입니다. GUI를 사용하지 않고 편리하게 진행과정을 프롬프트에서 바로 확인할 수 있도록 한 간단한 환경입니다.

#### 1. 환경 선언
****
그리드월드를 사용하기 위해서는 먼저 선언을 해주어야 합니다.

```python
GridWorld(width, height, state_mode="relative", relative_state_width=2, start=[0, 0], goal=None, 
start_method="left_top", goal_method="right_bottom", goal_included_in_state=True, 
dir_included_in_state=True)
```

선언에는 굉장히 많은 옵션이 있습니다.

 - width, height : 그리드월드의 가로 크기, 세로 크기를 정합니다.
 - state_mode : 반환하는 상태의 형태를 정합니다. "relative"는 현재 위치를 기준으로 주변 격자가 상태로 반환됩니다. "absolute"는 각 장애물의 상대 좌표값이 직접 상태로 반환됩니다.
 - relative_state_width : state_mode를 "relative"로 사용했을 경우 반환하는 격자의 크기를 말합니다. 현재 위치를 기준으로 (relative_state_width * 2+1) X  (relative_state_width * 2+1) 크기의 격자를 반환하게 됩니다.
 - start: 처음으로 시작할 위치입니다. 기본적으로 길이가 2인 배열을 받습니다.
 - goal: 도착해야할 목적지의 위치입니다.
 - start_method: 매 에피소드마다 시작할 위치를 정하는 방법입니다. "left_top" 일때는 항상 좌상단에서 시작하며,  "random"일 경우 무작위로 시작합니다.
 - goal_method: 매 에피소드마다 목적지의 위치를 정하는 방법입니다. "right_bottom"일 때는 항상 우하단이 목적지이며, "random"일 경우 무작위로 정해집니다.
 - goal_included_in_state: 반환하는 상태값에 목적지에 대한 정보가 포함되는지 여부에 대한 설정값입니다.
 - dir_included_in_state: 장애물의 방향 정보가 상태값에 포함되는지 여부에 대한 설정입니다. 장애물을 계속 정지시킬경우 이 옵션을 사용하는 것이 좋습니다.

```python
env = GridWorld(7, 7, [4, 5])
```

#### 2. 장애물 생성
****

```python
// 1, 1에 위치, 정지, (정지, 상, 하, 좌, 우) 중에서 랜덤으로 움직임
env.add_obstacles(1, 1, 0, "random")

//2, 2에 위치, 상, "reflect"(벽에 닿을 경우 튕김)
env.add_obstacles(2, 2, 1, "reflect") 

env.add_obstacles(2, 4, 0, "reflect", include_state=False)
```

.add_obstacles()를 통해 장애물을 생성할 수 있습니다. 장애물의 x, y좌표를 넣어주며 이동 방향을 숫자로 넣어줄 수 있습니다. 0, 1, 2, 3, 4 순서대로 정지, 상, 하, 좌, 우입니다. 그다음 4번째 매개변수로 이동 모드를 정해줄 수 있는데요, "random" 을 넣어주어 무작위로 움직이거나, 혹은 "reflect"옵션을 통해 벽에 부딪혔을 경우 튕기도록 하는 옵션이 있습니다.

마지막 5번째 매개변수로는 include_state 옵션이 있습니다. 기본값은 True이며 True일 경우 에이전트에게 해당 장애물의 상대적 위치와 이동 방향을 알려줍니다.


#### 3. 상태, 행동의 크기 받아오기
****

에이전트를 만드려면 상태의 크기와 행동의 크기를 알아야 합니다. .action_size와 .state_size를 통해서 그 크기를 알 수 있습니다.

```python
state_size = env.state_size
action_size = env.action_size
```

상태의 크기는 상태에 포함 옵션이 적용된 장애물의 개수에 따라 달라지게 되며 행동의 크기는 5입니다. (정지, 상, 하, 좌, 우)

#### 4. 보상 정보 설정
****

에이전트가 장애물에 닿거나, 목표에 도달하거나, 벽을 향하는 행동을 하거나, 혹은 스텝마다 패널티를 주고싶을 때 각각의 보상 정보를 설정해 줄 수 있습니다.

```python
env.obstacle_reward = -1 //장애물에 닿을시
env.goal_reward = 1 // 목표에 도달할 시
env.alive_reward = -0.1 // 스텝마다 패널티
env.unavailable_reward = -1 // 행동할 수 없는 행동을 할 시(왼쪽 벽에 닿아있는 상태에서 왼쪽으로 이동 등)
```

#### 5. 환경 초기화
****

학습을 시작하기 전 환경을 초기화 해주어야 합니다. 초기화 할 시 에이전트는 start 위치로 이동하며 장애물도 초기 설정 위치로 이동합니다.

현재 상태를 반환 합니다. 상태는 "absolute"일 경우 아래의 순서로 구성됩니다.

[에이전트X, 에이전트Y, 목표의 상대위치X, 목표의 상대위치Y, 장애물1 상대위치X, 장애물1 상대위치Y, 장애물1 방향, ....]

"relative"일 경우 격자 정보로 구성되며 마지막에 goal과의 상대 좌표가 포함됩니다.("goal_included_in_state"=True 일 경우)

이때 갈 수 없는 벽은 9로, 도착지는 8로, "dir_included_in_state"=False일때 장애물은 7로 표현되며 True일 경우 0~4의 방향값으로 표현됩니다.

```python
state = env.reset()
```

#### 6. 행동하기
****

.step(action, show)를 통해서 행동을 할 수 있습니다. 행동은 [0, 1, 2, 3, 4]중에 하나를 넣어 주어야 하며 show를 True로 설정할 경우 그리드월드가 프롬프트에 출력됩니다.

반환값으로 다음 상태와 보상, 그리고 목표에 도달 여부를 알려줍니다.

```python
next_state, reward, done = env.step(1, True)
```

```
state:[0, 0, 2, 2, 1, 1, 0], reward:-1.1, action:^
--------
|A # # |
|# O # |
|# # G |
--------
```

A가 에이전트이고 O는 장애물(움직일경우 방향(^v<>)이 표시됨) 이고 G가 목표입니다.

이때 화면을 출력할경우 각 화면의 딜레이는 env.DELAY로 지정해주면 됩니다. 기본값은 1(1초)입니다.





## 2. TIC TAC TOE 틱택토
1) 초기화, state = reset()

```python
env = TICTACTOE()

state = env.reset()
```

환경 객체를 생성하고 reset()함수를 통해 게임을 초기상태로 만들고 그때의 상태를 반환합니다.

2) 행동하기, next_state, reward, active, done = step(1, 2, show=False)

```python
next_state, reward, active, done = env.step(1, 2) # 1번 팀으로 2번 위치에 놓음
```

step()으로 행동을 한 스텝 할 수 있는데요, 틱택토에서 행동은 바로 돌을 놓는 것입니다. 여기서 중요한 점은 두개의 팀이 있다는 것인데요, step()함수의 첫번째 매개변수로 팀(1, 2)를 넣어줍니다. 그 다음으로 0~8까지 위치를 입력합니다.

반환값으로는 다음상태값, 보상, 그리고 유효값, 게임 완료여부를 반환합니다. 다음상태값은 돌을 놓고 난 후의 상태값이며, 해당 돌을 놓으므로써 얻는 보상, 유효값은 해당 행동이 유효했는지(이때 유효함이라 함은 실제로 돌을 놓는 행동을 했는지에 대한 여부입니다. 이미 돌이 놓여있는 곳에 놓음으로써 패널티를 받고 실제로 놓지 않았을 때는 해당 안됨), 그리고 게임 완료여부(1줄이 완성되었거나 9칸이 모두 꽉 찼을 때 게임이 완료됨)를 반환합니다.

위의 반환값 정보들로 학습에 활용할 수 있습니다.

추가적으로 step()의 세번째 인수로 프롬프트에 출력할 여부를 정할 수 있습니다.
