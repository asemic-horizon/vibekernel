"""
VibeKernel - A Jupyter kernel for the Hy language
"""

import sys
import traceback
from ipykernel.kernelbase import Kernel
import hy
from hy.models import Expression
from hy.reader import read_many
from hy.compiler import hy_eval_user as hy_eval
import builtins
import ast
import io
from contextlib import redirect_stdout, redirect_stderr


class VibeKernel(Kernel):
    implementation = 'VibeKernel'
    implementation_version = '0.1.0'
    language = 'hy'
    language_version = hy.__version__
    language_info = {
        'name': 'hy',
        'mimetype': 'text/x-hylang',
        'file_extension': '.hy',
        'codemirror_mode': 'scheme',
        'help_links': [
            {
                'text': 'Hy Documentation',
                'url': 'https://hylang.org/hy/doc/',
            },
        ],
    }
    banner = f"VibeKernel - Hy {hy.__version__} Jupyter Kernel"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize the Hy environment
        self.hy_globals = {}
        self.execution_count = 0
        
        # Initialize with basic Python builtins
        self.hy_globals.update(builtins.__dict__)

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        """Execute Hy code"""
        if not code.strip():
            return {'status': 'ok', 'execution_count': self.execution_count, 'payload': [], 'user_expressions': {}}

        self.execution_count += 1
        
        # Capture stdout and stderr
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        
        try:
            # Parse Hy code first (outside of stdout/stderr capture)
            try:
                parsed_expressions = list(read_many(code))
            except Exception as e:
                if not silent:
                    self._send_error('HyParseError', str(e), 
                                   ['  File "<vibekernel>", line 1', 
                                    f'    {code.strip()[:50]}{"..." if len(code.strip()) > 50 else ""}',
                                    f'HyParseError: {str(e)}'])
                return self._error_response('HyParseError', str(e))
            
            with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
                result = None
                # Execute each expression
                for i, expr in enumerate(parsed_expressions):
                    try:
                        # Use Hy's eval function
                        result = hy_eval(expr, globals=self.hy_globals, locals=self.hy_globals)
                    except Exception as e:
                        # Get better traceback formatting
                        tb_lines = traceback.format_exc().splitlines()
                        # Filter out internal kernel frames for cleaner output
                        clean_tb = []
                        for line in tb_lines:
                            if 'vibekernel/kernel.py' in line or 'ipykernel' in line:
                                continue
                            clean_tb.append(line)
                        
                        if not clean_tb:
                            clean_tb = [f'{type(e).__name__}: {str(e)}']
                        
                        if not silent:
                            self._send_error(type(e).__name__, str(e), clean_tb)
                        return self._error_response(type(e).__name__, str(e))
            
            # Send stdout content
            stdout_content = stdout_buffer.getvalue()
            if stdout_content and not silent:
                self.send_response(self.iopub_socket, 'stream', {
                    'name': 'stdout',
                    'text': stdout_content
                })
            
            # Send stderr content
            stderr_content = stderr_buffer.getvalue()
            if stderr_content and not silent:
                self.send_response(self.iopub_socket, 'stream', {
                    'name': 'stderr',
                    'text': stderr_content
                })
            
            # Send result if there is one
            if result is not None and not silent:
                self.send_response(self.iopub_socket, 'execute_result', {
                    'execution_count': self.execution_count,
                    'data': self._format_result(result),
                    'metadata': {}
                })
                    
        except Exception as e:
            if not silent:
                self._send_error(type(e).__name__, str(e), traceback.format_exc().splitlines())
            return self._error_response(type(e).__name__, str(e))

        return {'status': 'ok', 'execution_count': self.execution_count, 'payload': [], 'user_expressions': {}}
    
    def _send_error(self, ename, evalue, traceback_list):
        """Helper method to send error messages"""
        self.send_response(self.iopub_socket, 'error', {
            'ename': ename,
            'evalue': evalue,
            'traceback': traceback_list
        })
    
    def _error_response(self, ename, evalue):
        """Helper method to create error response"""
        return {
            'status': 'error', 
            'execution_count': self.execution_count, 
            'ename': ename, 
            'evalue': evalue, 
            'traceback': []
        }
    
    def _format_result(self, result):
        """Format result for display with multiple representations"""
        data = {'text/plain': repr(result)}
        
        # Add HTML representation for certain types
        if hasattr(result, '_repr_html_'):
            data['text/html'] = result._repr_html_()
        elif hasattr(result, '__dict__') and hasattr(result, '__class__'):
            # For objects, show a nicer representation
            data['text/plain'] = f"<{result.__class__.__module__}.{result.__class__.__name__} at {hex(id(result))}>"
        
        return data

    def do_complete(self, code, cursor_pos):
        """Provide basic completion"""
        # Extract the current word being typed
        line = code[:cursor_pos].split('\n')[-1]
        words = line.split()
        if not words:
            return {
                'status': 'ok',
                'matches': [],
                'cursor_start': cursor_pos,
                'cursor_end': cursor_pos,
                'metadata': {}
            }
        
        # Get the current word
        current_word = words[-1]
        word_start = cursor_pos - len(current_word)
        
        # Basic completion from builtins and current namespace
        matches = []
        for name in dir(builtins):
            if name.startswith(current_word):
                matches.append(name)
        
        for name in self.hy_globals:
            if isinstance(name, str) and name.startswith(current_word):
                matches.append(name)
        
        return {
            'status': 'ok',
            'matches': sorted(set(matches)),
            'cursor_start': word_start,
            'cursor_end': cursor_pos,
            'metadata': {}
        }

    def do_inspect(self, code, cursor_pos, detail_level=0):
        """Provide object introspection"""
        return {
            'status': 'ok',
            'found': False,
            'data': {},
            'metadata': {}
        }


if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=VibeKernel)