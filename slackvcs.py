from errbot import BotPlugin, botcmd, arg_botcmd, webhook
import requests
import json
import os

import mdparser

class SlackVCS(BotPlugin):
    """
    Version control for files uploaded to Slack
    """
    
    @botcmd
    def pwd(self, msg, args):
        return os.getcwd()



    @arg_botcmd("filename", type=str)
    def track(self, msg, filename=None):

        method = "files.list"
        data = { "types": "spaces" } # Only posts

        request = self._bot.sc.api_call(method, data=data)

        matching = [ i for i in request["files"] if i["title"] == filename ]

        if len(matching) == 0:
            return "Post with that name does not exist"
        elif len(matching) == 1:
            file_url = matching[0]["url_private"]
            yield "Found post with matching name:"
            yield file_url

            token = "REDACTED"
            r = requests.get(file_url, headers = {'Authorization': ("Bearer " + token)})
            content_string = r.content.decode("utf-8")

            p = mdparser.JSONToMarkdownParser()
            p.parse(content_string, "output.md")
            yield filename + " successfully tracked"
        else:
            return "Multiple posts with that name found. Please rename to resolve name collision."


    @botcmd(split_args_with=None)
    def debug_placeholder(self, msg, args):
        """A command which simply returns 'Example'"""
        return str(args)

