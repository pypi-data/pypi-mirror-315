"""NextGen Insurance Listing model."""

from pywinauto.controls.uia_controls import ListItemWrapper
from t_object import ThoughtfulObject


class InsuranceListing(ThoughtfulObject):
    """Insurance Listing Model."""

    payer_row: ListItemWrapper
    payer: str = ""
    policy_number: str = ""
