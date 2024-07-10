from jupyterhub.auth import DummyAuthenticator
from jupyterhub.spawner import SimpleLocalProcessSpawner

import jupyterhub_share

c.JupyterHub.authenticator_class = DummyAuthenticator
c.JupyterHub.spawner_class = SimpleLocalProcessSpawner

c.SimpleLocalProcessSpawner.options_form = """
          Choose a system:
          <select name="system">
              <option value="Local">Local</option>
              <option value="Remote-A">Remote A</option>
              <option value="Remote-B">Remote B</option>
          </select>
          <select name="image">
              <option value="a">Image A</option>
              <option value="b">Image B</option>
          </select>
          <input type="checkbox" name="Check02" value="true" checked="true" />
          <input type="checkbox" name="Check01" value="true" />
          <input type="text" name="textf" class="form-control" id="repository" data-lpignore="true" placeholder="GitHub repository name or URL">
          <input type="number" name="runtime-input" value="30" min="10" max="1440" required="required">
          <input type="range" name="range1" min="0" max="100" value="90" step="10" />
      """
c.SimpleLocalProcessSpawner.default_url = "/hub/home"

import os

s = os.getcwd()
c.JupyterHub.template_paths = os.path.join(s, "share", "templates")

c.JupyterHub.allow_named_servers = True
