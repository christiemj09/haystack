"""
Install haystack.
"""

def main():
	try:
		from setuptools import setup
	except ImportError:
		from distutils.core import setup

	config = {
		'description': 'Generate addresses for fields in a file.',
		'author': 'Matt Christie',
		'download_url': 'https://github.com/christiemj09/haystack.git',
		'author_email': 'christiemj09@gmail.com',
		'version': '0.1',
		'install_requires': [],
		'packages': ['haystack'],
		'scripts': [],
		'entry_points': {
		    'console_scripts': [],
		},
		'name': 'haystack',
	}

	setup(**config)	

if __name__ == '__main__':
	main()

