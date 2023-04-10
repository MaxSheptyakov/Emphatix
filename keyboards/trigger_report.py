from localization import _
from keyboards.common import main_page_button, create_keyboard



def generate_trigger_report_keyboard(emotions):
    keyboard = create_keyboard(emotions, with_main=True, row_width=3)
    return keyboard