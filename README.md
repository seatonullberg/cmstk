
# cmstk

Computational Materials Science Tool Kit

The goal of this project is to provide a robust and user-friendly interface for
a wide range of materials science related programs in order to accelerate the
pace of computational research.

## Optional Environment Variables

**CMSTK_INCAR_DEFAULTS** - Path to a json file containing sets of default INCAR tag values. The json file should look something like the following example:

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
