from decimal import Decimal
from t_object import ThoughtfulObject

from pywinauto.controls.uia_controls import ListItemWrapper


class COBDetails(ThoughtfulObject):
    """Represents details of a COB entry."""

    rsn_code: str = ""
    rsn_amt: Decimal = Decimal(0)
    rsn_amt_element: ListItemWrapper
