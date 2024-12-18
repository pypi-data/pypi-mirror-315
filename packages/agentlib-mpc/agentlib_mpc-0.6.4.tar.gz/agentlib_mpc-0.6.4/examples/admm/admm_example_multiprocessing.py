"""
Example for running a multi-agent-system performing a distributed MPC with
ADMM. Creates three agents, one for the AHU, one for a supplied room and one
for simulating the system.

Each agent is started in its own process and communicates through multiprocessing. Since
scheduling of the algorithm is dependent on real time, only RealTime
simulations are possible, making this quite slow. It can however be used as a
demonstration for the agentlibs communication potential.

With this file belong the models
    - ca_cooler_model.py
    - ca_room_model.py
    - simulation_model.py

And the config files
    - cooled_room.json
    - cooler.json
    - simulator.json
    - multiprocessing_broadcast.json
"""

import logging
import os

import json

from agentlib.utils import MultiProcessingBroker
from agentlib.utils.multi_agent_system import MultiProcessingMAS

agent_configs = [
    "configs//cooler.json",
    "configs//cooled_room.json",
    "configs//simulator.json",
]

env_config = {"rt": True, "strict": False, "factor": 0.05, "t_sample": 60}


def plot(results, start_pred: float):
    import matplotlib.pyplot as plt
    from agentlib_mpc.utils.analysis import admm_at_time_step

    res_sim = results["Simulation"]["simulator"]
    start_time = res_sim.index[0]
    res_sim.index = res_sim.index - start_time
    mpc_room_results = results["CooledRoom"]["admm_module"]

    room_res = admm_at_time_step(
        data=mpc_room_results,
        time_step=start_pred,
        iteration=-1,
        index_offset=start_time,
    )

    fig, ax = plt.subplots(2, 1)
    ax[0].axhline(294.55, label="reference value")
    ax[0].plot(res_sim["T_0_out"], label="temperature")
    ax[0].plot(room_res["variable"]["T_0"], label="temperature prediction")
    ax[1].plot(res_sim["mDot_0"], label="air mass flow")
    ax[1].plot(room_res["variable"]["mDot_0"].dropna(), label="air flow prediction")
    ax[1].legend()
    ax[0].legend()
    plt.show()


def run_example(
    with_plots=True,
    until=2000,
    log_level: int = logging.INFO,
    cleanup=True,
    start_pred=0,
    TESTING: bool = False,
):
    # Set the log-level
    logging.basicConfig(level=log_level)

    # Change the working directly so that relative paths work
    os.chdir(os.path.dirname(__file__))

    conf_dicts = []
    for conf in agent_configs:
        with open(conf) as f:
            conf_dict = json.load(f)
        modules = conf_dict["modules"]
        for i, mod in enumerate(modules):
            if isinstance(mod, str):
                with open(mod) as f:
                    mod = json.load(f)
            if mod["type"] == "mqtt" or mod["type"] == "local_broadcast":
                conf_dict["modules"][i] = (
                    "configs//communicators//multiprocessing_broadcast.json"
                )

        conf_dicts.append(conf_dict)

    broker = MultiProcessingBroker(config={"port": 32300})
    mas = MultiProcessingMAS(
        agent_configs=conf_dicts,
        env=env_config,
        variable_logging=True,
        cleanup=cleanup,
        log_level=log_level,
    )
    mas.run(until=until)
    results = mas.get_results()

    if with_plots:
        plot(results, start_pred)

    if TESTING:
        # assertion temperature is lowered for unittest
        cooledRoom_T = results["CooledRoom"]["AgentLogger"]["T_0"]
        cooler_m = results["CooledRoom"]["AgentLogger"]["mDot"]
        print(f"Room temp: {cooledRoom_T.iloc[-1]}")
        print(f"Mass flow: {cooler_m.iloc[-1]}")
        assert cooledRoom_T.iloc[0] > cooledRoom_T.iloc[-1]

        return results


if __name__ == "__main__":
    run_example(
        with_plots=True,
        until=500,
        log_level=logging.DEBUG,
        cleanup=True,
    )
