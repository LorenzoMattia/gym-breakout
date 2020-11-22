from gym.envs.registration import register

register(
    id='breakout-v0',
    entry_point='gym_breakout.envs:BreakoutEnv',
)
register(
    id='breakout-extrahard-v0',
    entry_point='gym_foo.envs:BreakoutExtraHardEnv',
)