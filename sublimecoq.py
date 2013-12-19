import re
import sublime, sublime_plugin
from SublimeCoq.coqtop import Coqtop

'''
returns (the next statement, rest) or
        None if there are no more well-formed statements
'''
def next_statement(program):
    if program == '':
        return None
    elif re.match('\\s+', program) is not None:
        return next_statement(re.sub('\\s+', '', program, 1))
    elif program[0:2] == '(*':
        try:
            index = program.index('*)')
        except ValueError:
            return None
        else:
            return ((program[0:index+2], program[index+2:]) if index+2 < len(program) else (program[0:index+2], ''))
    else:
        try:
            index = program.index('.')
        except ValueError:
            return None
        else:
            return ((program[0:index+1], program[index+1:]) if index+1 < len(program) else (program[0:index+1], ''))

class RunCoqCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        coq_syntax = self.view.settings().get('syntax')
        program = self.view.substr(sublime.Region(0, self.view.size()))
        window = self.view.window()
        coqtop_view = window.new_file()
        coqtop_view.insert(edit, 0, program)
        coqtop_view.set_read_only(True)
        coqtop_view.set_scratch(True)
        coqtop_view.set_syntax_file(coq_syntax)
        coqtop_view.set_name('*COQTOP*')

class CoqContext(sublime_plugin.EventListener):
    def on_query_context(self, view, key, operator, operand, match_all):
        if key == 'running_coqtop':
            running = view.settings().get('coqtop_running')
            if running is None:
                return None
            if operator == sublime.OP_EQUAL:
                return running
            elif operator == sublime.OP_NOT_EQUAL:
                return not running
            else:
                return False
        return None