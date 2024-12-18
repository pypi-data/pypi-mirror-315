import logging
from pathlib import Path
import matplotlib.pyplot as plt
import os

from agentlib.utils.multi_agent_system import LocalMASAgency
from agentlib_mpc.utils.plotting.mpc import plot_mpc

logger = logging.getLogger(__name__)

# script variables
ub = 295.15

ENV_CONFIG = {"rt": False, "factor": 0.01, "t_sample": 60}


def agent_configs(ml_model_path: str) -> list[dict]:
    agent_mpc = {
        "id": "myMPCAgent",
        "modules": [
            {"module_id": "Ag1Com", "type": "local_broadcast"},
            {
                "module_id": "myMPC",
                "type": "agentlib_mpc.mpc",
                "optimization_backend": {
                    "type": "casadi_ml",
                    "model": {
                        "type": {
                            "file": "model.py",
                            "class_name": "DataDrivenModel",
                        },
                        "ml_model_sources": [ml_model_path],
                    },
                    "discretization_options": {
                        "method": "multiple_shooting",
                    },
                    "results_file": "results//opt.csv",
                    "solver": {"name": "qpoases"},
                },
                "time_step": 300,
                "prediction_horizon": 15,
                "parameters": [
                    {"name": "s_T", "value": 3},
                    {"name": "r_mDot", "value": 1},
                ],
                "inputs": [
                    {"name": "T_in", "value": 290.15},
                    {"name": "load", "value": 150},
                    {"name": "T_upper", "value": ub},
                ],
                "controls": [{"name": "mDot", "value": 0.02, "ub": 0.05, "lb": 0}],
                "states": [{"name": "T", "value": 298.16, "ub": 303.15, "lb": 288.15}],
            },
        ],
    }
    agent_sim = {
        "id": "SimAgent",
        "modules": [
            {"module_id": "Ag1Com", "type": "local_broadcast"},
            {
                "module_id": "room",
                "type": "simulator",
                "model": {
                    "type": {
                        "file": "model.py",
                        "class_name": "PhysicalModel",
                    },
                    "states": [{"name": "T", "value": 298.16}],
                },
                "t_sample": 10,
                "save_results": True,
                "update_inputs_on_callback": False,
                "outputs": [
                    {"name": "T_out", "value": 298, "alias": "T"},
                ],
                "inputs": [
                    {"name": "mDot", "value": 0.02, "alias": "mDot"},
                ],
            },
        ],
    }
    return [agent_mpc, agent_sim]


def run_example(with_plots=True, log_level=logging.INFO, until=8000):
    # Change the working directly so that relative paths work
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    logging.basicConfig(level=log_level)

    # gets the subdirectory of anns with the highest number, i.e. the longest training
    # time
    try:
        ann_path = list(Path.cwd().glob("linregs/*/ml_model.json"))[-1]
    except IndexError:
        # if there is none, we have to perform the training first
        import training_linreg

        training_linreg.main(
            training_time=3600 * 24 * 1, plot_results=False, step_size=300
        )
        ann_path = list(Path.cwd().glob("linregs/*/ml_model.json"))[-1]

    # model.sim_step(mDot=0.02, load=30, T_in=290.15, cp=1000, C=100_000, T=298)
    mas = LocalMASAgency(
        agent_configs=agent_configs(ml_model_path=str(ann_path)),
        env=ENV_CONFIG,
        variable_logging=True,
    )
    mas.run(until=until)
    results = mas.get_results()
    if with_plots:
        mpc_results = results["myMPCAgent"]["myMPC"]
        sim_res = results["SimAgent"]["room"]
        fig, ax = plt.subplots(2, 1, sharex=True)
        t_sim = sim_res["T_out"]
        t_sample = t_sim.index[1] - t_sim.index[0]
        aie_kh = (t_sim - ub).abs().sum() * t_sample / 3600
        energy_cost_kWh = (
            (sim_res["mDot"] * (sim_res["T_out"] - sim_res["T_in"])).sum()
            * t_sample
            * 1
            / 3600
        )  # cp is 1
        print(f"Absoulute integral error: {aie_kh} Kh.")
        print(f"Cooling energy used: {energy_cost_kWh} kWh.")
        temperature = mpc_results["variable"]["T"] - 273.15
        plot_mpc(
            series=temperature,
            ax=ax[0],
            plot_actual_values=True,
            plot_predictions=True,
        )
        ax[0].axhline(ub - 273.15, color="grey", linestyle="--", label="upper boundary")
        plot_mpc(
            series=mpc_results["variable"]["mDot"],
            ax=ax[1],
            plot_actual_values=True,
            plot_predictions=True,
        )

        ax[1].legend()
        ax[0].legend()
        ax[0].set_ylabel("$T_{room}$ / °C")
        ax[1].set_ylabel("$\dot{m}_{air}$ / kg/s")
        ax[1].set_xlabel("simulation time / s")
        ax[1].set_ylim([0, 0.06])
        ax[1].set_xlim([0, until])
        plt.show()

    return results


if __name__ == "__main__":
    run_example(with_plots=True, until=3600)
