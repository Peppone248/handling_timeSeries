# hts/core.py
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from typing import Union

Index  = Union[list, np.ndarray, pd.Index, pd.Series]
Values = Union[list, np.ndarray, pd.Series, pd.DataFrame]


class _HTSeriesBase(ABC):

    def __init__(
        self,
        t: Index,
        values: Values,
        name: str = "hts",
        time_unit: str | None = None,
    ):
        self._t      = self._parse_index(t)
        self._values = self._parse_values(values)
        self._validate(self._t, self._values)
        self.name      = name
        self.time_unit = time_unit

    # --- parsing ---

    def _parse_index(self, t: Index) -> np.ndarray:
        # TODO 1: converti l'input in np.ndarray 1D
        #   - se è già DatetimeIndex o lista di stringhe datetime,
        #     convertilo in float (secondi da epoch) con pd.to_datetime + .astype(float)
        #   - altrimenti: np.asarray(t, dtype=float)
        #   - solleva ValueError se non è convertibile
        if (isinstance(t, list) and all(isinstance(value, str) for value in t)) or \
            isinstance(t, pd.DatetimeIndex):
            t = pd.to_datetime(t).astype(np.int64) / 1e9
            return t
        else:
            t = np.asarray(t, dtype=float)
            return t

    @abstractmethod
    def _parse_values(self, values: Values):
        pass

    # --- validazione ---

    def _validate(self, t: np.ndarray, values) -> None:
        # TODO 2: len(t) == len(values)
        # TODO 3: t non ha duplicati  → np.unique(t).size == t.size
        # TODO 4: t è ordinato        → np.all(np.diff(t) > 0)
        if len(t) != len(values):
            raise ValueError(f"t e values hanno lunghezze diverse: {len(t)} vs {len(values)}")
        if np.unique(t).size != t.size:
            raise ValueError("t contiene timestamp duplicati")
        if not np.all(np.diff(t) > 0):
            raise ValueError("t non è strettamente crescente")

    # --- proprietà temporali ---

    @property
    def t(self) -> np.ndarray:
        return self._t

    @property
    def dt(self) -> np.ndarray:
        # TODO 5: restituisci np.diff(self._t)
        # rappresenta gli intervalli tra campioni
        return np.diff(self._t)
        pass

    @property
    def is_regular(self) -> bool:
        # TODO 6: tutti gli intervalli dt sono uguali?
        # usa np.allclose(self.dt, self.dt[0])
        # gestisci il caso len < 2
        if (len(self._t) < 2):
            return True
        else:
            regular = np.allclose(self.dt, self.dt[0])
            return regular

        pass

    @property
    def fs(self) -> float | None:
        # TODO 7: se is_regular → 1.0 / self.dt[0]
        #         altrimenti → None
        if (len(self._t) < 2):
            return None
        if self.is_regular:
            return 1/self.dt[0]
        return None

    @property
    def duration(self) -> float:
        # TODO 8: t[-1] - t[0]
        return self._t[-1] - self._t[0]

    @property
    def n(self) -> int:
        # TODO 9
        return len(self._t)

    # --- dunder ---

    def __len__(self) -> int:
        return self.n

    @abstractmethod
    def __repr__(self) -> str:
        pass


class HTSeries(_HTSeriesBase):

    def _parse_values(self, values: Values) -> np.ndarray:
        # TODO 10: converti in np.ndarray 1D di float
        #          solleva TypeError se non numerico
        arr = np.asarray(values)
        if not np.issubdtype(arr.dtype, np.number):
            raise TypeError(f"values deve contenere valori numerici, trovato: {arr.dtype}")
        return arr.astype(np.float64)  # float64 è preferibile a float32 per precisione

    @property
    def values(self) -> np.ndarray:
        return self._values

    def __repr__(self) -> str:
        # TODO 11:
        # HTSeries('engine_rpm', n=10000, fs=100.0 Hz, duration=100.0 s)
        # se irregolare: fs=irregular
        return f"HTSeries('{self.name}', n={self.n}, fs={self.fs}, duration={self.duration:.2f} {self.time_unit or 's'})"
        


class HTMultiSeries(_HTSeriesBase):

    def _parse_values(self, values: Values) -> np.ndarray:
        # TODO 12: converti in np.ndarray 2D shape (n, k)
        #          k = numero di canali
        #          solleva TypeError se non numerico
        return f"HTMultiSeries('{self.name}', channels={self.n_channels}, n={self.n}, fs={self.fs}, duration={self.duration:.2f} {self.time_unit or 's'})"

    @property
    def values(self) -> np.ndarray:
        return self._values

    @property
    def n_channels(self) -> int:
        # TODO 13: numero di colonne (canali)
        return self._values.shape[1]
        pass

    def __repr__(self) -> str:
        # TODO 14:
        # HTMultiSeries('car_ecu', channels=12, n=10000, fs=100.0 Hz, duration=100.0 s)
        pass    