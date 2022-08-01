import sys
import shutil
from pathlib import Path

from .args import *
from ..exec.workflow_exec import exec_preprocessing


def run_cmd() -> None:
    """obtains all parameters and executes workflows

    Parameters
    ----------
    params : list
        list of user provided parameters

    Returns
    -------
    None
    """
    # collecting parameters
    params = sys.argv[1:]
    if len(params) == 0:
        raise RuntimeError("please provide a mode")

    mode_type = params[0]

    # checking if mode type is supported
    supported_modes = ["init", "run", "test"]
    if mode_type not in supported_modes:
        raise ValueError(
            f"{mode_type} is not a mode supported modes: {supported_modes}"
        )

    # checking if more than one mode is provided, raise error
    bool_mask = [param in supported_modes for param in params]
    check = len([_bool for _bool in bool_mask if _bool == True])
    if check > 1:
        raise RuntimeError("two modes detected, please select one")

    # parsing arguments based on modes
    if mode_type == "init":

        init_args = parse_init_args(params)

        # setting up file paths
        platemap_path = str(Path(init_args.platemap).absolute())
        barcode_path = str(Path(init_args.barcode).absolute())
        metadata_path = str(Path(init_args.metadata).absolute())

        # create data folder
        # raises error if data directory exists (prevents overwriting)
        data_dir_obj = Path("data")
        data_dir_obj.mkdir(exist_ok=False)
        data_dir_path = str(data_dir_obj.absolute())

        # moving all input files
        for data_file in init_args.data:
            f_path = str(Path(data_file).absolute())
            shutil.move(f_path, data_dir_path)

        shutil.move(platemap_path, data_dir_path)
        shutil.move(barcode_path, data_dir_path)
        shutil.move(metadata_path, data_dir_path)

    elif mode_type == "run":
        # selecting workflow process
        proc_sel = params[1]

        # checking if the workflow process exists
        supported_workflows = ["cp_process", "dp_process"]
        if proc_sel not in supported_workflows:
            raise ValueError(f"{proc_sel} is not a supported workflow")

        # executing process
        if proc_sel == "cp_process":
            cp_process_args = parse_cp_process_args(params)

            print("executing cell profiler preprocessing")
            status = exec_preprocessing(cp_process_args)
            if status:
                sys.exit(status)
            else:
                print("Error: Unable to execute workflow")
                sys.exit(1)

        elif proc_sel == "dp_process":
            pass


if __name__ == "__main__":

    run_cmd()
