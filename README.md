# JupyterHub User Options Share
This small package allows users to share their chosen `user_options` with others.  
In combination with the right `options_form`, it can lead to FAIR digital objects in your JupyterHub installation.

## Installation
`pip install juypterhub-share`

## Configuration
In the `jupyterhub_config.py` file one have to add `import jupyterhub_share`.  
Furthermore, the new `spawn.html` template file must be used.  

## Usage
Users may select the `user_options` as they're used to. Before clicking on "Start", one can click on the share icon next to "Server Options". This will generate a unique URL. If any user opens this link, they'll redirected to the spawn page with the previously selected `user_options`.
