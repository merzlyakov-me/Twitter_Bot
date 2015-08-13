from distutils import setup


files = []

setup(name="twitter-bot",
    version='0.1',
    description="simple twitter bot",
    author="EC HTP group01",
    author_email="",
    url="",
    packages=['bot'],
    package_data={'package': files},
    scripts=['bot/tw_daemon.py', 'bot/tw_client.py']
    )
