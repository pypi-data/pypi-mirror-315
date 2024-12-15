from setuptools import setup

setup(
    name='mkdocs-img2webp',
    version='0.1',
    install_requires=[
        'mkdocs >= 1.4.2',
        'pillow',
        'importlib-metadata; python_version == "3.8"',
    ],
    author='hyj0824',
    author_email='admin@hyj.ac.cn',
    url='https://github.com/hyj0824',
    download_url='https://github.com/hyj0824/mkdocs-images-to-webp',
    keywords=['mkdocs', 'images', 'webp'],

    entry_points={
        'mkdocs.plugins': [
            'images-to-webp = mkdocs_images_to_webp.plugin:ConvertImagesToWebpPlugin',
        ]
    }
)
