project('python-limited-api', 'c',
        version: '1.2.3',
        meson_version: '>=1.3.0')

py_mod = import('python')
py = py_mod.find_installation(get_option('python'))

ext_mod_limited = py.extension_module('limited',
  'limited.c',
  limited_api: '3.15',
  install: true,
  c_args: ['-DPy_TARGET_ABI3T=0x030f0000'],
)
