
# Computational Materials Science Tool Kit

The goal of this project is to provide a robust and user-friendly interface for
a wide range of materials science related programs in order to accelerate the
pace of computational research.

## Optional Environment Variables

**CMSTK_INCAR_DEFAULTS** - Path to a json file containing sets of default INCAR
tag values. The json file should look something like the following example:

```json
{
    "spin": {
        "ISPIN": 2,
        "LORBIT": 11
    },
    "non_spin": {
        "ISPIN": 1
    }
}
```

**CMSTK_HPC_DEFAULTS** - Path to a json file containing sets of default job
submission script tags and commands. The `tags` and `cmds` sections are required
to differentiate the content type. The json file should look something like the
following example:

```json
{
    "slurm_vasp": {
        "tags": {
            "--job-name": "vasp_simulation"
        },
        "cmds": [
            "module load intel impi",
            "srun --mpi=pmi2 $VASP_BIN > vasp.log"
        ]
    },
    "slurm_atat": {
        "tags": {
            "--job-name": "atat_simulation"
        },
        "cmds": [
            "module load atat",
            "corrdump -l=rndstr.in -ro -noe -nop -2=5.2"
        ]
    }
}
```
