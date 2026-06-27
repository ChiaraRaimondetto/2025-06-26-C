from dataclasses import dataclass

from model.costruttore import Costructor


@dataclass
class Arco:
    c1:Costructor
    c2:Costructor
    peso:int