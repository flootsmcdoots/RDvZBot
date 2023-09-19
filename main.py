import bot_core
import yaml
import os.path

if __name__ == '__main__':
    # Execute bot
    path = './bot-config.yml'
    if os.path.isfile(path):
        with open(path, 'r') as file:
            config = yaml.safe_load(file)

        bot_core.run_bot_core(config)
    else:
        print("No config provided, unable to start bot (Please create a bot-config.yml)!")
    pass
