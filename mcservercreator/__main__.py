"""
Entry for MCSC
"""

import sys

import inquirer
import os
from pip._internal.cli.main import main as pipmain

from mcservercreator import constants
from mcservercreator.utils import tools
from mcservercreator.utils import more_options
from mcservercreator.utils.properties_parser import Properties

info = '''
{0} {1} by Ivan1F
Thanks for using {0}!
{2} is open source, u can find it here: {3}
{2} is still under development, it may not work well
If u find any bug, please report it in the github issue
'''.format(constants.FULL_NAME, constants.VERSION, constants.SHORT_NAME, constants.GITHUB_REPO)

def print_info():
    print(info)

questions = [
    inquirer.List('mcversion', message='Input the version of the minecraft server core', choices=tools.get_all_versions_id()),
    inquirer.Confirm('fabric', message='Do u want to install fabric', default=True),
    inquirer.Confirm('mcdr', message='Do u want to install MCDReforged', default=True),
    inquirer.Checkbox('more', message="More options", choices=more_options.ALL)
]

def main():
    print_info()

    here = os.getcwd()

    if len(os.listdir(here)) != 0:
        ans = inquirer.prompt([inquirer.Confirm('confirm', message='The current directory is not empty, do u want to continue')])
        if not ans['confirm']:
            exit(0)

    # Show questions
    answers = inquirer.prompt(questions)

    more = answers['more']

    # More questions
    more_questions = []
    if more_options.CONFIG_PORT in more:
        more_questions.append(inquirer.Text('port', message='Input the server port'))
    if more_options.CONFIG_SEED in more:
        more_questions.append(inquirer.Text('seed', message='Input the world seed'))
    if more_options.CONFIG_DEFAULT_GAMEMODE in more:
        more_questions.append(inquirer.List('gamemode', message='Input the default gamemode', choices=['survival', 'creative', 'spectator', 'adventure']))
    if more_options.CONFIG_LEVEL_TYPE in more:
        more_questions.append(inquirer.List('level_type', message='Select the level type', choices=['default', 'flat', 'largebiomes', 'amplified', 'buffet']))
    if more_options.CONFIG_DIFFICULTLY in more:
        more_questions.append(inquirer.List('difficulty', message='Select the difficulty', choices=['easy', 'hard', 'normal', 'peaceful']))

    more_questions_ans = inquirer.prompt(more_questions)

    # Download MCDReforged
    if answers['mcdr']:
        if 'mcdreforged' not in tools.get_all_installed_packages():
            print('MCDReforged not found, installing it using pip...')
            pipmain(['install', 'mcdreforged'])
        else:
            print('Running MCDReforged to generate files of MCDR...')
            os.system('python -m mcdreforged')

    # Download vanilla server core
    tools.download_server_jar(os.path.join(here, 'server', 'server.jar'), answers['mcversion'])

    # Download and install Fabric
    tools.download_fabric_installer(os.path.join(here, 'server', 'fabric-installer.jar'))
    print('Installing Fabric Loader...')
    os.chdir(os.path.join(here, 'server'))
    cmd = 'java -jar {} server -mcversion {} nogui'.format('fabric-installer.jar', answers['mcversion'])
    # print(cmd, os.getcwd())
    os.system(cmd)
    os.chdir(here)

    print('Copying default server.properties to the server folder...')
    with open(os.path.join(here, 'server', 'server.properties'), 'w+') as f:
        f.write(constants.DEFAULT_SERVER_PROPERTIES)

    # Edit MCDR config file
    print('Editing MCDR config file...')
    mcdr_config_file = os.path.join(here, 'config.yml')
    if answers['fabric']:
        tools.replace_in_file(mcdr_config_file, 'minecraft_server', 'fabric-server-launch')  # Replace server core file in run command
    else:
        tools.replace_in_file(mcdr_config_file, 'minecraft_server', 'server')    # Replace server core file in run command

    if more_options.MCDR_LANG_ZH_CN in more:
        tools.replace_in_file(mcdr_config_file, 'en_us', 'zh_cn')

    # EULA
    print('Creating eula.txt')
    if more_options.AGREE_TO_EULA in more:
        with open(os.path.join(here, 'server', 'eula.txt'), 'w+') as f:
            f.write('eula=true')
            f.close()

    # Edit Minecraft config file
    print('Editing Minecraft config file...')
    server_properties_file = os.path.join(here, 'server', 'server.properties')
    properties = Properties(server_properties_file)
    if more_options.ALLOW_COMMAND_BLOCKS in more:
        properties.put('enable-command-block', 'true')
    if more_options.DISABLE_ONLINE_MODE in more:
        properties.put('online-mode', 'false')
    if more_options.CONFIG_PORT in more:
        properties.put('server-port', more_questions_ans['port'])
    if more_options.CONFIG_SEED in more:
        properties.put('level-seed', more_questions_ans['seed'])
    if more_options.CONFIG_DEFAULT_GAMEMODE in more:
        properties.put('gamemode', more_questions_ans['gamemode'])
    if more_options.CONFIG_LEVEL_TYPE in more:
        properties.put('level-type', more_questions_ans['level_type'])
    if more_options.CONFIG_DIFFICULTLY in more:
        properties.put('difficulty', more_questions_ans['difficulty'])

    properties.save()

    # Done
    print('Your server is ready! 🎉')
    ans = inquirer.prompt([inquirer.Confirm('run', message='Do u want to start now?', default=True)])
    if ans['run']:
        os.system('python -m mcdreforged')


if __name__ == '__main__':
    sys.exit(main())