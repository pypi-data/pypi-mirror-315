"""Dataframe Interface for the Xray Atlas Database."""

import polars as pl
from xray_atlas.server import get_dataset, DataSet, get_molecule, Molecule, Experiment
from dataclasses import dataclass
import matplotlib.pyplot as plt


@dataclass
class NexafsData:
    """Dataclass to hold the nexafs data."""

    _molecule: Molecule
    _experiment: Experiment
    _dataset: DataSet | None = None

    df: pl.DataFrame | None = None
    formula: str | None = None

    def __post_init__(self):
        self._dataset = get_dataset(self._molecule["name"], self._experiment)
        self.df = parse_dataset(self._dataset)
        self.formula = self._molecule["chemical_formula"]


def parse_dataset(dataset: DataSet) -> pl.DataFrame:
    """Parse the dataset from the xray-atlas server."""
    data = dataset["dataset"]
    raw_df = pl.DataFrame(data)
    geometries = raw_df.group_by(pl.col("geometry"))
    dfs = []
    for geo, d in geometries:
        _df = pl.DataFrame(
            {
                f"Energy [{d["energy"][0]["unit"]}]": pl.Series(
                    d["energy"][0]["signal"]
                ),
                f"μ [{d["intensity"][0]["unit"]}]": pl.Series(
                    d["intensity"][0]["signal"]
                ),
            }
        )
        _df = _df.with_columns(
            pl.Series(
                "θ [°]", [geo[0]["e_field_polar"]] * len(d["energy"][0]["signal"])
            ),
            pl.Series(
                "φ [°]", [geo[0]["e_field_azimuth"]] * len(d["energy"][0]["signal"])
            ),
        )
        dfs.append(_df)
    return pl.concat(dfs)


if __name__ == "__main__":
    mol = get_molecule("D18")
    exp = mol["data"][0]

    nexafs = NexafsData(mol, exp)
    df = nexafs.df

    plt.plot(df["Energy [eV]"], df["μ [arb. units]"])
    plt.show()
