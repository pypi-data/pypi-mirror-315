import streamlit as st
import json
import os

def fix_name(name):
    return name.replace(":", "").replace(" ", "_")

class SessionStateManager:
    def __init__(self, instance_id, main_key, keys):
        instance_id = instance_id if instance_id is not None else "DEFAULT"
        self.main_key, self.main_default, valid_values = main_key
        self.config_dir = f"session_manager_configs/{fix_name(instance_id)}"
        self.keys = keys

        os.makedirs(self.config_dir, exist_ok=True)

        default_config = f"{self.config_dir}/default.json"
        value = self.main_default
        if os.path.exists(default_config):
            try:
                value = json.loads(open(default_config).read())[self.main_key]
            except Exception:
                pass
        if value in valid_values:
            st.session_state[self.main_key] = value

        self.current_value = value


    def initialize(self, defaults):
        # load secondary values based on main_key value
        self.current_value = st.session_state[self.main_key]
        secondary_config = f"{self.config_dir}/{fix_name(st.session_state[self.main_key])}.json"

        if os.path.exists(secondary_config):
            try:
                cached_settings = json.loads(open(secondary_config).read())
            except Exception:
                cached_settings = {}
        else:
            cached_settings = {}

        for key, value in defaults.items():
            if key in cached_settings:
                st.session_state[key] = cached_settings[key]
            else:
                st.session_state[key] = defaults[key]

    def save(self):
        # First, save the main_key, main_value in default config:
        default_config = f"{self.config_dir}/default.json"

        with open(default_config, "w") as fp:
            json.dump({self.main_key: st.session_state[self.main_key]}, fp)
        # Save the old one:
        self.save_config(self.current_value)
        self.current_value = st.session_state[self.main_key]

    def save_config(self, main_value=None):
        main_value = main_value if main_value is not None else st.session_state[self.main_key]
        # save the keys in secondary config:
        if main_value != self.main_default:
            secondary_config = f"{self.config_dir}/{fix_name(main_value)}.json"
            settings = {}
            for key in self.keys:
                if key in st.session_state:
                    settings[key] = st.session_state[key]

            with open(secondary_config, "w") as fp:
                json.dump(settings, fp)
