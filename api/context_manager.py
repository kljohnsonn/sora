class ContextManager:
    def __init__(self):
        self.contexts = {}
        self.user_models = {}

    def update_context(self, user_id, user_message, bot_response):
        if user_id not in self.contexts:
            self.contexts[user_id] = []
        self.contexts[user_id].append({"role": "user", "content": user_message})
        self.contexts[user_id].append({"role": "assistant", "content": bot_response})

    def get_context(self, user_id):
        return self.contexts.get(user_id, [])

    def clear_context(self, user_id):
        if user_id in self.contexts:
            self.contexts[user_id] = []

    def set_user_model(self, user_id, model):
        self.user_models[user_id] = model

    def get_user_model(self, user_id):
        return self.user_models.get(user_id, "teknium/openhermes-2.5-mistral-7b")