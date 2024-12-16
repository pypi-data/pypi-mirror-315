from streamlit_mui_elements.core.elements import ElementsManager
from streamlit_mui_elements.core.exceptions import *
from streamlit_mui_elements.modules import *
from streamlit_mui_elements.version import __version__

def elements(key: str) -> ElementsManager:
    """Create a Streamlit Elements frame using ElementsManager."""
    return ElementsManager(key)

