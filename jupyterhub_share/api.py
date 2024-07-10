import json
import secrets

from jupyterhub.apihandlers import APIHandler
from jupyterhub.apihandlers import default_handlers
from jupyterhub.handlers.pages import SpawnHandler
from jupyterhub.scopes import needs_scope
from tornado import web
from tornado.httputil import url_concat

from .orm import UserOptionsShares


class ShareUserOptionsAPIHandler(APIHandler):
    @needs_scope("servers")
    async def post(self):
        data = self.get_json_body()
        self.log.info(data)
        db_entry = UserOptionsShares.find(self.db, user_options=data)
        if db_entry is None:
            secret = secrets.token_urlsafe(8)
            new_entry = UserOptionsShares(share_id=secret, user_options=data)
            self.db.add(new_entry)
            self.db.commit()
        else:
            secret = db_entry.share_id
        self.log.info(secret)
        self.set_status(200)
        self.set_header("Content-Type", "text/plain")
        self.write(secret)


class ShareUserOptionsSpawnHandler(SpawnHandler):
    async def _render_form(
        self, for_user, spawner_options_form, spawner_options_form_values, message=""
    ):
        auth_state = await for_user.get_auth_state()
        return await self.render_template(
            "spawn.html",
            for_user=for_user,
            auth_state=auth_state,
            spawner_options_form=spawner_options_form,
            spawner_options_form_values=spawner_options_form_values,
            error_message=message,
            url=url_concat(
                self.request.uri, {"_xsrf": self.xsrf_token.decode("ascii")}
            ),
            spawner=for_user.spawner,
        )

    @web.authenticated
    async def get(self, secret):
        user = self.current_user
        db_entry = UserOptionsShares.find_by_share_id(self.db, secret)
        spawner_options_form_values = {}
        message = ""
        if not db_entry:
            message = f"{secret} is not known. Cannot fill user_options."
        else:
            spawner_options_form_values = db_entry.user_options
        dummy_spawner = user.get_spawner("", replace_failed=True)
        spawner_options_form = await dummy_spawner.get_options_form()
        form = await self._render_form(
            user,
            spawner_options_form=spawner_options_form,
            spawner_options_form_values=spawner_options_form_values,
            message=message,
        )
        self.finish(form)


default_handlers.append((r"/api/share/user_options", ShareUserOptionsAPIHandler))
default_handlers.append((r"/share/user_options/([^/]+)", ShareUserOptionsSpawnHandler))
