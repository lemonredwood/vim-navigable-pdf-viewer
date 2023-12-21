import keyboard
from viewer import viewer

def on_key_event(e):
    if e.event_type == keyboard.KEY_DOWN:
        if e.name == 'h':
            print(f'\nKey {e.name} was pressed')

        if e.name == 'j':
            viewer.scroll_down()
            print(f'\nKey {e.name} was pressed')

        if e.name == 'k':
            print(f'\nKey {e.name} was pressed')
        
        if e.name == 'l':
            print(f'\nKey {e.name} was pressed')

keyboard.hook(on_key_event)

keyboard.wait('esc')  

keyboard.unhook_all()

