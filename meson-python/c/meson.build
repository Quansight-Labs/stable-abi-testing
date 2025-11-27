project('python-limited-api', 'c',
        version: '1.2.3',
        meson_version: '>=1.3.0')

py_mod = import('python')
py = py_mod.find_installation(get_option('python'))

ext_mod_limited = py.extension_module('limited',
  'limited.c',
  limited_api: '3.15',
  install: true,
  c_args: ['-D_Py_OPAQUE_PYOBJECT'],
)

test('load-test',
  py,
  args: [files('test_limited.py')],
  env: { 'PYTHONPATH': meson.current_build_dir() },
  workdir: meson.current_source_dir()
)
