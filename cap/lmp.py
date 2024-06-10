import os
import ast

from typing import Optional
import astunparse
from openai import OpenAI

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import PythonLexer
from tenacity import retry, stop_after_attempt, wait_random_exponential
from cap.helpers import call_api, logger


def var_exists(name, all_vars):
    try:
        eval(name, all_vars)
    except:
        exists = False
    else:
        exists = True
    return exists


def merge_dicts(dicts):
    return {
        k : v
        for d in dicts
        for k, v in d.items()
    }


def exec_safe(code_str, gvars=None, lvars=None):
    banned_phrases = ['import', '__']
    for phrase in banned_phrases:
        assert phrase not in code_str

    if gvars is None:
        gvars = {}
    if lvars is None:
        lvars = {}
    empty_fn = lambda *args, **kwargs: None
    custom_gvars = merge_dicts([
        gvars,
        {'exec': empty_fn, 'eval': empty_fn}
    ])
    exec(code_str, custom_gvars, lvars)


class LMP:
    def __init__(self, name: str, cfg: dict, lmp_fgen: 'LMPFGen', fixed_vars: dict, variable_vars: dict):
        """An implementation of Language Model generated Programs (LMPs)

        Args:
            - name: whatever name
            - cfg: a dictionary that stores all the configurations
            - lmp_fgen: interface to another language model instance that generates implementations of missing functions
            - fixed_vars: variables that come from `import` at the top. This includes `np` and everything from `shapely.geometry`, `shapely.affinity`
            - variable_vars: both the primitives we provide (e.g., `put_first_on_second`) and the ones that LMPFGen handles (e.g., `parse_obj_name`)
        """
        self._name = name
        self._cfg = cfg

        self._base_prompt = self._cfg['prompt_text']

        self._stop_tokens = list(self._cfg['stop'])

        self._lmp_fgen = lmp_fgen

        self._fixed_vars = fixed_vars
        self._variable_vars = variable_vars
        self.exec_hist = ''

    def clear_exec_hist(self):
        self.exec_hist = ''

    def build_prompt(self, query, context=''):
        if len(self._variable_vars) > 0:
            variable_vars_imports_str = f"from utils import {', '.join(self._variable_vars.keys())}"
        else:
            variable_vars_imports_str = ''
        prompt = self._base_prompt.replace('{variable_vars_imports}', variable_vars_imports_str)

        if self._cfg['maintain_session']:
            prompt += f'\n{self.exec_hist}'

        if context != '':
            prompt += f'\n{context}'

        use_query = f'{self._cfg["query_prefix"]}{query}{self._cfg["query_suffix"]}'
        prompt += f'\n{use_query}'

        return prompt, use_query

    def _fake_call(self, query, code_str, context='', **kwargs):
        prompt, use_query = self.build_prompt(query, context=context)
        context = ''
        if self._cfg['include_context'] and context != '':
            to_exec = f'{context}\n{code_str}'
            to_log = f'{context}\n{use_query}\n{code_str}'
        else:
            to_exec = code_str
            to_log = f'{use_query}\n{to_exec}'

        to_log_pretty = highlight(to_log, PythonLexer(), TerminalFormatter())
        print(f'LMP {self._name} exec:\n\n{to_log_pretty}\n')

        # NOTE: When code_str contains some of the "loosely-defined" functions
        # (i.e., ['parse_obj_name', 'parse_position', 'parse_question', 'transform_shape_pts']),
        # we do not use fgen --> new_fs will be empty.
        if self._lmp_fgen is not None:
            new_fs = self._lmp_fgen.create_new_fs_from_code(code_str)
            self._variable_vars.update(new_fs)

        gvars = merge_dicts([self._fixed_vars, self._variable_vars])
        lvars = kwargs

        # Execute the code
        if not self._cfg['debug_mode']:
            exec_safe(to_exec, gvars, lvars)

        self.exec_hist += f'\n{to_exec}'

        if self._cfg['maintain_session']:
            self._variable_vars.update(lvars)

        if self._cfg['has_return']:
            return lvars[self._cfg['return_val_name']]

    # @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def __call__(self, query, context='', callback=None, **kwargs):
        prompt, use_query = self.build_prompt(query, context=context)

        import gtts, requests
        try:
            code_str = call_api(
                engine=self._cfg['engine'],
                prompt=prompt,
                stop=self._stop_tokens,
                temperature=self._cfg['temperature'],
                max_tokens=self._cfg['max_tokens']
            )
        except (OSError, gtts.tts.gTTSError, requests.exceptions.ConnectionError) as e:
            import traceback
            traceback.print_exc()
            say('I\'m sorry, I cannot reach the internet now')
            code_str = ''

        if callback is not None:
            assert callable(callback)
            callback({'query': query, 'code_str': code_str, 'context': context})


        if self._cfg['include_context'] and context != '':
            to_exec = f'{context}\n{code_str}'
            to_log = f'{context}\n{use_query}\n{code_str}'
        else:
            to_exec = code_str
            to_log = f'{use_query}\n{to_exec}'

        to_log_pretty = highlight(to_log, PythonLexer(), TerminalFormatter())
        print(f'LMP [{self._name}] exec:\n\n{to_log_pretty}\n')

        # NOTE: When code_str contains some of the "loosely-defined" functions
        # (i.e., ['parse_obj_name', 'parse_position', 'parse_question', 'transform_shape_pts']),
        # we do not use fgen --> new_fs will be empty.
        if self._lmp_fgen is not None:
            new_fs = self._lmp_fgen.create_new_fs_from_code(code_str)
            self._variable_vars.update(new_fs)

        gvars = merge_dicts([self._fixed_vars, self._variable_vars])
        lvars = kwargs

        # Execute the code
        if not self._cfg['debug_mode']:
            exec_safe(to_exec, gvars, lvars)

        self.exec_hist += f'\n{to_exec}'

        if self._cfg['maintain_session']:
            self._variable_vars.update(lvars)

        if self._cfg['has_return']:
            return lvars[self._cfg['return_val_name']]


    # Take a code string generated from elsewhere and execute it
    def execute_code_string(self, user_query, code_str, context='', callback=None, **kwargs):

        if self._cfg['include_context'] and context != '':
            to_exec = f'{context}\n{code_str}'
            to_log = f'{context}\n{user_query}\n{code_str}'
        else:
            to_exec = code_str
            to_log = f'{user_query}\n{to_exec}'

        to_log_pretty = highlight('# ' + to_log, PythonLexer(), TerminalFormatter())
        print(f'LMP {self._name} exec:\n\n{to_log_pretty}\n')
        if callback is not None:
            try:
                print('Running callback for execute_code_string!')
                data = {'code_str': code_str, 'query': user_query}
                callback(data)
            except Exception as e:
                import traceback
                logger.warn('callback on generated code failed!')
                traceback.print_exc()

        # NOTE: When code_str contains some of the "loosely-defined" functions
        # (i.e., ['parse_obj_name', 'parse_position', 'parse_question', 'transform_shape_pts']),
        # we do not use fgen --> new_fs will be empty.
        if self._lmp_fgen is not None:
            new_fs = self._lmp_fgen.create_new_fs_from_code(code_str)
            self._variable_vars.update(new_fs)

        gvars = merge_dicts([self._fixed_vars, self._variable_vars])
        lvars = kwargs

        # Execute the code
        if not self._cfg['debug_mode']:
            exec_safe(to_exec, gvars, lvars)

        self.exec_hist += f'\n{to_exec}'

        if self._cfg['maintain_session']:
            self._variable_vars.update(lvars)

        if self._cfg['has_return']:
            return lvars[self._cfg['return_val_name']]

class LMPFGen:

    def __init__(self, cfg, fixed_vars, variable_vars):
        self._cfg = cfg

        self._stop_tokens = list(self._cfg['stop'])
        self._fixed_vars = fixed_vars
        self._variable_vars = variable_vars

        self._base_prompt = self._cfg['prompt_text']

    # @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def create_f_from_sig(self, f_name, f_sig, other_vars=None, fix_bugs=False, return_src=False):
        """Generates a missing function
        """
        print(f'Creating function: {f_sig}')

        use_query = f'{self._cfg["query_prefix"]}{f_sig}{self._cfg["query_suffix"]}'
        prompt = f'{self._base_prompt}\n{use_query}'

        f_src = call_api(
            prompt=prompt,
            stop=self._stop_tokens,
            temperature=self._cfg['temperature'],
            engine=self._cfg['engine'],
            max_tokens=self._cfg['max_tokens']
        )

        if fix_bugs:
            f_src = client.edits.create(model='code-davinci-edit-001',
            input='# ' + f_src,
            temperature=0,
            instruction='Fix the bug if there is one. Improve readability. Keep same inputs and outputs. Only small changes. No comments.')['choices'][0]['text'].strip()

        if other_vars is None:
            other_vars = {}
        gvars = merge_dicts([self._fixed_vars, self._variable_vars, other_vars])
        lvars = {}

        exec_safe(f_src, gvars, lvars)

        f = lvars[f_name]

        to_print = highlight(f'{use_query}\n{f_src}', PythonLexer(), TerminalFormatter())
        print(f'LMP FGEN created:\n\n{to_print}\n')

        if return_src:
            return f, f_src
        return f

    def create_new_fs_from_code(self, code_str: str, other_vars: Optional[dict] = None, fix_bugs: bool = False, return_src: bool = False):
        """

        Returns:
          - new_fs:
              a) empty dictionary (if all symbols in code_str already exist in the predefined set of modules)
              b) fn name and fn object (otherwise)
        """

        fs, f_assigns = {}, {}
        f_parser = FunctionParser(fs, f_assigns)
        f_parser.visit(ast.parse(code_str))
        for f_name, f_assign in f_assigns.items():
            if f_name in fs:
                fs[f_name] = f_assign

        if other_vars is None:
            other_vars = {}

        new_fs = {}
        srcs = {}
        # NOTE:
        # Given the code_str as follows:
        # say("Ok - picking up the Rubik's cube and putting it in the drawer")
        # put_first_on_second("Rubik's cube", 'drawer')
        #
        # `fs` is:`
        # {
        #   'say': 'say("Ok - picking up the Rubik\'s cube and putting it in the drawer")',
        #   'put_first_on_second': 'put_first_on_second("Rubik\'s cube", \'drawer\')'
        # }
        # or:
        # {
        #   'say': "say('Building a tower at the center')",
        #   'stack_objects_in_order': 'stack_objects_in_order(object_names=order_bottom_to_top)'
        # }

        for f_name, f_sig in fs.items():
            all_vars = merge_dicts([self._fixed_vars, self._variable_vars, new_fs, other_vars])

            # Check if the symbol `f_name` is in a predefined set of modules
            if not var_exists(f_name, all_vars):
                print('f_name', f_name)
                print('f_sig', f_sig)

                # Generate function implementation
                # - f: function object
                # - f_src: function string
                f, f_src = self.create_f_from_sig(f_name, f_sig, new_fs, fix_bugs=fix_bugs, return_src=True)

                # recursively define child_fs in the function body if needed
                # Get the body of the function as string
                f_def_body = astunparse.unparse(ast.parse(f_src).body[0].body)
                child_fs, child_f_srcs = self.create_new_fs_from_code(
                    f_def_body, other_vars=all_vars, fix_bugs=fix_bugs, return_src=True
                )

                if len(child_fs) > 0:
                    new_fs.update(child_fs)
                    srcs.update(child_f_srcs)

                    # redefine parent f so newly created child_fs are in scope
                    gvars = merge_dicts([self._fixed_vars, self._variable_vars, new_fs, other_vars])
                    lvars = {}

                    exec_safe(f_src, gvars, lvars)

                    f = lvars[f_name]

                new_fs[f_name], srcs[f_name] = f, f_src

        if return_src:
            return new_fs, srcs
        return new_fs


class FunctionParser(ast.NodeTransformer):

    def __init__(self, fs, f_assigns):
      super().__init__()
      self._fs = fs
      self._f_assigns = f_assigns

    def visit_Call(self, node):
        self.generic_visit(node)
        if isinstance(node.func, ast.Name):
            f_sig = astunparse.unparse(node).strip()
            f_name = astunparse.unparse(node.func).strip()
            self._fs[f_name] = f_sig
        return node

    def visit_Assign(self, node):
        self.generic_visit(node)
        if isinstance(node.value, ast.Call):
            assign_str = astunparse.unparse(node).strip()
            f_name = astunparse.unparse(node.value.func).strip()
            self._f_assigns[f_name] = assign_str
        return node
