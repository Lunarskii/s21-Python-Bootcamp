import yaml


def generate_package_tasks(packages):
    return [{'ansible.builtin.apt': {'name': package}} for package in packages]


def generate_copy_tasks(files):
    return [{'ansible.builtin.copy': {'src': f'{file}', 'dest': f'/path/to/{file}', 'follow': 'yes'}} for file in files]


def generate_shell_tasks(files, bad_guys):
    tasks = []
    for file in files:
        cmd = f'python3 {file}{" -e " + ",".join(bad_guys) if file == "consumer.py" else ""}'
        tasks.append({'ansible.builtin.shell': {'cmd': cmd, 'delegate_to': 'localhost'}})
    return tasks


def generate_tasks(data):
    install_packages_tasks = generate_package_tasks(data['server']['install_packages'])
    copy_tasks = generate_copy_tasks(data['server']['exploit_files'])
    shell_tasks = generate_shell_tasks(data['server']['exploit_files'], data['bad_guys'])
    return {'tasks': install_packages_tasks + copy_tasks + shell_tasks}


if __name__ == '__main__':
    with open('../materials/todo.yml') as input_file:
        data = yaml.load(input_file, Loader=yaml.FullLoader)

        with open('deploy.yml', 'w') as output_file:
            output_file.write(yaml.dump(generate_tasks(data)))
