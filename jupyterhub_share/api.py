import secrets

from jupyterhub.apihandlers import APIHandler
from jupyterhub.apihandlers import default_handlers
from jupyterhub.scopes import needs_scope

from .orm import UserOptionsShares


class ShareUserOptionsAPIHandler(APIHandler):
    @needs_scope("servers")
    async def post(self):
        data = self.get_json_body()
        db_entry = UserOptionsShares.find(self.db, user_options=data)
        if db_entry is None:
            share_id = secrets.token_urlsafe(8)
            new_entry = UserOptionsShares(share_id=share_id, user_options=data)
            self.db.add(new_entry)
            self.db.commit()
        else:
            share_id = db_entry.share_id
        self.set_status(200)
        self.set_header("Content-Type", "text/plain")
        self.write(share_id)

default_handlers.append((r"/api/share/user_options", ShareUserOptionsAPIHandler))