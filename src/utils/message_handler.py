class MessageHandler:
    @staticmethod
    def process_message(message, model):
        """
        处理消息的静态方法，可以根据不同模型返回不同的响应
        
        :param message: 用户输入的消息
        :param model: 选择的AI模型
        :return: AI的响应消息
        """
        # 这里可以根据不同的模型实现不同的处理逻辑
        # 目前是一个简单的模拟实现
        if model == 'gpt-4o':
            return f"GPT-4o正在思考: {message}"
        elif model == 'gpt-o1':
            return f"GPT-o1分析中: {message}"
        else:
            return f"未知模型，无法处理消息: {message}"
