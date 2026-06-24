
## Подготовка к выполнению


1. Создайте пустой публичный репозиторий в своём любом проекте: `my_own_collection`.
2. Скачайте репозиторий Ansible: `git clone https://github.com/ansible/ansible.git` по любому, удобному вам пути.
3. Зайдите в директорию Ansible: `cd ansible`.
4. Создайте виртуальное окружение: `python3 -m venv venv`.
5. Активируйте виртуальное окружение: `. venv/bin/activate`. Дальнейшие действия производятся только в виртуальном окружении.
6. Установите зависимости `pip install -r requirements.txt`.
7. Запустите настройку окружения `. hacking/env-setup`.
8. Если все шаги прошли успешно — выйдите из виртуального окружения `deactivate`.
9. Ваше окружение настроено. Чтобы запустить его, нужно находиться в директории `ansible` и выполнить конструкцию `. venv/bin/activate && . hacking/env-setup`.

## Основная часть

Ваша цель — написать собственный module, который вы можете использовать в своей role через playbook. Всё это должно быть собрано в виде collection и отправлено в ваш репозиторий.

**Шаг 1.** В виртуальном окружении создайте новый `my_own_module.py` файл.

## **Шаг 2.** Наполните его содержимым:
```python
#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_test

short_description: This is my test module

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is my longer description explaining my test module.

options:
    name:
        description: This is the message to send to the test module.
        required: true
        type: str
    new:
        description:
            - Control to demo if the result of this module is changed or not.
            - Parameter description can be a list as well.
        required: false
        type: bool
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - my_namespace.my_collection.my_doc_fragment_name

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_namespace.my_collection.my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_namespace.my_collection.my_test:
    name: fail me
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
'''

from ansible.module_utils.basic import AnsibleModule


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True),
        new=dict(type='bool', required=False, default=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result['original_message'] = module.params['name']
    result['message'] = 'goodbye'

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if module.params['new']:
        result['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['name'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
```
Или возьмите это наполнение [из статьи](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html#creating-a-module).
## 
**Шаг 3.** Заполните файл в соответствии с требованиями Ansible так, чтобы он выполнял основную задачу: module должен создавать текстовый файл на удалённом хосте по пути, определённом в параметре `path`, с содержимым, определённым в параметре `content`.

**Шаг 4.** Проверьте module на исполняемость локально.

**Шаг 5.** Напишите single task playbook и используйте module в нём.

**Шаг 6.** Проверьте через playbook на идемпотентность.

**Шаг 7.** Выйдите из виртуального окружения.

**Шаг 8.** Инициализируйте новую collection: `ansible-galaxy collection init my_own_namespace.yandex_cloud_elk`.

**Шаг 9.** В эту collection перенесите свой module в соответствующую директорию.

**Шаг 10.** Single task playbook преобразуйте в single task role и перенесите в collection. У role должны быть default всех параметров module.

**Шаг 11.** Создайте playbook для использования этой role.

**Шаг 12.** Заполните всю документацию по collection, выложите в свой репозиторий, поставьте тег `1.0.0` на этот коммит.

**Шаг 13.** Создайте .tar.gz этой collection: `ansible-galaxy collection build` в корневой директории collection.

**Шаг 14.** Создайте ещё одну директорию любого наименования, перенесите туда single task playbook и архив c collection.

**Шаг 15.** Установите collection из локального архива: `ansible-galaxy collection install <archivename>.tar.gz`.

**Шаг 16.** Запустите playbook, убедитесь, что он работает.

**Шаг 17.** В ответ необходимо прислать ссылки на collection и tar.gz архив, а также скриншоты выполнения пунктов 4, 6, 15 и 16.

## Необязательная часть


1. Реализуйте свой модуль для создания хостов в Yandex Cloud.
2. Модуль может и должен иметь зависимость от `yc`, основной функционал: создание ВМ с нужным сайзингом на основе нужной ОС. Дополнительные модули по созданию кластеров ClickHouse, MySQL и прочего реализовывать не надо, достаточно простейшего создания ВМ.
3. Модуль может формировать динамическое inventory, но эта часть не является обязательной, достаточно, чтобы он делал хосты с указанной спецификацией в YAML.
4. Протестируйте модуль на идемпотентность, исполнимость. При успехе добавьте этот модуль в свою коллекцию.
5. Измените playbook так, чтобы он умел создавать инфраструктуру под inventory, а после устанавливал весь ваш стек Observability на нужные хосты и настраивал его.
6. В итоге ваша коллекция обязательно должна содержать: clickhouse-role (если есть своя), lighthouse-role, vector-role, два модуля: my_own_module и модуль управления Yandex Cloud хостами и playbook, который демонстрирует создание Observability стека.


# Разбор решения задания
Создал публичный репозиторий на своем гитхаб, инициировал локальный гит в этот репозиторий. Клонировал репозиторий ansible, перешел в него и активировал виртуальное окружение. 
1. В окружении создал файл скрипта и проверил его наличие:
```bash
touch my_own_module.py
ls -l my_own_module.py
```
2. Записал в него приведенное  в примере задания содержимое в полном объеме.
3. Заполняю файл в соответствии с заданной логикой:
  - Если файла нет - создать его и вернуть `changed=True`.
  - Если файл есть, но содержимое отличается - перезаписать его и вернуть `changed=True`. 
  - Если файл уже есть и содержимое совпадает - ничего не делать и вернуть `changed=False`
  
  https://oneuptime.com/blog/post/2026-02-21-ansible-ansiblemodule-class/view
  https://docs.ansible.com/archive/ansible/2.6/dev_guide/developing_modules_general.html
``` python
#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module

short_description: Create a text file on the remote host from path whis data from content


version_added: "1.0.0"

description: - Creates a text file on the remote host.
             - The file path in C(path), and data from C(content).
             - Supports check mode.

options:
    path:
        description:
            - Absolute path to the file
        required: true
        type: str
    content:
        description:
            - Text content to write into the file.
        required: true
        type: str

extends_documentation_fragment:
    - my_namespace.my_collection.my_doc_fragment_name

author:
    - Artur
notes:
    - Supports check_mode.
'''

EXAMPLES = r'''
- name: Create file with content
  my_own_module:
    path: /tmp/test.txt
    content: "hello! Iam your custom module"

'''

RETURN = r'''
path:
    description: Path to the file.
    type: str
    returned: always
    sample: /tmp/test.txt
content:
    description: Content written to the file.
    type: str
    returned: always
    sample: hello! Iam your custom module
message:
    description: Module execution message.
    type: str
    returned: always
    sample: File created successfully
'''

import os
from ansible.module_utils.basic import AnsibleModule


def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True)
    )

    result = dict(
        path='',
        content='',
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']

    result['path'] = path
    result['content'] = content

    current_content = None
    file_exists = os.path.exists(path)

    if file_exists:
        try:
            with open(path, 'r') as f:
                current_content = f.read()
        except Exception as e:
            module.fail_json(msg=f'Failed to read existing file: {e}', **result)

    if (not file_exists) or (current_content != content):
        result['changed'] = True

        if module.check_mode:
            result['message'] = 'File would be created or updated'
            module.exit_json(**result)

        try:
            with open(path, 'w') as f:
                f.write(content)
        except Exception as e:
            module.fail_json(msg=f'Failed to write file: {e}', **result)

        if file_exists:
            result['message'] = 'File updated successfully'
        else:
            result['message'] = 'File created successfully'
    else:
        result['message'] = 'File already exists with the desired content'

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
```
Здесь: 
```python
#!/usr/bin/python
from __future__ import absolute_import, division, print_function
__metaclass__ = type
```
Первая строка `#!/usr/bin/python`  это shebang, то есть указание, каким интерпретатором выполнять файл как исполняемый скрипт.
Строка `from __future__ import ...`   шаблон совместимости Python, из официальной документации Ansible. 
`__metaclass__ = type` тоже про совместимость и единообразие структуры модуля в примерах из документации.
```python
DOCUMENTATION = r'''
---
module: my_own_module
...
'''
```
`DOCUMENTATION` это специальная строка с YAML-подобным описанием модуля. Ansible использует её для генерации справки, в том числе через `ansible-doc`, и рекомендует описывать в ней имя модуля, краткое назначение, параметры, автора и дополнительные заметки.
Примеры и возвращаемые значения:
```python
EXAMPLES = r'''
- name: Create file with content
  my_own_module:
    path: /tmp/test.txt
    content: "hello! Iam your custom module"
'''

RETURN = r'''
path:
    description: Path to the file.
...
'''
```
`EXAMPLES` показывает, как вызывается модуль в playbook, чтобы можно было быстро понять интерфейс модуля.
`RETURN` показывает, какие поля модуль возвращает при выполнении. Общие поля как `changed` и `failed` Ansible обрабатывает как стандартные, а специфичные поля вроде `path`, `content`, `message` нужно описывать отдельно.
**Импорты:**
```python
import os
from ansible.module_utils.basic import AnsibleModule
```
`import os` нужен для работы с файловой системой, для проверки существования файла через `os.path.exists()`.
`AnsibleModule` это главный переводчик для кастомного модуля. Он отвечает за разбор входных параметров, их валидацию, поддержку `check mode` и корректное завершение модуля через `structured` JSON-ответ.
(https://docs.ansible.com/projects/ansible/latest/dev_guide/developing_modules_general.html, https://oneuptime.com/blog/post/2026-02-21-ansible-ansiblemodule-class/view)
```python
def run_module():
```
Основная рабочая функция. В ней:
- входные параметры;
- начальное состояние результата;
- создание объекта `AnsibleModule`;
- основную логику;
- завершение через `exit_json()` или `fail_json()`
**Параметры**
```python
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True)
    )
```
Здесь задан `argument_spec`, то есть спецификация параметров модуля. Ansible рекомендует явно описывать все параметры, которые модуль принимает, включая их типы и обязательность: (https://docs.ansible.com/projects/ansible/latest/collections/ansible/builtin/validate_argument_spec_module.html, https://dev.to/austincunningham/write-a-ansible-module-with-python-2eb8)
- `path` - строка, обязательная;
- `content` - строка, обязательная.
**result**
```python
    result = dict(
        changed=False,
        path='',
        content='',
        message=''
    )
```
`result` это словарь, который будет постепенно наполняться и в конце вернётся в `module.exit_json(**result)`. (https://docs.ansible.com/projects/ansible/latest/dev_guide/developing_modules_general.html)
`changed` явно сообщит, изменил ли он состояние удалённой системы. 
**Создание AnsibleModule**
```python
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
```
Создание объекта `AnsibleModule` и передача ему описания параметров. 
`supports_check_mode=True` говорит Ansible, что модуль умеет работать в режиме dry-run.
**Чтение параметров**
```python
    path = module.params['path']
    content = module.params['content']
```
параметры доступны через `module.params`. Это словарь co значениями по именам, объявленным в `argument_spec`.
**Заполнение result**
```python
    result['path'] = path
    result['content'] = content
```
входные значения записываются в возвращаемый результат, чтобы видеть, с какими параметрами модуль реально отработал
**Проверка текущего состояния**
```python
    current_content = None
    file_exists = os.path.exists(path)
```
`file_exists` проверяет, существует ли файл по указанному пути,
`current_content` готовится для возможного чтения содержимого. Модуль не должен переписывать файл на каждом запуске. Сначала он должен понять текущее состояние, а потом сравнить его с желаемым состоянием. (https://www.nebulaworks.com/insights/posts/how-to-create-a-repeatable-framework-for-ansible-modules/)
**Чтение существующего файла**
```python
    if file_exists:
        try:
            with open(path, 'r') as f:
                current_content = f.read()
        except Exception as e:
            module.fail_json(msg=f'Failed to read existing file: {e}', **result)
```
Если файл существует, то читается его содержимое. Конструкция `with open(...)`  это стандартный Python-способ безопасно открыть файл и автоматически закрыть его после чтения. Если чтение не удалось - вызвать `module.fail_json(msg=..., **result)`, чтобы задача завершилась статусом failed с соответствующим сообщением

**Проверка идемпотентности**
```python
    if (not file_exists) or (current_content != content):
        result['changed'] = True
```
означает:
- если файла нет - надо создать, значит будет изменение;
- если файл есть, но его содержимое не совпадает - надо обновить, значит тоже будет изменение. Если условие ложно, это значит, что файл уже существует и его содержимое уже такое, как нужно. В этом случае менять ничего не надо, а `changed` должен остаться `False`
**Поддержка check mode**
```python
        if module.check_mode:
            result['message'] = 'File would be created or updated'
            module.exit_json(**result)
```
`module.check_mode` позволяет определить, что модуль выполняется в `dry-run` режиме. Если Ansible запущен в check mode и изменение **понадобилось бы**, то нужно остановиться и вернуть результат без реальной записи файла. Он должен вернуть `changed=True`, но саму запись не выполнять. (https://forum.ansible.com/t/add-check-mode-feature-to-an-existing-module/24902)
**Запись файла**
```python
        try:
            with open(path, 'w') as f:
                f.write(content)
        except Exception as e:
            module.fail_json(msg=f'Failed to write file: {e}', **result)
```
Если `check mode` не активен и изменения действительно нужны, открывается файл на запись и записывается новое содержимое. Режим `'w'` означает создание файла при отсутствии или полную перезапись при наличии. Если операция записи провалилась, снова используется `fail_json()` (https://docs.ansible.com/projects/ansible/latest/reference_appendices/module_utils.html)
**Сообщение о результате**
```python
        if file_exists:
            result['message'] = 'File updated successfully'
        else:
            result['message'] = 'File created successfully'
    else:
        result['message'] = 'File already exists with the desired content'
```
Человекочитаемое пояснение результата. Если файла раньше не было, то пишется, что он создан; если был, но содержимое изменилось - что обновлён; если изменений не потребовалось - что файл уже соответствовал желаемому состоянию. Модуль возвращает не только `changed`, но и `message`
**Успешное завершение**
```python
    module.exit_json(**result)
```
`exit_json()` завершает модуль успешно и возвращает сформированный словарь результата обратно в Ansible.

**`main` и точка входа**
```python
def main():
    run_module()


if __name__ == '__main__':
    main()
```
`main()`  это обёртка над `run_module()`. А условие `if __name__ == '__main__':` означает, что `main()` будет вызвана, если файл запущен как самостоятельный Python-скрипт. 

4. Создал файл `args.json` в директории с модулем и запустил его:
```json
cat > args.json <<EOF
 {
   "ANSIBLE_MODULE_ARGS": {
     "path": "test.txt",
     "content": "hello! Iam your custom module"
   }
 }
EOF
 python3 my_own_module.py /tmp/args.json
```
![Pasted image 20260624145018](https://github.com/ArturP1rozhkov/my_own_collection/blob/main/screenshots/Pasted%20image%2020260624145018.png)
- модуль запускается как отдельный Python-скрипт и возвращает валидный JSON для Ansible;
- модуль создаёт файл по переданному пути;
- поле `changed: true` показывает, что модуль посчитал текущее выполнение изменяющим состояние системы;
- сообщение `File created successfully` подтверждает, что файл был создан;
- файл `test.txt` появился в каталоге

5. Создал директорию `library` в папке проекта `my_own_collection/` и скопировал в нее скрипт
```bash
mkdir -p library
cp my_own_module.py library/my_own_module.py
```
- создал `playbook.yml` с содержимым:
``` yaml
---
- name: Test custom module
  hosts: localhost
  connection: local
  gather_facts: false

  tasks:
    - name: Create test file with custom module
      my_own_module:
        path: ./playbook_test.txt
        content: "hello from playbook"
```
`playbook` содержит ровно одну задачу, а модуль вызывается по имени файла без `.py`. Это стандартное поведение Ansible для custom modules из `library/`. 
Когда `library/` рядом с `playbook`, не требуется отдельного `ansible.cfg`,  установки `collection` и проверяется через  `ansible-playbook` (https://stackoverflow.com/questions/45902515/how-to-create-the-custom-module-in-the-ansible, https://stackoverflow.com/questions/53750049/location-to-keep-ansible-custom-modules&rut=f019260b9f72cadf76e64c750f138930840e5be2578da3b6ce99649660cc0481)

Запустил `playbook` командой `ansible-playbook playbook.yml`
![Pasted image 20260624154330](https://github.com/ArturP1rozhkov/my_own_collection/blob/main/screenshots/Pasted%20image%2020260624154330.png)
`playbook` отработал, задача выполнилась на `localhost`, а `changed=1` на первом запуске обозначает, что модуль создал новый файл.

6. Проверка на идемпотентность путем повторного запуска `playbook`
```bash
ansible-playbook playbook.yml
```
![Pasted image 20260624154714](https://github.com/ArturP1rozhkov/my_own_collection/blob/main/screenshots/Pasted%20image%2020260624154714.png)
на втором запуске задача вернулась со статусом `ok`, а в recap `changed=0`, значит модуль распознал, что целевой файл уже находится в нужном состоянии, и повторно ничего не менял. 

7. Вышел из виртуального окружения командой `deactivate`
8. Инициировал новую `collections` командой `ansible-galaxy collection init my_own_namespace.yandex_cloud_elk`
![Pasted image 20260624194930](https://github.com/ArturP1rozhkov/my_own_collection/blob/main/screenshots/Pasted%20image%2020260624194930.png)

9. Перенес `module` в соответствующую созданную директорию:
```bash
mkdir -p my_own_namespace/yandex_cloud_elk/plugins/modules
cp my_own_module.py my_own_namespace/yandex_cloud_elk/plugins/modules/my_own_module.py
```
10. Инициировал `role` из корня проекта:
```bash
ansible-galaxy role init my_own_namespace/yandex_cloud_elk/roles/my_own_role
```
   ![Pasted image 20260624200143.](https://github.com/ArturP1rozhkov/my_own_collection/blob/main/screenshots/Pasted%20image%2020260624200143.png)
перенес параметры в `defaults/main.yml`, а сам вызов модуля - в `tasks/main.yml`
`defaults/main.yml`
```yaml
---
my_own_role_path: "./role_test.txt"
my_own_role_content: "hello from role"
```
`tasks/main.yml
```yaml
---
- name: Create file with custom module
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: "{{ my_own_role_path }}"
    content: "{{ my_own_role_content }}"
```
(https://github.com/ansible/ansible/issues/68198) об использовании полного  имени модуля

11. Создал `playbook` для этой `role`. Для этого создал директорию `/playbook` внутри `collection` 
```bash
mkdir -p my_own_namespace/yandex_cloud_elk/playbooks
```
и файл `my_own_namespace/yandex_cloud_elk/playbooks/test_role.yml` следующего содержания:
```yaml
---
- name: Test role from collection
  hosts: localhost
  connection: local
  gather_facts: false

  roles:
    - role: my_own_namespace.yandex_cloud_elk.my_own_role
```
ссылка на роль внутри `colltction` по полному имени - **Fully Qualified Collection Name** или сокращенно **FQCN** (https://stackoverflow.com/questions/64836917/ansible-playbook-which-uses-a-role-defined-in-a-collection/64873724. https://docs.ansible.com/ansible/latest/dev_guide/developing_modules.html)
Запустил по полному имени:
```bash
ansible-playbook my_own_namespace.yandex_cloud_elk.test_role
```
![Pasted image 20260624202315](https://github.com/ArturP1rozhkov/my_own_collection/blob/main/screenshots/Pasted%20image%2020260624202315.png)
повторно:
![Pasted image 20260624202343](https://github.com/ArturP1rozhkov/my_own_collection/blob/main/screenshots/Pasted%20image%2020260624202343.png)
12. Заполнил документацию
файл `galaxy.yml`
```text
namespace: my_own_namespace
name: yandex_cloud_elk
version: 1.0.0
readme: README.md
authors:
  - Artur P1rozhkov
description: An test Ansible collection with a custom module, role, and playbook for file creation.
license:
  - MIT
tags:
  - ansible
  - collection
  - module
  - role
  - devops
repository: https://github.com/ArturP1rozhkov/my_own_collection
documentation: https://github.com/ArturP1rozhkov/my_own_collection
homepage: https://github.com/ArturP1rozhkov/my_own_collection
issues: https://github.com/ArturP1rozhkov/my_own_collection/issues
dependencies: {}
```

файл `README.md`
```text
# yandex_cloud_elk

Test Ansible collection whis:
- custom module `my_own_module`
- role `my_own_role`
- playbook `test_role`

## Structure
- `plugins/modules/my_own_module.py` — custom module
- `roles/my_own_role` — role, used module
- `playbooks/test_role.yml` — playbook for local start

## Run

export ANSIBLE_COLLECTIONS_PATH=~/my_own_collection
ansible-playbook my_own_namespace.yandex_cloud_elk.test_role

## Result

On the first run, a file is created, on the second run, the playbook returns `changed=0`, which confirms idempotency.


```

файл `docs/usage.md`
```text
# Usage

## Local run

export ANSIBLE_COLLECTIONS_PATH=~/my_own_collection
ansible-playbook my_own_namespace.yandex_cloud_elk.test_role

## What it does
Role `my_own_role` calls custom module `my_own_namespace.yandex_cloud_elk.my_own_module` and creates a file with content from role defaults.

## Idempotency
Repeated run returns `ok` and `changed=0`.
```

Закоммитил изменения, создал аннотированный тег, запушил в удаленный репозиторий
```bash
git status
git add .
git commit -m "Finalize collection documentation and release 1.0.0"
git tag -a 1.0.0 -m "Release 1.0.0"
git push origin main
git push origin 1.0.0
git tag # проверка
git show 1.0.0 # просмотр тега
```

13. В корневой директории collection создал `.tar.gz` этой  `collection`: `ansible-galaxy collection build` 
```bash
cd ~/my_own_collection/ansible_collections/my_own_namespace/yandex_cloud_elk
ansible-galaxy collection build

```
После успешной сборки рядом появился архив с именем `my_own_namespace-yandex_cloud_elk-1.0.0.tar.gz`

14. Создал директорию `collection_install_test` и перенес в нее файл `playbook.yml` который можно использовать как single task playbook и архив
```bash
cd ~/my_own_collection
mkdir -p collection_install_test
cp playbook.yml collection_install_test/
cp ansible_collections/my_own_namespace/yandex_cloud_elk/my_own_namespace-yandex_cloud_elk-1.0.0.tar.gz collection_install_test/
```
поправил в `playbook` пути и имя FQCN модуля
```yaml
---
- name: Test installed collection module
  hosts: localhost
  connection: local
  gather_facts: false

  tasks:
    - name: Create test file with installed collection module
      my_own_namespace.yandex_cloud_elk.my_own_module:
        path: ./installed_playbook_test.txt
        content: "hello from installed collection"
```
 (https://kkloudtarus.net/en/blog/ansible-galaxy-and-collections)

15. Установил `collection` из локального архива:
```bash
cd ~/my_own_collection/collection_install_test
ansible-galaxy collection install my_own_namespace-yandex_cloud_elk-1.0.0.tar.gz
```
Поскольку ansible не хочет повторно устанавливать коллекцию из архива, поскольку видит ранее установленную аналогичную коллекцию в директории `my_own_collection/ansible_collections`, нужно установить архив в **отдельный путь** и запускать `playbook` так, чтобы Ansible видел только эту установленную копию `collection`.
```bash
mkdir -p .collections
ansible-galaxy collection install my_own_namespace-yandex_cloud_elk-1.0.0.tar.gz -p .collections --force
```
![Pasted image 20260624214848](https://github.com/ArturP1rozhkov/my_own_collection/blob/main/screenshots/Pasted%20image%2020260624214848.png)

указал Ansible новый путь поиска коллекций. Для этого явно указал `ANSIBLE_COLLECTIONS_PATH` на каталог, в который установил архив.
```bash
export ANSIBLE_COLLECTIONS_PATH=~/my_own_collection/collection_install_test/.collections
ansible-galaxy collection list my_own_namespace.yandex_cloud_elk
```
![Pasted image 20260624215117](https://github.com/ArturP1rozhkov/my_own_collection/blob/main/screenshots/Pasted%20image%2020260624215117.png)

16. Запустил коллекцию командой два раза подряд
```bash
ansible-playbook playbook.yml
```
![Pasted image 20260624215603](https://github.com/ArturP1rozhkov/my_own_collection/blob/main/screenshots/Pasted%20image%2020260624215603.png)
файл создан в целевой директории с заданным содержимым:
![Pasted image 20260624215732](https://github.com/ArturP1rozhkov/my_own_collection/blob/main/screenshots/Pasted%20image%2020260624215732.png)


