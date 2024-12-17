import threading
from datetime import datetime
import os,sys


def notice_main_module_update_var(queue,variable_name, variable_value):
    cmd_and_data = {
        "action": "update_variable",
        "variable_name": variable_name,
        "value": variable_value}
    
    status_message = {
        "target": "variable_update",
        "content":cmd_and_data
    }
    queue.put(status_message)


def notice_main_module_msg(queue, METADATA, msg_text=""):
    status_message = {
        "target": "status_bar",
        "content": {
            "message": f"{METADATA['name']} (v{METADATA['version']}) {msg_text} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        }
    }
    queue.put(status_message)

def notice_main_module_update_table(queue,plug_name,column_index, new_value):
    """
    
    plug_name如果使用plug_name则会自动获取插件的基本文件名。
    """

    


    print("预期获取插件文件名，实际="+plug_name)
    cmd_and_data = {
        "plug_name": plug_name,
        "column_index": column_index,
        "value": new_value}
    
    status_message = {
        "target": "update_table",
        "content":cmd_and_data
    }
    queue.put(status_message)

    
class PluginBase:
    def __init__(self, main_module):
        self.main_module = main_module
        self.is_running = False        
        if hasattr(self.main_module, 'if_debug') and self.main_module.if_debug:
            print(f"[{type(self).__name__}] Plugin initialized.")        




    def start(self):
        threading.Thread(target=self.plugin_func).start()
        if hasattr(self.main_module, 'if_debug') and self.main_module.if_debug:
            print(f"[{type(self).__name__}] Plugin started.")

    def stop(self):
        self.is_running = False
        if hasattr(self.main_module, 'if_debug') and self.main_module.if_debug:
            print(f"[{type(self).__name__}] Plugin stopped.")


    def plugin_func(self, message):
        pass
        self.main_module.add_message(message)


