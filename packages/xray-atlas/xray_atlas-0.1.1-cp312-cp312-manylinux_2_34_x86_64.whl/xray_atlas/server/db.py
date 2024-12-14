from typing import List, Optional, Dict, TypedDict


class Signal(TypedDict):
    signal: List[int]
    units: str


class Molecule(TypedDict):
    name: str
    synonyms: List[str]
    chemical_formula: str
    description: str
    SMILES: str
    InChI: str
    img: str
    data: Optional[List["Experiment"]]


class Experiment(TypedDict):
    edge: str
    method: str
    facility: str
    instrument: str
    group: str
    source: str


class User(TypedDict):
    name: str
    affiliation: str
    group: str
    email: str
    doi: Optional[str]


class Instrument(TypedDict):
    facility: str
    instrument: str
    edge: str
    normalization_method: str
    technique: str
    technical_details: str


class Sample(TypedDict):
    vendor: str
    preparation_method: Dict[str, str]
    mol_orientation_details: str


class Data(TypedDict):
    geometry: Dict[str, float]
    energy: Signal
    intensity: Signal
    error: Optional[Signal]
    io: Optional[Signal]


class DataSet(TypedDict):
    user: User
    instrument: Instrument
    sample: Sample
    dataset: List[Data]


def Uid(experiment: Experiment) -> str:
    return f"{experiment['edge']}_{experiment['method']}_{experiment['facility']}_{experiment['instrument']}_{experiment['group']}_{experiment['source']}"
